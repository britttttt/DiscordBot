import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import sys
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

role_name = "Valkyrie"
mlady_tom = "<:TomMlady:1237200706474344520>"  # Custom emoji

###Events
@bot.event
async def on_ready():
    print(f"{bot.user.name} ready for duty! We're going in!")
    if GUILD_ID:
        try:
            guild_obj = discord.Object(id=int(GUILD_ID))
            await bot.tree.sync(guild=guild_obj)
            print(f"Synced app commands to guild {GUILD_ID}")
        except Exception:
            await bot.tree.sync()
            print("Fallback: synced global commands")
    else:
        await bot.tree.sync()


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="👋｜hello-get-on-in-here")
    if channel:
        await channel.send(f"Welcome to Valhalla, {member.mention} {mlady_tom}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        await ctx.send(f"An error occurred: {error}")

###Commands

@bot.command()
async def hello(ctx):
    await ctx.send(f"Well Howdy Do {ctx.author.mention} {mlady_tom}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="verified_user")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {role_name}")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name="verified_user")
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


### Slash commands
@bot.tree.command(name="hello", description="Say hello using a slash command")
async def hello_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"Well Howdy Do {interaction.user.mention} {mlady_tom}!")


### MAin 
async def main():
    await bot.load_extension("cogs.dadjoke")
    await bot.load_extension("cogs.twitch")
    await bot.load_extension("cogs.dice")
    await bot.load_extension("cogs.duck_photo")
    await bot.load_extension("cogs.tictactoe")
    await bot.load_extension("cogs.text_commands")

    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
