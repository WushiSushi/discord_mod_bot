import discord
import time
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!", help_command=None, case_insensitive=True)

#bot getting ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Complaints in DMs."))
    print('{0.user}'.format(client) + " is ready to operate.")
    
    
#errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
        
        
#ban
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, arg):
    guild = client.get_guild(<guild.id>)
    channel = guild.get_channel(<channel.id>)
    await member.ban(reason=arg)
    await ctx.trigger_typing()
    time.sleep(1)
    await ctx.send(f"**{member.display_name}** has been banned.\nReason: **{arg}**")

    #for mod log
    embed = discord.Embed(title="Member Banned.", description=f"**{member} has been banned.** *ID: {member.id}* \n**Reason: **{arg}")
    embed.color = 0xfcaeae
    embed.set_thumbnail(url=f"{member.avatar_url}")
    await channel.send(embed=embed)        
    
    
#ban error
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("**You are not allowed to use this command!** " + ctx.author.mention)

    elif isinstance(error, commands.MemberNotFound):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("**Either Reason is missing or Member is not specified.**")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("**Either Reason is missing or Member is not specified.**")
            
            
#kick
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, arg):
    guild = client.get_guild(<guild.id>)
    channel = guild.get_channel(<channel.id>)
    await member.kick(reason=arg)
    await ctx.send(f"**{member.display_name}** has been kicked.\nReason: **{arg}**")

    #for mod log
    embed = discord.Embed(title="Member Kicked.",description=f"**{member} has been kicked.** *ID: {member.id}* \n**Reason: **{arg}")
    embed.color = 0xfcaeae
    embed.set_thumbnail(url=f"{member.avatar_url}")
    await channel.send(embed=embed)


#kick error
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f"**Either Reason is missing or Member is not specified.**")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("**You are not allowed to use this command!** " + ctx.author.mention)

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("**Either Reason is missing or Member is not specified.**")    
            
            
#warnings
@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, channel: discord.TextChannel, *, arg):
    guild = client.get_guild(<guild.id>)
    channel2 = guild.get_channel(<channel.id>)
                 
    #for mod log
    embed = discord.Embed(title="Warning ⚠️", description=f"**{member} has been warned.**\n**Reason: **{arg}")
    embed.color = 0x00ffff
    embed.set_footer(text=f"ID: {member.id}", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=f"{member.avatar_url}")

    await channel.send(f"**Warning** has been issued to {member.mention}. \n**Reason:** {arg}")
    await channel2.send(embed=embed)
    await member.send(f"**⚠️ You have been warned!** Reason: {arg}")                


#warn error
@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("**You are not allowed to use this command!** " + ctx.author.mention)

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send("Arguments missing.", delete_after=5)
        


#complaints in DMs
@client.listen()
async def on_message(message):
    if message.guild == None:
        if message.author == client.user:
            pass

        elif message.author is not client.user:
            guild = client.get_guild(<guild.id>)
            channel = guild.get_channel(<channel.id>)
            await channel.send(f"{message.author.mention} said: {message.content}")
              
              
client.run(TOKEN)            
