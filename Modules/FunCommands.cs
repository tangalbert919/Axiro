using Axiro.Services;
using Discord.Interactions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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

        [SlashCommand("8ball", "Ask the magic 8-ball anything!")]
        public async Task EightBall(string question)
        {
            // TODO: Create 8-ball enum?
            await RespondAsync("Coming soon");
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
