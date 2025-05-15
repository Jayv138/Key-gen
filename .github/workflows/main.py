import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# Flask web server for uptime
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Intents and Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

KEY_CHANNEL_NAME = "key"
DATA_FILE = "key_data.json"

# Load or initialize key data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"used_keys": [], "users": {}}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_today():
    return datetime.utcnow().strftime('%Y-%m-%d')

@bot.command()
async def getkey(ctx):
    if ctx.channel.name != KEY_CHANNEL_NAME:
        return await ctx.send(f"Use the #{KEY_CHANNEL_NAME} channel to get a key.")

    user_id = str(ctx.author.id)
    today = get_today()

    if user_id in data["users"] and data["users"][user_id]["date"] == today:
        return await ctx.send(f"You already got your key today: **{data['users'][user_id]['key']}**")

    all_keys = [f"Druski{i}" for i in range(1, 10001)]
    available_keys = list(set(all_keys) - set(data["used_keys"]))

    if not available_keys:
        return await ctx.send("All keys have been claimed.")

    selected_key = random.choice(available_keys)
    data["used_keys"].append(selected_key)
    data["users"][user_id] = {"date": today, "key": selected_key}
    save_data()

    try:
        await ctx.author.send(f"Your key: **{selected_key}**")
        await ctx.send("I sent your key in a private message!")
    except discord.Forbidden:
        await ctx.send("I couldn't DM you. Enable DMs from server members.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Run web server and bot
keep_alive()
bot.run(os.getenv("MTM3MjM4NTIzNzM1ODYwODUxNw.GhYXhO.nlIi0HcLLRKZdsmHrnL_4nmIShRXlnQpkIJuaQ"))
