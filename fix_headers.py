# ============================================================
# MobilCV - fix_headers v3 (nav ve footer BAĞIMSIZ kontrol edilir)
# ============================================================
# v1: class="active" olan linkleri (kendi sayfasını vurgulayan
#     sayfalarda) atlıyordu.
# v2: footer'da "cv-ornekleri.html" varsa TÜM dosyayı atlıyordu,
#     nav'daki eksikliği kaçırıyordu (cv-rehberi.html'de yaşanan
#     tam olarak buydu).
# v3: nav-links ve footer-links bloklarını AYRI AYRI, BAĞIMSIZ
#     kontrol eder - biri eksikse SADECE onu tamamlar.
# Güvenli: birden fazla kez çalıştırılabilir, zaten doğru olan
# kısımlara dokunmaz.
# ============================================================

import re
import glob


def fix_block(content, block_pattern, link_pattern, link_replacement):
    """block_pattern ile bir HTML bloğunu bulur, içinde 'cv-ornekleri.html'
    yoksa link_pattern eşleşmesinin hemen önüne link_replacement ekler."""
    block_match = re.search(block_pattern, content, re.DOTALL)
    if not block_match:
        return content, False  # blok bulunamadı

    block_text = block_match.group(0)
    if "cv-ornekleri.html" in block_text:
        return content, False  # bu blokta zaten var

    new_block_text, count = re.subn(link_pattern, link_replacement, block_text, count=1)
    if count == 0:
        return content, False  # beklenen link deseni bulunamadı

    content = content[:block_match.start()] + new_block_text + content[block_match.end():]
    return content, True


def main():
    html_files = glob.glob("*.html")
    if not html_files:
        print("⚠️  Bu klasörde hiç .html dosyası bulunamadı.")
        return

    nav_block_pattern = r'<ul class="nav-links">.*?</ul>'
    nav_link_pattern = r'(<li><a href="cv-rehberi\.html"[^>]*>CV Rehberi</a></li>)'
    nav_link_replacement = r'<li><a href="cv-ornekleri.html">CV Örnekleri</a></li>\n                \1'

    footer_block_pattern = r'<div class="footer-links">.*?</div>'
    footer_link_pattern = r'(<a href="cv-rehberi\.html"[^>]*>CV Rehberi</a>)'
    footer_link_replacement = r'<a href="cv-ornekleri.html">CV Örnekleri</a>\n            \1'

    updated = []
    no_change = []

    for filename in html_files:
        with open(filename, encoding='utf-8') as f:
            content = f.read()

        original = content
        changed_nav = False
        changed_footer = False

        content, changed_nav = fix_block(content, nav_block_pattern, nav_link_pattern, nav_link_replacement)
        content, changed_footer = fix_block(content, footer_block_pattern, footer_link_pattern, footer_link_replacement)

        if changed_nav or changed_footer:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            detail = []
            if changed_nav:
                detail.append("nav")
            if changed_footer:
                detail.append("footer")
            updated.append(f"{filename} ({' + '.join(detail)})")
        else:
            no_change.append(filename)

    print(f"\n✅ Güncellenen dosyalar ({len(updated)}):")
    for f in updated:
        print(f"   - {f}")

    print(f"\n☑️  Değişmeyen dosyalar ({len(no_change)}) - zaten güncel veya beklenmeyen yapıda:")
    for f in no_change:
        print(f"   - {f}")

    print(f"\n🎉 Tamamlandı!")


if __name__ == "__main__":
    main()
