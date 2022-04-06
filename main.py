import os
import discord
from discord.ext import commands

from config import emo

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(
    case_insensitive=True,
    description="codeforcer - Codeforces contests reminder",
    command_prefix='$',
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name='reload')
async def reload(ctx, module : str):
    if ctx.author.name == '0xlampardNK':
        print(f"reloading {module}")
        try:
            bot.unload_extension(module)
            bot.load_extension(module)
        except Exception as e:
            await ctx.send(emo['pistol'])
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(emo['ok'])   
    else:
        print("not onwer, cant use command")

if __name__ == "__main__":
    bot.load_extension("cogs.login")
    bot.load_extension("cogs.background")
    bot.load_extension("cogs.contests")

    key = os.getenv("BOT_TOKEN")
    bot.run(key)
