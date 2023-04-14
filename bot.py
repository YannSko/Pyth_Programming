import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents = intents)


my_list = list_chained("début d'historique") 


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("Hello"):
        await message.channel.send("hello")


@client.event
async def on_ready():
    channel = client.get_channel(1091265494771843095)
    await channel.send('the bot is ready')


@client.command()
async def append(ctx, data):
    my_list.append(data)
    await ctx.send(f'Data "{data}" appended to the list.')


@client.command()
async def insert_first(ctx, data):
    my_list.insert_first(data)
    await ctx.send(f'Data "{data}" inserted as the first element in the list.')


@client.command()
async def size(ctx):
    size = my_list.size()
    await ctx.send(f'Size of the list: {size}')


@client.command()
async def insert(ctx, index, data):
    my_list.insert(int(index), data)
    await ctx.send(f'Data "{data}" inserted at index {index} in the list.')


@client.command()
async def read_all(ctx):
    all_data = my_list.read_all()
    await ctx.send(f'All data in the list: {all_data}')


@client.command()
async def read(ctx, index):
    data = my_list.read(int(index))
    await ctx.send(f'Data at index {index}: {data}')
    

client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")