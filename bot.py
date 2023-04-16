import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node

intents = discord.Intents.all()

client = commands.Bot(command_prefix ="!", intents = intents)


my_list = list_chained("début d'historique") 
nod = Node("pipi")
@client.event
async def on_message(message):
    if message.author == client.user:
        
        return
    if message.content != None:
        await add_to_history(message)
    if message.content.startswith("Hello"):
        await message.channel.send("hello")
     
    if message.content.startswith(client.command_prefix):
        ctx = await client.get_context(message)
        await client.invoke(ctx)


@client.event
async def on_ready():
    channel = client.get_channel(1091265494771843095)
    await channel.send('the bot is ready')


async def add_to_history(message):
    global Component_history
    Component_history = Node(message.content)
    my_list.append(Component_history.data)
    await message.channel.send(f'le message "{Component_history.data}" est placé dans lhistorique')

@client.command(name="history")
async def show_history(ctx):
    
    history_list = my_list.show_all()
    history_str = "\n".join(history_list)
    if history_str:
        await ctx.channel.send("Les messages de l'historique sont:\n" + history_str)
    else:
        await ctx.channel.send("Fin historique.")
@client.command(name="last")
async def delete_last_message(ctx):
    my_list.delete_last()
    await ctx.send('plus de dernier message')

@client.command(name="sup")
async def delete_message(ctx, index: int):
    my_list.delete_at_index(index)
    await ctx.send(f'le message num {index} est sup.')

@client.command(name="tout")
async def delete_all_messages(ctx):
    my_list.delete_all()
    await ctx.send('tout les messages = supprime')



client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")