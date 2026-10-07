# -*- coding: utf-8 -*-
"""
mobilcv.net - tek seferlik blog düzeltme scripti
Deponun KÖK klasöründe çalıştırın:   python blog_duzelt.py

Yaptıkları:
 1) Eski makalelerin içine yanlışlıkla gömülmüş ikinci HTML belgesini
    (<!DOCTYPE>, <html>, <head>, <title>, <body>) ve ikinci <h1> başlığını temizler.
 2) Canonical etiketi olmayan tüm sayfalara canonical ekler.
 3) Açıklaması (meta description) olmayan blog ana sayfalarına açıklama ekler.
Tekrar çalıştırmak zararsızdır.
"""
import re
from pathlib import Path

BASE = "https://mobilcv.net"
DESCS = {
    "index.html": "MobilCV Blog: CV hazırlama, iş mülakatı ve kariyer planlama üzerine ücretsiz rehberler, ipuçları ve meslek bazlı CV örnekleri.",
    "haftalik-ipuclari.html": "Her hafta yeni kariyer ipuçları: CV hazırlama, mülakat teknikleri ve iş arama stratejileri üzerine kısa ve uygulanabilir öneriler.",
}


def url_for(rel):
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-len('index.html')]}"
    return f"{BASE}/{rel}"


def clean_article(inner):
    s = re.sub(r"```[a-zA-Z]*", "", inner)
    s = re.sub(r"<!DOCTYPE[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<head[^>]*>[\s\S]*?</head>", "", s, flags=re.I)
    s = re.sub(r"<title[^>]*>[\s\S]*?</title>", "", s, flags=re.I)
    s = re.sub(r"<meta[^>]*>", "", s, flags=re.I)
    s = re.sub(r"</?(html|body)[^>]*>", "", s, flags=re.I)
    # ilk <h1> (şablonun başlığı) kalır, sonrakiler silinir
    parts = re.split(r"(<h1[^>]*>[\s\S]*?</h1>)", s, flags=re.I)
    seen = False
    out = []
    for p in parts:
        if re.match(r"<h1[^>]*>", p, flags=re.I):
            if seen:
                continue
            seen = True
        out.append(p)
    s = "".join(out)
    s = re.sub(r"<header>\s*</header>", "", s, flags=re.I)
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s)
    return s


def main():
    root = Path(".")
    if not (root / "MobilCV.AIEngine").exists():
        raise SystemExit("HATA: Scripti mobilcv-net deposunun kök klasöründe çalıştırın.")
    fixed_art = fixed_can = fixed_desc = 0
    for f in sorted(root.rglob("*.html")):
        rel = f.as_posix()
        if rel.startswith("MobilCV.AIEngine/") or f.name.startswith("google"):
            continue
        s = f.read_text(encoding="utf-8")
        orig = s

        m = re.search(r"(<article>)([\s\S]*)(</article>)", s)
        if m:
            new_inner = clean_article(m.group(2))
            if new_inner != m.group(2):
                s = s[:m.start(2)] + new_inner + s[m.end(2):]
                fixed_art += 1

        if rel in DESCS and not re.search(r'<meta name="description"', s):
            s = re.sub(r"(</title>)", lambda mm: mm.group(1) + f'\n    <meta name="description" content="{DESCS[rel]}">', s, count=1)
            fixed_desc += 1

        if not re.search(r'<link rel="canonical"', s):
            anchor = re.search(r'<meta name="description"[^>]*>', s) or re.search(r"</title>", s)
            if anchor:
                s = s[:anchor.end()] + f'\n    <link rel="canonical" href="{url_for(rel)}">' + s[anchor.end():]
                fixed_can += 1

        if s != orig:
            f.write_text(s, encoding="utf-8")

    print(f"Temizlenen makale: {fixed_art}")
    print(f"Eklenen canonical: {fixed_can}")
    print(f"Eklenen açıklama : {fixed_desc}")
    print("TAMAM. Şimdi: git add .  /  git commit -m \"Blog duzeltme\"  /  git push  (ayrı ayrı)")


if __name__ == "__main__":
    main()
