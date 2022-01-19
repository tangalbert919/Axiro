using Axiro.Services;
using Discord.Interactions;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class ImageCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;
        private HttpClient client;

        public ImageCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        [SlashCommand("neko", "Get a neko image")]
        public async Task Neko()
        {
            client = new();
            StreamReader reader = new(await client.GetStreamAsync("https://nekos.life/api/v2/img/neko"));

            DataSet set = JsonConvert.DeserializeObject<DataSet>(reader.ReadToEnd());
            DataTable dt = set.Tables[0];
            await RespondAsync("Coming soon");
        }

        // TODO: Find some image boards that aren't anime.
        [SlashCommand("danbooru", "Get an image from Project Danbooru")]
        [RequireNsfw]
        public async Task Danbooru([Summary(description: "Search with this tag")]string tag = null)
        {
            await RespondAsync("Coming soon");
        }

        [SlashCommand("konachan", "Get an image from Konachan")]
        [RequireNsfw]
        public async Task Konachan([Summary(description: "Search with this tag")]string tag = null)
        {
            await RespondAsync("Coming soon");
        }

        [SlashCommand("yandere", "Get an image from Yande.re")]
        [RequireNsfw]
        public async Task Yandere([Summary(description: "Search with this tag")]string tag = null)
        {
            await RespondAsync("Coming soon");
        }
    }
}
