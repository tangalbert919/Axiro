using Axiro.Services;
using Discord;
using Discord.Interactions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class MiscCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        // This is for the pig latin command.
        private readonly static char[] vowels = { 'a', 'e', 'i', 'o', 'u' };

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
            await RespondAsync(embed: builder.Build());
        }

        [SlashCommand("chrome", "For some reason, Chrome.")]
        public async Task Chrome()
        {
            await RespondAsync("Cannot get current version of Chrome at this time.");
        }

        [SlashCommand("piglatin", "Translate something to pig latin.")]
        public async Task PigLatin(string str)
        {
            // Copy all the words in the string to a collection.
            string temp = str.ToLower();
            List<string> process = new();
            while (temp.Contains(' '))
            {
                process.Add(temp.Substring(0, temp.IndexOf(' ')));
                temp = temp[(temp.IndexOf(' ') + 1)..];
            }
            // Add last word.
            process.Add(temp);

            // Translate every entry in the collection to pig latin.
            // https://en.wikipedia.org/wiki/Pig_Latin
            List<String> result = new();
            foreach (string word in process)
            {
                Console.WriteLine($"DEBUG: Word to be processed is {word}");
                char[] newword = word.ToCharArray();
                // Word starts with a vowel
                if (Array.IndexOf(vowels, newword[0]) > -1)
                    temp = word + "yay";
                // Word starts with a consonant.
                else
                {
                    // Word does not start with consonant clusters.
                    if (Array.IndexOf(vowels, newword[1]) > -1)
                        temp = word[1..] + word[0] + "ay";
                    // Word does start with consonant clusters.
                    else
                    {
                        int index = 1;
                        while (Array.IndexOf(vowels, newword[index]) == -1)
                        {
                            index++;
                            if (index >= word.Length)
                            {
                                Console.WriteLine($"ERROR: Invalid word {word}");
                                await RespondAsync("TRANSLATION FAILED!");
                            }
                        }
                        temp = word[index..] + word[0..index] + "ay";
                    }
                }
                result.Add(temp);
                Console.WriteLine($"DEBUG: Word has been processed: {temp}");
            }
            await RespondAsync(result.ToString());
        }
    }
}
