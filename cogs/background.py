import asyncio
from email.policy import default
from discord.ext import commands
import datetime
from datetime import datetime, timedelta
import discord
from discord.commands import SlashCommandGroup
import asyncio
import time

import config
from config import emo,fetch

global archive,solved,subscribers,guild_checks,added,guildObj,ids

solved = [] #solves updates sent
subscribers = [] #solves updates subscribers

archive = [] #contests scanned
ids = [] #contests ids scanned
guild_checks = [] #contest scanner subscribers
added = [] #contest scheduled
guildObj = [] #guild objects

global check_pause,live_pause
check_pause = 30
live_pause = 3
cd = 30

async def contest_scheduler(contest):
        for guild in guildObj:
            check = True
            
            with config.Connect() as cnx:
                cursor = cnx.cursor(buffered=True)
                cursor.execute(
                    'SELECT id from codeforcer.added WHERE contest_name=%s and guild_id=%s',
                    (
                        contest['name'],
                        guild.id
                    )
                )

                for rows in cursor:
                    check = False
                    break
            
            if guild.id in guild_checks and check:
                ts = contest['start']

                await guild.create_scheduled_event(
                    name = contest['name'], 
                    description = str(str(contest['dura']) + " hour " + contest['des']) + " contest", 
                    start_time = (datetime.utcfromtimestamp(ts - 1800)), 
                    end_time = (datetime.utcfromtimestamp(ts) + timedelta(hours = contest['dura'])),
                    location = f"https://codeforces.com/contests/{contest['id']}"
                )

                with config.Connect() as cnx:
                    cursor = cnx.cursor(buffered=True)
                    cursor.execute(
                        'INSERT INTO codeforcer.added (contest_name, guild_id)'\
                        'VALUES (%s, %s)',
                        (
                            contest['name'],
                            guild.id
                        )
                    )
                    
                    cnx.commit()

class Background(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    background = SlashCommandGroup('background', 'Group of commands for background tasks',)
    
    @commands.Cog.listener()
    async def on_ready(self):
        with config.Connect() as cnx:
            cursor = cnx.cursor(buffered=True)

            cursor.execute(
                'SELECT guild_id FROM guild_subscribers'
            )

            for rows in cursor:
                guild_checks.append(int(rows[0]))
                guildObj.append(self.bot.get_guild(int(rows[0])))

        print("DLU READY")
        while True:
            url = "https://codeforces.com/api/contest.list"
            c,e = fetch(url)

            if c['status'] == "OK" and not e:
                for i in c["result"]:
                    status = i["phase"]

                    contest = {
                        'id' : i['id'],
                        'name' : i['name'],
                        'start' : i['startTimeSeconds'],
                        'before_start' : i['relativeTimeSeconds'],
                        'des' : i['type'],
                        'dura' : (i['durationSeconds']/60/60)
                    }

                    if(status == "BEFORE" and contest['id'] not in ids):
                        print(f"{contest['name']} added to archive")

                        archive.append(contest)
                        ids.append(contest['id'])
                        
                    elif(contest in archive and status == "FINISHED"):
                        archive.remove(contest)
            
            for contest in archive:
                await contest_scheduler(contest)

            await asyncio.sleep(check_pause)

    @background.command(
        description="Start background update"
    )
    @commands.cooldown(2, cd, commands.BucketType.user)
    async def check_contest(self,ctx):  
        with config.Connect() as cnx:
            cursor = cnx.cursor(buffered=True)

            if ctx.guild.id not in guild_checks:
                await ctx.respond("`Background scanning ON`")

                cursor.execute(
                    'INSERT INTO codeforcer.guild_subscribers (guild_id)'\
                    'VALUES (%s)',
                    (
                        ctx.guild.id,
                    )
                )
                
                cnx.commit()

                guildObj.append(self.bot.get_guild(int(ctx.guild.id)))
                guild_checks.append(ctx.guild.id)

            else:
                await ctx.respond("`Background scanning OFF`")

                cursor.execute(
                    'DELETE FROM guild_subscribers WHERE guild_id=%s',
                    (
                        ctx.guild.id,
                    )
                )

                cnx.commit()

                guildObj.remove(self.bot.get_guild(int(ctx.guild.id)))
                guild_checks.remove(ctx.guild.id)

#--------------------------------------------------------------------#

    @commands.Cog.listener()
    async def on_connect(self):
        print("LSU READY")
        while(True):
            handles = []
            discord_id = []
            
            with config.Connect() as cnx:
                cursor = cnx.cursor()

                cursor.execute(
                    'SELECT discord_id, cf_handle from creds'
                )

                for rows in cursor:
                    discord_id.append(rows[0])
                    handles.append(rows[1])
                
                cursor.execute(
                    'SELECT * from solves_subscribers'
                )

                for rows in cursor:
                    subscribers.append(rows)

            updated = []

            for s in subscribers:
                s_dis = s[0]

                if s_dis in discord_id and s_dis not in updated:
                    cf = handles[discord_id.index(s_dis)]

                    url = f"https://codeforces.com/api/user.status?handle={cf}&from=1&count=1"
                    c,e = fetch(url)

                    if c["status"] == "OK" and not e:
                        for i in c["result"]:
                            if "verdict" in i and i["verdict"] == "OK":
                                id = i['problem']['name']
                                
                                for l in subscribers:
                                    if l[0] == s_dis:
                                        c_id = int(l[1])
                                        channel = self.bot.get_channel(c_id)
                                        ac = str(cf) + "-" + str(id) + "-" + str(c_id)

                                        if ac not in solved and (time.time() - i['creationTimeSeconds'] < 30):
                                            print(f"Live updating for {s_dis} - {cf} in channel {c_id}")
                                            await channel.send(f"`[{s_dis}]` just solved `{id}` {emo['tick']}")

                                            solved.append(ac)

                    updated.append(s_dis)

            updated.clear()
            await asyncio.sleep(live_pause)

    @background.command(
        description="Start solve updates"
    )
    @commands.cooldown(2, cd, commands.BucketType.user)
    async def solves_updater(
        self,
        ctx,
        choice: 
        discord.Option(
            str,
            "Subscribe to live updates for your solves? (y/n)",
            default = "y"
        ),
    ):  
        flag = False

        with config.Connect() as cnx:
            cursor = cnx.cursor(buffered=True)

            cursor.execute(
                'SELECT discord_id from solves_subscribers WHERE discord_id=%s and channel_id=%s',
                (
                    ctx.author.name,
                    ctx.channel.id
                )
            )

            for rows in cursor:
                flag = True
                break

            if choice == 'y':
                if flag:
                    await ctx.respond("`Already checking ur solves`", ephemeral = True)
                else:
                    await ctx.respond(f"Enabling live solves update for `[{ctx.author.name}]`", ephemeral = True)
                    cursor.execute(
                        'INSERT INTO codeforcer.solves_subscribers (discord_id, channel_id)'\
                        'VALUES (%s, %s)',
                        (
                            ctx.author.name,
                            ctx.channel.id
                        )
                    )

                    cnx.commit()

            elif choice == 'n':
                if flag:
                    await ctx.respond(f"`[{ctx.author.name}]` have disabled live solve update", ephemeral = True)
                    cursor.execute(
                        'DELETE FROM solves_subscribers WHERE discord_id=%s and channel_id=%s;',
                        (
                            ctx.author.name,
                            ctx.channel.id
                        )
                    )

                    cnx.commit()

                else:
                    await ctx.respond(f"`You have not enabled live solve update` {emo['x']}", ephemeral = True)
            else:
                await ctx.respond("Please use `'y'` or `'n'` as slash command parameter", ephemeral = True)

#--------------------------------------------------------------------#

    @check_contest.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, discord.errors.ApplicationCommandInvokeError):
            await ctx.respond(f'This command is on cooldown, you can use it in {cd}s', ephemeral=True)

    @solves_updater.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, discord.errors.ApplicationCommandInvokeError):
            await ctx.respond(f'This command is on cooldown, you can use it in {cd}s', ephemeral=True)

def setup(bot):
    bot.add_cog(Background(bot))

