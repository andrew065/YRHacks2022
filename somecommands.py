from discord.ext import commands


class SomeCommands(commands.Cog):
    '''A couple of simple commands.'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        '''Get the bot's current websocket latency.'''
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


def setup(bot: commands.Bot):
    bot.add_cog(SomeCommands(bot))
