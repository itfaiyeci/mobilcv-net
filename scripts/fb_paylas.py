# -*- coding: utf-8 -*-
"""Facebook sayfası (Mobilcv.com) resmi Graph API ile paylaşım.
Kullanım:
  python3 scripts/fb_paylas.py kontrol   -> anahtar ve sayfa kontrolü (paylaşım YOK)
  python3 scripts/fb_paylas.py paylas    -> kuyrukta onay=true, platformlarda "facebook" olan, fb_paylasildi boş kayıtları paylaşır
Anahtar: FB_PAGE_TOKEN (sayfa erişim anahtarı; GitHub Secrets). Tanımlı değilse paylaş modunda sessizce atlar, kontrolde hata verir.
Metin: "aciklama_facebook" varsa o; yoksa "aciklama_threads"; yoksa "aciklama".
Not: Meta uygulaması geliştirme modundayken API gönderileri yalnızca uygulamada rolü olanlara görünür; herkese açık olması için uygulama Canlı (Live) olmalı."""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://graph.facebook.com/v21.0"
BEKLENEN_SAYFA = "Mobilcv.com"
KUYRUK = Path("sosyal/kuyruk.json")
TOKEN = os.environ.get("FB_PAGE_TOKEN", "").strip()

def istek(yol, veri=None, yontem="GET"):
    params = dict(veri or {}); params["access_token"] = TOKEN
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{API}/{yol}" + ("?" + q if yontem == "GET" else ""), data=(q.encode() if yontem == "POST" else None), method=yontem)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        govde = e.read().decode(errors="replace")
        govde = govde.replace(TOKEN, "***") if TOKEN else govde
        raise SystemExit(f"Facebook API hatası {e.code} ({yol}): {govde[:500]}")

def sayfa():
    me = istek("me", {"fields": "id,name"})
    if me.get("name") != BEKLENEN_SAYFA:
        raise SystemExit(f"Beklenmeyen hesap/sayfa: {me.get('name')} (beklenen {BEKLENEN_SAYFA}). Sayfa anahtarı değil ya da yanlış sayfa. Durduruldu.")
    return me

def kontrol():
    me = sayfa()
    print(f"Facebook sayfa anahtarı çalışıyor. Sayfa: {me['name']} | id: {me['id']}")

def paylas():
    me = sayfa(); pid = me["id"]
    kuyruk = json.loads(KUYRUK.read_text(encoding="utf-8")) if KUYRUK.exists() else []
    bekleyen = [g for g in kuyruk if g.get("onay") is True and "facebook" in g.get("platformlar", ["instagram"]) and not g.get("fb_paylasildi")]
    if not bekleyen:
        print("Facebook için onaylı ve paylaşılmamış gönderi yok."); return
    for g in bekleyen[:2]:  # bir çalışmada en fazla 2 gönderi
        metin = (g.get("aciklama_facebook") or g.get("aciklama_threads") or g.get("aciklama") or "").strip()
        if g.get("gorsel_url"):
            r = istek(f"{pid}/photos", {"url": g["gorsel_url"], "caption": metin, "published": "true"}, "POST")
            gid = r.get("post_id") or r.get("id")
        else:
            gid = istek(f"{pid}/feed", {"message": metin}, "POST")["id"]
        time.sleep(3)
        link = istek(gid, {"fields": "permalink_url"}).get("permalink_url", "")
        g["fb_paylasildi"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"); g["fb_medya_id"] = gid; g["fb_baglanti"] = link
        print(f"Facebook'ta paylaşıldı: {g['id']} -> {link}")
        time.sleep(10)
    KUYRUK.write_text(json.dumps(kuyruk, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    islem = sys.argv[1] if len(sys.argv) > 1 else "kontrol"
    if not TOKEN:
        if islem == "kontrol": raise SystemExit("FB_PAGE_TOKEN tanımlı değil.")
        print("FB_PAGE_TOKEN tanımlı değil; Facebook adımı atlandı."); sys.exit(0)
    {"kontrol": kontrol, "paylas": paylas}[islem]()
