from request import getPlayerData
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

from keep_alive import keep_alive

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

keep_alive()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

##Enabling Permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents = intents)
##added users tracks users added to the leaderboard
added_users = []

@bot.event
async def on_ready():
    print(f"we are ready")

@bot.command()
async def lb(ctx):
    await ctx.send("Processing Request")
    leaderboard_string = ""
    leaderboard_list = []
    ##Have to create a leaderboard list to be currently accurate
    for tag in added_users:
        ##Retrieve user data & Add to Memory
        user_data = getPlayerData(tag)

        ##Round rank to 2 decimals
        rounded_rank = round(float(user_data[1]),2)

        ##Set a tuple of (rank number, player code) add to list and then sort that list
        user = user_data[0]
        rank = str(rounded_rank)
        name = user_data[5]
        leaderboard_list.append((rank,user,name))
    
    leaderboard_list.sort(reverse=True)
    rank = 1
    for tag in leaderboard_list:
        temp_str = ""
        if rank == 1:
            temp_str += "🥇" + "**" + tag[2] + "**" + " " + "(" + tag[1] + ")" + " - " + tag[0] + "\n"
        elif rank == 2:
            temp_str += "🥈" + "**" + tag[2] + "**" + " " + "(" + tag[1] + ")" + " - " + tag[0] + "\n"
        elif rank == 3:
            temp_str += "🥉" + "**" + tag[2] + "**" + " " + "(" + tag[1] + ")" + " - " + tag[0] + "\n"
        else:
            temp_str += str(rank) + ". " + "**" + tag[2] + "**" + " " + "(" + tag[1] + ")" + " - " + tag[0] + "\n"
        leaderboard_string += temp_str
        rank += 1
    embed = discord.Embed(title="🏆 Slippi Leaderboard", description= leaderboard_string)
    await ctx.send(embed=embed)

@bot.command()
async def rankadd(ctx, tag):
    tag_upper = str(tag).upper()
    if tag_upper in added_users:
        await ctx.send("User Already Added")
    else:
        ##Retrieve user data & Add to Memory
        user_data = getPlayerData(tag_upper)
        ##If user exists add them to added_users, otherwise return invalid
        if user_data != None:
            added_users.append(tag_upper)
            await ctx.send(tag_upper + " Added to the Leaderboard")
        else:
            await ctx.send("Invalid User")

@bot.command()
async def rankremove(ctx, tag):
    ##If the tag is in added_users remove it, otherwise return invlaid
    tag_upper = str(tag).upper()
    if tag_upper in added_users:
        added_users.remove(tag_upper)
        await ctx.send(tag_upper + " Removed From Leaderboard")
    else:
        await ctx.send(tag_upper + " Not On Leaderboard")


@bot.command()
async def rank(ctx, tag):
    slippi_user = getPlayerData(tag)
    rounded = round(float(slippi_user[1]), 2)
    await ctx.send(str(rounded))

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="P+Bot Commands", description= "?rank [tag] - Gives the rank of the tag \n ?rankadd [tag] - adds the tag to the slippi leaderboard \n ?rankremove [tag] - removes the tag from the slippi leaderboard \n ?lb - retrieves the current ranked leaderboard")
    await ctx.send(embed=embed)

##Running the Bot and creating logging
bot.run(token, log_handler=handler, log_level=logging.DEBUG)