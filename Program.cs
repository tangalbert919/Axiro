using Discord;
using Discord.WebSocket;
using System;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace Axiro
{
    class Config
    {
        public string DiscordToken { get; set; }
    }
    class Program
    {
        private readonly DiscordSocketClient _client;

        static void Main(string[] args)
            => new Program().MainAsync().GetAwaiter().GetResult();

        public Program()
        {
            _client = new DiscordSocketClient();

            _client.Log += LogAsync;
            _client.Ready += ReadyAsync;
            _client.MessageReceived += MessageReceivedAsync;
        }
        public async Task MainAsync()
        {
            // Load configuration JSON file.
            string fileName = "config.json";
            using FileStream stream = File.OpenRead(fileName);
            Config config = await JsonSerializer.DeserializeAsync<Config>(stream);

            await _client.LoginAsync(TokenType.Bot, $"{config.DiscordToken}");
            await Task.Delay(Timeout.Infinite);
        }
        private Task LogAsync(LogMessage arg)
        {
            throw new NotImplementedException();
        }

        private Task ReadyAsync()
        {
            Console.WriteLine($"{_client.CurrentUser} is now ready.");
            return Task.CompletedTask;
        }

        private Task MessageReceivedAsync(SocketMessage arg)
        {
            throw new NotImplementedException();
        }
    }
}
