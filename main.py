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
    "Do not be afraid of competition.",
    "An exciting opportunity lies ahead of you.",
    "You love peace.",
    "Get your mind set…confidence will lead you on.",
    "You will always be surrounded by true friends.",
    "Sell your ideas-they have exceptional merit.",
    "You should be able to undertake and complete anything.",
    "You are kind and friendly.",
    "You are wise beyond your years.",
    "Your ability to juggle many tasks will take you far.",
    "A routine task will turn into an enchanting adventure.",
    "Beware of all enterprises that require new clothes.",
    "Be true to your work, your word, and your friend.",
    "Goodness is the only investment that never fails.",
    "A journey of a thousand miles begins with a single step.",
    "Forget injuries; never forget kindnesses.",
    "Respect yourself and others will respect you.",
    "A man cannot be comfortable without his own approval.",
    "Always do right. This will gratify some people and astonish the rest.",
    "It is easier to stay out than to get out.",
    "Sing everyday and chase the mean blues away.",
    "You will receive money from an unexpected source.",
    "Attitude is a little thing that makes a big difference.",
    "Plan for many pleasures ahead.",
    "Experience is the best teacher.",
    "You will be happy with your spouse.",
    "Expect the unexpected.",
    "Stay healthy. Walk a mile.",
    "The family that plays together stays together.",
    "Eat chocolate to have a sweeter life.",
    "Once you make a decision the universe conspires to make it happen.",
    "Make yourself necessary to someone.",
    "The only way to have a friend is to be one.",
    "Nothing great was ever achieved without enthusiasm.",
    "Dance as if no one is watching.",
    "Live this day as if it were your last.",
    "Your life will be happy and peaceful.",
    "Reach for joy and all else will follow.",
    "Move in the direction of your dreams.",
    "Bloom where you are planted.",
    "Appreciate. Appreciate.  Appreciate.",
    "Happy News is on its way.",
    "A closed mouth gathers no feet.",
    "He who throws dirt is losing ground.",
    "Paradise is always where love dwells.",
    "The one you love is closer than you think.",
    "Love is like wildflowers…it is often found in the most unlikely places.",
    "In dreams and in love there are no impossibilities.",
    "Love isn't something you find. Love is something that finds you.",
    "True love is not something that comes everyday, follow your heart, it knows the right answer."
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
bot.start(token)