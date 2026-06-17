#!/usr/bin/env python3
"""
Tlumaczenie wpisow PL -> EN przez Anthropic API (Claude).

Uzycie (CLI):
    python scripts/translate_post.py _posts/2026-05-18-Kara-umowna.md [kolejne pliki...]

Uzycie (stdin, jeden plik per linia — pewniejsze dla nazw z non-ASCII):
    printf '_posts/2026-06-17-Wlasciwosc.md\n' | python scripts/translate_post.py --stdin

Dla kazdego podanego pliku wpisu PL:
  - parsuje front-matter + tresc,
  - prosi Claude o tlumaczenie (title, summary, body) + wygenerowanie EN slug,
  - zapisuje nowy plik EN `_posts/{data}-{slug_en}.md` z poprawnym front-matter
    (lang: en, jawny permalink /en/aktualnosci/..., niezmieniony tag,
     odziedziczone flagi sitemap/robots, dwukierunkowy lang_alt),
  - aktualizuje plik PL: ustawia jego lang_alt na URL nowego wpisu EN.

Wymaga zmiennej srodowiskowej ANTHROPIC_API_KEY.

Loop guard: pomija wpis PL, ktory ma juz ustawione lang_alt ORAZ istnieje
plik EN, do ktorego to lang_alt wskazuje. Dzieki temu po scaleniu PR-a
ponowny trigger workflow nic nie robi.

Exit codes (eksplicite — workflow ma byc glosny gdy cos nie tak):
  0 = wszystko dobrze (utworzono >=1 plik EN, albo wszystkie pominiete
      legitnie loop-guardem)
  1 = blad konfiguracji (brak klucza, brak argumentow)
  2 = blad przy przetwarzaniu pliku (brak pliku, blad parsera, blad API)
"""

import os
import re
import sys
import json
import argparse

try:
    import yaml
except ImportError:
    sys.exit("Brak modulu pyyaml — zainstaluj: pip install -r scripts/requirements.txt")

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("Brak modulu anthropic — zainstaluj: pip install -r scripts/requirements.txt")


POSTS_DIR = "_posts"
MODEL = os.environ.get("TRANSLATE_MODEL", "claude-sonnet-4-6")
IS_CI = bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))

FM_DELIM = "---"

SYSTEM_PROMPT = """You are a professional legal translator for a Polish law firm \
(Kancelaria Adwokacka Piotra Modzelewskiego). You translate Polish blog/news posts \
into clear, professional British English suitable for a solicitor's website.

Rules:
- Preserve the Markdown structure EXACTLY: same headings (##, ###), same paragraph
  breaks, same bold/italic, same lists, same blockquotes (>). Do not add or remove
  sections.
- Keep the measured, first-person professional register a lawyer would use.
- Translate Polish legal terms to their accepted English equivalents (e.g.
  "zachowek" -> "the legitime (zachowek)", "kara umowna" -> "contractual penalty",
  "Sąd Najwyższy" -> "the Supreme Court"). When a term has no clean equivalent,
  give the English term followed by the Polish in parentheses on first use.
- Do NOT translate proper names, the firm name, case signatures (sygn. akt), or
  statute references — keep them as-is.
- The English slug must be lowercase ASCII, words separated by single hyphens,
  derived from the translated title, no trailing/leading hyphens, max ~8 words.

Return ONLY a JSON object, no prose, with exactly these keys:
  "title_en"   - translated title (string, no surrounding quotes)
  "summary_en" - translated summary (string)
  "slug_en"    - the English slug (string)
  "body_en"    - the full translated Markdown body (string)
"""


def parse_post(path):
    """Zwraca (front_matter_dict, body_str, raw_fm_str)."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    if not raw.startswith(FM_DELIM):
        raise ValueError(f"{path}: brak front-matter")
    parts = raw.split(FM_DELIM, 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: nieprawidlowy front-matter")
    raw_fm = parts[1]
    body = parts[2].lstrip("\n")
    fm = yaml.safe_load(raw_fm) or {}
    return fm, body, raw_fm


def slug_from_filename(path):
    """`_posts/2026-05-18-Kara-umowna.md` -> ('2026-05-18', 'kara-umowna')."""
    name = os.path.basename(path)
    name = re.sub(r"\.md$", "", name)
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", name)
    if not m:
        raise ValueError(f"{path}: nazwa pliku nie pasuje do RRRR-MM-DD-slug")
    return m.group(1), m.group(2).lower()


def date_parts(date_str):
    s = str(date_str)[:10]
    y, mo, d = s.split("-")
    return y, mo, d


def en_file_exists_for(lang_alt):
    if not lang_alt:
        return False
    m = re.search(r"/en/aktualnosci/(\d{4})/(\d{2})/(\d{2})/([^/]+)/?", lang_alt)
    if not m:
        return False
    y, mo, d, slug = m.groups()
    candidate = os.path.join(POSTS_DIR, f"{y}-{mo}-{d}-{slug}.md")
    return os.path.exists(candidate)


def build_en_frontmatter(fm, slug_en, title_en, summary_en, permalink_en, lang_alt_en):
    lines = ["---"]
    lines.append(f'title: "{title_en}"')
    lines.append(f"date: {fm['date']}")
    lines.append("lang: en")
    lines.append(f"tag: {fm['tag']}")
    lines.append(f'summary: "{summary_en}"')
    lines.append(f"permalink: {permalink_en}")
    lines.append(f"lang_alt: {lang_alt_en}")
    if "sitemap" in fm:
        lines.append(f"sitemap: {str(fm['sitemap']).lower()}")
    if "robots" in fm:
        lines.append(f"robots: {fm['robots']}")
    lines.append("---")
    return "\n".join(lines)


def patch_pl_lang_alt(path, raw_fm, new_lang_alt):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    if re.search(r"^lang_alt:.*$", raw_fm, flags=re.MULTILINE):
        new_raw = re.sub(
            r"^lang_alt:.*$",
            f"lang_alt: {new_lang_alt}",
            raw,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        new_raw = re.sub(
            r"(^tag:.*$)",
            r"\1\n" + f"lang_alt: {new_lang_alt}",
            raw,
            count=1,
            flags=re.MULTILINE,
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_raw)


def translate(client, fm, body):
    user_msg = (
        f"Title (PL): {fm.get('title','')}\n"
        f"Summary (PL): {fm.get('summary','')}\n\n"
        f"Body (PL Markdown):\n{body}"
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "".join(block.text for block in resp.content if block.type == "text").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(text)


class SkipReason:
    NOT_PL = "not-pl"
    NO_TAG = "no-tag"
    ALREADY_TRANSLATED = "already-translated"


def process(path, client):
    """Zwraca (status, info). status in {'created','skipped','error'}."""
    if not os.path.exists(path):
        return ("error", f"plik nie istnieje: {path!r}")

    try:
        fm, body, raw_fm = parse_post(path)
    except Exception as e:
        return ("error", f"parse error: {e}")

    if fm.get("lang") != "pl":
        return ("skipped", SkipReason.NOT_PL)

    if fm.get("lang_alt") and en_file_exists_for(fm["lang_alt"]):
        return ("skipped", SkipReason.ALREADY_TRANSLATED)

    if not fm.get("tag"):
        return ("error", f"{path}: brak pola `tag` we front-matter")

    try:
        date_str, pl_slug = slug_from_filename(path)
        y, mo, d = date_parts(fm["date"])
    except Exception as e:
        return ("error", f"{path}: {e}")

    try:
        result = translate(client, fm, body)
    except Exception as e:
        return ("error", f"{path}: API error: {e}")

    try:
        slug_en = result["slug_en"].strip().strip("-").lower()
    except (KeyError, AttributeError) as e:
        return ("error", f"{path}: bad API response shape: {e}; got: {result!r}")

    permalink_en = f"/en/aktualnosci/{y}/{mo}/{d}/{slug_en}/"
    lang_alt_en = f"/aktualnosci/{y}/{mo}/{d}/{pl_slug}/"

    en_fm = build_en_frontmatter(
        fm, slug_en, result["title_en"], result["summary_en"],
        permalink_en, lang_alt_en,
    )
    en_path = os.path.join(POSTS_DIR, f"{date_str}-{slug_en}.md")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_fm + "\n\n" + result["body_en"].rstrip() + "\n")

    patch_pl_lang_alt(path, raw_fm, permalink_en)

    return ("created", en_path)


def read_paths_from_stdin():
    paths = []
    for line in sys.stdin:
        s = line.strip()
        if s:
            paths.append(s)
    return paths


def main():
    parser = argparse.ArgumentParser(description="Tlumaczenie wpisow PL -> EN.")
    parser.add_argument("files", nargs="*", help="Sciezki do plikow PL")
    parser.add_argument("--stdin", action="store_true",
                        help="Czytaj liste plikow ze stdin (jeden per linia)")
    args = parser.parse_args()

    paths = read_paths_from_stdin() if args.stdin else args.files
    if not paths:
        print("BLAD: brak plikow do przetworzenia.", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # W CI to twardy blad — workflow musi byc glosny.
        # Lokalnie tez bez sensu probowac bez klucza.
        msg = "BLAD: ANTHROPIC_API_KEY nie jest ustawiony."
        if IS_CI:
            msg += " W CI to oznacza brak/niedostepny secret repo."
        print(msg, file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    created, skipped, errors = [], [], []
    for path in paths:
        status, info = process(path, client)
        if status == "created":
            created.append(info)
            print(f"UTWORZONO: {info}")
        elif status == "skipped":
            skipped.append((path, info))
            print(f"POMINIETO ({info}): {path}")
        else:
            errors.append((path, info))
            print(f"BLAD: {info}", file=sys.stderr)

    print()
    print(f"Podsumowanie: utworzono={len(created)}, pominieto={len(skipped)}, bledow={len(errors)}")

    if errors:
        # Jakikolwiek blad twardy = exit nonzero. Workflow ma to zobaczyc.
        sys.exit(2)

    # Wszystkie skipowania moga byc OK (loop-guard po scaleniu PR-a).
    # Tylko gdy wszystkie skipy to NOT_PL/ALREADY_TRANSLATED — to spodziewany "nic do roboty".
    if not created:
        non_loopguard = [r for _, r in skipped
                         if r not in (SkipReason.NOT_PL, SkipReason.ALREADY_TRANSLATED)]
        if non_loopguard:
            print(f"BLAD: nic nie utworzono i sa nieoczekiwane skipy: {non_loopguard}",
                  file=sys.stderr)
            sys.exit(2)
        print("(Nic do tlumaczenia — wszystkie wpisy juz maja EN albo nie sa PL.)")

    sys.exit(0)


if __name__ == "__main__":
    main()
