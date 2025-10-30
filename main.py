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


# @bot.tree.command(name="assign", description="Assign yourself the verified_user role")
# async def assign_slash(interaction: discord.Interaction):
#     role = discord.utils.get(interaction.guild.roles, name="verified_user")
#     if role:
#         await interaction.user.add_roles(role)
#         await interaction.response.send_message(f"{interaction.user.mention} is now assigned to {role_name}")
#     else:
#         await interaction.response.send_message("Role doesn't exist")


# @bot.tree.command(name="remove", description="Remove yourself from the verified_user role")
# async def remove_slash(interaction: discord.Interaction):
#     role = discord.utils.get(interaction.guild.roles, name="verified_user")
#     if role:
#         await interaction.user.remove_roles(role)
#         await interaction.response.send_message(f"{interaction.user.mention} is no longer assigned to {role_name} role")
#     else:
#         await interaction.response.send_message("Role doesn't exist")


# @bot.tree.command(name="valkyrie", description="Welcome to Valhalla (requires role)")
# async def valkyrie_slash(interaction: discord.Interaction):
#     role = discord.utils.get(interaction.guild.roles, name=role_name)
#     if role and role in interaction.user.roles:
#         await interaction.response.send_message("Welcome to Valhalla!")
#     else:
#         await interaction.response.send_message("You do not have permissions to do that!")


### MAin 
async def main():
    # Load cogs if you want
    # await bot.load_extension("cogs.dadjoke")
    # await bot.load_extension("cogs.twitch")
    # await bot.load_extension("cogs.dice")
    # await bot.load_extension("cogs.tictactoe")
    # await bot.load_extension("cogs.text_commands")

    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
