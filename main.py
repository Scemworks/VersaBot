#Main file for VersaBot
import interactions
from interactions import*
import os
from dotenv import load_dotenv
import random

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
    description="Ping and get latency of the bot"
)
async def ping(ctx: SlashContext):
    pings = Embed(
        title="Pong!",
        description=f"{round(bot.latency * 1000)}ms",
        color=interactions.Color.random()
        )
    await ctx.send(embeds=[pings])

@slash_command(
    name="dice",
    description="Rolls a dice"
)
async def dice(ctx: SlashContext):
    dice1 = ['⚀','⚁','⚂','⚃','⚄','⚅']
    diceembed = Embed(
        title="Dice Roll",
        description="Rolling the dice...",
        color=interactions.Color.random()
    )
    msg = await ctx.send(embeds=[diceembed])
    await asyncio.sleep(5)

    diceembed2 = Embed(
        title="Dice Roll",
        description=f"Rolled dice {random.choices(dice1)}",
        color=interactions.Color.random()
    )
    await msg1.edit(embeds=[diceembed2])

    
bot.start(token)