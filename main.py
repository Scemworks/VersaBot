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

bot.start(token)