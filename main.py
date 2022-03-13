import discord
import os

bot = discord.Bot(
    case_insensitive=True,
    description="codeforcer - Codeforces contests manager",
)
testingServer = ['859772204812206080','951052594078433351']
logo = "https://bit.ly/cf-logo-dis"
guildObj = []

for i in testingServer:
    guildObj.append(bot.get_guild(i))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")   

if __name__ == "__main__":
    bot.load_extension("background")
    bot.load_extension("contests")
    bot.load_extension("login")

    key = os.getenv("BOT_TOKEN")
    bot.run(key)
