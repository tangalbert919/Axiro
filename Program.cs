﻿using Axiro.Services;
using Discord;
using Discord.Commands;
using Discord.WebSocket;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
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
        public string NewsAPIToken { get; set; }
        public string TopGGToken { get; set; }
    }
    class Program
    {
        private readonly DiscordSocketClient _client;

        static void Main(string[] args)
        {
            // One of the more flexable ways to access the configuration data is to use the Microsoft's Configuration model,
            // this way we can avoid hard coding the environment secrets. I opted to use the Json and environment variable providers here.
            IConfiguration config = new ConfigurationBuilder()
                .AddEnvironmentVariables(prefix: "test_")
                .AddJsonFile("appsettings.json", optional: true)
                .Build();

            MainAsync(config).GetAwaiter().GetResult();
        }

        /*public Program()
        {
            _client = new DiscordSocketClient();

            _client.Log += LogAsync;
            _client.Ready += ReadyAsync;
            _client.MessageReceived += MessageReceivedAsync;
        }*/
        public static async Task MainAsync(IConfiguration config)
        {
            // You should dispose a service provider created using ASP.NET
            // when you are finished using it, at the end of your app's lifetime.
            // If you use another dependency injection framework, you should inspect
            // its documentation for the best way to do this.
            using var services = ConfigureServices(config);
            
            var client = services.GetRequiredService<DiscordSocketClient>();

            client.Log += LogAsync;
            //client.Ready += ReadyAsync;
            services.GetRequiredService<CommandService>().Log += LogAsync;

            /*string fileName = "config.json";
            string filePath = Path.GetFullPath(fileName);
            using FileStream stream = File.OpenRead(fileName);
            Config config = await JsonSerializer.DeserializeAsync<Config>(stream);*/

            // Tokens should be considered secret data and never hard-coded.
            // We can read from the environment variable to avoid hard coding.
            await client.LoginAsync(TokenType.Bot, config["DiscordToken"]);
            await client.StartAsync();

            // Here we initialize the logic required to register our commands.
            await services.GetRequiredService<CommandHandlingService>().InitializeAsync();

            await Task.Delay(Timeout.Infinite);
        }
        private static Task LogAsync(LogMessage arg)
        {
            Console.WriteLine(arg.ToString());
            return Task.CompletedTask;
        }

        /*private Task ReadyAsync()
        {
            Console.WriteLine($"{_client.CurrentUser} is now ready.");
            return Task.CompletedTask;
        }*/

        private Task MessageReceivedAsync(SocketMessage arg)
        {
            throw new NotImplementedException();
        }
        private static ServiceProvider ConfigureServices(IConfiguration config)
        {
            return new ServiceCollection()
                .AddSingleton<DiscordSocketClient>()
                .AddSingleton<CommandService>()
                .AddSingleton<CommandHandlingService>()
                //.AddSingleton<HttpClient>()
                //.AddSingleton<PictureService>()
                .BuildServiceProvider();
        }
    }
}