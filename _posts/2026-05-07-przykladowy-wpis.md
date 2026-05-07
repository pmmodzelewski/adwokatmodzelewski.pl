---
title: "Przykładowy wpis — jak korzystać z bloga"
date: 2026-05-07
lang: pl
summary: "Krótki przykład pokazujący jak wygląda i jak powstaje pojedynczy wpis blogowy. Można go bezpiecznie usunąć po dodaniu pierwszego prawdziwego artykułu."
lang_alt: /en/blog/2026/05/07/sample-post/
---

To jest **przykładowy wpis**, który pokazuje jak wygląda gotowy artykuł na blogu.
Można go usunąć, gdy pojawi się pierwszy prawdziwy wpis.

## Jak dodać nowy wpis

Każdy wpis to pojedynczy plik Markdown (`.md`) w katalogu `_posts/`.
Nazwa pliku musi mieć format:

```
RRRR-MM-DD-skrocony-tytul.md
```

Na przykład: `2026-05-07-rozwod-podzial-majatku.md`.

## Front-matter (metadane na górze pliku)

Na samej górze pliku, pomiędzy dwoma liniami `---`, znajdują się metadane:

- `title` — tytuł wpisu (wyświetlany na liście i na stronie wpisu)
- `date` — data publikacji w formacie `RRRR-MM-DD` (decyduje o sortowaniu)
- `lang` — `pl` lub `en`
- `summary` — krótki opis wyświetlany na liście wpisów
- `lang_alt` *(opcjonalnie)* — adres tej samej treści w drugim języku

## Treść wpisu

Pod metadanymi jest zwykły tekst w formacie Markdown:

- **pogrubienie** zapisujemy gwiazdkami
- *kursywę* też gwiazdkami (jedną)
- listy zaczynamy od `-` lub `*`
- linki [w taki sposób](https://example.com)
- nagłówki: `## Nagłówek`, `### Mniejszy nagłówek`

> Cytaty zaczynamy od znaku `>` na początku linii.

Po commicie i pushu na GitHuba wpis pojawia się na stronie automatycznie
w ciągu około minuty.
