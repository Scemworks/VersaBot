#Main file for VersaBot
import interactions
from interactions import*
import os
from dotenv import load_dotenv

#Import token from .env file
load_dotenv()
token = os.getenv("TOKEN")


bot = Client(intents=Intents.DEFAULT)

@bot.event()
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Owned by: {bot.owner}")

@slash_command(
    name="ping",
    description="Ping the latency of the bot",
)
async def ping(ctx: SlashContext):
    ping = Embed(
        title = "Pong!",
        description=f"{round(bot.latency * 1000)}ms",
        color = interactions.Color.random()
    )
    await ctx.send(embeds=ping)

bot.start(token)