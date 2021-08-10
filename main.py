import discord
import os
import requests
from discord.ext import commands

bot = commands.Bot(("l!", "link ", "l?", "link?", "link!"), case_insensitive=True, help_command=None)


@bot.command(name="check", aliases=['check_link', 'checklink', 'linkcheck', 'link_check', 'trace', 'trace_link', 'tracelink'])
async def check(ctx, *, link):
    try:
        r = requests.head(link, allow_redirects=True)
        result = "Link Trace Results:\n"
        index = 0
        for hist in r.history:
            result += (f"{r.history[index]} - <" + hist.url + ">\n")
            index += 1
        result += (f"Destination ({r}) - <" + r.url + ">\n")
        await ctx.send(result)
    except:
        ...


@bot.command(name="help", aliases=["bothelp"])
async def bot_help(ctx):
    with open(os.path.join("docs", "help.txt"), "r") as f:
        await ctx.send(f.read())


@bot.command(name="version", aliases=["botversion"])
async def bot_version(ctx):
    with open(os.path.join("docs", "version.txt"), "r") as f:
        await ctx.send(f.read())


@bot.event
async def on_connect():
    print("Bot connected to Discord API")
    await bot.change_presence(activity=discord.Game(name="For help type link!help"))

bot.run(os.getenv("token"))
