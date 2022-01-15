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
    public class GeneralCommands : InteractionModuleBase<SocketInteractionContext>
    {
        // Dependencies can be accessed through Property injection,
        // public properties with public setters will be set by the service provider
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public GeneralCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        [SlashCommand("help", "Display the help")]
        public async Task Help()
        {
            await RespondAsync("This command is currently unavailable.");
        }

        [SlashCommand("time", "Get the current time")]
        public async Task Time()
        {
            DateTime time = DateTime.Now;
            await RespondAsync(time.ToString());
        }
        [SlashCommand("avatar", "Get the user avatar")]
        public async Task Avatar(IUser user)
        {
            EmbedBuilder builder = new EmbedBuilder();
            builder.Color = Color.Red;
            builder.ImageUrl = user.GetAvatarUrl();
            builder.Title = $"Here is {user.Username}'s avatar.";
            await RespondAsync("", null, false, false, null, null, null, builder.Build());
        }
    }
}
