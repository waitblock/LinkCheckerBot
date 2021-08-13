import json
import os

import discord
import pandas as pd
import requests
from discord.ext import commands
from sklearn.linear_model import SGDClassifier

with open("config.json", "r") as config_file:
    blacklisted_sites = json.load(config_file)['blacklisted-sites']


df = pd.read_csv(os.path.join("training_data", "data.csv"), header=0)
headers = list(df.columns.values)
raw_data = df.values

x = []
y = []

for i in range(len(raw_data)):
    x.append(raw_data[i][0])
    y.append(raw_data[i][1])

x_train, x_test, y_train, y_test = x[:320000], x[320000:], y[:320000], y[:320000]
y_train_bad = []

for i in range(len(y_train)):
    if y_train[i] == 'good':
        y_train_bad.append(False)
    if y_train[i] == 'bad':
        y_train_bad.append(True)

sgd_clf = SGDClassifier(random_state=42)


bot = commands.Bot(("l!", "link ", "l?", "link?", "link!"), case_insensitive=True, help_command=None)


@bot.command(name="code", aliases=["statuscode", "httpcode", "responsecode"])
async def code(ctx, *, status_code):
    try:
        with open(os.path.join("status_codes", status_code + ".txt")) as status:
            result = status.read()
    except FileNotFoundError:
        with open(os.path.join("status_codes", "invalid_code.txt"), "r") as invalid:
            result = invalid.read()
    if status_code == "ATTRIBUTION" or status_code == "LICENSE" or status_code == "invalid_code":
        with open(os.path.join("status_codes", "invalid_code.txt"), "r") as invalid:
            result = invalid.read()
    await ctx.send(result)


@bot.command(name="help", aliases=["bothelp"])
async def bot_help(ctx):
    with open("help.txt", "r") as f:
        await ctx.send(f.read())


@bot.command(name="ping", aliases=["botping"])
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong! {round(bot.latency*100, 2)}ms")


@bot.command(name="trace", aliases=['check', 'check_link', 'checklink', 'linkcheck', 'link_check', 'trace_link', 'tracelink'])
async def check(ctx, *, link):
    try:
        r = requests.head(link, allow_redirects=True)
        result = "Link Trace Results:\n"
        index = 0
        contains_blacklisted = False
        for hist in r.history:
            for site in blacklisted_sites:
                if site in hist.url:
                    contains_blacklisted = True
            result += (f"{r.history[index]} - <" + hist.url + ">\n")
            index += 1
        result += (f"Destination ({r}) - <" + r.url + ">\n")
        if contains_blacklisted is True:
            result += "```css\n⚠️ [Malicious Link(s) Detected During Trace]```\n"
        await ctx.send(result)
    except requests.exceptions.MissingSchema:
        await ctx.send("Try adding http:// to the front of the link.")
    except requests.exceptions.ConnectionError:
        await ctx.send("The URL refused to connect.")
    except discord.ext.commands.errors.MissingRequiredArgument:
        await ctx.send("Link was not provided.")


@bot.command(name="version", aliases=["botversion"])
async def bot_version(ctx):
    with open("version.txt", "r") as f:
        await ctx.send(f.read())


@bot.event
async def on_connect():
    print("Bot connected to Discord API")
    await bot.change_presence(activity=discord.Game(name="For help type link!help"))

with open("TOKEN", "r") as token:
    bot.run(token.read())
