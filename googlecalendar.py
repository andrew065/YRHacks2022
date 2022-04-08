from discord.ext import commands

class googlecalendar(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='addevent')
    async def addevent(self, ctx: commands.Context):
        await ctx.send('event added (totally)')


def setup(bot: commands.Bot):
    bot.add_cog(googlecalendar(bot))
