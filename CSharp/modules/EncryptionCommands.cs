using Axiro.Services;
using Discord.Interactions;
using System;
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
            string result;
            if (hash.ToLower().Equals("base64"))
                result = Convert.ToBase64String(Encoding.UTF8.GetBytes(message));
            else
            {
                await RespondAsync("This hash is currently unavailable");
                return;
            }
            await RespondAsync(result);
        }

        [SlashCommand("decode", "Decodes the message")]
        public async Task Decode(string hash, string message)
        {
            string result;
            if (hash.ToLower().Equals("base64"))
                result = Convert.FromBase64String(message).ToString();
            else
            {
                await RespondAsync("This hash is currently unavailable");
                return;
            }
            await RespondAsync(result);
        }

        [SlashCommand("reverse", "Reverses the message")]
        public async Task Reverse(string message)
        {
            char[] temp = message.ToCharArray();
            char[] result = new char[temp.Length];
            for (int i = 0; i < temp.Length; i++)
                result[i] = temp[temp.Length - 1 - i];
            await RespondAsync(result.ToString());
        }
    }
}
