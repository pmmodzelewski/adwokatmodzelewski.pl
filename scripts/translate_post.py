#!/usr/bin/env python3
"""
Tlumaczenie wpisow PL -> EN przez Anthropic API (Claude).

Uzycie:
    python scripts/translate_post.py _posts/2026-05-18-Kara-umowna.md [kolejne pliki...]

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
"""

import os
import re
import sys
import json
import glob

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

# Front-matter dzielimy recznie (nie YAML-dump z powrotem), zeby zachowac
# kolejnosc i formatowanie blisko tego, co pisze wlasciciel.
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
    # Split na: '', front-matter, body
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
    """'2026-05-18' -> ('2026', '05', '18'). Akceptuje tez date YAML."""
    s = str(date_str)[:10]
    y, mo, d = s.split("-")
    return y, mo, d


def en_file_exists_for(lang_alt):
    """Czy istnieje plik EN, do ktorego wskazuje lang_alt PL?
    lang_alt PL: /en/aktualnosci/YYYY/MM/DD/<slug>/  -> szukamy _posts/YYYY-MM-DD-<slug>.md
    """
    if not lang_alt:
        return False
    m = re.search(r"/en/aktualnosci/(\d{4})/(\d{2})/(\d{2})/([^/]+)/?", lang_alt)
    if not m:
        return False
    y, mo, d, slug = m.groups()
    candidate = os.path.join(POSTS_DIR, f"{y}-{mo}-{d}-{slug}.md")
    return os.path.exists(candidate)


def build_en_frontmatter(fm, slug_en, title_en, summary_en, permalink_en, lang_alt_en):
    """Sklada front-matter wpisu EN jako tekst (zachowujac sensowna kolejnosc)."""
    lines = ["---"]
    lines.append(f'title: "{title_en}"')
    lines.append(f"date: {fm['date']}")
    lines.append("lang: en")
    lines.append(f"tag: {fm['tag']}")            # NIEzmieniony — kanoniczny PL slug
    lines.append(f'summary: "{summary_en}"')
    lines.append(f"permalink: {permalink_en}")    # WYMAGANE dla prefiksu /en/
    lines.append(f"lang_alt: {lang_alt_en}")
    # Odziedzicz flagi pre-launch jesli sa w zrodle
    if "sitemap" in fm:
        lines.append(f"sitemap: {str(fm['sitemap']).lower()}")
    if "robots" in fm:
        lines.append(f"robots: {fm['robots']}")
    lines.append("---")
    return "\n".join(lines)


def patch_pl_lang_alt(path, raw_fm, new_lang_alt):
    """Ustawia/zamienia lang_alt w pliku PL, zachowujac reszte pliku 1:1."""
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
        # Wstaw lang_alt po linii z tag: (lub na koncu front-matter)
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
    """Wywolanie Anthropic API. System prompt cache'owany. Zwraca dict z JSON."""
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
    # Wytnij ewentualne ```json ... ``` ogrodzenie
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(text)


def process(path, client):
    fm, body, raw_fm = parse_post(path)

    if fm.get("lang") != "pl":
        print(f"POMINIETO (nie PL): {path}")
        return None

    # Loop guard
    if fm.get("lang_alt") and en_file_exists_for(fm["lang_alt"]):
        print(f"POMINIETO (EN juz istnieje): {path}")
        return None

    if not fm.get("tag"):
        print(f"POMINIETO (brak tag): {path}")
        return None

    date_str, pl_slug = slug_from_filename(path)
    y, mo, d = date_parts(fm["date"])

    result = translate(client, fm, body)
    slug_en = result["slug_en"].strip().strip("-").lower()

    permalink_en = f"/en/aktualnosci/{y}/{mo}/{d}/{slug_en}/"
    lang_alt_en = f"/aktualnosci/{y}/{mo}/{d}/{pl_slug}/"   # EN -> PL

    en_fm = build_en_frontmatter(
        fm, slug_en, result["title_en"], result["summary_en"],
        permalink_en, lang_alt_en,
    )
    en_path = os.path.join(POSTS_DIR, f"{date_str}-{slug_en}.md")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_fm + "\n\n" + result["body_en"].rstrip() + "\n")

    # Zaktualizuj PL lang_alt -> EN
    patch_pl_lang_alt(path, raw_fm, permalink_en)

    print(f"UTWORZONO: {en_path}")
    print(f"ZAKTUALIZOWANO lang_alt w: {path}")
    return en_path


def main():
    args = sys.argv[1:]
    if not args:
        print("Uzycie: python scripts/translate_post.py <plik_pl.md> [...]")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY nie ustawiony — pomijam tlumaczenie.")
        sys.exit(0)   # bezpieczny default (jak indexnow.yml)

    client = Anthropic(api_key=api_key)

    created = []
    for path in args:
        if not os.path.exists(path):
            print(f"POMINIETO (brak pliku): {path}")
            continue
        try:
            out = process(path, client)
            if out:
                created.append(out)
        except Exception as e:
            print(f"BLAD przy {path}: {e}", file=sys.stderr)

    if created:
        print(f"\nUtworzono {len(created)} plikow EN.")
    else:
        print("\nNic nie utworzono.")


if __name__ == "__main__":
    main()
