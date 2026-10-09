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
            // Model isteğe bağlı olarak OPENAI_MODEL ortam değişkeniyle değiştirilebilir (varsayılan: gpt-3.5-turbo)
            var model = Environment.GetEnvironmentVariable("OPENAI_MODEL");
            if (string.IsNullOrWhiteSpace(model)) model = "gpt-3.5-turbo";
            var client = new ChatClient(model, apiKey);
            Console.WriteLine($"🤖 Model: {model}");

            // Ek diller (de, fr, es, it, pt, ru, ar, zh) varsayilan olarak KAPALI.
            // Kalite icin yalnizca Turkce + Ingilizce uretilir. Acmak icin: EXTRA_LANGS=1
            bool extraLangs = Environment.GetEnvironmentVariable("EXTRA_LANGS") == "1";
            Console.WriteLine(extraLangs ? "🌍 Ek diller: ACIK" : "🌍 Ek diller: kapali (yalnizca TR + EN)");

            // İngilizce blog sayfalarındaki mobilcv.com linklerini İngilizce araç sayfasına çevir (tek seferlik, tekrar çalışması zararsız)
            MultiLang.FixEnglishCtaLinks();

            // ===== KATEGORİ VE KONU HAVUZU (TÜRKÇE) =====
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

            // ===== AYNI KONULARIN İNGİLİZCE BAŞLIKLARI =====
            // Her Türkçe konu başlığı için SABİT bir İngilizce karşılık. İngilizce slug, ek dillerde
            // (de, fr, es, it, pt, ru, ar, zh) de dosya adı olarak kullanılır.
            var topicsEnglish = new Dictionary<string, string>
            {
                ["CV'de Dikkat Edilmesi Gereken 7 Kritik Nokta"] = "7 Critical Points to Watch in Your CV",
                ["Etkili Bir Ön Yazı Nasıl Yazılır?"] = "How to Write an Effective Cover Letter?",
                ["CV'de Fotoğraf Kullanmalı mısınız?"] = "Should You Use a Photo on Your CV?",
                ["Yeni Mezunlar İçin CV Hazırlama Rehberi"] = "CV Writing Guide for New Graduates",
                ["ATS Sistemlerini Geçen CV Nasıl Hazırlanır?"] = "How to Write a CV That Passes ATS Systems?",
                ["CV'de Hangi Kelimeler Kullanılmamalı?"] = "Words You Should Avoid on Your CV",
                ["İngilizce CV Hazırlarken Dikkat Edilmesi Gerekenler"] = "What to Consider When Writing an English CV",
                ["CV ile Özgeçmiş Arasındaki Fark Nedir?"] = "What's the Difference Between a CV and a Resume?",
                ["Mülakatta Başarılı Olmanın 10 Altın Kuralı"] = "10 Golden Rules for Interview Success",
                ["En Zor Mülakat Sorularına Cevaplar"] = "Answers to the Toughest Interview Questions",
                ["Uzaktan Mülakatlarda Başarılı Olma Taktikleri"] = "Tactics for Succeeding in Remote Interviews",
                ["Mülakatta Maaş Pazarlığı Nasıl Yapılır?"] = "How to Negotiate Salary in an Interview",
                ["Grup Mülakatlarında Öne Çıkmanın Yolları"] = "Ways to Stand Out in Group Interviews",
                ["Mülakat Sonrası Teşekkür E-postası Nasıl Yazılır?"] = "How to Write a Thank-You Email After an Interview",
                ["Kariyer Planlaması Adım Adım Rehber"] = "Career Planning: A Step-by-Step Guide",
                ["30 Yaşından Önce Kariyerinde Yapman Gereken 5 Hamle"] = "5 Career Moves to Make Before Turning 30",
                ["Sektör Değiştirmek İsteyenler İçin Rehber"] = "A Guide for Those Who Want to Change Industries",
                ["Kariyer Molası Vermek İsteyenler İçin Öneriler"] = "Tips for Those Considering a Career Break",
                ["İkinci Bir Kariyere Nasıl Başlanır?"] = "How to Start a Second Career",
                ["2026'nın En Popüler 10 Mesleği"] = "The 10 Most Popular Professions of 2026",
                ["Uzaktan Çalışmanın Geleceği ve Trendler"] = "The Future of Remote Work and Emerging Trends",
                ["Yapay Zeka Hangi Meslekleri Dönüştürecek?"] = "Which Professions Will AI Transform?",
                ["Hibrit Çalışma Modeli Kariyerini Nasıl Etkiler?"] = "How Does the Hybrid Work Model Affect Your Career?",
                ["Freelance Çalışmaya Geçiş Rehberi"] = "A Guide to Transitioning to Freelance Work",
                ["Sektör Değiştirerek Hayalindeki İşe Ulaşanlar"] = "Success Stories: Changing Industries to Land a Dream Job",
                ["Girişimcilik Hikayeleri Sıfırdan Başarıya"] = "Entrepreneurship Stories: From Zero to Success",
                ["Kadın Girişimcilerin Başarı Hikayeleri"] = "Success Stories of Women Entrepreneurs",
                ["Küçük Bir Fikirden Büyük Bir Şirkete Uzanan Yolculuklar"] = "From a Small Idea to a Big Company: Growth Journeys"
            };

            // ===== DAHA ÖNCE YAZILMIŞ KONULARI HAVUZDAN ÇIKAR =====
            // Bir konu; Türkçe, İngilizce veya ek dillerden (de, fr, es, it, pt, ru, ar, zh) HERHANGİ
            // birinde eksikse hâlâ "işlenmemiş" sayılır ve seçildiğinde yalnızca eksik diller üretilir.
            var availableTopics = new List<(string Category, string Topic, string Slug)>();
            foreach (var kvp in topics)
            {
                foreach (var t in kvp.Value)
                {
                    string s = Slugify(t);
                    string pathTr = Path.Combine("..", $"{s}.html");
                    string slugEnCheck = Slugify(topicsEnglish.ContainsKey(t) ? topicsEnglish[t] : t);
                    string pathEn = Path.Combine("..", "en", $"{slugEnCheck}.html");
                    bool trExists = File.Exists(pathTr);
                    bool enExists = File.Exists(pathEn);
                    if (!trExists || !enExists || (extraLangs && MultiLang.AnyMissing(slugEnCheck)))
                    {
                        availableTopics.Add((kvp.Key, t, s));
                    }
                }
            }

            if (availableTopics.Count == 0)
            {
                Console.WriteLine("⚠️ Havuzdaki tüm konular zaten tüm dillerde yazılmış! Yukarıdaki 'topics' sözlüğüne yeni konular eklemeniz gerekiyor. İşlem sonlandırılıyor (hata değil).");
                return;
            }

            // ===== RASTGELE (AMA DAHA ÖNCE TAMAMLANMAMIŞ) KONU SEÇ =====
            Random random = new Random();
            var selected = availableTopics[random.Next(availableTopics.Count)];
            string selectedCategory = selected.Category;
            string topic = selected.Topic;
            string slug = selected.Slug;

            string topicEnglish = topicsEnglish.ContainsKey(topic) ? topicsEnglish[topic] : topic;
            string slugEnglish = Slugify(topicEnglish);

            Console.WriteLine($"📂 Kategori: {selectedCategory}");
            Console.WriteLine($"📝 Konu (TR): {topic}");
            Console.WriteLine($"📝 Konu (EN): {topicEnglish}");
            Console.WriteLine($"📊 Havuzda kalan işlenmemiş konu sayısı: {availableTopics.Count - 1}");

            bool needTr = !File.Exists(Path.Combine("..", $"{slug}.html"));
            bool needEn = !File.Exists(Path.Combine("..", "en", $"{slugEnglish}.html"));

            try
            {
                // ===== TÜRKÇE MAKALE =====
                if (needTr)
                {
                    var messagesTr = new List<ChatMessage>
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
                            1. Konuya ilgi çekici bir giriş (2-3 paragraf, <p> ile)
                            2. 4-6 alt başlık (H2) ile detaylandırılmış içerik
                               - Her bölümde özgün yorumlar, somut örnekler ve uygulanabilir adımlar kullan
                               - Gerektiğinde madde işaretli listeler (ul/li)
                            3. Sonuç bölümü (özet ve okuyucuya eylem çağrısı)
                            4. Makale sonunda 'Yararlanılan Kaynaklar' başlığı altında genel bilgi (örnek: 'Bu makale hazırlanırken çeşitli akademik yayınlar, sektör raporları ve iş dünyası analizlerinden yararlanılmıştır.')

                            **UNUTMA:**
                            - Tüm içerik %100 ÖZGÜN olmalı.
                            - Başka kaynaklardan birebir alıntı yapma.
                            - İstatistik ve verileri kendi cümlelerinle yorumla.

                            ÖNEMLİ BİÇİM KURALI: <!DOCTYPE>, <html>, <head>, <body>, <title>, <meta> ve <h1> etiketlerini KULLANMA
                            (sayfa başlığı zaten var). Doğrudan giriş paragrafıyla başla. Kod bloğu (```) kullanma.
                            Sadece makale gövdesinin HTML kodunu ver, başka bir açıklama yapma.
                        ")
                    };

                    var responseTr = await client.CompleteChatAsync(messagesTr);
                    string htmlContentTr = responseTr.Value.Content[0].Text;
                    htmlContentTr = await MultiLang.EnsureLengthAsync(client, messagesTr, htmlContentTr, false,
                        "Makale çok kısa ({N}). Aynı makaleyi baştan ve TAM haliyle yeniden yaz; her bölümü somut örnekler, adımlar ve ipuçlarıyla genişlet, toplam en az 1000 kelime olsun. Aynı biçim kurallarına uy: sadece makale gövdesinin HTML'i, <html>/<head>/<body>/<h1> yok.");
                    htmlContentTr = MultiLang.CleanArticleHtml(htmlContentTr);
                    string metaDescriptionTr = topic + " - " + selectedCategory.Replace("-", " ") + " kategorisinde kapsamlı bir rehber.";

                    string fullHtmlTr = BuildHtmlPage(topic, metaDescriptionTr, htmlContentTr, slug, selectedCategory, slugEnglish);
                    File.WriteAllText(Path.Combine("..", $"{slug}.html"), fullHtmlTr);
                    Console.WriteLine($"✅ {slug}.html (Türkçe) oluşturuldu!");

                    UpdateIndexPage(slug, topic);
                    Console.WriteLine("✅ index.html güncellendi!");

                    UpdateSitemap(slug);
                    Console.WriteLine("✅ sitemap.xml güncellendi (TR)!");
                }
                else
                {
                    Console.WriteLine("☑️ Türkçe versiyon zaten mevcut, atlanıyor.");
                }

                // ===== İNGİLİZCE MAKALE =====
                if (needEn)
                {
                    var messagesEn = new List<ChatMessage>
                    {
                        new SystemChatMessage(@"You are a career expert with 10 years of experience, closely following global job market trends.

                        **COPYRIGHT RULE (HARD LIMIT):**
                        - Never quote any source verbatim.
                        - When referencing statistics, data, or examples, synthesize and rephrase them ENTIRELY IN YOUR OWN WORDS.
                        - Do not cite a real, specific source in the references section - only give a general statement under a 'Sources' heading.
                        - Never copy text from any author, institution, or website.
                        - All content you produce must be 100% ORIGINAL and your own.
                        - When sharing a statistic or research finding, attribute it generally (e.g. 'research suggests...' or 'experts note...') rather than citing a specific source.

                        **CONTENT QUALITY:**
                        - Articles should be both informative and give actionable advice.
                        - Provide genuine value to the reader.
                        - Tone: professional but warm, informative, and easy to read.
                        - Written in natural, fluent English (not a translation - write as a native English-speaking career expert would)."),

                        new UserChatMessage($@"
                            Write a comprehensive, 100% ORIGINAL, copyright-safe blog article of 1000-1200 words on the following topic.

                            TOPIC: {topicEnglish}
                            CATEGORY: {selectedCategory.Replace("-", " ")}

                            The article should include:
                            1. An engaging introduction to the topic (2-3 paragraphs, using <p>)
                            2. 4-6 subheadings (H2) with detailed content
                               - Use original commentary, concrete examples, and actionable steps in each section
                               - Use bullet lists (ul/li) where appropriate
                            3. A conclusion section (summary and a call to action for the reader)
                            4. A 'Sources' section at the end with a general statement (e.g. 'This article was prepared drawing on various academic publications, industry reports, and business analyses.')

                            **REMEMBER:**
                            - All content must be 100% ORIGINAL.
                            - Do not quote any source verbatim.
                            - Rephrase all statistics and data in your own words.
                            - Write naturally in English, not as a translation of Turkish content.

                            FORMAT RULE: Do NOT use <!DOCTYPE>, <html>, <head>, <body>, <title>, <meta> or <h1> tags
                            (the page title already exists). Start directly with the introduction. No code fences (```).
                            Return only the article body HTML, no other explanation.
                        ")
                    };

                    var responseEn = await client.CompleteChatAsync(messagesEn);
                    string htmlContentEn = responseEn.Value.Content[0].Text;
                    htmlContentEn = await MultiLang.EnsureLengthAsync(client, messagesEn, htmlContentEn, false,
                        "The article is too short ({N}). Rewrite the COMPLETE article from scratch, expanding every section with concrete examples, steps and practical tips, so it reaches at least 1000 words. Follow the same format rules: article body HTML only, no <html>/<head>/<body>/<h1>.");
                    htmlContentEn = MultiLang.CleanArticleHtml(htmlContentEn);
                    string metaDescriptionEn = topicEnglish + " - a comprehensive guide with practical tips and expert insights.";

                    string fullHtmlEn = BuildHtmlPageEnglish(topicEnglish, metaDescriptionEn, htmlContentEn, slugEnglish, selectedCategory, slug);
                    string enDir = Path.Combine("..", "en");
                    Directory.CreateDirectory(enDir);
                    File.WriteAllText(Path.Combine(enDir, $"{slugEnglish}.html"), fullHtmlEn);
                    Console.WriteLine($"✅ en/{slugEnglish}.html (English) oluşturuldu!");

                    UpdateIndexPageEnglish(slugEnglish, topicEnglish);
                    Console.WriteLine("✅ en/index.html güncellendi!");

                    UpdateSitemapEnglish(slugEnglish);
                    Console.WriteLine("✅ sitemap.xml güncellendi (EN)!");
                }
                else
                {
                    Console.WriteLine("☑️ İngilizce versiyon zaten mevcut, atlanıyor.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ HATA: {ex.Message}");
                Environment.Exit(1);
            }

            // ===== EK DİLLER (de, fr, es, it, pt, ru, ar, zh) =====
            if (extraLangs)
            {
                await MultiLang.GenerateMissingAsync(client, topicEnglish, selectedCategory, slugEnglish, slug);
            }

            // ===== TÜM DİL SÜRÜMLERİNDE hreflang ETİKETLERİNİ EŞİTLE =====
            MultiLang.SyncHreflang(slug, slugEnglish);

            Console.WriteLine("🏁 Tamamlandı.");
        }

        // ===== SLUG (URL) OLUŞTURMA =====
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

        // ===== TÜRKÇE ANA SAYFAYI GÜNCELLE =====
        static void UpdateIndexPage(string slug, string title)
        {
            string indexPath = Path.Combine("..", "index.html");
            if (!File.Exists(indexPath)) 
            {
                Console.WriteLine("⚠️ index.html bulunamadı!");
                return;
            }

            string content = File.ReadAllText(indexPath);

            string existingEntryPattern = $@"<li>\s*<a href=""{Regex.Escape(slug)}\.html"">.*?</a>\s*</li>";
            content = Regex.Replace(content, existingEntryPattern, "", RegexOptions.Singleline);

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

        // ===== İNGİLİZCE ANA SAYFAYI GÜNCELLE =====
        static void UpdateIndexPageEnglish(string slug, string title)
        {
            string indexPath = Path.Combine("..", "en", "index.html");
            if (!File.Exists(indexPath))
            {
                Console.WriteLine("⚠️ en/index.html bulunamadı!");
                return;
            }

            string content = File.ReadAllText(indexPath);

            string existingEntryPattern = $@"<li>\s*<a href=""{Regex.Escape(slug)}\.html"">.*?</a>\s*</li>";
            content = Regex.Replace(content, existingEntryPattern, "", RegexOptions.Singleline);

            string formattedDate = DateTime.Now.ToString("dd MMMM yyyy", new CultureInfo("en-US"));

            string newEntry = $@"
<li>
    <a href=""{slug}.html"">
        <div class=""post-title"">{title}</div>
        <div class=""post-meta""><span class=""badge"">New</span> 📅 {formattedDate}</div>
    </a>
</li>";

            if (content.Contains("<!-- BLOG_POSTS -->"))
            {
                content = content.Replace("<!-- BLOG_POSTS -->", $"<!-- BLOG_POSTS -->\n{newEntry}");
                File.WriteAllText(indexPath, content);
            }
            else
            {
                Console.WriteLine("⚠️ en/index.html'de <!-- BLOG_POSTS --> yorumu bulunamadı!");
            }
        }

        // ===== TÜRKÇE SITEMAP.XML GÜNCELLE =====
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
                return;
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

        // ===== İNGİLİZCE SAYFALAR İÇİN SITEMAP.XML GÜNCELLE =====
        static void UpdateSitemapEnglish(string slug)
        {
            string sitemapPath = Path.Combine("..", "sitemap.xml");
            if (!File.Exists(sitemapPath))
            {
                Console.WriteLine("⚠️ sitemap.xml bulunamadı, bu adım atlanıyor.");
                return;
            }

            string content = File.ReadAllText(sitemapPath);
            string url = $"https://mobilcv.net/en/{slug}.html";

            if (content.Contains($"<loc>{url}</loc>"))
            {
                return;
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

        // ===== TÜRKÇE MAKALE ŞABLONU =====
        static string BuildHtmlPage(string title, string metaDescription, string htmlBody, string slug, string category, string slugEn)
        {
            string hreflangTags = $@"
    <link rel=""alternate"" hreflang=""tr"" href=""https://mobilcv.net/{slug}.html"">
    <link rel=""alternate"" hreflang=""en"" href=""https://mobilcv.net/en/{slugEn}.html"">
    <link rel=""alternate"" hreflang=""x-default"" href=""https://mobilcv.net/{slug}.html"">";
            string canonicalUrl = $"https://mobilcv.net/{slug}.html";
            string langSwitch = $@"
                <li><a href=""https://mobilcv.net/en/{slugEn}.html"" class=""lang-switch"">🇬🇧 English</a></li>";

            return $@"<!DOCTYPE html>
<html lang=""tr"">
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>{title} | MobilCV</title>
    <meta name=""description"" content=""{metaDescription}"">
    <link rel=""canonical"" href=""{canonicalUrl}"">{hreflangTags}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            line-height: 1.8;
            padding: 20px;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; background: #fff; border-radius: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.06); overflow: hidden; }}
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
            align-items: center;
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
        .lang-switch {{
            padding: 6px 14px; border: 1px solid #e2e8f0; border-radius: 40px;
            color: #64748b; text-decoration: none; font-size: 0.85em; font-weight: 700;
        }}
        .lang-switch:hover {{ background: #f1f5f9; }}
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

    <header class=""site-header"">
        <a href=""https://mobilcv.net"" class=""logo"">Mobil<span>CV</span></a>
        <nav>
            <ul class=""nav-links"">
                <li><a href=""https://mobilcv.com"">Ana Site</a></li>
                <li><a href=""https://mobilcv.net"">Blog</a></li>
                <li><a href=""https://mobilcv.net/"">CV Örnekleri</a></li>
                <li><a href=""cv-rehberi.html"">CV Rehberi</a></li>
                <li><a href=""iletisim.html"">İletişim</a></li>
                <li><a href=""https://mobilcv.net"" class=""nav-cta"">🚀 Keşfet</a></li>{langSwitch}
            </ul>
        </nav>
    </header>

    <div class=""page-content"">
        <span class=""category-tag"">📂 {category.Replace("-", " ")}</span>
        <article>
            <h1>{title}</h1>
            {htmlBody}
        </article>

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

        <div class=""cta-box"">
            <p>✨ CV'ni hemen oluştur!</p>
            <a href=""https://mobilcv.com"" class=""cta-button"">🚀 MobilCV ile CV Oluştur</a>
        </div>

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

    <footer class=""footer"">
        <div class=""footer-links"">
            <a href=""https://mobilcv.com"">Ana Site</a>
            <a href=""https://mobilcv.net"">Blog</a>
            <a href=""https://mobilcv.net/"">CV Örnekleri</a>
            <a href=""cv-rehberi.html"">CV Rehberi</a>
            <a href=""iletisim.html"">İletişim</a>
        </div>
        <p>&copy; {DateTime.UtcNow.Year} MobilCV &mdash; <a href=""https://mobilcv.com"">mobilcv.com</a> ile güçlendirilmiştir.</p>
    </footer>

</div>
</body>
</html>";
        }

        // ===== İNGİLİZCE MAKALE ŞABLONU =====
        // Not: Araç linkleri artık https://www.mobilcv.com/en/ (İngilizce araç sayfası) adresine gider.
        static string BuildHtmlPageEnglish(string title, string metaDescription, string htmlBody, string slug, string category, string slugTr)
        {
            string hreflangTags = $@"
    <link rel=""alternate"" hreflang=""tr"" href=""https://mobilcv.net/{slugTr}.html"">
    <link rel=""alternate"" hreflang=""en"" href=""https://mobilcv.net/en/{slug}.html"">
    <link rel=""alternate"" hreflang=""x-default"" href=""https://mobilcv.net/{slugTr}.html"">";
            string canonicalUrl = $"https://mobilcv.net/en/{slug}.html";

            return $@"<!DOCTYPE html>
<html lang=""en"">
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>{title} | MobilCV</title>
    <meta name=""description"" content=""{metaDescription}"">
    <link rel=""canonical"" href=""{canonicalUrl}"">{hreflangTags}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            line-height: 1.8;
            padding: 20px;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; background: #fff; border-radius: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.06); overflow: hidden; }}
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
            align-items: center;
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
        .lang-switch {{
            padding: 6px 14px; border: 1px solid #e2e8f0; border-radius: 40px;
            color: #64748b; text-decoration: none; font-size: 0.85em; font-weight: 700;
        }}
        .lang-switch:hover {{ background: #f1f5f9; }}
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
        }}
    </style>
</head>
<body>
<div class=""container"">

    <header class=""site-header"">
        <a href=""https://mobilcv.net/en/"" class=""logo"">Mobil<span>CV</span></a>
        <nav>
            <ul class=""nav-links"">
                <li><a href=""https://www.mobilcv.com/en/"">Homepage</a></li>
                <li><a href=""https://mobilcv.net/en/"">Blog</a></li>
                <li><a href=""cv-examples.html"">CV Examples</a></li>
                <li><a href=""cv-guide.html"">CV Guide</a></li>
                <li><a href=""contact.html"">Contact</a></li>
                <li><a href=""https://www.mobilcv.com/en/"" class=""nav-cta"">🚀 Create Now</a></li>
                <li><a href=""https://mobilcv.net/{slugTr}.html"" class=""lang-switch"">🇹🇷 Türkçe</a></li>
            </ul>
        </nav>
    </header>

    <div class=""page-content"">
        <span class=""category-tag"">📂 {category.Replace("-", " ")}</span>
        <article>
            <h1>{title}</h1>
            {htmlBody}
        </article>

        <div class=""share-box"">
            <p>📤 Share this article:</p>
            <div class=""share-buttons"">
                <a href=""https://www.linkedin.com/sharing/share-offsite/?url=https://mobilcv.net/en/{slug}.html"" 
                   target=""_blank"" class=""share-btn share-linkedin"">LinkedIn</a>
                <a href=""https://twitter.com/intent/tweet?url=https://mobilcv.net/en/{slug}.html&text={title}"" 
                   target=""_blank"" class=""share-btn share-twitter"">X (Twitter)</a>
                <a href=""https://api.whatsapp.com/send?text={title} - https://mobilcv.net/en/{slug}.html"" 
                   target=""_blank"" class=""share-btn share-whatsapp"">WhatsApp</a>
            </div>
        </div>

        <div class=""cta-box"">
            <p>✨ Create your CV now!</p>
            <a href=""https://www.mobilcv.com/en/"" class=""cta-button"">🚀 Create Your CV With MobilCV</a>
        </div>
    </div>

    <footer class=""footer"">
        <div class=""footer-links"">
            <a href=""https://www.mobilcv.com/en/"">Homepage</a>
            <a href=""https://mobilcv.net/en/"">Blog</a>
            <a href=""cv-examples.html"">CV Examples</a>
        </div>
        <p>&copy; {DateTime.UtcNow.Year} MobilCV &mdash; powered by <a href=""https://www.mobilcv.com/en/"">mobilcv.com</a>.</p>
    </footer>

</div>
</body>
</html>";
        }
    }
}
