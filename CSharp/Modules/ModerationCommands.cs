using Axiro.Services;
using Discord;
using Discord.Interactions;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class ModerationCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public ModerationCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        [SlashCommand("kick", "Kick the specified user")]
        [RequireUserPermission(GuildPermission.KickMembers)]
        [RequireBotPermission(GuildPermission.KickMembers)]
        public async Task Kick(IGuildUser user, [Summary(description: "Kick with specified reason")] string reason = null)
        {
            await user.KickAsync(reason);
            await RespondAsync("User kicked.");
        }

        [SlashCommand("ban", "Bans the specified user")]
        [RequireUserPermission(GuildPermission.BanMembers)]
        [RequireBotPermission(GuildPermission.BanMembers)]
        public async Task Ban(IGuildUser user, [Summary(description: "Prune messages for this many days")] int days = 0,
            [Summary(description: "Ban with specified reason")] string reason = null)
        {
            await user.BanAsync(days, reason);
            await RespondAsync("User banned.");
        }

        [SlashCommand("mute", "Mutes the specified user")]
        public async Task Mute()
        {
            await RespondAsync("Coming soon");
        }

        [SlashCommand("prune", "Prunes messages")]
        [RequireUserPermission(GuildPermission.ManageMessages)]
        [RequireBotPermission(GuildPermission.ManageMessages)]
        public async Task Prune(int messages)
        {
            await RespondAsync("Coming soon");
        }
    }
}
