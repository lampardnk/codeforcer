import os
import sys
import discord
from discord.ext import commands

from config import emo

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(
    case_insensitive=True,
    description="codeforcer - Codeforces contests reminder",
    command_prefix='$',
    intents=intents
)

dir = "cogs."

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        name = "codeforcer | $help",
        type=discord.ActivityType.playing
        
        )
    )

@bot.command(name='reload')
async def reload(ctx, module : str):
    if ctx.author.name == '0xlampardNK':
        print(f"reloading {module}")
        try:
            bot.unload_extension(f"{dir}{module}")
            bot.load_extension(f"{dir}{module}")
        except Exception as e:
            await ctx.send(emo['pistol'])
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(emo['ok'])   
    else:
        print("not onwer, cant use command")

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title = "codeforcer", 
        url = "https://github.com/lampardnk/codeforcer/blob/master/README.md", 
        color = discord.Color.blue()
    )

    embed.add_field(
        name = "/contest list", 
        value = "Return an embed with a list of upcoming Codeforces contests", 
        inline = False
    )

    embed.add_field(
        name = "/contest summary {contest_id}", 
        value = "Return a summary of the channel members results in a contest", 
        inline = False
    )

    embed.add_field(
        name = "/contest signup", 
        value = "Sign up for ALL Codeforces contests (that are open for register) on codeforces.com itself, using the handle that you logged in with", 
        inline = False
    )

    embed.add_field(
        name = "/background check_contest", 
        value = "Can be toggled. Check Codeforces API for all upcoming contests and create discord events for them", 
        inline = False
    )

    embed.add_field(
        name = "/background solves_updater {y/n}", 
        value = "Can be toggled. Sends a message to the channel the command was used in whenever command user solved a problem", 
        inline = False
    )

    embed.set_footer(text="Contact me through Discord if you need help: 0xlampardNK#2683")

    await ctx.reply(
        embed=embed
    )

if __name__ == "__main__":
    bot.load_extension(f"{dir}login")
    bot.load_extension(f"{dir}background")
    bot.load_extension(f"{dir}contests")

    key = os.getenv("BOT_TOKEN")
    bot.run(key)
