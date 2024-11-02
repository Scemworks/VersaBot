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
    opt_type=OptionType.STRING
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
        box_size=10
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color or "black", back_color="white").convert("RGB")
    if logo_url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(logo_url) as resp:
                    resp.raise_for_status()
                logo_data = await resp.read()
            logo = Image.open(BytesIO(logo_data))
            qr_width, qr_height = img.size
            logo_size = int(qr_width * 0.2)
            logo = logo.resize((logo_size, logo_size))

            logo_position = ((qr_width - logo_size)//2,(qr_height - logo_size)//2)
            img.paste(logo, logo_position, mask = logo if logo.mode == "RGBA" else None)
        except Exception as e:
            print(f"Error occurred while downloading logo: {e}")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    file = File(file=buffer, filename="qrcode.png")
    qrembed = Embed(
        title="QR Code",
        description=f"QR Code generated for {link}",
        color=interactions.Color.random()
    )
    qrembed.set_footer(f"Requested by {ctx.author}")
    qrembed.set_image(url="attachment://qrcode.png")
    await ctx.send(embeds=[qrembed], files=[file])

bot.start(token)