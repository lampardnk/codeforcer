import asyncio
from unicodedata import name
import requests
import json
from discord.ext import commands
import datetime
from datetime import datetime, timedelta
import sys
import discord
from discord.commands import SlashCommandGroup
import asyncio
import pytz

from main import testingServer

class Background(commands.Cog):
    global archive
    global done_setup
    global solved
    global tmp

    solved = []
    archive = []
    done_setup = []
    tmp = []

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    background = SlashCommandGroup('background', 'Group of commands for background tasks', guild_ids=testingServer)

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            log_time = datetime.now(pytz.timezone('Asia/Singapore'))

            try:
                response = requests.get("https://codeforces.com/api/contest.list")

                if response.status_code == 200:
                    print(f"{log_time} Connected to CF API for daily update")

                    c = response.content
                    c = json.loads(c)

                    if c["status"] == "OK":
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

                            if(status == "BEFORE" and contest not in archive):
                                archive.append(contest)
                            
                            elif(contest in archive and status == "FINISHED"):
                                archive.remove(contest)

                    else:
                        print(f"{log_time} JSON Error - Status code {response.status_code} but can't load JSON")
                else:
                    print(f"{log_time} CF API req returned {response.status_code}")

            except:
                print(f"{log_time} Errors encountered")
                print(sys.exc_info()[0])
                pass

            await asyncio.sleep(30)

    @background.command(
        description="Start background update"
    )

    async def check_contest(self,ctx):  
        if ctx.guild.id not in done_setup:
            await ctx.respond("`Background scanning ON`")
            done_setup.append(ctx.guild.id)
            tmp = []

            while True:
                for contest in archive:
                    unique = f"{contest['name']}+{ctx.guild.id}"

                    if unique not in tmp:
                        ts = contest['start']

                        await ctx.guild.create_scheduled_event(
                            name = contest['name'], 
                            description = str(str(contest['dura']) + " hour " + contest['des']) + " contest", 
                            start_time = (datetime.utcfromtimestamp(ts - 1800)), 
                            end_time = (datetime.utcfromtimestamp(ts) + timedelta(hours = contest['dura'])),
                            location = f"https://codeforces.com/contests/{contest['id']}"
                        )

                        tmp.append(unique)

                await asyncio.sleep(10)
        else:
            await ctx.respond("`Already scanning`")

    @background.command(
        description="Start solve updates"
    )

    async def solves_updater(
        self,
        ctx,
        choice: 
        discord.Option(
            str,
            "Turn on live update for your solves?(y/n)"
        ),
    ):  
        sender = ctx.author.name

        if choice == "y":
            if sender in done_setup:
                await ctx.respond("`Already checking ur solves`")
            else:
                await ctx.respond("`Enabling live solves update`")
                done_setup.append(sender)

                while(True):
                    global handles
                    global discord_id
                    
                    handles = []
                    discord_id = []
                    
                    with open('creds.txt', 'r') as f:
                        for line in f:
                            a = []
                            a = line.split()
                            handles.append(a[2])
                            discord_id.append(a[0])

                    f.close()
                    print(discord_id)
                    print(handles)

                    if sender in done_setup:
                        log_time = datetime.now(pytz.timezone('Asia/Singapore'))

                        try:
                            h = handles[discord_id.index(sender)]
                            print(f"Updating for {sender} : {h}")

                            response = requests.get(f"https://codeforces.com/api/user.status?handle={h}&from=1&count=100")

                            if response.status_code == 200:
                                c = response.content
                                c = json.loads(c)

                                if c["status"] == "OK":
                                    for i in c["result"]:
                                        if "verdict" in i and i["verdict"] == "OK":
                                            id = i['problem']['name']
                                            ac = sender + "-" + id
                                            
                                            if ac not in solved:
                                                solved.append(ac)
                                                await ctx.send(f"{sender} solved problem `{id}`")

                                else:
                                    print(f"{log_time} JSON Error - Status code {response.status_code} but can't load JSON")
                            else:
                                print(f"{log_time} CF API req returned {response.status_code}")

                        except:
                            await ctx.respond(f"Please `DM` the bot with `$login cf_handle cf_password`")
                            print(f"{log_time} Errors encountered")
                            print(sys.exc_info()[0])
                            break

                        await asyncio.sleep(10)
                    else:
                        break
        else:
            if sender in done_setup:
                done_setup.remove(sender)
            else:
                await ctx.respond("`You have not enabled live solve update`")

def setup(bot):
    bot.add_cog(Background(bot))
