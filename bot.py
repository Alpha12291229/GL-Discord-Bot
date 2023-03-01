# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Getting values from hidden environment files
load_dotenv("hidden.env")
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    
    #Printing When Connected
    print(f'{bot.user} has connected to Discord!')

    #Printing Servers the Bot is currently in
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')

#When people join the server
@bot.event 
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to my Discord server!'
	)

from os import listdir
for file in listdir('cogs/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)