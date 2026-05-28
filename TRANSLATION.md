# Automatyczne tłumaczenia wpisów (PL → EN)

> Ten plik jest **wykluczony z outputu Jekyll** (`exclude:` w `_config.yml`) —
> nie trafia na stronę. To dokumentacja dla właściciela / współpracowników.

## Co to robi

Gdy na `main` pojawi się nowy wpis po polsku w `_posts/`, GitHub Action
tłumaczy go na angielski przez Anthropic API (Claude) i **otwiera Pull Request**
z gotowym plikiem EN. Właściciel przegląda tłumaczenie i scala PR — dopiero
wtedy wpis EN trafia na stronę. Żadne tłumaczenie nie publikuje się samo.

## Przepływ

1. Dodajesz wpis PL: `_posts/RRRR-MM-DD-tytul.md` (jak zwykle).
2. Push na `main`.
3. Workflow `Translate new posts (PL -> EN)` wykrywa nowy plik, tłumaczy,
   otwiera PR zatytułowany „Tłumaczenie EN: nowe wpisy".
4. Przeglądasz PR — sprawdzasz jakość i terminy prawne, możesz edytować pliki
   bezpośrednio w PR.
5. Scalasz PR. Wpis EN jest na stronie pod `/en/aktualnosci/...`.

## Kontrakt pliku EN (co generuje skrypt)

Dla wpisu PL `_posts/2026-05-18-kara-umowna.md` powstaje
`_posts/2026-05-18-<angielski-slug>.md`:

```yaml
---
title: "(przetłumaczony tytuł)"
date: 2026-05-18                 # taka sama jak w PL
lang: en
tag: prawo-cywilne              # NIEzmieniony — kanoniczny PL slug
summary: "(przetłumaczony opis)"
permalink: /en/aktualnosci/2026/05/18/<angielski-slug>/   # WYMAGANE
lang_alt: /aktualnosci/2026/05/18/kara-umowna/            # link do PL
sitemap: false                  # dziedziczone z PL (jeśli były)
robots: noindex                 # dziedziczone z PL (jeśli były)
---
(przetłumaczona treść Markdown)
```

Kluczowe zasady:
- **`permalink` jest wymagany** w plikach EN. Globalny permalink w `_config.yml`
  (`/aktualnosci/:year/...`) nie ma prefiksu `/en/`, więc bez jawnego
  `permalink:` wpis EN wylądowałby pod `/aktualnosci/...`. Jawny permalink daje
  poprawny `/en/aktualnosci/...`. (Tak samo robią strony specjalizacji EN.)
- **`tag` się nie tłumaczy** — zostaje kanoniczny PL slug. Listy EN mapują go
  na etykietę/URL EN przez `_data/tags.yml`.
- **`lang_alt` jest dwukierunkowy**: wpis PL wskazuje na EN, wpis EN na PL.
  Skrypt aktualizuje też `lang_alt` w oryginalnym pliku PL.

## Loop guard (dlaczego nie ma nieskończonej pętli)

Scalenie PR-a to push na `main` → ponowny trigger workflow. Skrypt pomija
wpis PL, który ma już `lang_alt` wskazujący na **istniejący** plik EN. Po
scaleniu oba warunki są spełnione, więc kolejny run nic nie robi.

## Jak uruchomić ręcznie

- **Z GitHuba:** zakładka Actions → „Translate new posts (PL -> EN)" →
  „Run workflow". Przy ręcznym odpaleniu skrypt sprawdza wszystkie wpisy
  i tłumaczy te bez odpowiednika EN.
- **Lokalnie** (np. żeby zobaczyć wynik przed pushem):
  ```bash
  # przez wirtualne srodowisko .env (zasada projektu)
  export ANTHROPIC_API_KEY=sk-ant-...
  python scripts/translate_post.py _posts/2026-05-18-kara-umowna.md
  ```
  Skrypt utworzy plik EN i zaktualizuje `lang_alt` w PL. Obejrzyj `git diff`,
  potem commit/PR ręcznie.

## Konfiguracja (jednorazowa, po stronie właściciela repo)

1. **Klucz API:** utwórz na console.anthropic.com (to osobny, płatny od zużycia
   produkt — subskrypcja Claude Max go NIE obejmuje).
2. **Sekret repo:** Settings → Secrets and variables → Actions → New repository
   secret, nazwa `ANTHROPIC_API_KEY`.
3. **Uprawnienia Actions:** Settings → Actions → General → Workflow permissions →
   „Read and write permissions" + zaznacz „Allow GitHub Actions to create and
   approve pull requests". Bez tego workflow nie otworzy PR-a.

Bez sekretu skrypt loguje informację i kończy bez błędu — repo się nie psuje.

## Koszt

Rzędu 1–4 centów za wpis (model `claude-sonnet`, ~200–400 słów + system prompt
z cache). Przy paru wpisach miesięcznie — grosze.

## Zła jakość tłumaczenia?

Edytuj plik EN bezpośrednio w PR przed scaleniem. Jeśli chcesz przetłumaczyć
od nowa: usuń plik EN i `lang_alt` z pliku PL, potem odpal workflow ręcznie.

## Zmiana modelu

Skrypt czyta `TRANSLATE_MODEL` ze środowiska (domyślnie `claude-sonnet-4-6`).
Można nadpisać w workflow albo lokalnie.
