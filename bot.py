import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node, fifo

intents = discord.Intents.all()

client = commands.Bot(command_prefix ="!", intents = intents)


my_list = list_chained("historique=liste chainée") 
nod = Node("Ne")
fifo = fifo(None)
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

# _________________________________________History Related____________________________________________
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
    

#____________________________Menu_for_History______________________________
'''
@client.command(name="menu")
async def menu(ctx):
    while True:
        menu_str = "Que voulez-vous faire?\n" \
                   "1. Afficher l'historique\n" \
                   "2. Supprimer le dernier message\n" \
                   "3. Supprimer un message spécifique\n" \
                   "4. Tout supprimer\n" \
                   "Répondez avec le numéro de l'option."
        await ctx.send(menu_str)
        try:
            message = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Commande annulée.")
            return

        if message.content == "1":
            await show_history(ctx)
        elif message.content == "2":
            await delete_last_message(ctx)
        elif message.content == "3":
            await ctx.send("Quel est l'index du message à supprimer?")
            try:
                index_message = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé. Commande annulée.")
                return
            await delete_message(ctx, int(index_message.content))
        elif message.content == "4":
            await delete_all_messages(ctx)
        elif message.content.lower() == "menu":
            continue
        else:
            await ctx.send("Option invalide.")
        
        await ctx.send("Tapez 'menu' pour retourner au menu principal, ou attendez 30 secondes pour quitter.")
        try:
            message = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Commande annulée.")
            return
        if message.content.lower() == "menu":
            continue
        else:
            return
'''
@client.command(name="menu")
async def menu(ctx):
    global fifo

    # Check if user is first in fifo, if not add them to the end
    if fifo.peek() is None:
        fifo.push(ctx.author.id)
    elif fifo.peek().data != ctx.author.id:
        fifo.push(ctx.author.id)
        if fifo.peek().data != ctx.author.id: # double-check that user is not first in line
            await ctx.send("You are not currently first in line. Please wait your turn.")
            return

    while True:
        menu_str = "Que voulez-vous faire?\n" \
                   "1. Afficher l'historique\n" \
                   "2. Supprimer le dernier message\n" \
                   "3. Supprimer un message spécifique\n" \
                   "4. Tout supprimer\n" \
                   "5. Quitter\n" \
                   "Répondez avec le numéro de l'option."
        await ctx.send(menu_str)
        try:
            message = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Commande annulée.")
            fifo.pop(ctx.author.id) # Remove user from fifo when they time out
            return

        if message.content == "1":
            await show_history(ctx)
        elif message.content == "2":
            await delete_last_message(ctx)
        elif message.content == "3":
            await ctx.send("Quel est l'index du message à supprimer?")
            try:
                index_message = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé. Commande annulée.")
                fifo.pop(ctx.author.id) # Remove user from fifo when they time out
                return
            await delete_message(ctx, int(index_message.content))
        elif message.content == "4":
            await delete_all_messages(ctx)
        elif message.content == "5":
            fifo.pop(ctx.author.id)
            await ctx.send("Vous avez quitté la commande de menu.")
            return
        elif message.content.lower() == "menu":
            continue
        else:
            await ctx.send("Option invalide.")
        
        await ctx.send("Tapez 'menu' pour retourner au menu principal, ou attendez 30 secondes pour quitter.")
        try:
            message = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Commande annulée.")
            fifo.pop(ctx.author.id) 
            return
        if message.content.lower() == "menu":
            continue
        else:
            fifo.pop(ctx.author.id) 
            return



client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")