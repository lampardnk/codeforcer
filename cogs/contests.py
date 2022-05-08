from time import sleep
from discord import Option
import discord
from discord.ext import commands
import datetime
from datetime import datetime, timedelta
from discord.commands import SlashCommandGroup
import sys 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

import config
from config import logo, emo, fetch

class Contests(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    contests = SlashCommandGroup('contests', 'Group of commands relating to contests')

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

        url = "https://codeforces.com/api/contest.list"

        c,e = fetch(url)

        if c["status"] == "OK" and not e:

            for i in c["result"]:
                
                id = i['id']
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

                    contests_name.append(f"[{id}] {name}")
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

            await ctx.respond(embed=embed, ephemeral = True)
            
            contests_name.clear()
            contests_info.clear()
        
    @contests.command(
        description="Post-contest summary of logged in users in the channel"
    )
    async def summary(self,ctx, contest_id : Option(int, "Enter contest id")):
        m_list = ctx.channel.members
        dis_users = []
        table = []
        h = ""
        r = ""
        pts = ""

        for member in m_list:
            dis_users.append(member.name)

        cf = ""

        with config.Connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute(
                'SELECT discord_id, cf_handle from creds'
            )

            tmp = []
            for lines in cursor:
                dis = lines[0]
                hand = lines[1]
                if dis in dis_users and hand not in tmp:
                    cf += hand + ";"
                    tmp.append(hand)
        
        c,e = fetch(f"https://codeforces.com/api/contest.standings?contestId={contest_id}&handles={cf[:-1]}&showUnofficial=false")
        
        if e:
            await ctx.respond("Contest not found, please try again", ephemeral = True)
        else:
            embed = discord.Embed(
                title = f"Summary for contest #{contest_id}",
                url = f"https://codeforces.com/contest/{contest_id}/standings",
                color = discord.Color.blue()
            )
            
            try:
                for parties in c['result']['rows']:
                    class player:
                        handle = parties['party']['members'][0]['handle']
                        rank =  parties['rank']
                        points = parties['points']
                    
                    table.append(player())
                
                if (len(table) == 0):
                    await ctx.respond(f"No logged-in users participated in contest #{contest_id} {emo['cry']}", ephemeral = True)
                else:
                    table.sort(key = lambda x: x.rank)

                    for p in table:
                        h += " | " + str(p.handle) + "\n"
                        r += str(p.rank) + "\n"
                        pts += " | " + str(p.points) + "\n"

                    embed.add_field(
                        name = 'Rank',
                        value = r,
                        inline = True
                    )

                    embed.add_field(
                        name = '| Handle',
                        value = h,
                        inline = True
                    )

                    embed.add_field(
                        name = '| Points',
                        value = pts,
                        inline = True
                    )

                    await ctx.respond(embed=embed, ephemeral = True)
            except:
                await ctx.respond("Contest not found, please try again", ephemeral = True)
                print(sys.exc_info())
            
    @contests.command(
        description="Register for ALL codeforces contests with handle"
    )
    async def signup(self,ctx,contest_id : Option(int, "Enter contest id", default = -1)):
        def login():
            password=lines[2]
            
            handle_elem = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.NAME, "handleOrEmail"))
            )
            handle_elem.send_keys(handle)
            driver.find_element_by_name('password').send_keys(password)
            driver.find_element_by_class_name('submit').submit()
            sleep(5)
            elem = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.lang-chooser"))
            )
            if handle in elem.text:
                return

        def single_singup(ctx, contest):
            url = "https://codeforces.com/contestRegistration/" + str(contest['id'])
            print(url)
            driver.get(url)
            if "Login" in driver.title:
                login()
                sleep(5)

            if "Register" in driver.title:
                try:
                    reg = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.submit"))
                    )
                    reg.submit()
                    sleep(5)
                    reg = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.lang-chooser"))
                    )
                    await ctx.send(f"{emo['tick']} Registered {ctx.author.name} for contest {contest_id}")

                except NoSuchElementException:
                    await ctx.send(f"{emo['x']} Can not register {ctx.author.name} for contest {contest_id}")
                    pass
                

        await ctx.respond("Registered, please check https://codeforces.com/contests to confirm", ephemeral = True)

        with config.Connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute(
                'SELECT * from creds'
            )
            
            for lines in cursor:
                if lines[0] == ctx.author.name:
                    handle = lines[1]
                    wait_time = 10

                    options = Options()
                    options.headless = True
                    driver = webdriver.Firefox(options=options)

                    # driver = webdriver.Firefox()

                    c,e = fetch("https://codeforces.com/api/contest.list")                    
                    if e == False: 
                        if contest_id == -1:
                            for contest in c['result']:
                                if contest['phase'] == "BEFORE":
                                    single_singup(ctx,contest)

                                else:
                                    print("All done")
                                    driver.quit()
                                    break
                        else:
                            for contest in c['result']:
                                if int(contest['id']) == contest_id:
                                    single_singup(ctx,contest)
                                    print("All done")
                                    driver.quit()
                                    break
                                     
                    else:
                        print("Error")
                        driver.quit()
                        
                        
def setup(bot):
    bot.add_cog(Contests(bot))
