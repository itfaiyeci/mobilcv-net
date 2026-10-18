# Sosyal medya kuyruğu

- `kuyruk.json`: paylaşılacak gönderiler. Her kayıt: `id`, `gorsel_url` (https://mobilcv.net/sosyal/... JPEG), `aciklama` (Instagram metni), `aciklama_threads` (isteğe bağlı; Threads metni, en çok 500 karakter, yoksa `aciklama` kullanılır), `platformlar` (ör. `["instagram", "threads"]`; İngilizce hesap için `"instagram_en"` ve isteğe bağlı `aciklama_en`, `gorsel_url_en`; yazılmazsa yalnızca Türkçe Instagram), `onay` (kurucu "ok" deyince true).
- Otomatik doldurulan alanlar: Instagram için `paylasildi`, `medya_id`, `baglanti`; Threads için `th_paylasildi`, `th_medya_id`, `th_baglanti`; İngilizce Instagram için `en_paylasildi`, `en_medya_id`, `en_baglanti`.
- Paylaşım `.github/workflows/instagram.yml` ile yapılır (önce Instagram, sonra Threads; biri hata verse de diğeri çalışır). Sıra: Türkçe Instagram, İngilizce Instagram, Threads. Anahtarlar GitHub Secrets'ta: `IG_TOKEN`, `IG_TOKEN_EN`, `THREADS_TOKEN`.
- Kurucu onayı olmadan `onay: true` yapılmaz. Bir çalışmada platform başına en fazla 2 gönderi.
