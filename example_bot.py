import os
os.system("cd pycord-master")
os.system("pip install -U .")

import discord

bot = discord.Bot()

testingServer = ['859772204812206080']

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids = testingServer, description="blabla" )
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")
    print(f"Received hello-req from {ctx.author.name}")

bot.run("OTQ5MTk0NDEyOTM4ODg3MTg5.YiG0Lw.x6q-diEuCi_M1BDcmhN3gmYFxeQ")

# import requests

# response = requests.get("https://codeforces.com/api/contest.list")
# print(response.status_code)

