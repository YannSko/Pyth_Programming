import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node, fifo, Stack

from datetime import datetime, timedelta
from Hashtable_user import HashTableUser
import json
import os
import requests
from bs4 import BeautifulSoup
from binary_tree_bot import *
intents = discord.Intents.all()

client = commands.Bot(command_prefix ="!", intents = intents)


my_list = list_chained("historique=liste chainée") 
nod = Node("Ne")
fifo = fifo(None)

###____Reminder____
reminder_stack = Stack(None)

def load_suggestions():
    with open("suggestions.json", "r") as f:
        suggestions = json.load(f)
    return suggestions

suggestions = load_suggestions()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(client.command_prefix):
        ctx = await client.get_context(message)
        await client.invoke(ctx)
  

    if message.content.startswith("Hello"):
        await message.channel.send("hello")
    await add_to_history(message)


    if message.author == client.user:
        return
'''
    if message.content.lower() == 'reset':
        await client.process_commands(message)
        return
    elif message.content.lower().startswith('speak about '):
        topic = message.content.lower().split('speak about ')[1]
        if topic in ['python', 'sports', 'music']:
            await message.channel.send(f"Je peux parler de {topic} !")
        else:
            await message.channel.send(f"Je ne peux pas parler de {topic}...")
    else:
        question = tree.get_question()
        await message.channel.send(question)
        response = message.content.lower()
        tree.send_answer(response)
        next_question = tree.get_question()
        await message.channel.send(next_question)
'''
### Ajout Historique du message
        
@client.event
async def on_ready():
    channel = client.get_channel(1091265494771843095)
    await channel.send('the bot is ready')

async def check_reminders():
    global reminder_stack

    while True:
        # Check if it's time to remind the user of a stored reminder
        if reminder_stack.size > 0 and reminder_stack.peek()[0] <= datetime.now():
            # Send the reminder message to the user
            remind_time, reminder = reminder_stack.pop()
            await client.send(f'Reminder: {reminder}')

        # Sleep for 1 second before checking again
        await asyncio.sleep(1)

# Call the check_reminders function to start the loop
check_reminders()




# _________________________________________History Related____________________________________________


HashTableUser = HashTableUser(bucket_size=10)

# fonction pour ajouter un message à l'historique
async def add_to_history(message):
    if not message.content.startswith(tuple(str(i) for i in range(10))): # prevent le !menu
        author_id = str(message.author.id)
        timestamp = str(datetime.now())

        message_content = message.content
        message_data = f'Message : {message_content} | Auteur : {author_id} | Date/Heure : {timestamp}'
        Component_history = Node(message_data)
        my_list.append(Component_history.data)
        await message.channel.send(f'Le message "{Component_history.data}" est placé dans l\'historique.')
        
        # lier l'historique à l'utilisateur
        user_history = HashTableUser.get(author_id)
        
        # si l'historique n'existe pas encore, créer une nouvelle liste chainée pour cet utilisateur
        if not user_history:
            user_history = list_chained(f"Historique de {message.author.display_name}")
            HashTableUser.append(author_id, user_history)

        # ajouter le message à l'historique de l'utilisateur
        user_history.append(Component_history.data)

        await message.channel.send(f'Le message "{Component_history.data}" est placé dans l\'historique de {message.author.display_name}.')
        
        # enregistrer les données dans un fichier texte
        with open("history.txt", "a") as f:
            f.write(message_data + "\n")


# fonction pour sauvegarder les données dans hastable
def save_data():
    with open("history.txt", "w") as f:
        for user_id in HashTableUser.buckets:
            user_history = HashTableUser.get(user_id[0])
            for message_data in user_history:
                f.write(message_data + "\n")

def save_suggestions():
    with open("suggestions.json", "w") as f:
        json.dump(suggestions, f)

# fonction pour fermer le bot et sauvegarder les données avant de quitter

async def on_shutdown():
    save_data()
    await client.close()


        
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

### Mouvement + last + user_history
@client.command(name="back")
async def navigate_backward(ctx):
    message = my_list.navigate_backward()
    await ctx.channel.send(message)

@client.command(name="forward")
async def navigate_forward(ctx):
    message = my_list.navigate_forward()
    await ctx.channel.send(message)

@client.command(name="last_message")
async def show_last_message(ctx):
    last_message = my_list.last_elmt()
    await ctx.channel.send("Le dernier message de l'historique est : " + last_message)

@client.command(name="user_history")
async def show_user_history(ctx, user_id: int):
    user_messages = [msg for msg in my_list.show_all() if str(user_id) in msg]
    if user_messages:
        message = "\n".join(user_messages)
        await ctx.channel.send(f"L'historique pour l'utilisateur avec l'ID {user_id} est :\n{message}")
    else:
        await ctx.channel.send(f"Aucun message pour l'utilisateur avec l'ID {user_id}")
#____________________________Menu_for_History______________________________
@client.command(name="menu")
async def menu(ctx):
    global fifo

    # regarde si qqn dans fifo , sinon place à la suite
    if fifo.peek() is None:
        fifo.push(ctx.author.id)
    else:
        if fifo.peek().data != ctx.author.id:
            fifo.push(ctx.author.id)
        if fifo.peek() is None: # regarde si cest toujours null ou non
            await ctx.send("You are not currently first in line. Please wait your turn.")
            return


    while True:
        menu_str = "Que voulez-vous faire?\n" \
                   "1. Afficher l'historique\n" \
                   "2. Supprimer le dernier message\n" \
                   "3. Supprimer un message spécifique\n" \
                   "4. Tout supprimer\n" \
                   "5. Naviguer en arrière\n" \
                   "6. Naviguer en avant\n" \
                   "7. Afficher le dernier message\n" \
                   "8. Afficher l'historique d'un utilisateur\n" \
                   "9. Quitter\n" \
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
            message = my_list.navigate_backward()
            await ctx.channel.send(message)
        elif message.content == "6":
            message = my_list.navigate_forward()
            await ctx.channel.send(message)
        elif message.content == "7":
            last_message = show_last_message(ctx)
            await ctx.send(last_message)
        elif message.content == "8":
            await ctx.send("Veuillez mentionner l'utilisateur dont vous voulez voir l'historique.")
            try:
                user_mention = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé. Commande annulée.")
                fifo.pop(ctx.author.id) # Remove user from fifo when they time out
                return
            await show_user_history(ctx, user_mention.content)
        elif message.content == "9":
            await ctx.send("Au revoir !")
            fifo.pop() # vire user from fifo
            return
        else:
            await ctx.send("Option invalide. Veuillez réessayer.")

#_________________________ABRE POUR PAPOTER __________________________________( FAIS POST DEMO EN CLASSE)
### INITIER ARBRE

cooking_tree = Binary_Tree()
cooking_tree.add_subject("cooking", "What type of cuisine do you want to cook?")
cooking_tree.root = Junction(cooking_tree.print_subject("cooking"))
cooking_tree.root.add_junction("Do you want to cook Asian cuisine?", True)
cooking_tree.root.add_junction("Do you want to cook European cuisine?", False)
cooking_tree.root.right.add_junction("Do you want to cook Chinese cuisine?", True)
cooking_tree.root.right.add_junction("Do you want to cook Japanese cuisine?", False)
cooking_tree.root.right.right.add_leaf("Awesome, here are some Chinese cooking recipes! DOG !", True)
cooking_tree.root.right.left.add_leaf("Awesome, here are some Japanese cooking recipes! MIAOU ! ", False)
cooking_tree.root.left.add_junction("Do you want to cook Italian cuisine?", True)
cooking_tree.root.left.add_junction("Do you want to cook French cuisine?", False)
cooking_tree.root.left.right.add_leaf("Awesome, here are some Italian cooking recipes! : Pasta ", True)
cooking_tree.root.left.left.add_leaf("Awesome, here are some French cooking recipes! PAIN ", False)

### INTERACTION AVEC LARBRE  ( pour reset cliquer sur la croix)  
@client.command(name="tree")
async def display_help_message(ctx):
    global actual_tree_node
    actual_tree_node = cooking_tree.root
    message = await ctx.send(actual_tree_node)
    await ctx.message.add_reaction("✅")
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id

    try:
        while True:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '❌':
                await message.delete()
                break
            elif str(reaction.emoji) == '✅':
                actual_tree_node = cooking_tree.root
                await message.edit(content=actual_tree_node)
            elif str(reaction.emoji) == '👍':
                actual_tree_node = cooking_tree.next_junction(actual_tree_node, True)
                if isinstance(actual_tree_node, Junction):
                    await message.edit(content=actual_tree_node)
                else:
                    await message.edit(content=actual_tree_node)
                    break
            elif str(reaction.emoji) == '👎':
                actual_tree_node = cooking_tree.next_junction(actual_tree_node, False)
                if isinstance(actual_tree_node, Junction):
                    await message.edit(content=actual_tree_node)
                else:
                    await message.edit(content=actual_tree_node)
                    break
    except asyncio.TimeoutError:
        await message.delete()
##  sLECTION DES SUJETS EN FONCTION DE LA PRESENCE DE SUJET DANS LE TREE
@client.command(name="subject")
async def get_existing_subjects(ctx):
    existing_subjects = list(cooking_tree.subjects.keys())
    message = f"The existing subjects are {existing_subjects}"
    await ctx.send(message)


#####__________________________Option++___________________________________

#________________Sondage_____________________________ via list chained
with open("suggestions.json", "r") as f:
    suggestions = json.load(f)


# Emettre une suggestion
@client.command(name="sug")
async def suggestion(ctx, *, suggestion):
    author = ctx.message.author
    # Ajout la sug
    suggestions.append({"author": author.id, "suggestion": suggestion, "votes": []})
    await ctx.send(f"{author.mention} Votre suggestion a été prise en compte !")
    save_suggestions()

# affiche la liste de sug
@client.command(name="show_sug")
async def list_suggestions(ctx):
    # Récupération de la liste de suggestions
    suggestions_list = []
    for i, suggestion in enumerate(suggestions):
        votes_emoji = "👍 " + str(len(suggestion["votes"])) if suggestion["votes"] else ""
        suggestion_text = f"{i}. {suggestion['suggestion']} - {ctx.guild.get_member(suggestion['author']).mention} {votes_emoji}"
        suggestions_list.append(suggestion_text)
    # Envoi de la liste de suggestions dans un message
    await ctx.send("\n\n".join(suggestions_list))

# Commande pour voter 
@client.command(name="vote")
async def vote(ctx, suggestion_number):
    author = ctx.message.author
    try:
        suggestion_number = int(suggestion_number)
        # Récupération de la suggestion correspondante 
        suggestion = suggestions[suggestion_number]
        # Vérification que l'auteur
        if author.id not in suggestion["votes"]:
            # Ajout du vote à la suggestion
            suggestion["votes"].append(author.id)
            await ctx.message.add_reaction("👍")
            save_suggestions()
        else:
            await ctx.send(f"{author.mention} Vous avez déjà voté pour cette suggestion.")
    except:
        await ctx.send(f"{author.mention} La suggestion n°{suggestion_number} n'existe pas.")
@client.command(name="show_vot")
async def show_all_suggestions(ctx):
    
    suggestions_list = list_chained("")
    
    for suggestion in suggestions:
        votes_emoji = "👍 " + str(len(suggestion["votes"])) if suggestion["votes"] else ""
        suggestion_text = f"{suggestion['suggestion']} - {ctx.guild.get_member(suggestion['author']).mention} {votes_emoji}"
        suggestions_list.append(suggestion_text)
    # Envoi de toutes les suggestions dans un message
    await ctx.send("\n\n".join(suggestions_list.show_all()))

#_______ 2eme___Options________Reminder
@client.command(name='remindme')
async def remindme(ctx, time_str: int, *, reminder: str):
    global reminder_stack
    
    remind_time = None
    
    
    try:
        remind_time = datetime.now() + timedelta(seconds=int(time_str))
    except ValueError:
        await ctx.send('Invalid input. Usage: !remindme [time in seconds] [reminder message]')
        return

    # Push the reminder message and time onto the stack
    reminder_stack.push((remind_time, reminder))

    # Send a confirmation message to the user
    await ctx.send(f'Reminder set for {remind_time.strftime("%m/%d/%Y %I:%M %p")} with message: {reminder}')

#_____option lol _____________
@client.command(name="lol")
async def youtube(ctx, *, url):
    
    if "youtube.com/watch?v=" not in url:
        await ctx.send("Ce n'est pas un lien valide de vidéo YouTube.")
        return

    # Supprime l'éventuelle balise "<>" 
    url = url.strip("<>")
    # Récupère l'identifiant 
    video_id = url.split("youtube.com/watch?v=")[1].split("&")[0]
    
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    os.system(f"start {video_url}")
    await ctx.send(f"Ouverture de la vidéo : {video_url}")
#________HIHI_____________
@client.command(name="scrap")
async def image(ctx, *, mot):
    # Effectuer une recherche Google Images avec le mot
    recherche = mot.replace(' ', '+')
    url = f'https://www.google.com/search?q={recherche}&tbm=isch'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')

    # Télécharger la première image 
    for image in images:
        src = image['src']
        if src.startswith('https') and not src.endswith('.svg'):
            response = requests.get(src, stream=True)
            if response.status_code == 200:
                with open(f'{mot}.jpg', 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                break
    
     # Stocker le mot de la recherche et le nom de l'image dans un fichier JSON
    data = {'mot': mot, 'image': f'{mot}.jpg'}
    with open('Images.json', 'w') as file:
        json.dump(data, file)

    # Envoyer l'image dans le canal Discord
    with open(f'{mot}.jpg', 'rb') as file:
        image = discord.File(file)
        await ctx.send(file=image)

##________________Ma note _____________ ( lancez la commande !)

@client.command(name="note")
async def note20(ctx):
   
    message = await ctx.send("Donnez une note sur 20 à Yann :")
    
    # 
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        note_message = await client.wait_for('message', check=check, timeout=10.0)
    except asyncio.TimeoutError:
        await message.edit(content=" Je me suis endormi ...")
        return

    # Vérifie que la note = un nombre 
    try:
        note = float(note_message.content)
    except ValueError:
        await ctx.send("Une note cest un nombre ... on part sur 20 merci ! ")
        return
    
    # Vérifie que la note est entre 0 et 20
    if note < 0 or note > 20:
        await ctx.send("La note doit être entre 0 et 20, cest pas du jeu sinon")
        return
    
    
    await ctx.send("Un 20 ? Merci ça régale :) !")

client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.GllGTP.3YWLuyn8VsxMbsjL2KkGOVCr_FJO7rWOt02uBE")