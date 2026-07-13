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

            string topic = "Yapay zeka iş dünyasını nasıl değiştiriyor?";
            string slug = "yapay-zeka-is-dunyasini-nasil-degistiriyor";

            Console.WriteLine($"📝 Konu: {topic}");

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

            string fileName = $"{slug}.html";
            string filePath = Path.Combine("..", fileName);
            File.WriteAllText(filePath, htmlContent);

            Console.WriteLine($"✅ {fileName} oluşturuldu!");
        }
    }
}
