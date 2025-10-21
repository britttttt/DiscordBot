import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import aiohttp
import asyncio

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content=True
intents.members = True 

bot = commands.Bot(command_prefix='/', intents=intents)

verified_user = "Valkyrie"

#Custom emoji
mlady_tom ="<:TomMlady:1237200706474344520>"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='👋｜hello-get-on-in-here')
    await member.send(f"Welcome to Valhalla,{member.mention} {mlady_tom}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found.')
    else:
        await ctx.send(f'An error occurred: {error}')

# /hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Well Howdy Do {ctx.author.mention} {mlady_tom}!")

@bot.command()
async def d20(ctx):
    number = random.randint(1,20)
    await ctx.send(f"{ctx.author.mention} you rolled a {number}")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name ="verified_user")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {verified_user}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name ="verified_user")
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is no longer assigned to {verified_user} role")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
@commands.has_role(verified_user)
async def valkyrie(ctx):
    await ctx.send("Welcome to Valhalla!")

@valkyrie.error
async def valkyrie_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permissions to do that!")
    
@bot.command()
async def dadjoke(ctx):
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json",
        "User-Agent": "DiscordBot (https://github.com/youruser/DiscordBot, 1.0)"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    joke = data.get("joke")
                    if joke:
                        await ctx.send(joke)
                        return
                await ctx.send("Couldn't fetch a joke right now. Try again later.")
    except asyncio.TimeoutError:
        await ctx.send("Request timed out. Try again later.")
    except Exception:
        logging.exception("Failed to fetch dad joke")
        await ctx.send("Error fetching joke.")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)