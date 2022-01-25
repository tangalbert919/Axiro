using Axiro.Services;
using Discord;
using Discord.Interactions;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class ImageCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public ImageCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        private class NekoAPI
        {
            public string url { get; set; }
        }

        [SlashCommand("neko", "Get a neko image")]
        public async Task Neko()
        {
            HttpClient client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/neko"));

            NekoAPI result = JsonConvert.DeserializeObject<NekoAPI>(reader.ReadToEnd());
            EmbedBuilder builder = new();
            builder.Title = "From nekos.life";
            builder.ImageUrl = result.url;
            builder.Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username);
            await RespondAsync(embed: builder.Build());
        }

        // TODO: Find some image boards that aren't anime.
        [SlashCommand("danbooru", "Get an image from Project Danbooru")]
        [RequireNsfw]
        public async Task Danbooru([Summary(description: "Search with this tag")] string tag = null)
        {
            HttpClient client = new();

            JsonDocument result = JsonDocument.ParseAsync(
                client.GetStreamAsync("https://danbooru.donmai.us/posts/random.json").Result).Result;
#if DEBUG
            Console.WriteLine(result.RootElement);
            Console.WriteLine(result.RootElement.GetProperty("id").GetUInt32());
#endif
            EmbedBuilder builder = new();
            builder.Title = "From Project Danbooru";
            builder.ImageUrl = result.RootElement.GetProperty("file_url").GetString();
            builder.Footer = new EmbedFooterBuilder().WithText("Requested by " + Context.User.Username);
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("konachan", "Get an image from Konachan")]
        [RequireNsfw]
        public async Task Konachan([Summary(description: "Search with this tag")] string tag = null)
        {
            /*HttpClient client = new();

            JsonDocument result = JsonDocument.ParseAsync(
                client.GetStreamAsync("https://konachan.com/post/random").Result).Result;*/
            await RespondAsync("Coming soon");
        }

        [SlashCommand("yandere", "Get an image from Yande.re")]
        [RequireNsfw]
        public async Task Yandere([Summary(description: "Search with this tag")] string tag = null)
        {
            await RespondAsync("Coming soon");
        }
    }
}
