import discord
from discord.ext import commands
import os


intents = discord.Intents.all()
intents.members = True
intents.presences = True

client = commands.Bot(intents=intents, command_prefix="!",
                      help_command=None, case_insensitive=True)


@client.event
async def on_ready():
    await client.wait_until_ready()
    await cogs_load()


async def cogs_load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")


async def meta():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Complaints in DMs."))
    print('{0.user}'.format(client) + " is ready to operate.")


def launch_discord_bot(token: str):
    client.run(token)
