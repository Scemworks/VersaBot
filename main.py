#Main file for VersaBot
import interactions
from interactions import*
import os
from dotenv import load_dotenv
import random
import asyncio
import qrcode
from io import BytesIO
from PIL import Image
import aiohttp

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
    msg1 = await ctx.send(embeds=[diceembed])
    await asyncio.sleep(3)

    diceembed2 = Embed(
        title="Dice Roll",
        description=f"Rolled dice {random.choices(dice1)}",
        color=interactions.Color.random()
    )
    await msg1.edit(embeds=[diceembed2])

@slash_command(
    name="flip",
    description="Flips a coin"
)
async def flip(ctx: SlashContext):
    coin = ['Heads', 'Tails']
    coinembed = Embed(
        title="Coin Flip",
        description="Flipping the coin...",
        color=interactions.Color.random()
    )
    msg = await ctx.send(embeds=[coinembed])
    await asyncio.sleep(3)

    coinembed2 = Embed(
        title="Coin Flip",
        description=f"Flipped to {random.choice(coin)}",
        color=interactions.Color.random()
    )
    await msg.edit(embeds=[coinembed2])

@slash_command(
    name="qr",
    description="Generates a QR Code from link/text given (with optional support for logo and color)"
    )
@slash_option(
    name="link",
    description="Link to generate QR Code from",
    opt_type=OptionType.STRING,
    required=True
    )
@slash_option(
    name="logo_url",
    description="URL of image to use as logo",
    opt_type=OptionType.STRING,
    required=False
)
@slash_option(
    name="color",
    description="Color to use for QR Code",
    opt_type=OptionType.STRING,
    required=False
)
async def qr(ctx: SlashContext, link: str, logo_url: str = None, color: str = None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color or "black", back_color="white").convert("RGB")
    if logo_url:
        try:
            async with aiohttp.ClientSession() as session:    
                async with session.get(logo_url) as r:
                    r.raise_for_status() 
                    logo_data = await r.read()  

            logo = Image.open(BytesIO(logo_data)) 
            qr_width, qr_height = img.size 
            logo_size = int(qr_width * 0.2) 
            logo = logo.resize((logo_size, logo_size)) 

            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, logo_position, mask=logo if logo.mode == "RGBA" else None)
        except Exception as e:
            await ctx.send(f"An error occurred while fetching the logo: {str(e)}")
            return
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    file = File(file=buffer, file_name="qrcode.png")
    qrembed = Embed(
        title="QR Code",
        description=f"QR Code generated for {link}",
        color=interactions.Color.random()
    )
    qrembed.set_footer(f"Requested by {ctx.author}")
    qrembed.set_image(url="attachment://qrcode.png")
    await ctx.send(embeds=[qrembed], files=[file])

@slash_command(
    name="fortune",
    description="Get a random fortune"
)
async def fortune(ctx:SlashContext):
    fortunes=[
        "What is the meaning of your life? Your life is very mean.",
        "Error:404, Fortune not found ",
        "Eat until the age your all teeth falls",
        "I see money in your future, it is not yours though",
        "We don't know the future, but you just got a free cookie",
        "Oops.... You don't have a future",
        " In future you will become a vegetarian",
        " Error:143, No boyfriend/girlfriend found during your life ",
        "Don't go out, road is full of gutters",
        " To truly  find yourself you should play hide and seek alone",
        " Better you go and sleep, you are useless",
        " Someone had googled you recently , but haven't found!",
        "You will be hungry again in an hour",
        "Ouch!! your future is complicated and it burns",
        "Please create your own future ",
        " Beware you are getting aged!!!",
        " In your beginning you will find your end",
        " Look at the time you have a bad time ",
        "Lol!!! It's better i don't tell you",
        "Love awaits you at nearest pet shop!",
        "You will receive a call... at some point in your life .You might get an email too",
        "Winter is coming, don't tell anyone",
        "Yes!! the universe agrees you should eat more ice creams",
        "People will forever ask you ridiculous question"
    ]
    fembed = Embed(
        title="Fortune",
        description="Finding your fortune...",
        color=interactions.Color.random())
    msg = await ctx.send(embeds=[fembed])
    await asyncio.sleep(3)

    fembed2 = Embed(
        title="Fortune",
        description=f"{random.choice(fortunes)}",
        color=interactions.Color.random())
    await msg.edit(embeds=[fembed2])

@slash_command(
    name="tarot",
    description="Draw a tarot card with an emoji!"
)
async def tarot(ctx: SlashContext):

    tarot_cards = [
    {"name": "The Fool", "emoji": "🤹"},
    {"name": "The Magician", "emoji": "🧙"},
    {"name": "The High Priestess", "emoji": "👸"},
    {"name": "The Empress", "emoji": "👑"},
    {"name": "The Emperor", "emoji": "🤴"},
    {"name": "The Hierophant", "emoji": "🧙‍♀️"},
    {"name": "The lovers", "emoji": "👩‍❤️‍👩"},
    {"name": "The Chariot", "emoji": "🚀"},
    {"name": "Strength", "emoji": "💪"},
    {"name": "The Hermit", "emoji": "🧝"},
    {"name": "Wheel of Fortune", "emoji": "🎲"},
    {"name": "Justice", "emoji": "⚔️"},
    {"name": "The Hanged Man", "emoji": "🏳️"},
    {"name": "Death", "emoji": "☠️"},
    {"name": "Temperance", "emoji": "🧙‍♂️"},
    {"name": "The Devil", "emoji": "👹"},
    {"name": "The Tower", "emoji": "🏰"},
    {"name": "The Star", "emoji": "⭐"},
    {"name": "The Moon", "emoji": "🌙"},
    {"name": "The Sun", "emoji": "☀️"},
    {"name": "Judgement", "emoji": "⚖️"},
    {"name": "The World", "emoji": "🌎"},
    {"name": "Error 404: Card Not Found", "emoji": "❓"}
]
    tembed = Embed(
        title="Tarot Card",
        description="Drawing a tarot card...",
        color=interactions.Color.random()
    )
    msg = await ctx.send(embeds=[tembed])
    await asyncio.sleep(3)

    tembed2 = Embed(
        title="Tarot Card",
        description=f"Your tarot card is {random.choice(tarot_cards)['name']} {random.choice(tarot_cards)['emoji']}",
        color=interactions.Color.random()
    )
    await msg.edit(embeds=[tembed2])

@slash_command(
    name="help",
    description="Get help with the bot"
)
async def help(ctx: SlashContext):
    hembed = Embed(
        title="Help",
        description="Here are the commands you can use with the bot",
        color=interactions.Color.random()
    )
    hembed.add_field(
        name="`/help`",
        value="> Shows this message",
        inline=False
    )
    hembed.add_field(
        name="`/dice`",
        value="> Rolls a dice",
        inline=False
    )
    hembed.add_field(
        name="`/flip`",
        value="> Flips a coin",
        inline=False
    )
    hembed.add_field(
        name="`/qr`",
        value="> Generates a QR Code from link/text given (with optional support for logo and color)",
        inline=False
    )
    hembed.add_field(
        name="`/fortune`",
        value="> Get a random fortune",
        inline=False
    )
    hembed.add_field(
        name="`/tarot`",
        value="> Draw a tarot card with an emoji!",
        inline=False
    )
    await ctx.send(embeds=[hembed])
@bot.event()
async def on_message_create(event: Message):
    if event.message.author.bot:
        return
    emoji_list = [
        "🤔","😕","🙄","🤨","🤷","👮","😊","👍","👎","👌","👏","🙏","🤝","👌"
    ]
    prod_reply = random.choice(emoji_list)
    await event.message.reply(content=prod_reply)
bot.start(token)