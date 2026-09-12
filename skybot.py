import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

collection_file = "collections.json"

def load_collections():
    if os.path.exists(collection_file):
        with open(collection_file, 'r') as file:
            return json.load(file)

    return {}

def save_collections(collections):
    with open(collection_file, 'w') as file:
        json.dump(collections, file, indent = 4)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.command()
async def commands(ctx):
    items = [
        "!commands for a list of commands",
        "!shop for a link to the Elder Vault website",
        "!tracker for a link to the Elder Vault Collection Tracker",
        "!setcollection <amount> to set the total number of figures in your collection",
        "!collection to view your collection progress"
    ]

    command_list = "\n\n".join(f"• {item}" for item in items)

    await ctx.send(f"Here is a list of commands you can use:\n\n{command_list}")

@bot.command()
async def tracker(ctx):
    ctx.send("https://theeldervault.com/pages/collection-tracker")

@bot.command()
async def shop(ctx):
    await ctx.send("https://theeldervault.com/")

@bot.command()
async def setcollection(ctx, amount: int):
    total = 603

    if amount < 0 or amount > total:
        await ctx.send('Please enter a valid amount between 0 and 603.')
        return

    collections = load_collections()

    user_id = str(ctx.author.id)
    collections[user_id] = amount
    save_collections(collections)

    percentage = amount / total * 100

    await ctx.send(f"Collection updated: {amount}/{total} - {percentage:.1f}%")

@bot.command()
async def collection(ctx):
    total = 603

    collections = load_collections()

    user_id = str(ctx.author.id)

    if user_id not in collections:
        await ctx.send("You haven't set your collection yet!\n"
                       "Use '!setcollection <amount>' first.\n"
                       "For example: !setcollection 100"
                       )
        return

    owned = collections[user_id]

    percentage = owned / total * 100

    await ctx.send(f"{owned}/{total} - {percentage:.1f}%")


bot.run(token, log_handler = handler, log_level = logging.DEBUG)