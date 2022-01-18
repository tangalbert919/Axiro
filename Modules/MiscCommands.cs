using Axiro.Services;
using Discord;
using Discord.Interactions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class MiscCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public MiscCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        // TODO: Turn this into a command group.
        [SlashCommand("news", "Get the news")]
        public async Task News()
        {
            await RespondAsync("Coming soon");
        }

        [SlashCommand("uptime", "Get bot uptime")]
        public async Task Uptime()
        {
            await RespondAsync("Coming soon");
        }

        [SlashCommand("winner", "Declare someone a winner")]
        public async Task Winner()
        {
            IAsyncEnumerable<IReadOnlyCollection<IUser>> temp = Context.Channel.GetUsersAsync();
            IEnumerable<IUser> result = temp.FlattenAsync().GetAwaiter().GetResult();
            IUser[] users = result.ToArray();
            Random rand = new();
            IUser selected = users[rand.Next(users.Length)];
            await RespondAsync($"Congratulations! {selected.Username} is a winner!");
        }

        [SlashCommand("loser", "Declare someone a loser")]
        public async Task Loser()
        {
            IAsyncEnumerable<IReadOnlyCollection<IUser>> temp = Context.Channel.GetUsersAsync();
            IEnumerable<IUser> result = temp.FlattenAsync().GetAwaiter().GetResult();
            IUser[] users = result.ToArray();
            Random rand = new();
            IUser selected = users[rand.Next(users.Length)];
            await RespondAsync($"Sorry! {selected.Username} is a loser!");
        }

        [SlashCommand("drumpf", "Changes someone's nickname to Donald Drumpf.")]
        [RequireUserPermission(GuildPermission.ManageNicknames)]
        [RequireBotPermission(GuildPermission.ManageNicknames)]
        public async Task Drumpf(IGuildUser user)
        {
            await user.ModifyAsync(x =>
            {
                x.Nickname = "Donald Drumpf";
            });
            await RespondAsync("Someone's nickname got changed to \"Donald Drumpf\".");
        }

        [SlashCommand("wegothim", "WE GOT HIM!")]
        public async Task WeGotHim()
        {
            EmbedBuilder builder = new();
            builder.Color = Color.Red;
            builder.Title = "WE GOT HIM!";
            builder.ImageUrl = "https://media1.tenor.com/images/4a08ff9d3f956dd814fc8ee1cfaac592/tenor.gif?itemid=10407619";
            await RespondAsync(null, null, false, false, null, null, null, builder.Build());
        }

        [SlashCommand("chrome", "For some reason, Chrome.")]
        public async Task Chrome()
        {
            await RespondAsync("Cannot get current version of Chrome at this time.");
        }
    }
}
