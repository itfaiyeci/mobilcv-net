# -*- coding: utf-8 -*-
"""Instagram resmi API (Instagram Login) ile paylasim.
Kullanim:
  python3 scripts/ig_paylas.py kontrol [tr|en]  -> anahtar ve hesap kontrolu (paylasim YOK)
  python3 scripts/ig_paylas.py paylas  [tr|en]  -> kuyruktaki onayli ve paylasilmamis gonderileri paylasir
Hesaplar: tr = @mobilcvcom (IG_TOKEN, platform "instagram", alanlar paylasildi/medya_id/baglanti)
          en = @mobilcv.en (IG_TOKEN_EN, platform "instagram_en", alanlar en_paylasildi/en_medya_id/en_baglanti;
               metin "aciklama_en", gorsel "gorsel_url_en"; yoksa aciklama/gorsel_url)
EN anahtari tanimli degilse paylas sessizce atlar; kontrol hata verir. Gorseller herkese acik adresten (https://mobilcv.net/sosyal/...) cekilir."""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://graph.instagram.com"
HESAPLAR = {
    "tr": {"kullanici": "mobilcvcom", "anahtar": "IG_TOKEN", "platform": "instagram", "on": "", "metin": "aciklama", "gorsel": "gorsel_url"},
    "en": {"kullanici": "mobilcv.en", "anahtar": "IG_TOKEN_EN", "platform": "instagram_en", "on": "en_", "metin": "aciklama_en", "gorsel": "gorsel_url_en"},
}
HESAP = HESAPLAR[sys.argv[2] if len(sys.argv) > 2 else "tr"]
BEKLENEN_KULLANICI = HESAP["kullanici"]
KUYRUK = Path("sosyal/kuyruk.json")
TOKEN = os.environ.get(HESAP["anahtar"], "").strip()

def istek(yol, veri=None, yontem="GET"):
    params = dict(veri or {}); params["access_token"] = TOKEN
    q = urllib.parse.urlencode(params)
    url = f"{API}/{yol}"
    req = urllib.request.Request(url + ("?" + q if yontem == "GET" else ""), data=(q.encode() if yontem == "POST" else None), method=yontem)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        govde = e.read().decode(errors="replace")
        govde = govde.replace(TOKEN, "***") if TOKEN else govde
        raise SystemExit(f"API hatasi {e.code} ({yol}): {govde[:500]}")

def hesap():
    me = istek("me", {"fields": "user_id,username,account_type"})
    if me.get("username") != BEKLENEN_KULLANICI:
        raise SystemExit(f"Beklenmeyen hesap: {me.get('username')} (beklenen {BEKLENEN_KULLANICI}). Durduruldu.")
    return me

def kontrol():
    me = hesap()
    print(f"Anahtar calisiyor. Hesap: @{me['username']} | tur: {me.get('account_type')} | id: {me.get('user_id')}")

def paylas():
    me = hesap(); uid = me["user_id"]
    kuyruk = json.loads(KUYRUK.read_text(encoding="utf-8")) if KUYRUK.exists() else []
    on = HESAP["on"]
    bekleyen = [g for g in kuyruk if g.get("onay") is True and HESAP["platform"] in g.get("platformlar", ["instagram"]) and not g.get(on + "paylasildi")]
    if not bekleyen:
        print("Onayli ve paylasilmamis gonderi yok."); return
    for g in bekleyen[:2]:  # bir calismada en fazla 2 gonderi
        gorsel = g.get(HESAP["gorsel"]) or g["gorsel_url"]; metin = g.get(HESAP["metin"]) or g["aciklama"]
        kap = istek(f"{uid}/media", {"image_url": gorsel, "caption": metin}, "POST")
        cid = kap["id"]
        for _ in range(20):
            durum = istek(cid, {"fields": "status_code"}).get("status_code")
            if durum == "FINISHED": break
            if durum in ("ERROR", "EXPIRED"): raise SystemExit(f"Gorsel islenemedi ({g['id']}): {durum}")
            time.sleep(5)
        yay = istek(f"{uid}/media_publish", {"creation_id": cid}, "POST")
        mid = yay["id"]
        link = istek(mid, {"fields": "permalink"}).get("permalink", "")
        g[on + "paylasildi"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"); g[on + "medya_id"] = mid; g[on + "baglanti"] = link
        print(f"Paylasildi (@{BEKLENEN_KULLANICI}): {g['id']} -> {link}")
        time.sleep(10)
    KUYRUK.write_text(json.dumps(kuyruk, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    islem = sys.argv[1] if len(sys.argv) > 1 else "kontrol"
    if not TOKEN:
        if islem == "paylas" and HESAP["anahtar"] != "IG_TOKEN":
            print(f"{HESAP['anahtar']} tanimli degil; @{BEKLENEN_KULLANICI} adimi atlandi."); sys.exit(0)
        raise SystemExit(f"{HESAP['anahtar']} tanimli degil.")
    {"kontrol": kontrol, "paylas": paylas}[islem]()
