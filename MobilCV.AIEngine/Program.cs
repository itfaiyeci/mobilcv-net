using OpenAI.Chat;

namespace MobilCV.AIEngine
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("🚀 MobilCV AI Motoru Başlatılıyor...");
            
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("OPENAI_API_KEY bulunamadı!");
            var client = new ChatClient("gpt-3.5-turbo", apiKey);

            // Rastgele konu seçimi
            string[] topics = {
                "CV'de Dikkat Edilmesi Gereken 5 Kritik Nokta",
                "Mülakatta Başarılı Olmanın 7 Altın Kuralı",
                "2026'nın En Popüler 10 Mesleği",
                "Kariyer Değiştirmek İsteyenler İçin Rehber",
                "Yapay Zeka İş Dünyasını Nasıl Dönüştürüyor?"
            };

            Random random = new Random();
            string topic = topics[random.Next(topics.Length)];
            string slug = topic
    .ToLowerInvariant()
    .Replace("?", "")
    .Replace(",", "")
    .Replace(".", "")
    .Replace("'", "")
    .Replace("ü", "u")
    .Replace("ğ", "g")
    .Replace("ş", "s")
    .Replace("ı", "i")
    .Replace("ö", "o")
    .Replace("ç", "c")
    .Replace("İ", "i")   // <-- BU SATIRI EKLE
    .Replace(" ", "-")
    .Trim('-');

            Console.WriteLine($"📝 Konu: {topic}");

            try
            {
                var messages = new List<ChatMessage>
                {
                    new SystemChatMessage("Sen bir kariyer uzmanısın."),
                    new UserChatMessage($@"
                        Konu: {topic}
                        500-700 kelimelik SEO uyumlu bir blog makalesi yaz.
                        Tam bir HTML belgesi olarak ver.
                        Sadece HTML kodunu ver.
                    ")
                };

                var response = await client.CompleteChatAsync(messages);
                string htmlContent = response.Value.Content[0].Text;

                // Makale başlığını ve meta açıklamayı ayıkla
                string title = topic;
                string metaDescription = topic + " - Kariyer rehberi ve iş dünyası ipuçları.";

                // HTML dosyasını oluştur
                string fileName = $"{slug}.html";
                string fullHtml = BuildHtmlPage(title, metaDescription, htmlContent);
                
                string filePath = Path.Combine("..", fileName);
                File.WriteAllText(filePath, fullHtml);

                Console.WriteLine($"✅ {fileName} oluşturuldu!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ HATA: {ex.Message}");
                Environment.Exit(1);
            }
        }

        // ===== YENİ MAKALE ŞABLONU (HEADER + FOOTER DAHİL) =====
        static string BuildHtmlPage(string title, string metaDescription, string htmlBody)
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
        <article>
            <h1>{title}</h1>
            {htmlBody}
        </article>
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
