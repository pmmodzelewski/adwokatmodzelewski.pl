---
title: "Sample post — how the blog works"
date: 2026-05-07
lang: en
summary: "A short example showing how a single blog post looks and is authored. Safe to delete once the first real article is added."
lang_alt: /blog/2026/05/07/przykladowy-wpis/
sitemap: false
robots: noindex
---

This is a **sample post** showing what a finished blog article looks like.
It can be removed once the first real post is added.

## How to add a new post

Each post is a single Markdown (`.md`) file in the `_posts/` directory.
The filename must follow this pattern:

```
YYYY-MM-DD-short-title.md
```

For example: `2026-05-07-divorce-asset-division.md`.

## Front-matter (metadata at the top)

At the very top of the file, between two `---` lines, are the metadata fields:

- `title` — the post title (shown on the list and on the post page)
- `date` — publication date in `YYYY-MM-DD` format (controls sorting)
- `lang` — `pl` or `en`
- `summary` — short description shown on the post list
- `lang_alt` *(optional)* — URL of the same content in the other language

## Body

Below the metadata, the body is plain Markdown text:

- **bold** with double asterisks
- *italic* with single asterisks
- lists start with `-` or `*`
- links [like this](https://example.com)
- headings: `## Heading`, `### Smaller heading`

> Quotes start with a `>` at the beginning of the line.

After committing and pushing to GitHub, the post appears on the site
automatically within about a minute.
