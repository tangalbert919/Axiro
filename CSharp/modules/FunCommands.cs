using Axiro.Services;
using Discord;
using Discord.Interactions;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class FunCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public FunCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        private class NekoAPI
        {
            public string Url { get; set; }
        }

        [SlashCommand("8ball", "Ask the magic 8-ball anything!")]
        public async Task EightBall(string question)
        {
            // TODO: Create 8-ball enum?
            await RespondAsync("Coming soon");
        }

        [SlashCommand("kiss", "Why?")]
        public async Task Kiss(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/kiss"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} just kissed {user.Username}. Weird...",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("hug", "Hug a user!")]
        public async Task Hug(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/hug"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} hugged {user.Username}. How comforting...",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("tickle", "Tickle a user!")]
        public async Task Tickle(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/tickle"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} tickled {user.Username}. They're having fun...",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("poke", "Poke a user!")]
        public async Task Poke(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/poke"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} poked {user.Username}. Yikes.",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("slap", "Slap a user!")]
        public async Task Slap(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/slap"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} slapped {user.Username}.",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("cuddle", "Cuddle a user!")]
        public async Task Cuddle(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/cuddle"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} cuddled {user.Username}. How comforting.",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("pat", "Pat a user!")]
        public async Task Pat(IGuildUser user)
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/pat"));
            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new()
            {
                Title = $"{Context.User.Username} patted {user.Username}. That's nice.",
                ImageUrl = result.Url,
                Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username)
            };
            await RespondAsync(embed: builder.Build());
        }

        [Group("random", "Random command")]
        public class RandomCommand : InteractionModuleBase<SocketInteractionContext>
        {
            [SlashCommand("number", "Get a random number")]
            public async Task Number()
            {
                Random rand = new();
                await RespondAsync(rand.Next().ToString());
            }
            [SlashCommand("fact", "Get a random fact.")]
            public async Task Fact()
            {
                await RespondAsync("Coming soon");
            }

            [SlashCommand("quote", "Get a random quote.")]
            public async Task Quote()
            {
                await RespondAsync("Coming soon");
            }
        }
    }
}
