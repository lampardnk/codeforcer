from discord.ext import commands
import requests
import datetime
from datetime import datetime, timezone
import sys
from bs4 import BeautifulSoup

async def link(ctx,username,password):
    await ctx.reply("Processing")
    try:
        log_time = datetime.now()
        log_time.replace(tzinfo=timezone.utc)
        sender = ctx.author.name
        
        if sender not in discord_id:
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
                    
                    discord_id.append(sender)

                    await ctx.reply(f"Login successfully, welcome {username}")
                    with open('creds.txt', 'w') as f:
                        for item in handles:
                            f.write(f"{discord_id[handles.index(item)]} - {item}")

                    f.close()
            else:
                raise Exception
        else:
            print(discord_id)
            await ctx.reply(f"Can only link to one CF handle per discord user")

    except:
        print(f"{log_time} Login error encountered")
        print(sys.exc_info())
        print(f"Received {username} and {password}")

        await ctx.reply(f"Login unsuccessful, please retry later")
        pass

class Login(commands.Cog):
    global handles
    global discord_id

    handles = []
    discord_id = []
    passwords = []

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content.startswith('$login'):
            creds = message.content.split()
            await link(
                message,        
                str(creds[1]),  #username
                str(creds[2])   #password
            )

def setup(bot):
    bot.add_cog(Login(bot))