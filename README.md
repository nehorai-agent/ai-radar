# Radar AI

A light static Hebrew RTL site. Every edition is a standalone page in `editions/YYYY-MM-DD.html`; `index.html` points to the latest, `archive.html` lists all editions.

To publish an **already fact-checked** edition, write its article body as an HTML fragment using headings, paragraphs, details/summary cards, and real source links, then run:

```sh
python3 scripts/publish.py YYYY-MM-DD /tmp/radar-edition.html 'כותרת המהדורה' 'משפט קצר שמחבר את הסיפורים'
git add index.html archive.html editions/ scripts/ style.css
git commit -m 'Publish radar YYYY-MM-DD'
git push origin main
```

Do not put private data, secrets, or unreviewed third-party HTML in a public repository. The script only blocks obvious active tags; it does not sanitize all HTML. Confirm published URL and render on a narrow mobile viewport after pushing. For the first publish, enable GitHub Pages in repository Settings → Pages, source Deploy from a branch, main / (root). GitHub Pages deployment is not immediate.
