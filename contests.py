import discord
import requests
import json
from discord.ext import commands
import datetime
from datetime import datetime, timedelta, timezone
import sys
from discord.commands import SlashCommandGroup

from main import testingServer, logo

class Contests(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    contests = SlashCommandGroup('contests', 'Group of commands relating to contests', guild_ids=testingServer)

    @contests.command(
        description="Return codeforces contest list"
    )
    async def list(self,ctx):
        contests_name = []
        contests_info = []

        embed = discord.Embed(
            title = "CodeForces Contests", 
            url = "https://codeforces.com/contests", 
            color = discord.Color.red()
        )

        log_time = datetime.now()
        log_time.replace(tzinfo=timezone.utc)

        try:
            response = requests.get("https://codeforces.com/api/contest.list")
            
            if response.status_code == 200:
                print("Connected to CF API")
            else:
                print("Can't connect to CF API")
                await ctx.respond("CF API down, please try again later")
                raise Exception()

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

def setup(bot):
    bot.add_cog(Contests(bot))
