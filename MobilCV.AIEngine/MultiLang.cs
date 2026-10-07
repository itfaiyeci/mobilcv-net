using OpenAI.Chat;
using System.Globalization;
using System.Text.RegularExpressions;

namespace MobilCV.AIEngine
{
    // =====================================================================
    // EK DİLLER (de, fr, es, it, pt, ru, ar, zh)
    // ---------------------------------------------------------------------
    // - Her dildeki makale: ../{dil}/{ingilizce-slug}.html
    //   (Rusça/Arapça/Çince başlıklardan Latin harfli adres üretilemediği için
    //    tüm ek dillerde İngilizce slug kullanılıyor; adresler tutarlı kalıyor.)
    // - Makalenin "Hemen oluştur" butonu mobilcv.com'un AYNI DİLDEKİ sayfasına gider
    //   (ör. https://www.mobilcv.com/de/).
    // - Her dil için blog ana sayfası (../{dil}/index.html) yoksa otomatik oluşturulur.
    // - hreflang etiketleri, o konunun var olan TÜM dil sürümlerinde senkronize edilir.
    // =====================================================================
    static class MultiLang
    {
        public record Lang(
            string Code, string LangName, string Flag, string Culture, bool Rtl,
            string NewBadge, string Home, string Blog, string CreateNow, string Share,
            string CtaText, string CtaBtn, string IndexTitle, string IndexDesc,
            string IndexH1, string Footer);

        public static readonly Lang[] Langs =
        {
            new("de", "German", "🇩🇪 Deutsch", "de-DE", false, "Neu", "Startseite", "Blog", "🚀 Jetzt erstellen",
                "📤 Artikel teilen:", "✨ Erstelle jetzt deinen Lebenslauf!", "🚀 Lebenslauf mit MobilCV erstellen",
                "MobilCV Blog – Tipps zu Lebenslauf, Bewerbung und Karriere",
                "Praktische Tipps zu Lebenslauf, Vorstellungsgespräch und Karriereplanung – kostenlos von MobilCV.",
                "Karriere-Blog", "Ein Projekt von"),
            new("fr", "French", "🇫🇷 Français", "fr-FR", false, "Nouveau", "Accueil", "Blog", "🚀 Créer maintenant",
                "📤 Partager cet article :", "✨ Crée ton CV dès maintenant !", "🚀 Créer mon CV avec MobilCV",
                "Blog MobilCV – Conseils CV, entretien et carrière",
                "Conseils pratiques pour votre CV, vos entretiens d'embauche et votre carrière – gratuit avec MobilCV.",
                "Blog carrière", "Un projet de"),
            new("es", "Spanish", "🇪🇸 Español", "es-ES", false, "Nuevo", "Inicio", "Blog", "🚀 Crear ahora",
                "📤 Comparte este artículo:", "✨ ¡Crea tu currículum ahora!", "🚀 Crear mi CV con MobilCV",
                "Blog de MobilCV – Consejos de currículum, entrevistas y carrera",
                "Consejos prácticos sobre currículum, entrevistas de trabajo y planificación profesional – gratis con MobilCV.",
                "Blog de carrera", "Un proyecto de"),
            new("it", "Italian", "🇮🇹 Italiano", "it-IT", false, "Nuovo", "Home", "Blog", "🚀 Crea ora",
                "📤 Condividi l'articolo:", "✨ Crea subito il tuo CV!", "🚀 Crea il CV con MobilCV",
                "Blog MobilCV – Consigli su CV, colloqui e carriera",
                "Consigli pratici su CV, colloqui di lavoro e pianificazione della carriera – gratis con MobilCV.",
                "Blog carriera", "Un progetto di"),
            new("pt", "Brazilian Portuguese", "🇧🇷 Português", "pt-BR", false, "Novo", "Início", "Blog", "🚀 Criar agora",
                "📤 Compartilhe este artigo:", "✨ Crie seu currículo agora!", "🚀 Criar currículo com MobilCV",
                "Blog MobilCV – Dicas de currículo, entrevista e carreira",
                "Dicas práticas sobre currículo, entrevistas de emprego e planejamento de carreira – grátis com MobilCV.",
                "Blog de carreira", "Um projeto de"),
            new("ru", "Russian", "🇷🇺 Русский", "ru-RU", false, "Новое", "Главная", "Блог", "🚀 Создать сейчас",
                "📤 Поделиться статьёй:", "✨ Создайте резюме прямо сейчас!", "🚀 Создать резюме в MobilCV",
                "Блог MobilCV – советы по резюме, собеседованию и карьере",
                "Практические советы по резюме, собеседованиям и планированию карьеры – бесплатно с MobilCV.",
                "Карьерный блог", "Проект"),
            new("ar", "Modern Standard Arabic", "🇸🇦 العربية", "ar-SA", true, "جديد", "الرئيسية", "المدونة", "🚀 أنشئ الآن",
                "📤 شارك المقال:", "✨ أنشئ سيرتك الذاتية الآن!", "🚀 أنشئ سيرتك الذاتية مع MobilCV",
                "مدونة MobilCV – نصائح السيرة الذاتية والمقابلات والمسار المهني",
                "نصائح عملية حول كتابة السيرة الذاتية ومقابلات العمل والتخطيط المهني – مجانًا مع MobilCV.",
                "المدونة المهنية", "مشروع من"),
            new("zh", "Simplified Chinese", "🇨🇳 中文", "zh-CN", false, "新", "首页", "博客", "🚀 立即创建",
                "📤 分享本文：", "✨ 立即创建你的简历！", "🚀 用 MobilCV 创建简历",
                "MobilCV 博客 – 简历、面试与职业发展技巧",
                "关于简历写作、求职面试和职业规划的实用建议 – MobilCV 免费提供。",
                "职业博客", "项目来自"),
        };

        const string NetBase = "https://mobilcv.net";
        const string ComBase = "https://www.mobilcv.com";
        static readonly string Root = "..";

        static string ArticlePath(string code, string slugEn) => Path.Combine(Root, code, $"{slugEn}.html");

        // Bu konunun ek dillerden en az birinde eksik olup olmadığı
        public static bool AnyMissing(string slugEn) => Langs.Any(l => !File.Exists(ArticlePath(l.Code, slugEn)));

        // ===== EKSİK DİLLERİ ÜRET =====
        // Bir dilde hata olursa diğer dillere devam edilir (hata o dili bir sonraki çalışmaya bırakır).
        public static async Task GenerateMissingAsync(ChatClient client, string topicEnglish, string category, string slugEn, string slugTr)
        {
            foreach (var l in Langs)
            {
                string path = ArticlePath(l.Code, slugEn);
                if (File.Exists(path))
                {
                    Console.WriteLine($"☑️ {l.Code}: zaten mevcut, atlanıyor.");
                    continue;
                }

                try
                {
                    var messages = new List<ChatMessage>
                    {
                        new SystemChatMessage(SystemPrompt(l)),
                        new UserChatMessage(UserPrompt(l, topicEnglish, category))
                    };

                    var response = await client.CompleteChatAsync(messages);
                    string raw = response.Value.Content[0].Text;
                    raw = await EnsureLengthAsync(client, messages, raw, l.Code == "zh",
                        $"The article is too short ({{N}}). Rewrite the COMPLETE article from scratch in {l.LangName}, expanding every section with concrete examples, steps and practical tips, so that it reaches at least 1000 words (for Chinese: at least 1800 characters). Keep EXACTLY the same output format (TITLE:, META:, ---, article HTML).");
                    var (title, meta, body) = ParseResponse(raw, topicEnglish);

                    Directory.CreateDirectory(Path.Combine(Root, l.Code));
                    EnsureBlogIndex(l);

                    File.WriteAllText(path, BuildPage(l, title, meta, body, slugEn));
                    UpdateBlogIndex(l, slugEn, title);
                    UpdateSitemap($"{NetBase}/{l.Code}/{slugEn}.html");
                    Console.WriteLine($"✅ {l.Code}/{slugEn}.html oluşturuldu ({l.LangName})");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ {l.Code} HATA: {ex.Message} (diğer dillere devam ediliyor)");
                }
            }
        }

        static string SystemPrompt(Lang l) => $@"You are a career expert with 10 years of experience who writes natively in {l.LangName}.

**COPYRIGHT RULE (HARD LIMIT):**
- Never quote any source verbatim. Never copy text from any author, institution, or website.
- Rephrase all statistics and data entirely in your own words and attribute them only generally (e.g. 'research suggests...').
- Do not cite a real, specific source. All content must be 100% ORIGINAL.

**LANGUAGE AND AUDIENCE:**
- Write ONLY in {l.LangName}, naturally, as a native {l.LangName}-speaking career expert would. It must not read like a translation.
- Adapt examples, job-market context and CV conventions to readers in countries where {l.LangName} is spoken.
- Do not refer to Turkey unless the topic requires it.

**CONTENT QUALITY:**
- Informative, practical, actionable advice. Professional but warm tone.";

        static string UserPrompt(Lang l, string topicEnglish, string category)
        {
            string length = l.Code == "zh"
                ? "about 1800-2200 Chinese characters"
                : "1000-1200 words";
            return $@"Write a comprehensive, original blog article in {l.LangName} ({length}).

TOPIC (given in English for reference; write the title and the article in {l.LangName}): {topicEnglish}
CATEGORY: {category.Replace("-", " ")}

Return EXACTLY this format and nothing else:
TITLE: <SEO-friendly title in {l.LangName}, max 65 characters>
META: <meta description in {l.LangName}, 140-160 characters>
---
<article HTML>

Rules for the article HTML:
- Do NOT include <h1>, <html>, <head>, <body>, <title> or <meta> tags, and no markdown code fences.
- Start with a 2-3 paragraph introduction using <p>.
- Then 4-6 sections with <h2> subheadings, using <ul><li> lists where useful.
- Then a conclusion with a call to action.
- End with a short 'Sources' section (heading translated into {l.LangName}) containing only a general statement, e.g. that the article draws on academic publications, industry reports and business analyses.";
        }

        // ===== MODEL ÇIKTISINI AYRIŞTIR =====
        static (string Title, string Meta, string Body) ParseResponse(string raw, string fallbackTitle)
        {
            string text = Regex.Replace(raw ?? "", @"```[a-zA-Z]*", "").Trim();

            string title = fallbackTitle;
            string meta = "";

            var mt = Regex.Match(text, @"^\s*TITLE\s*:\s*(.+)$", RegexOptions.Multiline);
            if (mt.Success) title = mt.Groups[1].Value.Trim();
            var mm = Regex.Match(text, @"^\s*META\s*:\s*(.+)$", RegexOptions.Multiline);
            if (mm.Success) meta = mm.Groups[1].Value.Trim();

            string body;
            var sep = Regex.Match(text, @"^\s*---\s*$", RegexOptions.Multiline);
            if (sep.Success)
            {
                body = text.Substring(sep.Index + sep.Length);
            }
            else
            {
                body = Regex.Replace(text, @"^\s*(TITLE|META)\s*:.*$", "", RegexOptions.Multiline);
            }

            body = CleanArticleHtml(body);

            title = StripTags(title).Trim().Trim('"', '“', '”', '«', '»');
            if (string.IsNullOrWhiteSpace(title)) title = fallbackTitle;

            meta = StripTags(meta).Trim().Trim('"');
            if (string.IsNullOrWhiteSpace(meta))
            {
                string plain = Regex.Replace(StripTags(body), @"\s+", " ").Trim();
                meta = plain.Length > 155 ? plain.Substring(0, 155).TrimEnd() + "…" : plain;
            }

            return (title, meta, body);
        }

        // ===== MODELİN DÖNDÜRDÜĞÜ HTML'İ TEMİZLE =====
        // Model bazen makaleyi tam bir HTML belgesi olarak (<!DOCTYPE>, <html>, <head>, <title>, <body>)
        // ve kendi <h1> başlığıyla döndürüyor; şablonun içine gömülünce sayfa bozuluyordu.
        public static string CleanArticleHtml(string html)
        {
            string s = Regex.Replace(html ?? "", @"```[a-zA-Z]*", "");
            s = Regex.Replace(s, @"<!DOCTYPE[^>]*>", "", RegexOptions.IgnoreCase);
            s = Regex.Replace(s, @"<head[^>]*>[\s\S]*?</head>", "", RegexOptions.IgnoreCase);
            s = Regex.Replace(s, @"<title[^>]*>[\s\S]*?</title>", "", RegexOptions.IgnoreCase);
            s = Regex.Replace(s, @"<meta[^>]*>", "", RegexOptions.IgnoreCase);
            s = Regex.Replace(s, @"</?(html|body)[^>]*>", "", RegexOptions.IgnoreCase);
            s = Regex.Replace(s, @"<h1[^>]*>[\s\S]*?</h1>", "", RegexOptions.IgnoreCase);
            s = Regex.Replace(s, @"<header>\s*</header>", "", RegexOptions.IgnoreCase);
            return s.Trim();
        }

        // ===== METİN UZUNLUĞU KONTROLÜ =====
        // Model istenen uzunluğa çoğu zaman uymuyor (200-400 kelime). Metin kısaysa en fazla 2 kez
        // "genişleterek yeniden yaz" isteği gönderilir; daha uzun sonuç gelirse o kullanılır.
        public static async Task<string> EnsureLengthAsync(ChatClient client, List<ChatMessage> messages, string raw, bool isChinese, string expandInstruction)
        {
            int min = isChinese ? 1400 : 800;
            for (int attempt = 0; attempt < 2; attempt++)
            {
                int n = CountLength(raw, isChinese);
                if (n >= min) break;
                string unit = isChinese ? "characters" : "words";
                Console.WriteLine($"   ↻ Metin kısa ({n} {(isChinese ? "karakter" : "kelime")}), genişletme isteniyor...");
                var msgs = new List<ChatMessage>(messages)
                {
                    new AssistantChatMessage(raw),
                    new UserChatMessage(expandInstruction.Replace("{N}", $"{n} {unit}"))
                };
                try
                {
                    var r = await client.CompleteChatAsync(msgs);
                    string candidate = r.Value.Content[0].Text;
                    if (CountLength(candidate, isChinese) > n) raw = candidate;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"   ⚠️ Genişletme başarısız: {ex.Message}");
                    break;
                }
            }
            return raw;
        }

        static int CountLength(string html, bool isChinese)
        {
            string text = Regex.Replace(StripTags(html ?? ""), @"\s+", " ").Trim();
            if (isChinese) return text.Count(c => c >= 0x4E00 && c <= 0x9FFF);
            return text.Length == 0 ? 0 : text.Split(' ').Length;
        }

        static string StripTags(string s) => Regex.Replace(s ?? "", "<[^>]+>", "");

        static string Attr(string s) => (s ?? "").Replace("&", "&amp;").Replace("\"", "&quot;").Replace("<", "&lt;").Replace(">", "&gt;");

        // ===== DİL BLOG ANA SAYFASI (yoksa oluştur) =====
        static void EnsureBlogIndex(Lang l)
        {
            string indexPath = Path.Combine(Root, l.Code, "index.html");
            if (File.Exists(indexPath)) return;

            string dir = l.Rtl ? " dir=\"rtl\"" : "";
            string html = $@"<!DOCTYPE html>
<html lang=""{l.Code}""{dir}>
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>{Attr(l.IndexTitle)}</title>
    <meta name=""description"" content=""{Attr(l.IndexDesc)}"">
    <link rel=""canonical"" href=""{NetBase}/{l.Code}/"">
    <style>{Css(l)}
        .intro {{ color: #475569; margin-bottom: 24px; font-size: 1.05em; }}
        .post-list {{ list-style: none; margin: 0 !important; padding: 0; }}
        .post-list li {{ margin-bottom: 12px !important; }}
        .post-list a {{ display: block; padding: 18px 22px; border: 1px solid #e2e8f0; border-radius: 16px; text-decoration: none; color: #0f172a; transition: all 0.2s ease; }}
        .post-list a:hover {{ border-color: #2563eb; box-shadow: 0 4px 16px rgba(37,99,235,0.08); }}
        .post-title {{ font-weight: 700; font-size: 1.1em; margin-bottom: 4px; }}
        .post-meta {{ color: #94a3b8; font-size: 0.85em; }}
        .badge {{ background: #dbeafe; color: #2563eb; padding: 2px 10px; border-radius: 40px; font-weight: 700; font-size: 0.85em; }}
    </style>
</head>
<body>
<div class=""container"">
{Header(l, $"{NetBase}/en/")}
    <div class=""page-content"">
        <h1>{l.IndexH1}</h1>
        <p class=""intro"">{l.IndexDesc}</p>
        <ul class=""post-list"">
<!-- BLOG_POSTS -->
        </ul>
        <div class=""cta-box"">
            <p>{l.CtaText}</p>
            <a href=""{ComBase}/{l.Code}/"" class=""cta-button"">{l.CtaBtn}</a>
        </div>
    </div>
{Footer(l)}
</div>
</body>
</html>";
            File.WriteAllText(indexPath, html);
            UpdateSitemap($"{NetBase}/{l.Code}/");
            Console.WriteLine($"✅ {l.Code}/index.html (blog ana sayfası) oluşturuldu");
        }

        static void UpdateBlogIndex(Lang l, string slug, string title)
        {
            string indexPath = Path.Combine(Root, l.Code, "index.html");
            if (!File.Exists(indexPath)) return;

            string content = File.ReadAllText(indexPath);
            string existingEntryPattern = $@"<li>\s*<a href=""{Regex.Escape(slug)}\.html"">.*?</a>\s*</li>";
            content = Regex.Replace(content, existingEntryPattern, "", RegexOptions.Singleline);

            string formattedDate = DateTime.Now.ToString("dd MMMM yyyy", new CultureInfo(l.Culture));
            string newEntry = $@"
<li>
    <a href=""{slug}.html"">
        <div class=""post-title"">{Attr(title)}</div>
        <div class=""post-meta""><span class=""badge"">{l.NewBadge}</span> 📅 {formattedDate}</div>
    </a>
</li>";

            if (content.Contains("<!-- BLOG_POSTS -->"))
            {
                content = content.Replace("<!-- BLOG_POSTS -->", $"<!-- BLOG_POSTS -->\n{newEntry}");
                File.WriteAllText(indexPath, content);
            }
            else
            {
                Console.WriteLine($"⚠️ {l.Code}/index.html'de <!-- BLOG_POSTS --> yorumu bulunamadı!");
            }
        }

        static void UpdateSitemap(string url)
        {
            string sitemapPath = Path.Combine(Root, "sitemap.xml");
            if (!File.Exists(sitemapPath)) return;

            string content = File.ReadAllText(sitemapPath);
            if (content.Contains($"<loc>{url}</loc>")) return;

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
                File.WriteAllText(sitemapPath, content.Replace("</urlset>", newUrlEntry));
            }
        }

        // ===== hreflang SENKRONİZASYONU =====
        // Konunun var olan tüm dil sürümlerinde (tr, en ve ek diller) aynı tam hreflang listesini yazar.
        public static void SyncHreflang(string slugTr, string slugEn)
        {
            var versions = new List<(string Code, string Path, string Url)>
            {
                ("tr", Path.Combine(Root, $"{slugTr}.html"), $"{NetBase}/{slugTr}.html"),
                ("en", Path.Combine(Root, "en", $"{slugEn}.html"), $"{NetBase}/en/{slugEn}.html")
            };
            foreach (var l in Langs)
            {
                versions.Add((l.Code, ArticlePath(l.Code, slugEn), $"{NetBase}/{l.Code}/{slugEn}.html"));
            }

            var existing = versions.Where(v => File.Exists(v.Path)).ToList();
            if (existing.Count < 2) return;

            string xDefault = existing.Where(v => v.Code == "tr").Select(v => v.Url).FirstOrDefault()
                              ?? existing[0].Url;

            string block = string.Concat(existing.Select(v =>
                $"\n    <link rel=\"alternate\" hreflang=\"{v.Code}\" href=\"{v.Url}\">"))
                + $"\n    <link rel=\"alternate\" hreflang=\"x-default\" href=\"{xDefault}\">";

            int updated = 0;
            foreach (var v in existing)
            {
                string content = File.ReadAllText(v.Path);
                string stripped = Regex.Replace(content, @"\s*<link rel=""alternate"" hreflang=""[^""]*"" href=""[^""]*""\s*/?>", "");
                var m = Regex.Match(stripped, @"<meta name=""description""[^>]*>");
                if (!m.Success) continue;

                string result = stripped.Insert(m.Index + m.Length, block);
                if (result != content)
                {
                    File.WriteAllText(v.Path, result);
                    updated++;
                }
            }
            Console.WriteLine($"🔗 hreflang senkronize edildi ({existing.Count} dil, {updated} dosya güncellendi)");
        }

        // ===== İNGİLİZCE SAYFALARDAKİ mobilcv.com LİNKLERİNİ /en/ SAYFASINA ÇEVİR =====
        // mobilcv.com ana sayfası artık her zaman Türkçe açılıyor; İngilizce blogdan gelen
        // okuyucuların İngilizce araç sayfasına (https://www.mobilcv.com/en/) gitmesi gerekiyor.
        public static void FixEnglishCtaLinks()
        {
            string enDir = Path.Combine(Root, "en");
            if (!Directory.Exists(enDir)) return;

            int fixedCount = 0;
            foreach (var file in Directory.GetFiles(enDir, "*.html"))
            {
                string content = File.ReadAllText(file);
                string result = Regex.Replace(content, @"href=""https://(www\.)?mobilcv\.com/?""", $@"href=""{ComBase}/en/""");
                if (result != content)
                {
                    File.WriteAllText(file, result);
                    fixedCount++;
                }
            }
            if (fixedCount > 0)
                Console.WriteLine($"🔧 {fixedCount} İngilizce sayfada mobilcv.com linki /en/ sayfasına çevrildi");
        }

        // ===== MAKALE ŞABLONU =====
        static string BuildPage(Lang l, string title, string meta, string body, string slugEn)
        {
            string url = $"{NetBase}/{l.Code}/{slugEn}.html";
            string enc = Uri.EscapeDataString(url);
            string encTitle = Uri.EscapeDataString(title);
            string dir = l.Rtl ? " dir=\"rtl\"" : "";

            return $@"<!DOCTYPE html>
<html lang=""{l.Code}""{dir}>
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>{Attr(title)} | MobilCV</title>
    <meta name=""description"" content=""{Attr(meta)}"">
    <link rel=""canonical"" href=""{url}"">
    <style>{Css(l)}
    </style>
</head>
<body>
<div class=""container"">
{Header(l, $"{NetBase}/en/{slugEn}.html")}
    <div class=""page-content"">
        <article>
            <h1>{Attr(title)}</h1>
            {body}
        </article>

        <div class=""share-box"">
            <p>{l.Share}</p>
            <div class=""share-buttons"">
                <a href=""https://www.linkedin.com/sharing/share-offsite/?url={enc}"" target=""_blank"" rel=""noopener"" class=""share-btn share-linkedin"">LinkedIn</a>
                <a href=""https://twitter.com/intent/tweet?url={enc}&text={encTitle}"" target=""_blank"" rel=""noopener"" class=""share-btn share-twitter"">X (Twitter)</a>
                <a href=""https://api.whatsapp.com/send?text={encTitle}%20-%20{enc}"" target=""_blank"" rel=""noopener"" class=""share-btn share-whatsapp"">WhatsApp</a>
            </div>
        </div>

        <div class=""cta-box"">
            <p>{l.CtaText}</p>
            <a href=""{ComBase}/{l.Code}/"" class=""cta-button"">{l.CtaBtn}</a>
        </div>
    </div>
{Footer(l)}
</div>
</body>
</html>";
        }

        static string Header(Lang l, string englishLink) => $@"
    <header class=""site-header"">
        <a href=""{NetBase}/{l.Code}/"" class=""logo"">Mobil<span>CV</span></a>
        <nav>
            <ul class=""nav-links"">
                <li><a href=""{ComBase}/{l.Code}/"">{l.Home}</a></li>
                <li><a href=""{NetBase}/{l.Code}/"">{l.Blog}</a></li>
                <li><a href=""{ComBase}/{l.Code}/"" class=""nav-cta"">{l.CreateNow}</a></li>
                <li><a href=""{englishLink}"" class=""lang-switch"">🇬🇧 English</a></li>
            </ul>
        </nav>
    </header>";

        static string Footer(Lang l) => $@"
    <footer class=""footer"">
        <div class=""footer-links"">
            <a href=""{ComBase}/{l.Code}/"">{l.Home}</a>
            <a href=""{NetBase}/{l.Code}/"">{l.Blog}</a>
        </div>
        <p>&copy; {DateTime.UtcNow.Year} MobilCV &mdash; {l.Footer} <a href=""{ComBase}/{l.Code}/"">mobilcv.com</a></p>
    </footer>";

        static string Css(Lang l)
        {
            string listSide = l.Rtl ? "margin-right: 24px;" : "margin-left: 24px;";
            return $@"
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #0f172a; line-height: 1.8; padding: 20px; }}
        .container {{ max-width: 1100px; margin: 0 auto; background: #fff; border-radius: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.06); overflow: hidden; }}
        .site-header {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 28px; background: #fff; border-bottom: 1px solid #e2e8f0; flex-wrap: wrap; }}
        .logo {{ font-size: 1.6em; font-weight: 900; color: #0f172a; text-decoration: none; }}
        .logo span {{ color: #2563eb; }}
        .nav-links {{ display: flex; list-style: none; gap: 6px; flex-wrap: wrap; align-items: center; }}
        .nav-links a {{ padding: 10px 20px; color: #64748b; text-decoration: none; font-weight: 600; font-size: 0.95em; border-radius: 40px; transition: all 0.25s ease; }}
        .nav-links a:hover {{ color: #2563eb; background: #dbeafe; }}
        .nav-cta {{ background: #2563eb; color: #fff !important; padding: 10px 24px; border-radius: 40px; font-weight: 700; }}
        .nav-cta:hover {{ background: #1d4ed8 !important; }}
        .lang-switch {{ padding: 6px 14px; border: 1px solid #e2e8f0; border-radius: 40px; color: #64748b; text-decoration: none; font-size: 0.85em; font-weight: 700; }}
        .page-content {{ padding: 48px 40px 40px; }}
        .page-content h1 {{ font-size: 2.4em; font-weight: 800; margin-bottom: 16px; color: #0f172a; line-height: 1.3; }}
        .page-content p {{ color: #334155; margin-bottom: 16px; font-size: 1.05em; }}
        .page-content h2 {{ font-size: 1.6em; font-weight: 700; margin-top: 32px; margin-bottom: 12px; color: #0f172a; }}
        .page-content h3 {{ font-size: 1.25em; font-weight: 700; margin-top: 20px; margin-bottom: 8px; }}
        .page-content ul, .page-content ol {{ {listSide} margin-bottom: 20px; color: #334155; }}
        .page-content li {{ margin-bottom: 8px; }}
        .share-box {{ text-align: center; margin: 30px 0; padding: 20px; background: #f8fafc; border-radius: 12px; }}
        .share-box p {{ font-size: 0.95em; color: #64748b; margin-bottom: 12px; }}
        .share-buttons {{ display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }}
        .share-btn {{ display: inline-block; padding: 8px 18px; border-radius: 40px; text-decoration: none; font-weight: 600; font-size: 0.85em; color: #fff !important; }}
        .share-linkedin {{ background: #0a66c2; }}
        .share-twitter {{ background: #000; }}
        .share-whatsapp {{ background: #25D366; }}
        .cta-box {{ text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); border-radius: 16px; border: 1px solid #e2e8f0; }}
        .cta-box p {{ font-size: 1.2em; font-weight: 700; color: #0f172a; margin-bottom: 12px; }}
        .cta-button {{ display: inline-block; background: #2563eb; color: #fff; padding: 14px 36px; border-radius: 40px; text-decoration: none; font-weight: 700; font-size: 1.1em; }}
        .cta-button:hover {{ background: #1d4ed8; }}
        .footer {{ background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 30px; text-align: center; color: #94a3b8; }}
        .footer a {{ color: #2563eb; text-decoration: none; font-weight: 600; }}
        .footer-links {{ display: flex; justify-content: center; gap: 28px; flex-wrap: wrap; margin-bottom: 10px; }}
        .footer-links a {{ color: #64748b; font-weight: 500; }}
        @media (max-width: 640px) {{
            .site-header {{ flex-direction: column; gap: 12px; padding: 16px; }}
            .nav-links {{ justify-content: center; }}
            .page-content {{ padding: 24px 18px; }}
            .page-content h1 {{ font-size: 1.8em; }}
            .cta-box {{ padding: 20px; }}
            .cta-button {{ padding: 12px 24px; font-size: 1em; }}
        }}";
        }
    }
}
