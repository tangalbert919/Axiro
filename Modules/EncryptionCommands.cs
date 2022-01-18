using Axiro.Services;
using Discord.Interactions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Axiro.Modules
{
    public class EncryptionCommands : InteractionModuleBase<SocketInteractionContext>
    {
        public InteractionService Commands { get; set; }

        private CommandHandler _handler;

        public EncryptionCommands(CommandHandler handler)
        {
            _handler = handler;
        }

        [SlashCommand("encode", "Encodes the message")]
        public async Task Encode(string hash, string message)
        {
            string result = "";
            if (hash.ToLower().Equals("base64"))
                result = Convert.ToBase64String(Encoding.UTF8.GetBytes(message));
            else
                await RespondAsync("This hash is currently unavailable");
            await RespondAsync(result);
        }
    }
}
