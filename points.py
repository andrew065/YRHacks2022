from database import get_database
from discord.ext import commands
from discord import Color, Embed

class Points(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = get_database()

    @commands.command(name='gimme')
    async def gimme(self, ctx: commands.Context, pts: int):
        self.db.users.update_one({ 'user_id': ctx.author.id }, { '$inc' : { 'points': pts } }, upsert=True)
        await ctx.send(f'{ctx.author.mention}! awarded {pts} points!')

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx: commands.Context):
        embed = Embed(title="Point Leaderboard", color=Color.blue())
        for x in self.db.users.find().sort('points', -1):
            user = await self.bot.fetch_user(x['user_id'])
            embed.add_field(name=user.name, value=x['points'], inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Points(bot))
