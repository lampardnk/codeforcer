import asyncio
import discord
import os
import requests
import json
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import sys

bot = discord.Bot()

first_time = True

testingServer = ['859772204812206080']
contests_name = []
contests_info = []
archive = []

handles = []
link = []
passwords = []

logo = "https://bit.ly/cf-logo-dis"

@bot.slash_command(
    guild_ids = testingServer, 
    description="Return list of upcoming codeforces contests" 
)
async def contests(ctx):
    embed = discord.Embed(
        title = "CodeForces Contests", 
        url = "https://codeforces.com/contests", 
        color = discord.Color.red()
    )

    response = requests.get("https://codeforces.com/api/contest.list")

    if response.status_code == 200:
        print("Connected to CF API")
        try:

            c = response.content
            c = json.loads(c)
            for i in c["result"]:

                name = i['name']
                status = i["phase"]
                start = int(i['startTimeSeconds'])
                before_start = i['relativeTimeSeconds']
                des = i['type']
                dura = (i['durationSeconds']/60/60)
                
                if(status == "BEFORE"):
                    ts = start
                    days = int(before_start/60/-60/24)
                    minutes = int(((before_start*-1) - (days*60*60*24))/60/60)

                    contests_name.append(name)
                    contests_info.append(
                        "`" + (datetime.utcfromtimestamp(ts) + timedelta(hours=8)).strftime('%d-%m-%Y   %H:%M') + " | " 
                        + str(dura) + " hour " + des + " contest`" + "\n" 
                        + "> Starting in __**" + str(str(days) + " days " + str(minutes) + " hours**__") + "\n\n"
                    )

                else:
                    break

            print(f"Received contest-req from {ctx.author.name}")

            contests_info.reverse()
            contests_name.reverse()

            for i in range(0,len(contests_name)):
                embed.add_field(
                    name = contests_name[i], 
                    value = contests_info[i], 
                    inline = False
                )

            embed.set_footer(text="Good luck have fun!")

            embed.set_thumbnail(
                url = logo
            )

            await ctx.respond(embed=embed)
            contests_name.clear()
            contests_info.clear()

        except:
            print(f"{log_time} Errors encountered")
            print(sys.exc_info()[0])
            pass

    else:
        print("Can't connect to CF API")
        await ctx.respond("CF API down, please try again later")

async def check_contest(
    ctx,
    update_interval,
    notify_before
):

    while True:
        log_time = datetime.now()

        try:
            response = requests.get("https://codeforces.com/api/contest.list")

            if response.status_code == 200:
                print(f"{log_time} Connected to CF API for daily update")

                c = response.content
                c = json.loads(c)

                for i in c["result"]:

                    name = i['name']
                    status = i["phase"]
                    start = int(i['startTimeSeconds'])
                    before_start = i['relativeTimeSeconds']
                    des = i['type']
                    dura = (i['durationSeconds']/60/60)

                    if(status == "BEFORE" and name not in archive):
                        await ctx.send("Added " + name)
                
                        ts = start

                        await ctx.guild.create_scheduled_event(
                            name = name, 
                            description = str(dura) + " hour " + des + " contest", 
                            start_time = (datetime.utcfromtimestamp(ts - notify_before)), 
                            end_time = (datetime.utcfromtimestamp(ts) + timedelta(hours = dura)),
                            location = f"https://codeforces.com/contests/{i['id']}"
                        )

                        archive.append(name)
            
                    else:
                        break

            else:
                print(f"{log_time} Can't connect to CF API for contest update")

        except:
            print(f"{log_time} Errors encountered")
            print(sys.exc_info()[0])
            pass

        await asyncio.sleep(update_interval)

@bot.slash_command(
    guild_ids = testingServer, 
    description="Set up" 
)
async def setup(
    ctx: discord.ApplicationContext,

    update_interval: 
    discord.Option(int, "Enter your preferred rate of update (seconds)",min_value=10, max_value=60, default=10),

    notify_before: 
    discord.Option(int, "Notify events before start (seconds)", min_value=0, max_value=3600, default=1800)
):

    global first_time
    
    if first_time == True:
        await ctx.respond("Performing 1st time set up")

        first_time = False
        bot.loop.create_task(check_contest(ctx,update_interval,notify_before))
    else:
        await ctx.respond("Set up has been performed")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")   
    

key = os.getenv("BOT_TOKEN")

bot.run(key)