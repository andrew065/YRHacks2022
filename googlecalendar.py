import datetime

import googleapiclient.errors
import database
import dateparser
from datetime import timedelta
from datetime import datetime
from discord import Color, Embed, Member
from discord_components import DiscordComponents, Button
from discord.ext import commands
from googleapiclient.discovery import build
from cal import get_creds


class GoogleCalendar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.creds = get_creds()
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.db = database.get_database()

        DiscordComponents(self.bot)

    @commands.command(name='addevent')
    async def addevent(self, ctx: commands.Context, name: str, dur: str, user: Member = None):
        if user is None:
            usr = self.db.users.find_one({'user_id': ctx.author.id})
        else:
            usr = self.db.users.find_one({'user_id': user.id})

        times = dur.split("-")
        for x in range(2):
            times[x] = str(dateparser.parse(times[x], settings={'TO_TIMEZONE': 'UTC'})).replace(' ', 'T')

        event = {
            'summary': name,
            'start': {
                'dateTime': times[0] + '+00:00'
            },
            'end': {
                'dateTime': times[1] + '+00:00'
            }
        }
        try:
            self.service.events().insert(calendarId=usr['calendar_id'], body=event).execute()
            await ctx.send('Event added!')
        except googleapiclient.errors.HttpError:
            await ctx.send('Unable to add to calendar. Check event start and end time.')

    @commands.command(name='upcoming')
    async def upcoming(self, ctx: commands.Context, user: Member = None):
        if user is None:
            usr = self.db.users.find_one({'user_id': ctx.author.id})
        else :
            usr = self.db.users.find_one({'user_id': user.id})

        now = datetime.utcnow()
        end = (now + timedelta(hours=28 - now.hour) - timedelta(minutes=now.minute) -
               timedelta(seconds=now.second) - timedelta(microseconds=now.microsecond))
        events_results = self.service.events().list(calendarId=usr['calendar_id'], timeMin=now.isoformat() + 'Z',
                                                    timeMax=end.isoformat() + 'Z', singleEvents=True,
                                                    orderBy='startTime').execute()
        events = events_results.get('items', [])

        if not events:
            await ctx.send('No more events today.')
            return
        embed = Embed(title='Events Today', color=Color.green())
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))[11:-9]
            end = event['end'].get('dateTime', event['end'].get('date'))[11:-9]
            embed.add_field(name=event['summary'].capitalize(), value=start + '-' + end)
        await ctx.send(embed=embed)

    @commands.command(name='next')
    async def next(self, ctx: commands.Context, num: int, user: Member = None):
        if user is None:
            usr = self.db.users.find_one({'user_id': ctx.author.id})
        else:
            usr = self.db.users.find_one({'user_id': user.id})

        now = datetime.utcnow().isoformat() + 'Z'
        events_results = self.service.events().list(calendarId=usr['calendar_id'], timeMin=now,
                                                    maxResults=num, singleEvents=True,
                                                    orderBy='startTime').execute()
        events = events_results.get('items', [])

        if not events:
            await ctx.send('No more events today.')
            return
        embed = Embed(title=f"Next {num} event(s):", color=Color.green())
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))[11:-9]
            end = event['end'].get('dateTime', event['end'].get('date'))[11:-9]
            embed.add_field(name=event['summary'].capitalize(), value=start + '-' + end)
        await ctx.send(embed=embed)

    @commands.command(name='new')
    async def new(self, ctx: commands.Context):
        usr = self.db.users.find_one({'user_id': ctx.author.id})
        if usr['calendar_id'] != '':
            await ctx.send('Calendar already exists for ' + ctx.author.mention)
        else:
            calendar = {'summary': str(ctx.author), 'description': str(ctx.author.id), 'timeZone': 'Canada/Eastern'}
            new_calendar = self.service.calendars().insert(body=calendar).execute()
            self.db.users.update_one({'user_id': ctx.author.id}, {'$set': {'calendar_id': new_calendar['id']}}, upsert=True)
            await ctx.send('New calendar created.')

    @commands.command(name='delete')
    async def delete(self, ctx, name: str):
        usr = self.db.users.find_one({'user_id': ctx.author.id})
        event = {}

        events_results = self.service.events().list(calendarId=usr['calendar_id'],
                                                    timeMin=datetime.utcnow().isoformat() + 'Z',
                                                    singleEvents=True, orderBy='startTime').execute()
        events = events_results.get('items', [])
        for x in events:
            if x['summary'] == name.lower():
                event = x
        if len(event) == 0:
            await ctx.send('Event not found.')
        else:
            self.service.events().delete(calendarId=usr['calendar_id'], eventId=event['id']).execute()
            await ctx.send('Event deleted')

    @commands.command(name='deletecal')
    async def delete_cal(self, ctx):
        usr = self.db.users.find_one({'user_id': ctx.author.id})

        self.service.calendars().delete(calendarId=usr['calendar_id']).execute()
        await ctx.send('Calendar deleted')


def setup(bot: commands.Bot):
    bot.add_cog(GoogleCalendar(bot))
