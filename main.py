import discord
import os

import requests
import datetime
from datetime import datetime, timezone
import sys
from discord.ext import commands
from bs4 import BeautifulSoup

bot = discord.Bot(
    case_insensitive=True,
    description="codeforcer - Codeforces contests manager",
)
testingServer = ['859772204812206080','951052594078433351']
logo = "https://bit.ly/cf-logo-dis"

global handles
global discord_id

handles = []
discord_id = []

async def link(ctx,username,password):
    await ctx.reply("Processing")
    try:
        log_time = datetime.now()
        log_time.replace(tzinfo=timezone.utc)
        
        if username not in handles and ctx.author not in discord_id:
            base = "https://codeforces.com"
            service_url = "{base}/{login}".format(base=base, login="enter")

            s = requests.session()
            dt = s.get(service_url)
            dt = dt.text
            ss = BeautifulSoup(dt, 'html.parser')
            csrf_token = ss.find_all("span", {"class": "csrf-token"})[0]["data-csrf"]
            print(csrf_token)

            headers = {
                'X-Csrf-Token': csrf_token
            }
            payload = {
                'csrf_token': csrf_token,
                'action': 'enter',
                'handleOrEmail': username,
                'password': password,
            }
            data = s.post(service_url, data=payload, headers=headers)
            data = data.text
            soup = BeautifulSoup(data, 'html.parser')

            logout = soup.select_one("a[href*=logout]")["href"]
            data = s.get(base + logout)

            if(data.status_code == 200):
                    handles.append(username)
                    discord_id.append(ctx.author)
                    await ctx.reply(f"Login successfully, welcome {username}")
            else:
                raise Exception
        else:
            await ctx.reply(f"You have already been linked to {username}")

    except:
        print(f"{log_time} Login error encountered")
        print(sys.exc_info())
        print(f"Received {username} and {password}")

        await ctx.reply(f"Login unsuccessful, please retry")
        pass

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")   

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$login'):
        creds = message.content.split()
        await link(message,str(creds[1]),str(creds[2]))

if __name__ == "__main__":
    bot.load_extension("background")
    bot.load_extension("contests")

    key = os.getenv("BOT_TOKEN")
    bot.run(key)
