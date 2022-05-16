from discord.ext import commands
import traceback
import sys


class ErrorHandler(commands.Cog):

    def __init__(self, client):
        print(f"initilised {__class__.__cog_name__} cog")
        self.client = client

    async def send_message(self, ctx, message: str):
        await ctx.trigger_typing()
        await ctx.send(f"**{message}!**", delete_after=5)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.CommandNotFound):
            pass

        if isinstance(error, commands.MissingPermissions):
            message = "You are not allowed to use this command"
            await self.send_message(self, ctx=ctx, message=message)

        elif isinstance(error, commands.MemberNotFound):
            message = "Member is not specified"
            await self.send_message(self, ctx=ctx, message=message)

        elif isinstance(error, commands.MissingRequiredArgument):
            message = "Reason is missing"
            await ctx.trigger_typing()
            await self.send_message(self, ctx=ctx, message=message)

        else:
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(ErrorHandler(client))
