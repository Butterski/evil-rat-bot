import os

import d20
import discord
from discord.errors import Forbidden, HTTPException
from discord.ext import commands, tasks
from discord.ext.commands.errors import CommandInvokeError
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


client = commands.Bot(
    command_prefix=".", help_command=None, intents=discord.Intents.all()
)


# -----COGS-----
COGS = ("cogs.dice", "cogs.schedule", "cogs.askRat")


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


client.run(TOKEN)
