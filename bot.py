import discord
from discord.ext import commands
import asyncio
import  Liste_chained

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents = intents)



@client.event
async def on_message(message):
    if (message.author == client.user):
        return
   

    if message.content.startswith("Hello"):
        await message.channel.send("hello")
@client.event
async def on_ready():
    channel = client.get_channel(1091265494771843095)
    await channel.send('the bot is ready')
    

client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")