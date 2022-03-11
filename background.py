import asyncio
import requests
import json
from discord.ext import commands
import datetime
from datetime import datetime, timedelta, timezone
import sys
import discord
from discord.commands import SlashCommandGroup
import asyncio

from main import testingServer

class Background(commands.Cog):
    global archive
    global done_setup
    archive = []
    done_setup = []

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    background = SlashCommandGroup('background', 'Group of commands for background tasks', guild_ids=testingServer)

    @background.command(
        description="Start background update"
    )

    async def check_contest(
    self,

    ctx,

    update_interval: 
    discord.Option(
        int, 
        "Enter your preferred rate of update (seconds)",
        min_value=10, max_value=60, default=30
    ),

    notify_before:
    discord.Option(
        int, 
        "Notify events before start (seconds)",
        min_value=0, max_value=3600, default=1800
    )
    ):  
        if ctx.guild.id not in done_setup:
            await ctx.respond("`Background scanning ON`")
            done_setup.append(ctx.guild.id)
            
            while True:
                log_time = datetime.now()
                log_time.replace(tzinfo=timezone.utc)

                try:
                    response = requests.get("https://codeforces.com/api/contest.list")

                    if response.status_code == 200:
                        print(f"{log_time} Connected to CF API for daily update")

                        c = response.content
                        c = json.loads(c)

                        for i in c["result"]:
                            
                            id = i['id']
                            name = i['name']
                            status = i["phase"]
                            start = int(i['startTimeSeconds'])
                            before_start = i['relativeTimeSeconds']
                            des = i['type']
                            dura = (i['durationSeconds']/60/60)
                            contest = (str(ctx.guild.id) + str(id))

                            if(status == "BEFORE" and contest not in archive):
                                await ctx.send("Added " + name)
                        
                                ts = start

                                await ctx.guild.create_scheduled_event(
                                    name = name, 
                                    description = str(dura) + " hour " + des + " contest", 
                                    start_time = (datetime.utcfromtimestamp(ts - notify_before)), 
                                    end_time = (datetime.utcfromtimestamp(ts) + timedelta(hours = dura)),
                                    location = f"https://codeforces.com/contests/{i['id']}"
                                )

                                archive.append(contest)
                            
                            elif(contest in archive and status == "FINISHED"):
                                archive.remove(contest)
                    
                            else:
                                break

                    else:
                        print(f"{log_time} Can't connect to CF API for contest update")

                except:
                    print(f"{log_time} Errors encountered")
                    print(sys.exc_info()[0])
                    pass

                await asyncio.sleep(update_interval)
        
        else:
            await ctx.respond("`Already scanning`")

def setup(bot):
    bot.add_cog(Background(bot))
