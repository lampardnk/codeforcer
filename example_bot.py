import asyncio
import discord
import os
import requests
import json
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import requests


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
    else:
        print("Can't connect to CF API")

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
                (datetime.utcfromtimestamp(ts) + timedelta(hours=8)).strftime('%d-%m-%Y %H:%M') + "\n" 
                + str(dura) + " hour long " + des + " contest" + "\n"
                + "> Starting in " + str(str(days) + " days " + str(minutes) + " hours") + "\n\n"
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

async def check_contest(ctx):
    while True:

        await ctx.send("Daily check")
        response = requests.get("https://codeforces.com/api/contest.list")

        c = response.content
        c = json.loads(c)

        if response.status_code == 200:
            print("Connected to CF API for daily update")
        else:
            print("Can't connect to CF API for daily update")

        for i in c["result"]:

            name = i['name']
            status = i["phase"]
            start = int(i['startTimeSeconds'])
            before_start = i['relativeTimeSeconds']
            des = i['type']
            dura = (i['durationSeconds']/60/60)

            if(status == "BEFORE" and name not in archive):
                await ctx.send("Adding " + name)
                
                ts = start

                await ctx.guild.create_scheduled_event(
                    name = name, 
                    description = str(dura) + " hour long " + des + " contest", 
                    start_time = (datetime.utcfromtimestamp(ts)), 
                    end_time = (datetime.utcfromtimestamp(ts) + timedelta(hours = dura)),
                    location = f"https://codeforces.com/contests/{i['id']}"
                )

                archive.append(name)
            
            else:
                break

        await asyncio.sleep(86400.0)

@bot.slash_command(
    guild_ids = testingServer, 
    description="Set up" 
)
async def setup(ctx):
    global first_time
    
    if first_time == True:
        await ctx.respond("Performing 1st time set up")
        first_time = False
        bot.loop.create_task(check_contest(ctx))
    else:
        await ctx.respond("Set up has been performed")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    

key = os.getenv("BOT_TOKEN")

bot.run(key)
