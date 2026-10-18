# -*- coding: utf-8 -*-
"""Instagram resmi API (Instagram Login) ile paylasim.
Kullanim:
  python3 scripts/ig_paylas.py kontrol   -> anahtar ve hesap kontrolu (paylasim YOK)
  python3 scripts/ig_paylas.py paylas    -> sosyal/kuyruk.json'da onay=true ve paylasildi=null olanlari paylasir
Anahtar: IG_TOKEN ortam degiskeni (GitHub Secrets). Gorseller herkese acik adresten (https://mobilcv.net/sosyal/...) cekilir."""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://graph.instagram.com"
BEKLENEN_KULLANICI = "mobilcvcom"
KUYRUK = Path("sosyal/kuyruk.json")
TOKEN = os.environ.get("IG_TOKEN", "").strip()

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
    bekleyen = [g for g in kuyruk if g.get("onay") is True and "instagram" in g.get("platformlar", ["instagram"]) and not g.get("paylasildi")]
    if not bekleyen:
        print("Onayli ve paylasilmamis gonderi yok."); return
    for g in bekleyen[:2]:  # bir calismada en fazla 2 gonderi
        kap = istek(f"{uid}/media", {"image_url": g["gorsel_url"], "caption": g["aciklama"]}, "POST")
        cid = kap["id"]
        for _ in range(20):
            durum = istek(cid, {"fields": "status_code"}).get("status_code")
            if durum == "FINISHED": break
            if durum in ("ERROR", "EXPIRED"): raise SystemExit(f"Gorsel islenemedi ({g['id']}): {durum}")
            time.sleep(5)
        yay = istek(f"{uid}/media_publish", {"creation_id": cid}, "POST")
        mid = yay["id"]
        link = istek(mid, {"fields": "permalink"}).get("permalink", "")
        g["paylasildi"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"); g["medya_id"] = mid; g["baglanti"] = link
        print(f"Paylasildi: {g['id']} -> {link}")
        time.sleep(10)
    KUYRUK.write_text(json.dumps(kuyruk, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    if not TOKEN: raise SystemExit("IG_TOKEN tanimli degil.")
    {"kontrol": kontrol, "paylas": paylas}[sys.argv[1] if len(sys.argv) > 1 else "kontrol"]()
