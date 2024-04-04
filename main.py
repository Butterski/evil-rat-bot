import datetime as d
import os

import d20
import discord
import openai
from discord.errors import Forbidden, HTTPException
from discord.ext import commands, tasks
from discord.ext.commands.errors import CommandInvokeError
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("DISCORD_TOKEN")
openai.api_key = os.environ.get("OPENAI_API")


client = commands.Bot(
    command_prefix=".", help_command=None, intents=discord.Intents.all()
)


# -----COGS-----
COGS = ("cogs.dice","cogs.schedule")


@client.event
async def on_ready():
    print("╔" + ("═" * 50) + "╗")
    print(
        "║\033[95m"
        + "Witaj w szczur bocie by github.com/Butterski/".center(50)
        + "\033[0m║"
    )
    print("║" + (f"Zalogowano jako: {client.user.name}").center(50) + "║")
    print("║" + (f"").center(50) + "║")
    print("║" + (f"Loading COGS:").center(50) + "║")
    for cog in COGS:
        await client.load_extension(cog)
        print("║" + (f"{cog} loaded").center(50) + "║")
    print("╚" + ("═" * 50) + "╝")

    await client.change_presence(
        status=discord.Status.online, activity=discord.Game("kiedy gramy?")
    )


@client.listen("on_command_error")
@client.listen("on_slash_command_error")
async def commands_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.reply("Nie potrafię wykonać tej komendy :(")
    elif isinstance(error, commands.MaxConcurrencyReached):
        return await ctx.send(str(error))
    elif isinstance(error, CommandInvokeError):
        original = error.original
        if isinstance(original, d20.RollError):
            return await ctx.send(f"Error in roll: {original}")
        elif isinstance(original, Forbidden):
            try:
                return await ctx.author.send(
                    "Error: I am missing permissions to run this command. "
                    f"Please make sure I have permission to send messages to <#{ctx.channel.id}>."
                )
            except HTTPException:
                try:
                    return await ctx.send(
                        f"Error: I cannot send messages to this user."
                    )
                except HTTPException:
                    return

    raise error


# @client.command(pass_context=True)
# async def kiedyGramy(ctx):


# @tasks.loop(hours=1)
# async def change_activity():
#     today = d.datetime.today()
#     weekday = (d.datetime.today().weekday()) + 1
#     time = today.hour
#     channel = client.get_channel(1018175837947830364)
#     tmr = d.datetime.today() + d.timedelta(days=1)
#     inwk = d.datetime.today() + d.timedelta(days=7)
#     if weekday == 7 and time == 11:
#         msg = await channel.send(f'**Witajcie podróżnicy, kiedy gramy?**\ndaty: <t:{int(tmr.timestamp())}:d> => <t:{int(inwk.timestamp())}:d>\nklikać emotki\n|| @here ||')
#         ids = [1020804462887043134, 1020804469274968115, 1020804467819552810,
#                1020804460450172968, 1020804464875163781, 1020804465860825089, 1020804461842677760]
#         for i in ids:
#             emo = client.get_emoji(i)
#             await msg.add_reaction(emo)

# 824970912382189571

client.run(token)
