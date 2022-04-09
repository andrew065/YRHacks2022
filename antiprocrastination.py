import asyncio
from discord.ext import tasks, commands

class antiprocrastination(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_unload(self):
        self.punish.cancel()

    @tasks.loop(count=5, seconds=1.0)
    async def punish(self, ctx: commands.Context):
        await ctx.send(f'{ctx.author.mention} punishment')

    @commands.command(name='mathhomework')
    async def mathhomework(self, ctx: commands.Context, duration: float, interval: float):
        if duration <= 0 or interval <= 0.01:
            return
        
        @tasks.loop(seconds=interval, count=duration / interval)
        async def check():
            can_confirm = lambda m: m.author == ctx.author and m.channel == ctx.channel
            await ctx.send(f'{ctx.author.mention} {ctx.author.mention} {ctx.author.mention} are you doing your math homework')
            try:
                confirm = await self.bot.wait_for('message', check=can_confirm, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f'{ctx.author.mention} timed out!!!! punishment')
                self.punish.start(ctx)
                check.cancel()

            if confirm.content == "yes":
                await ctx.send('good')
                return

            await ctx.send(f'{ctx.author.mention} bad!!! punishment')
            self.punish.start(ctx)
            check.cancel()

        check.start()


    @commands.command(name='cancel')
    async def cancel(self, ctx: commands.Context):
        pass

    @commands.command(name='punishme')
    async def punishme(self, ctx: commands.Context):
        await ctx.send('yes daddy')
        self.punish.start(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(antiprocrastination(bot))
