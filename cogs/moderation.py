import discord
from discord.ext import commands
from discord.ext.commands import Cog
import asyncio


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f"initilised {__class__.__cog_name__} cog")
        self.mod_log = None
        self.dm_channel = None

    async def send_message(self, channel, message: str):
        await channel.trigger_typing()
        await channel.send(f"{message}", delete_after=5)

    async def send_embed(self, member: discord.Member, title: str, description: str, color):
        await ctx.trigger_typing()
        embed = discord.Embed(
            title=title,
            description=description
        )
        embed.color = color
        embed.set_thumbnail(url=member.avatar_url)
        await self.mod_log.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, arg: str):
        await member.ban(reason=arg)
        message = f"**{member.display_name}** has been banned.\n**Reason:** {arg}"
        await self.send_message(self, channel=ctx.channel, message=message)
        if self.mod_log is not None:
            await self.send_embed(
                member=member,
                title="Member Banned",
                description=message,
                color=0xfcaeae
            )

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, arg):
        await member.kick(reason=arg)
        message = f"**{member.display_name}** has been kicked.\nReason: **{arg}**"
        await self.send_message(self, channel=ctx.channel, message=message)
        if self.mod_log is not None:
            await self.send_embed(
                member=member,
                title="Member Kicked",
                description=message,
                color=0xfcaeae
            )

    # warnings

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, channel: discord.TextChannel, *, arg):
        message = f"**Warning** has been issued to {member.mention}. \n**Reason:** {arg}"
        if self.mod_log is not None:
            await self.send_embed(
                member=member,
                title="Member warned",
                description=message,
                color=0x00ffff)

        # for mod log

        await channel.send(f"**Warning** has been issued to {member.mention}. \n**Reason:** {arg}")
        await member.send(f"**⚠️ You have been warned!** Reason: {arg}")

    #complaints in DMs

    @Cog.listener()
    async def on_message(message):
        if message.guild:
            return
        if message.author == client.user:
            return
        if self.dm_channel:
            await self.dm_channel.send(f"{message.author.mention} said: {message.content}")


def setup(client):
    client.add_cog(Moderation(client))
