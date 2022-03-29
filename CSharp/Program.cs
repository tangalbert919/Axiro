using Axiro.Services;
using Discord;
using Discord.Interactions;
using Discord.WebSocket;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace Axiro
{
    class Program
    {

        static void Main(string[] args)
        {
            // Load configuration.
            IConfiguration config = new ConfigurationBuilder()
                .AddEnvironmentVariables(prefix: "test_")
                .AddJsonFile("config.json", optional: false)
                .Build();

            // Start the bot.
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
            // Dependency injection is a key part of the Interactions framework but it
            // needs to be disposed at the end of the app's lifetime.
            using var services = ConfigureServices(config);
            
            var client = services.GetRequiredService<DiscordSocketClient>();
            var command = services.GetRequiredService<InteractionService>();

            client.Log += LogAsync;
            command.Log += LogAsync;

            // Register slash and context commands. Takes place after the bot is in READY state.
            // If in debug mode, register commands for testing guild only.
            client.Ready += async () =>
            {
#if DEBUG
                // ID of the test guild can be provided from the Configuration object
                await command.RegisterCommandsToGuildAsync(config.GetValue<ulong>("TestGuild"), true);
#else
                await command.RegisterCommandsGloballyAsync(true);
#endif
            };

            // Here we initialize the logic required to register our commands.
            await services.GetRequiredService<CommandHandler>().InitializeAsync();

            // Read the Discord Token from the configuration object created earlier.
            await client.LoginAsync(TokenType.Bot, config["DiscordToken"]);
            await client.StartAsync();

            await Task.Delay(Timeout.Infinite);
        }
        private static Task LogAsync(LogMessage arg)
        {
            Console.WriteLine(arg.ToString());
            return Task.CompletedTask;
        }
        private static ServiceProvider ConfigureServices(IConfiguration config)
        {
            return new ServiceCollection()
                .AddSingleton(config)
                .AddSingleton<DiscordSocketClient>()
                .AddSingleton(x => new InteractionService(x.GetRequiredService<DiscordSocketClient>()))
                .AddSingleton<CommandHandler>()
                .BuildServiceProvider();
        }
    }
}
