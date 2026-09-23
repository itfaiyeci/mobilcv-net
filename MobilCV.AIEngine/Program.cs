using OpenAI.Chat;
using System.Globalization;
using System.Text.RegularExpressions;

namespace MobilCV.AIEngine
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("🚀 MobilCV AI Motoru Başlatılıyor...");
            
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("OPENAI_API_KEY bulunamadı!");
            var client = new ChatClient("gpt-3.5-turbo", apiKey);

            // ===== KATEGORİ VE KONU HAVUZU =====
            // Not: Havuz genişletildi (17 -> 27 konu). Script artık aynı konuyu
            // tekrar seçmediği için, havuz ne kadar büyükse o kadar geç tükenir.
            var topics = new Dictionary<string, List<string>>
            {
                ["CV-Rehberi"] = new List<string>
                {
                    "CV'de Dikkat Edilmesi Gereken 7 Kritik Nokta",
                    "Etkili Bir Ön Yazı Nasıl Yazılır?",
                    "CV'de Fotoğraf Kullanmalı mısınız?",
                    "Yeni Mezunlar İçin CV Hazırlama Rehberi",
                    "ATS Sistemlerini Geçen CV Nasıl Hazırlanır?",
                    "CV'de Hangi Kelimeler Kullanılmamalı?",
                    "İngilizce CV Hazırlarken Dikkat Edilmesi Gerekenler",
                    "CV ile Özgeçmiş Arasındaki Fark Nedir?"
                },
                ["Mülakat-Taktikleri"] = new List<string>
                {
                    "Mülakatta Başarılı Olmanın 10 Altın Kuralı",
                    "En Zor Mülakat Sorularına Cevaplar",
                    "Uzaktan Mülakatlarda Başarılı Olma Taktikleri",
                    "Mülakatta Maaş Pazarlığı Nasıl Yapılır?",
                    "Grup Mülakatlarında Öne Çıkmanın Yolları",
                    "Mülakat Sonrası Teşekkür E-postası Nasıl Yazılır?"
                },
                ["Kariyer-Planlama"] = new List<string>
                {
                    "Kariyer Planlaması Adım Adım Rehber",
                    "30 Yaşından Önce Kariyerinde Yapman Gereken 5 Hamle",
                    "Sektör Değiştirmek İsteyenler İçin Rehber",
                    "Kariyer Molası Vermek İsteyenler İçin Öneriler",
                    "İkinci Bir Kariyere Nasıl Başlanır?"
                },
                ["İş-Dünyası-Trendleri"] = new List<string>
                {
                    "2026'nın En Popüler 10 Mesleği",
                    "Uzaktan Çalışmanın Geleceği ve Trendler",
                    "Yapay Zeka Hangi Meslekleri Dönüştürecek?",
                    "Hibrit Çalışma Modeli Kariyerini Nasıl Etkiler?",
                    "Freelance Çalışmaya Geçiş Rehberi"
                },
                ["Başarı-Hikayeleri"] = new List<string>
                {
                    "Sektör Değiştirerek Hayalindeki İşe Ulaşanlar",
                    "Girişimcilik Hikayeleri Sıfırdan Başarıya",
                    "Kadın Girişimcilerin Başarı Hikayeleri",
                    "Küçük Bir Fikirden Büyük Bir Şirkete Uzanan Yolculuklar"
                }
            };

            // ===== DAHA ÖNCE YAZILMIŞ KONULARI HAVUZDAN ÇIKAR =====
            // Önceki hatanın kök nedeni: script hangi konuların zaten işlendiğini
            // hiç kontrol etmiyordu. Artık slug'ı zaten bir HTML dosyası olarak
            // var olan konular aday listesinden çıkarılıyor.
            var availableTopics = new List<(string Category, string Topic, string Slug)>();
            foreach (var kvp in topics)
            {
                foreach (var t in kvp.Value)
                {
                    string s = Slugify(t);
                    string path = Path.Combine("..", $"{s}.html");
                    if (!File.Exists(path))
                    {
                        availableTopics.Add((kvp.Key, t, s));
                    }
                }
            }

            if (availableTopics.Count == 0)
            {
                Console.WriteLine("⚠️ Havuzdaki tüm konular zaten yazılmış! Yukarıdaki 'topics' sözlüğüne yeni konular eklemeniz gerekiyor. İşlem sonlandırılıyor (hata değil).");
                return;
            }

            // ===== RASTGELE (AMA DAHA ÖNCE YAZILMAMIŞ) KONU SEÇ =====
            Random random = new Random();
            var selected = availableTopics[random.Next(availableTopics.Count)];
            string selectedCategory = selected.Category;
            string topic = selected.Topic;
            string slug = selected.Slug;

            Console.WriteLine($"📂 Kategori: {selectedCategory}");
            Console.WriteLine($"📝 Konu: {topic}");
            Console.WriteLine($"📊 Havuzda kalan işlenmemiş konu sayısı: {availableTopics.Count - 1}");

            try
            {
                // ===== PROFESYONEL VE TELİF GÜVENLİ PROMPT =====
                var messages = new List<ChatMessage>
                {
                    new SystemChatMessage(@"Sen, 10 yıllık deneyime sahip, iş dünyası trendlerini yakından takip eden bir kariyer uzmanısın.

                    **TELİF HAKKI KURALI (KIRMIZI ÇİZGİ):**
                    - Asla başka kaynaklardan birebir alıntı yapma.
                    - İstatistikler, veriler veya örnekler verirken bunları KENDİ CÜMLELERİNLE yorumla ve sentezle.
                    - Kaynakça bölümünde gerçek bir kaynak belirtme, sadece 'Yararlanılan Kaynaklar' başlığı altında genel bir bilgi ver.
                    - Hiçbir şekilde başka bir yazarın, kurumun veya web sitesinin metnini kopyalama.
                    - Oluşturduğun tüm içerik %100 ÖZGÜN ve SANA AİT olmalı.
                    - Eğer bir istatistik veya araştırma sonucu paylaşacaksan, bunu 'araştırmalar gösteriyor ki...' veya 'uzmanların belirttiğine göre...' gibi genel ifadelerle belirt, doğrudan bir kaynağa atıf yapma.

                    **İÇERİK KALİTESİ:**
                    - Makalelerin hem bilgilendirici hem de uygulanabilir tavsiyeler içermeli.
                    - Okuyucuya gerçek değer katmalı.
                    - Yazım tarzı: Resmi ama samimi, bilgilendirici ve akıcı.
                    - Türkçe dilbilgisi kurallarına tam uygun."),
                    
                    new UserChatMessage($@"
                        Aşağıdaki konu hakkında 1000-1200 kelimelik, kapsamlı, ÖZGÜN ve TELİF HAKKINA UYGUN bir blog makalesi yaz.

                        KONU: {topic}
                        KATEGORİ: {selectedCategory}

                        Makalede şunlar olsun:
                        1. Dikkat çekici, SEO uyumlu bir başlık (H1)
                        2. Konuya ilgi çekici bir giriş (2-3 paragraf)
                        3. 4-6 alt başlık (H2) ile detaylandırılmış içerik
                           - Her bölümde özgün yorumlar, sentezlenmiş bilgiler ve genel eğilimler kullan
                           - Gerektiğinde madde işaretli listeler (ul/li)
                        4. Sonuç bölümü (özet ve okuyucuya eylem çağrısı)
                        5. 150-160 karakterlik meta açıklama
                        6. Makale sonunda 'Yararlanılan Kaynaklar' başlığı altında genel bilgi (örnek: 'Bu makale hazırlanırken çeşitli akademik yayınlar, sektör raporları ve iş dünyası analizlerinden yararlanılmıştır.')

                        **UNUTMA:**
                        - Tüm içerik %100 ÖZGÜN olmalı.
                        - Başka kaynaklardan birebir alıntı yapma.
                        - İstatistik ve verileri kendi cümlelerinle yorumla.

                        Sadece HTML kodunu ver, başka bir açıklama yapma.
                    ")
                };

                var response = await client.CompleteChatAsync(messages);
                string htmlContent = response.Value.Content[0].Text;

                // ===== META AÇIKLAMAYI ÇIKAR =====
                string metaDescription = topic + " - " + selectedCategory.Replace("-", " ") + " kategorisinde kapsamlı bir rehber.";

                // ===== HTML DOSYASINI OLUŞTUR =====
                string fileName = $"{slug}.html";
                string fullHtml = BuildHtmlPage(topic, metaDescription, htmlContent, slug, selectedCategory);
                
                string filePath = Path.Combine("..", fileName);
                File.WriteAllText(filePath, fullHtml);

                Console.WriteLine($"✅ {fileName} oluşturuldu!");

                // ===== ANA SAYFAYI GÜNCELLE =====
                UpdateIndexPage(slug, topic);
                Console.WriteLine("✅ index.html güncellendi!");

                // ===== SITEMAP.XML GÜNCELLE =====
                UpdateSitemap(slug);
                Console.WriteLine("✅ sitemap.xml güncellendi!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ HATA: {ex.Message}");
                Environment.Exit(1);
            }
        }

        // ===== SLUG (URL) OLUŞTURMA =====
        // Önceki hatanın kök nedeni: ':' karakteri temizlenmiyordu, bozuk URL'ler
        // oluşuyordu (örn. "girisimcilik-hikayeleri:-sifirdan-basariya.html").
        // Artık harf/rakam/boşluk DIŞINDAKİ her karakter (:, ?, !, (, ) vb.) genel
        // bir regex ile temizleniyor - gelecekte yeni bir özel karakter eklense
        // bile tekrar bozulmaz.
        static string Slugify(string text)
        {
            string s = text
                .ToLowerInvariant()
                .Replace("ü", "u").Replace("ğ", "g").Replace("ş", "s")
                .Replace("ı", "i").Replace("ö", "o").Replace("ç", "c")
                .Replace("İ", "i");

            s = Regex.Replace(s, @"[^a-z0-9\s-]", "");   // izin verilmeyen her karakteri sil
            s = Regex.Replace(s, @"\s+", "-");             // boşlukları tireye çevir
            s = Regex.Replace(s, @"-+", "-");              // ardışık tireleri teke indir
            return s.Trim('-');
        }

        // ===== ANA SAYFAYI GÜNCELLE =====
        static void UpdateIndexPage(string slug, string title)
        {
            string indexPath = Path.Combine("..", "index.html");
            if (!File.Exists(indexPath)) 
            {
                Console.WriteLine("⚠️ index.html bulunamadı!");
                return;
            }

            string content = File.ReadAllText(indexPath);

            // Önceki hatanın kök nedeni: aynı makale için (aynı href) ESKİ bir
            // liste girişi varsa siliniyordu, sadece EKLENİYORDU - bu yüzden
            // aynı yazı index.html'de birden fazla kez, farklı tarihlerle
            // görünüyordu. Artık önce eski girişi (varsa) siliyoruz.
            string existingEntryPattern = $@"<li>\s*<a href=""{Regex.Escape(slug)}\.html"">.*?</a>\s*</li>";
            content = Regex.Replace(content, existingEntryPattern, "", RegexOptions.Singleline);

            // Önceki hatanın kök nedeni: DateTime.Now:dd MMMM yyyy formatı,
            // sunucunun o anki dil ayarına bağımlıydı (bazen İngilizce ay ismi,
            // bazen Türkçe çıkıyordu). Artık kültür AÇIKÇA tr-TR olarak veriliyor.
            string formattedDate = DateTime.Now.ToString("dd MMMM yyyy", new CultureInfo("tr-TR"));

            string newEntry = $@"
<li>
    <a href=""{slug}.html"">
        <div class=""post-title"">{title}</div>
        <div class=""post-meta""><span class=""badge"">Yeni</span> 📅 {formattedDate}</div>
    </a>
</li>";

            if (content.Contains("<!-- BLOG_POSTS -->"))
            {
                content = content.Replace("<!-- BLOG_POSTS -->", $"<!-- BLOG_POSTS -->\n{newEntry}");
                File.WriteAllText(indexPath, content);
            }
            else
            {
                Console.WriteLine("⚠️ index.html'de <!-- BLOG_POSTS --> yorumu bulunamadı!");
            }
        }

        // ===== SITEMAP.XML GÜNCELLE (yeni eklendi) =====
        // Her yeni makale otomatik olarak sitemap.xml'e de eklenir, böylece
        // arama motorları yeni sayfaları daha hızlı keşfeder.
        static void UpdateSitemap(string slug)
        {
            string sitemapPath = Path.Combine("..", "sitemap.xml");
            if (!File.Exists(sitemapPath))
            {
                Console.WriteLine("⚠️ sitemap.xml bulunamadı, bu adım atlanıyor.");
                return;
            }

            string content = File.ReadAllText(sitemapPath);
            string url = $"https://mobilcv.net/{slug}.html";

            if (content.Contains($"<loc>{url}</loc>"))
            {
                return; // zaten ekli
            }

            string today = DateTime.UtcNow.ToString("yyyy-MM-dd");
            string newUrlEntry = $@"  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>";

            if (content.Contains("</urlset>"))
            {
                content = content.Replace("</urlset>", newUrlEntry);
                File.WriteAllText(sitemapPath, content);
            }
        }

        // ===== MAKALE ŞABLONU (HEADER + FOOTER + CTA + SOSYAL + NEWSLETTER + KATEGORİ) =====
        static string BuildHtmlPage(string title, string metaDescription, string htmlBody, string slug, string category)
        {
            return $@"<!DOCTYPE html>
<html lang=""tr"">
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>{title} | MobilCV</title>
    <meta name=""description"" content=""{metaDescription}"">
    <style>
        /* ===== TÜM SAYFALAR İÇİN ORTAK CSS ===== */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            line-height: 1.8;
            padding: 20px;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; background: #fff; border-radius: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.06); overflow: hidden; }}

        /* ===== HEADER ===== */
        .site-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 28px;
            background: #fff;
            border-bottom: 1px solid #e2e8f0;
            flex-wrap: wrap;
        }}
        .logo {{ font-size: 1.6em; font-weight: 900; color: #0f172a; text-decoration: none; }}
        .logo span {{ color: #2563eb; }}
        .nav-links {{
            display: flex;
            list-style: none;
            gap: 6px;
            flex-wrap: wrap;
        }}
        .nav-links a {{
            padding: 10px 20px;
            color: #64748b;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95em;
            border-radius: 40px;
            transition: all 0.25s ease;
        }}
        .nav-links a:hover {{ color: #2563eb; background: #dbeafe; }}
        .nav-links a.active {{ color: #fff; background: #2563eb; }}
        .nav-cta {{
            background: #2563eb;
            color: #fff !important;
            padding: 10px 24px;
            border-radius: 40px;
            font-weight: 700;
        }}
        .nav-cta:hover {{ background: #1d4ed8 !important; }}

        /* ===== MAKALE İÇERİĞİ ===== */
        .page-content {{
            padding: 48px 40px 40px;
        }}
        .page-content .category-tag {{
            display: inline-block;
            background: #dbeafe;
            color: #2563eb;
            padding: 4px 14px;
            border-radius: 40px;
            font-size: 0.75em;
            font-weight: 700;
            margin-bottom: 12px;
        }}
        .page-content h1 {{
            font-size: 2.4em;
            font-weight: 800;
            margin-bottom: 16px;
            color: #0f172a;
        }}
        .page-content p {{
            color: #334155;
            margin-bottom: 16px;
            font-size: 1.05em;
        }}
        .page-content h2 {{
            font-size: 1.6em;
            font-weight: 700;
            margin-top: 32px;
            margin-bottom: 12px;
            color: #0f172a;
        }}
        .page-content ul, .page-content ol {{
            margin-left: 24px;
            margin-bottom: 20px;
            color: #334155;
        }}
        .page-content li {{ margin-bottom: 8px; }}

        /* ===== SOSYAL PAYLAŞIM ===== */
        .share-box {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8fafc;
            border-radius: 12px;
        }}
        .share-box p {{
            font-size: 0.95em;
            color: #64748b;
            margin-bottom: 12px;
        }}
        .share-buttons {{
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .share-btn {{
            display: inline-block;
            padding: 8px 18px;
            border-radius: 40px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85em;
            color: #fff !important;
            transition: opacity 0.2s;
        }}
        .share-btn:hover {{ opacity: 0.8; }}
        .share-linkedin {{ background: #0a66c2; }}
        .share-twitter {{ background: #000; }}
        .share-whatsapp {{ background: #25D366; }}

        /* ===== CTA BUTONU ===== */
        .cta-box {{
            text-align: center;
            margin-top: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
        }}
        .cta-box p {{
            font-size: 1.2em;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 12px;
        }}
        .cta-button {{
            display: inline-block;
            background: #2563eb;
            color: #fff;
            padding: 14px 36px;
            border-radius: 40px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1em;
            transition: background 0.3s ease;
        }}
        .cta-button:hover {{ background: #1d4ed8; }}

        /* ===== NEWSLETTER ===== */
        .newsletter-box {{
            text-align: center;
            margin-top: 30px;
            padding: 30px;
            background: #0f172a;
            border-radius: 16px;
            color: #fff;
        }}
        .newsletter-box p {{
            color: #94a3b8;
        }}
        .newsletter-form {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            max-width: 440px;
            margin: 0 auto;
        }}
        .newsletter-form input {{
            flex: 1;
            min-width: 200px;
            padding: 12px 18px;
            border-radius: 40px;
            border: none;
            font-size: 0.95em;
        }}
        .newsletter-form button {{
            background: #2563eb;
            color: #fff;
            border: none;
            padding: 12px 28px;
            border-radius: 40px;
            font-weight: 700;
            font-size: 0.95em;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        .newsletter-form button:hover {{ background: #1d4ed8; }}
        .newsletter-note {{
            font-size: 0.75em;
            color: #64748b;
            margin-top: 12px;
        }}

        /* ===== FOOTER ===== */
        .footer {{
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            padding: 30px;
            text-align: center;
            color: #94a3b8;
        }}
        .footer a {{ color: #2563eb; text-decoration: none; font-weight: 600; }}
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 28px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }}
        .footer-links a {{ color: #64748b; font-weight: 500; }}
        .footer-links a:hover {{ color: #2563eb; }}

        @media (max-width: 640px) {{
            .site-header {{ flex-direction: column; gap: 12px; padding: 16px; }}
            .nav-links {{ justify-content: center; }}
            .page-content {{ padding: 24px 18px; }}
            .page-content h1 {{ font-size: 1.8em; }}
            .cta-box {{ padding: 20px; }}
            .cta-button {{ padding: 12px 24px; font-size: 1em; }}
            .newsletter-box {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
<div class=""container"">

    <!-- ===== HEADER ===== -->
    <header class=""site-header"">
        <a href=""https://mobilcv.net"" class=""logo"">Mobil<span>CV</span></a>
        <nav>
            <ul class=""nav-links"">
                <li><a href=""https://mobilcv.com"">Ana Site</a></li>
                <li><a href=""https://mobilcv.net"">Blog</a></li>
                <li><a href=""cv-rehberi.html"">CV Rehberi</a></li>
                <li><a href=""iletisim.html"">İletişim</a></li>
                <li><a href=""https://mobilcv.net"" class=""nav-cta"">🚀 Keşfet</a></li>
            </ul>
        </nav>
    </header>

    <!-- ===== MAKALE İÇERİĞİ ===== -->
    <div class=""page-content"">
        <span class=""category-tag"">📂 {category.Replace("-", " ")}</span>
        <article>
            <h1>{title}</h1>
            {htmlBody}
        </article>

        <!-- ===== SOSYAL PAYLAŞIM BUTONLARI ===== -->
        <div class=""share-box"">
            <p>📤 Bu makaleyi paylaş:</p>
            <div class=""share-buttons"">
                <a href=""https://www.linkedin.com/sharing/share-offsite/?url=https://mobilcv.net/{slug}.html"" 
                   target=""_blank"" class=""share-btn share-linkedin"">LinkedIn</a>
                <a href=""https://twitter.com/intent/tweet?url=https://mobilcv.net/{slug}.html&text={title}"" 
                   target=""_blank"" class=""share-btn share-twitter"">X (Twitter)</a>
                <a href=""https://api.whatsapp.com/send?text={title} - https://mobilcv.net/{slug}.html"" 
                   target=""_blank"" class=""share-btn share-whatsapp"">WhatsApp</a>
            </div>
        </div>

        <!-- ===== CTA BUTONU ===== -->
        <div class=""cta-box"">
            <p>✨ CV'ni hemen oluştur!</p>
            <a href=""https://mobilcv.com"" class=""cta-button"">🚀 MobilCV ile CV Oluştur</a>
        </div>

        <!-- ===== NEWSLETTER FORMU ===== -->
        <div class=""newsletter-box"">
            <p style=""font-size: 1.2em; font-weight: 700; color: #fff;"">📩 Haftalık Kariyer İpuçları</p>
            <p>En yeni makaleler ve kariyer tavsiyeleri e-posta kutunda.</p>
            <form action=""#"" method=""post"" class=""newsletter-form"">
                <input type=""email"" placeholder=""E-posta adresiniz"" required>
                <button type=""submit"">Abone Ol</button>
            </form>
            <p class=""newsletter-note"">Spam yok, istediğin zaman ayrılabilirsin.</p>
        </div>
    </div>

    <!-- ===== FOOTER ===== -->
    <footer class=""footer"">
        <div class=""footer-links"">
            <a href=""https://mobilcv.com"">Ana Site</a>
            <a href=""https://mobilcv.net"">Blog</a>
            <a href=""cv-rehberi.html"">CV Rehberi</a>
            <a href=""iletisim.html"">İletişim</a>
        </div>
        <p>&copy; {DateTime.UtcNow.Year} MobilCV &mdash; <a href=""https://mobilcv.com"">mobilcv.com</a> ile güçlendirilmiştir.</p>
    </footer>

</div>
</body>
</html>";
        }
    }
}
