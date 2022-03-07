import discord
import os
import requests
import json
from datetime import datetime

bot = discord.Bot()

testingServer = ['859772204812206080']
contests_name = []
contests_info = []


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids = testingServer, description="give cf contest list" )
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

key = os.getenv("BOT_TOKEN")

bot.run(key)