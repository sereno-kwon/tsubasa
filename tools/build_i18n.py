#!/usr/bin/env python3
"""Build the English and Japanese pages from the Korean index.html.

index.html (Korean) is the only page you edit by hand. This script reads it,
swaps every Korean string for the matching entry in i18n/<lang>.json and writes
<lang>/index.html. If a Korean string has no translation, the build stops and
lists what is missing, so the other languages never go out half-translated.

    python3 tools/build_i18n.py          # build en/ and ja/
    python3 tools/build_i18n.py --check  # only report missing translations
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
LANGS = ["en", "ja"]
HANGUL = re.compile(r"[가-힣]")
# Korean that may stay on translated pages: the language picker label and
# the official mail-order registration number.
ALLOWED = ["한국어", "2016-서울서초-2062"]
LEADING_PUNCT = tuple(".,;:!?。、")


def translate_text_nodes(html, table, missing):
    """Replace Korean text between tags, leaving <style>/<script> alone."""
    out, pos = [], 0
    for m in re.finditer(r"<(style|script)\b[^>]*>.*?</\1>", html, re.S):
        out.append(_text_nodes(html[pos:m.start()], table, missing))
        block = m.group(0)
        if 'type="application/ld+json"' in block:
            block = _jsonld(block, table, missing)
        out.append(block)
        pos = m.end()
    out.append(_text_nodes(html[pos:], table, missing))
    return "".join(out)


def _lookup(s, table, missing):
    if s in table:
        return table[s]
    missing.add(s)
    return s


def _text_nodes(chunk, table, missing):
    def node(m):
        raw = m.group(1)
        core = raw.strip()
        if not core or not HANGUL.search(core) or core in ALLOWED:
            return m.group(0)
        lead = raw[: len(raw) - len(raw.lstrip())]
        tail = raw[len(raw.rstrip()):]
        new = _lookup(core, table, missing)
        if new.startswith(LEADING_PUNCT):
            lead = ""
        return ">" + lead + new + tail + "<"

    chunk = re.sub(r">([^<>]+)<", node, chunk)

    def attr(m):
        val = m.group(2)
        if not HANGUL.search(val) or val in ALLOWED:
            return m.group(0)
        return f'{m.group(1)}="{_lookup(val, table, missing)}"'

    return re.sub(r'\b(alt|aria-label|title|content|placeholder)="([^"]*)"', attr, chunk)


def _jsonld(block, table, missing):
    def s(m):
        val = m.group(1)
        if not HANGUL.search(val):
            return m.group(0)
        return json.dumps(_lookup(val, table, missing), ensure_ascii=False)

    return re.sub(r'"([^"\\]*)"', s, block)


def build(lang, src):
    cfg = json.loads((ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
    html, missing = src, set()

    for ko, tr in cfg.get("blocks", []):
        if ko not in html:
            missing.add("[block] " + ko[:60].replace("\n", " ") + "...")
        html = html.replace(ko, tr)

    html = translate_text_nodes(html, cfg["text"], missing)

    url = cfg["url"]
    html = html.replace('<html lang="ko">', f'<html lang="{lang}">', 1)
    html = html.replace('<link rel="canonical" href="https://tsubasabicycles.co.kr/">',
                        f'<link rel="canonical" href="{url}">', 1)
    html = html.replace('<meta property="og:url" content="https://tsubasabicycles.co.kr/">',
                        f'<meta property="og:url" content="{url}">', 1)
    # og:locale: this language first, the other two as alternates
    locales = {"ko": "ko_KR", "en": "en_US", "ja": "ja_JP"}
    block = f'<meta property="og:locale" content="{locales[lang]}">' + "".join(
        f'\n<meta property="og:locale:alternate" content="{v}">' for k, v in locales.items() if k != lang)
    html = re.sub(r'<meta property="og:locale" content="ko_KR">(\n<meta property="og:locale:alternate"[^>]*>)*',
                  block, html, count=1)
    # fonts
    html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">',
                  f'<link rel="stylesheet" href="{cfg["fonts"]}">', html, count=1)
    html = re.sub(r"--ko:[^;]+;", f"--ko:{cfg['body_font']};", html, count=1)
    html = html.replace('"inLanguage": "ko-KR"', f'"inLanguage": "{cfg["locale"].replace("_", "-")}"', 1)
    # assets live one folder up
    html = re.sub(r'(src|href)="images/', r'\1="../images/', html)
    html = html.replace("url(images/", "url(../images/")
    # language links
    targets = {"ko": "../", "en": "../en/", "ja": "../ja/"}
    html = re.sub(r'data-lang="(ko|en|ja)"(\s+hreflang="\1"\s+lang="\1"\s+)href="[^"]*"',
                  lambda m: f'data-lang="{m.group(1)}"{m.group(2)}href="{targets[m.group(1)]}"', html)

    # Korean in code comments is fine; check only what a visitor or crawler sees
    visible = re.sub(r"<!--.*?-->|/\*.*?\*/", "", html, flags=re.S)
    leftover = sorted({s for s in re.findall(r"[^<>\"]*[가-힣][^<>\"]*", visible)
                       if not any(a in s for a in ALLOWED)})
    return html, sorted(missing), leftover


def main():
    check = "--check" in sys.argv
    src = SRC.read_text(encoding="utf-8")
    ok = True
    for lang in LANGS:
        html, missing, leftover = build(lang, src)
        if missing or leftover:
            ok = False
            print(f"[{lang}] missing translations ({len(missing)}):")
            for s in missing:
                print("   ", s)
            extra = [s for s in leftover if s.strip() not in missing]
            if extra:
                print(f"[{lang}] Korean left on the page:")
                for s in extra:
                    print("   ", s.strip())
            continue
        if not check:
            out = ROOT / lang / "index.html"
            out.parent.mkdir(exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print(f"[{lang}] wrote {out.relative_to(ROOT)}")
        else:
            print(f"[{lang}] ok")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
