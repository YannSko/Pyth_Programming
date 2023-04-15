import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node

intents = discord.Intents.all()

client = commands.Bot(command_prefix="8", intents = intents)


my_list = list_chained("début d'historique") 
nod = Node("pipi")
@client.event
async def on_message(message):
    if message.author == client.user:
        
        return
    if message.content != None:
        await history(message)
    if message.content.startswith("Hello"):
        await message.channel.send("hello")


@client.event
async def on_ready():
    channel = client.get_channel(1091265494771843095)
    await channel.send('the bot is ready')


async def history(message):
    Component_history = Node(message.content)
    my_list.append(Component_history)
    await message.channel.send(f'le message "{Component_history.data}" est placé dans lhistorique')



client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")