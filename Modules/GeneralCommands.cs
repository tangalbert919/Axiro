using Axiro.Services;
using Discord;
using Discord.Interactions;
using System;
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

        [SlashCommand("about", "About this bot")]
        public async Task About()
        {
            EmbedBuilder builder = new();
            builder.Title = "About Axiro";
            builder.Description = "This bot was created to do weird things.";
            builder.AddField("Author: ", "tangalbert919 (The Freaking iDroid)");
            builder.AddField("Stats: ", "Coming soon");
            builder.AddField("Version: ",
#if DEBUG
                "Developer build");
#else
                "Version 7");
#endif
            await RespondAsync(embed: builder.Build());
        }

        // TODO: Find a way to get current roles.
        [SlashCommand("user", "Get information about a user.")]
        public async Task User(IGuildUser user)
        {
            EmbedBuilder builder = new();
            builder.Title = "Information successfully collected!";
            builder.Description = "Here's what we know about this user!";
            builder.AddField("User ID: ", user.Id);
            builder.AddField("Current roles: ", "coming soon");
            builder.AddField("Joined Discord on: ", user.CreatedAt);
            builder.ThumbnailUrl = user.GetAvatarUrl();
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("avatar", "Get the user avatar")]
        public async Task Avatar(IUser user)
        {
            EmbedBuilder builder = new();
            builder.Color = Color.Red;
            builder.ImageUrl = user.GetAvatarUrl(ImageFormat.Auto, 1024);
            builder.Title = $"Here is {user.Username}'s avatar.";
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("invite", "Get the invite link for the bot")]
        public async Task Invite()
        {
            EmbedBuilder builder = new();
            builder.Title = "You want to invite me to your server?";
            builder.Description = "Invite me by clicking [here](https://discordapp.com/api/oauth2/authorize?client_id=458834071796187149&permissions=8&scope=bot).";
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("server", "Join Axiro's support server")]
        public async Task Server()
        {
            EmbedBuilder builder = new();
            builder.Title = "You want to join my support server?";
            builder.Description = "Join by clicking [here](https://discord.gg/NEpsy8h).";
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("suggest", "Send a suggestion!")]
        public async Task Suggestion(string suggestion)
        {
            EmbedBuilder builder = new();
            builder.Title = "Suggestion received!";
            builder.Description = $"We got a suggestion from {Context.User.Username}!";
            builder.AddField("Suggestion", suggestion);
            Embed[] embed = new Embed[1];
            embed[0] = builder.Build();
            await Context.Client.GetGuild(457696464475258881).GetTextChannel(460669314933063680)
                .SendMessageAsync(embeds: embed);
            await RespondAsync("Suggestion sent");
        }

        [SlashCommand("report", "Report a bug!")]
        public async Task Report(string report)
        {
            EmbedBuilder builder = new();
            builder.Title = "Report received!";
            builder.Description = $"We got a report from {Context.User.Username}!";
            builder.AddField("Suggestion", report);
            Embed[] embed = new Embed[1];
            embed[0] = builder.Build();
            await Context.Client.GetGuild(457696464475258881).GetTextChannel(460666448352641026)
                .SendMessageAsync(embeds: embed);
            await RespondAsync("Report sent");
        }

        [SlashCommand("github", "Get GitHub link!")]
        public async Task Github()
        {
            EmbedBuilder builder = new();
            builder.Title = "Are you a programmer and want to help?";
            builder.Description = "Click [here](https://github.com/tangalbert919/Axiro) to see my repository.";
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("upvote", "Upvote this bot!")]
        public async Task Upvote()
        {
            EmbedBuilder builder = new();
            builder.Title = "Vote for Axiro";
            builder.Description = "Do you really like using Axiro? You can upvote it by clicking [here](https://top.gg/bot/458834071796187149/vote)!";
            await RespondAsync(embed: builder.Build());
        }
    }
}
