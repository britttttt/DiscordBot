import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import aiohttp
import asyncio
import sys

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

# replace file handler with stream handler for cloud logging
handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])

intents = discord.Intents.default()
intents.message_content=True
intents.members = True 

bot = commands.Bot(command_prefix='/', intents=intents)

role_name = "Valkyrie"

#Custom emoji
mlady_tom ="<:TomMlady:1237200706474344520>"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='👋｜hello-get-on-in-here')
    if channel:
        await channel.send(f"Welcome to Valhalla, {member.mention} {mlady_tom}")

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
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name ="verified_user")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {role_name}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name ="verified_user")
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is no longer assigned to {role_name} role")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
@commands.has_role(role_name)
async def valkyrie(ctx):
    await ctx.send("Welcome to Valhalla!")

@valkyrie.error
async def valkyrie_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permissions to do that!")
    
async def main():
    async with bot:
        await bot.load_extension("cogs.dadjoke")
        await bot.load_extension("cogs.twitch")
        await bot.load_extension("cogs.dice")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())