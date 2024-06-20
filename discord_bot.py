import discord
from discord.ext import tasks, commands
import logging

logging.basicConfig(level=logging.INFO)

bot = discord.Bot()


@bot.event
async def on_ready():
    print("I'M ALIVE!")
    channel = bot.get_channel(771460089981829170)
    await channel.send("Bot is running!")


@bot.slash_command(name="hello", description="Say hi!")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

bot.load_extension("cogs.printFinishedCog")
bot.run('')
