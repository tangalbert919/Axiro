using Discord;
using Discord.WebSocket;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace Axiro
{
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

        private Task LogAsync(LogMessage arg)
        {
            throw new NotImplementedException();
        }

        private Task ReadyAsync()
        {
            throw new NotImplementedException();
        }

        private Task MessageReceivedAsync(SocketMessage arg)
        {
            throw new NotImplementedException();
        }

        public async Task MainAsync()
        {
            //mainClient = new DiscordWebhookClient("link here");

            //Console.WriteLine("Omaha Watch Bot is now active.");
            //await FetchOmaha();
            await Task.Delay(Timeout.Infinite);
        }
    }
}
