from discord.ext import commands
import requests
import datetime
from datetime import datetime, timezone
import sys
from bs4 import BeautifulSoup

import config
from config import emo

async def link(ctx,username,password):
    await ctx.reply("Processing")
    try:
        log_time = datetime.now()
        log_time.replace(tzinfo=timezone.utc)
        sender = ctx.author.name
        
        base = "https://codeforces.com"
        service_url = "{base}/{login}".format(base=base, login="enter")

        s = requests.session()
        dt = s.get(service_url)
        dt = dt.text
        ss = BeautifulSoup(dt, 'html.parser')
        csrf_token = ss.find_all("span", {"class": "csrf-token"})[0]["data-csrf"]
        # print(csrf_token)

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

            if sender not in discord_id:
                handles.append(username)
                discord_id.append(sender)

                await ctx.reply(f"Logged in successfully, welcome {username} {emo['tick']}")

                with config.Connect() as cnx:
                    cursor = cnx.cursor()

                    cursor.execute(
                        'INSERT INTO creds (discord_id, cf_handle, cf_password)'\
                        'VALUES (%s, %s, %s)',
                        (
                            sender,
                            username,
                            password
                        ),
                    )

                    cnx.commit()
            else:
                handles[discord_id.index(sender)] = username

                await ctx.reply(f"Handle updated successfully to {username} {emo['tick']}")

                with config.Connect() as cnx:
                    cursor = cnx.cursor()

                    cursor.execute(
                        'UPDATE codeforcer.creds'\
                        'SET (cf_handle, cf_password)'\
                        'VALUES (%s, %s)'
                        'WHERE discord_id=%s',
                        (
                            username,
                            password,
                            sender
                        ),
                    )

                    cnx.commit()
                
            print(f"Updated creds: \n{discord_id}\n{handles}")

        else:
            raise Exception

    except:
        print(f"{log_time} Login error encountered")
        print(sys.exc_info())
        print(f"Received {username} and {password}")

        await ctx.reply(f"Login unsuccessful, please retry later {emo['x']}")
        pass

class Login(commands.Cog):
    global handles
    global discord_id

    handles = []
    discord_id = []

    with config.Connect() as cnx:
        cursor = cnx.cursor()

        cursor.execute(
            'SELECT discord_id, cf_handle from creds'
        )

        for rows in cursor:
            discord_id.append(str(rows[0]))
            handles.append(str(rows[1]))
        
        print(f"Fetched creds: \n{discord_id}\n{handles}")

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="login")
    async def login(self,ctx):
        creds = ctx.message.content.split()
        await link(
            ctx,        
            str(creds[1]),  #username
            str(creds[2])   #password
        )

def setup(bot):
    bot.add_cog(Login(bot))