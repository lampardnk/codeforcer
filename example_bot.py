# import requests
# import getpass
# from bs4 import BeautifulSoup as bs

# base = "http://m1.codeforces.com"
# cf_enter = "{base}/{login}".format(base=base, login="enter")

# cliente = requests.session()
# r = cliente.get(cf_enter)
# html = r.content
# soup = bs(html)
# head = soup.head
# meta = head.findChildren('meta')
# csrf_token = [
#     m for m in meta if 'name' in m.attrs and m['name'] == 'X-Csrf-Token']
# csrf_token = csrf_token[0]["content"]

# print(csrf_token) # it's working, :)

# user = input('User:')
# password = getpass.getpass('Password:')

# login_data = {
#     'csrf_token': csrf_token,
#     'action': 'enter',
#     'handle': user,
#     'password': password,
# }

# headers = {
#     'Referer': cf_enter,
#     'User-agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
# }

# r = cliente.post(cf_enter, data=login_data, headers=headers)
# print(r.status_code)
# if r.status_code != 200:
#     print('fail to connect')

import asyncio
import discord
import os
import requests
import json
from discord.ext import tasks, commands
from datetime import datetime, timedelta

bot = discord.Bot()

testingServer = ['859772204812206080']
contests_name = []
contests_info = []
archive = []

first_time = True


@bot.slash_command(guild_ids = testingServer, description="Return list of upcoming codeforces contests" )
async def contests(ctx):
    embed = discord.Embed(title = "CodeForces Contests", url = "https://codeforces.com/contests", color = 0xFF5733)

    response = requests.get("https://codeforces.com/api/contest.list")

    if response.status_code == 200:
        print("Connected to CF API")
    else:
        print("Can't connect to CF API")

    c = response.content
    c = json.loads(c)

    for i in c["result"]:
        if(i["phase"] == "BEFORE"):
            ts = int(i['startTimeSeconds'])
            days = int(i['relativeTimeSeconds']/60/-60/24)
            minutes = int(((i['relativeTimeSeconds']*-1) - (days*60*60*24))/60/60)

            contests_name.append(i['name'])
            contests_info.append((datetime.utcfromtimestamp(ts) + timedelta(hours=8)).strftime('%d-%m-%Y %H:%M') + "\n" + "Starting in " + str(days) + " days " + str(minutes) + " hours" + "\n\n")

        else:
            break

    print(f"Received contest-req from {ctx.author.name}")

    contests_info.reverse()
    contests_name.reverse()

    for i in range(0,len(contests_name)):
        embed.add_field(name = contests_name[i], value = contests_info[i], inline = False)

    embed.set_footer(text="Good luck have fun!")
    embed.set_thumbnail(url="https://res.cloudinary.com/practicaldev/image/fetch/s--mzwvoucO--/c_imagga_scale,f_auto,fl_progressive,h_1080,q_auto,w_1080/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cer3l19eex0wy900b101.jpg")

    await ctx.respond(embed=embed)
    contests_name.clear()
    contests_info.clear()

# @bot.slash_command(guild_ids = testingServer, description="Create event list for upcoming codeforces contests")
async def check_contest(ctx):
    global first_time
    
    if first_time == True:
        await ctx.respond("Performing 1st time set up")
        first_time = False

        while True:

            await ctx.send("Daily check")
            response = requests.get("https://codeforces.com/api/contest.list")

            c = response.content
            c = json.loads(c)

            if response.status_code == 200:
                print("Connected to CF API for 3-day update")
            else:
                print("Can't connect to CF API for 3-day update")

            for i in c["result"]:
                if(i["phase"] == "BEFORE" and i['name'] not in archive):
                    await ctx.send("Adding " + i['name'])
                    
                    ts = int(i['startTimeSeconds'])
                    des = "Suitable for MMR < 1599" if "Div. 2" in i['name'] else "Suitable for tourists"
                    des = "Suitable for monkeys" if "Div. 3" in i['name'] else des

                    await ctx.guild.create_scheduled_event(name = i['name'], description = des, start_time = (datetime.utcfromtimestamp(ts)), end_time = (datetime.utcfromtimestamp(ts) + timedelta(hours = (i['durationSeconds']/60/60))),location = "https://codeforces.com/contests")
                    archive.append(i['name'])
                
                else:
                    break

            await asyncio.sleep(86400.0)
    else:
        await ctx.respond("Set up has been performed")

@bot.slash_command(guild_ids = testingServer, description="Set up" )
async def setup(ctx):
    bot.loop.create_task(check_contest(ctx))

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    

key = os.getenv("BOT_TOKEN")

bot.run(key)