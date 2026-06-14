import discord
import manager

BOT_TOKEN = "BOT TOKEN GOES HERE"
class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!ai'):
            manager_client = manager.Manager()
            response = manager_client.to_llm(message.content)
            await message.channel.send(response)
        else:
            pass





intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)
client.run(BOT_TOKEN)


