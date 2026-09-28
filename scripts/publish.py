#!/usr/bin/env python3
"""Publish one already-reviewed HTML article fragment as a dated radar edition.

Usage: python3 scripts/publish.py YYYY-MM-DD input.html 'Headline' 'Short summary'
Input is a trusted authored HTML fragment: review its facts and links before publication.
"""
import html
import pathlib
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv) != 5:
    sys.exit(__doc__)
day = date.fromisoformat(sys.argv[1]).isoformat()
fragment = pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')
title, summary = sys.argv[3:5]
if any(x in fragment.lower() for x in ('<script', '<iframe', 'javascript:', '<form')):
    sys.exit('Unsafe active HTML; remove scripts/iframes/forms before publication')
if not fragment.strip():
    sys.exit('Empty edition')
def esc(s): return html.escape(s, quote=True)
def page(title, description, body, prefix=''):
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#e8f0eb"><title>{esc(title)} | רדאר AI</title><link rel="stylesheet" href="{prefix}style.css"></head><body><header><div class="wrap"><a class="mark" href="{prefix}index.html">רדאר AI</a><a class="nav" href="{prefix}archive.html">כל המהדורות ←</a></div></header><main class="wrap">{body}</main><footer><div class="wrap">רדאר AI · מקורות וקישורים בתוך כל מהדורה. בדקו תאריך לפני פעולה על מידע שמשתנה.</div></footer></body></html>'''
editions = ROOT / 'editions'
editions.mkdir(exist_ok=True)
article = f'<article class="panel article"><p class="eyebrow">מהדורת {day}</p><h1>{esc(title)}</h1><p class="intro">{esc(summary)}</p>{fragment}</article>'
(editions / f'{day}.html').write_text(page(title, summary, article, '../'), encoding='utf-8')
entries = []
for file in sorted(editions.glob('????-??-??.html'), reverse=True):
    content = file.read_text(encoding='utf-8')
    import re
    head = re.search(r'<h1>(.*?)</h1>', content, re.S)
    desc = re.search(r'<p class="intro">(.*?)</p>', content, re.S)
    entries.append((file.stem, html.unescape(head.group(1)) if head else file.stem, html.unescape(desc.group(1)) if desc else ''))
latest_day, latest_title, latest_summary = entries[0]
hero = f'<section class="panel hero"><p class="eyebrow">המהדורה האחרונה · {latest_day}</p><h1>{esc(latest_title)}</h1><p class="lede">{esc(latest_summary)}</p><a class="action" href="editions/{latest_day}.html">לקריאת המהדורה</a></section>'
archive_link = '<p style="margin-top:26px"><a href="archive.html">כל המהדורות ←</a></p>'
(ROOT / 'index.html').write_text(page('מהדורה אחרונה', latest_summary, hero + archive_link), encoding='utf-8')
items = ''.join(f'<li><span class="date">{d}</span><br><a href="editions/{d}.html">{esc(t)}</a><br>{esc(s)}</li>' for d,t,s in entries)
(ROOT / 'archive.html').write_text(page('ארכיון', 'מהדורות קודמות של רדאר AI', '<h1>כל המהדורות</h1><div class="panel"><ol class="archive-list">'+items+'</ol></div>'), encoding='utf-8')
print(f'Published {day}; latest: {latest_day}; archive: {len(entries)} editions')
