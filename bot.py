import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node, fifo
from question_tree import Tree
import datetime
from Hashtable_user import HashTableUser

intents = discord.Intents.all()

client = commands.Bot(command_prefix ="!", intents = intents)


my_list = list_chained("historique=liste chainée") 
nod = Node("Ne")
fifo = fifo(None)
first_question = "What do you want to learn about Python?"

tree = Tree(first_question)
'''
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
'''
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(client.command_prefix):
        ctx = await client.get_context(message)
        await client.invoke(ctx)
    if message.content.lower() == "yes" or message.content.lower() == "no":
        response = tree.traverse(message.content.lower())
        if response:
            await message.channel.send(response)
    

    if message.content.startswith("Hello"):
        await message.channel.send("hello")
    await add_to_history(message)
        ### Arbre


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

# _________________________________________History Related____________________________________________
import datetime

HashTableUser = HashTableUser(bucket_size=10)

# fonction pour ajouter un message à l'historique
async def add_to_history(message):
    if not message.content.startswith(tuple(str(i) for i in range(10))): # prevent le !menu
        author_id = str(message.author.id)
        timestamp = str(datetime.datetime.now())
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


# fonction pour sauvegarder les données
def save_data():
    with open("history.txt", "w") as f:
        for user_id in HashTableUser.buckets:
            user_history = HashTableUser.get(user_id[0])
            for message_data in user_history:
                f.write(message_data + "\n")


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

'''@client.command(name="menu")
async def menu(ctx):
    global fifo

    # Check if user is first in fifo, if not add them to the end
    if fifo.peek() is None:
        fifo.push(ctx.author.id)
    else:
        if fifo.peek().data != ctx.author.id:
            fifo.push(ctx.author.id)
        if fifo.peek() is None: # Check if queue is still empty after adding the user
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
            '''
@client.command(name="menu")
async def menu(ctx):
    global fifo

    # Check if user is first in fifo, if not add them to the end
    if fifo.peek() is None:
        fifo.push(ctx.author.id)
    else:
        if fifo.peek().data != ctx.author.id:
            fifo.push(ctx.author.id)
        if fifo.peek() is None: # Check if queue is still empty after adding the user
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
            fifo.pop() # Remove user from fifo
            return
        else:
            await ctx.send("Option invalide. Veuillez réessayer.")

#_________________________ABRE POUR PAPOTER __________________________________


#### Arbre initialisation
def treep() -> Tree:
    tree = Tree('Do you wanna play a team sport or an individualist sport ?')
    tree.first_node.responses = ['team','individualist']

    # First level
    tree.append_question('Do you wanna play a sport with a ball or without a ball ?', ['team'], 'team')
    tree.append_question('Do you wanna play a sport with a racket or without a racket ?', ['individualist'], 'individualist')
    
    # Second level - team sports
    tree.append_question('Do you wanna play football or basket ?', ['ball'], 'team with a ball')
    tree.append_question('Do you prefer running or swimming ?', ['without a ball'], 'team without a ball')
    
    # Third level - team sports with a ball
    tree.append_question('Great choice football is a very famous sport for a reason', ['football'], 'football')
    tree.append_question('Great choice basket is a very famous sport for a reason', ['basket'], 'basket')
    
    # Third level - team sports without a ball
    tree.append_question('Great choice relay race is a very famous sport for a reason', ['running'], 'relay race')
    tree.append_question('Great choice swimming relay is a very famous sport for a reason', ['swimming'], 'swimming relay')
    
    # Second level - individualist sports
    tree.append_question('Do you wanna play tennis or badminton ?', ['racket'], 'individualist with a racket')
    tree.append_question('Do you prefer weightlifting or crossfit ?', ['without a racket'], 'individualist without a racket')
    
    # Third level - individualist sports with a racket
    tree.append_question('Great choice tennis is a very famous sport for a reason', ['tennis'], 'tennis')
    tree.append_question('Great choice badminton is a very famous sport for a reason', ['badminton'], 'badminton')
    
    # Third level - individualist sports without a racket
    tree.append_question('Great choice running is a very famous sport for a reason', ['running'], 'running')
    tree.append_question('Great choice weightlifting is a very famous sport for a reason', ['weightlifting'], 'weightlifting')
    
    return tree
###  Command

@client.command(name="tree")
async def help(ctx):
    await ctx.send('Bonjour ! Voulez-vous jouer à un sport d\'équipe ou à un sport individuel ? (Répondez par "team" ou "individualist")')

@client.command(name="reset_tree")
async def reset(ctx):
    global tree
    tree = Tree('Do you wanna play a team sport or an individualist sport ?')
    tree.first_node.responses = ['team','individualist']
    await ctx.send('Conversation réinitialisée. Voulez-vous jouer à un sport d\'équipe ou à un sport individuel ? (Répondez par "team" ou "individualist")')

@client.command(name="speak_about")
async def speak(ctx, topic):
   
    if topic in ['python', 'sports', 'music']:
        await ctx.send(f"Je peux parler de {topic} !")
    else:
        await ctx.send(f"Je ne peux pas parler de {topic}...")




#________________Arbre_____________



'''
papote_tree = Tree("Do you want to learn about Python?")

papote_tree.append("What is your current programming experience?", ["Beginner", "Intermediate", "Advanced"], "Do you want to learn about Python?")

papote_tree.append("Do you want to learn Python for web development?", ["Yes", "No"], "Beginner")
papote_tree.append("Do you want to learn Python for data analysis?", ["Yes", "No"], "Intermediate")
papote_tree.append("Do you want to learn Python for machine learning?", ["Yes", "No"], "Intermediate")
papote_tree.append("Do you want to learn Python for game development?", ["Yes", "No"], "Advanced")

papote_tree.append("Python is a great choice for web development. Are you interested in web frameworks like Django or Flask?", ["Yes", "No"], "Do you want to learn Python for web development?")
papote_tree.append("Python is widely used in data analysis. Are you interested in tools like Pandas, NumPy, or Matplotlib?", ["Yes", "No"], "Do you want to learn Python for data analysis?")
papote_tree.append("Python is a popular choice for machine learning. Are you interested in libraries like Scikit-learn, TensorFlow, or PyTorch?", ["Yes", "No"], "Do you want to learn Python for machine learning?")
papote_tree.append("Python can be used for game development with libraries like Pygame. Are you interested in game development?", ["Yes", "No"], "Do you want to learn Python for game development?")

papote_tree.append("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Python is a great choice for web development. Are you interested in web frameworks like Django or Flask?")
papote_tree.append("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Python is widely used in data analysis. Are you interested in tools like Pandas, NumPy, or Matplotlib?")
papote_tree.append("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Python is a popular choice for machine learning. Are you interested in libraries like Scikit-learn, TensorFlow, or PyTorch?")
papote_tree.append("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Python can be used for game development with libraries like Pygame. Are you interested in game development?") 
papote_tree.append("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Do you want to learn about Python?") 


'''

client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")