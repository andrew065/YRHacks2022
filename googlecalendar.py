from datetime import time

from discord.ext import commands
from google.protobuf import service
from googleapiclient.discovery import build

import GoogleCalendar.cal
import database


class googlecalendar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.cal = database.get_database()

    @commands.command(name='addevent')
    async def addevent(self, ctx: commands.Context, name: str):
        # usr = self.cal.find(ctx.author.id)
        creds = GoogleCalendar.cal.main()

        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': name,
            'start': {
                'dateTime': '2022-04-09T10:00:08+00:00'
            },
            'end': {
                'dateTime': '2022-04-09T12:00:08+00:00'
            }
        }

        service.events().insert(calendarId='primary', body=event).execute()

        await ctx.send('Event added!')

    @commands.command(name='new')
    async def new_token(self, ctx: commands.Context):
        link = {
            'type': 2,
            'style': 5,
            'custom_id': 'Authenticate',
            'url': ''
        }



def setup(bot: commands.Bot):
    bot.add_cog(googlecalendar(bot))
