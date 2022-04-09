from database import get_database
from discord.ext import commands
from discord import Color, Embed
from pymongo import ReturnDocument
from random import randint

class Points(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = get_database()

    @commands.command(name='addtask')
    async def addtask(self, ctx: commands.Context, name: str, *description):
        if not description:
            description = ('no description',)
        res = self.db.tasks.update_one(
            { 'user_id': ctx.author.id, 'name': name },
            { '$set': { 'description': ' '.join(description) } },
            upsert=True
        )
        await ctx.send(f'{ctx.author.mention} task {name} {"added" if res.upserted_id else "updated"} successfully!')

    @commands.command(name='done')
    async def done(self, ctx: commands.Context, name: str):
        res = self.db.tasks.delete_one({ 'user_id': ctx.author.id, 'name': name })
        if res.deleted_count:
            pts = randint(3, 7)
            user = self.db.users.find_one_and_update(
                { 'user_id': ctx.author.id },
                { '$inc' : { 'points': pts } },
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            await ctx.send(f'{ctx.author.mention} task {name} completed!\n'
                + f'You earned {pts} points (current points: {user["points"]})')
        else:
            await ctx.send(f'{ctx.author.mention} task {name} does not exist!')

    @commands.command(name='tasks')
    async def tasks(self, ctx: commands.Context):
        embed = Embed(title='Your Tasks', color=Color.green())
        for x in self.db.tasks.find({ 'user_id': ctx.author.id }):
            embed.add_field(name=x['name'], value=x['description'], inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Points(bot))
