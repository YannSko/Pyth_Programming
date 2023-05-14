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

    if message.content != None:
        await add_to_history(message)

    if message.content.startswith("Hello"):
        await message.channel.send("hello")


@client.event
async def on_ready():
    channel = client.get_channel(1091265494771843095)
    await channel.send('the bot is ready')

# _________________________________________History Related____________________________________________
async def add_to_history(message):
    if not message.content.startswith(tuple(str(i) for i in range(10))): # prevent le !menu
        author_id = str(message.author.id)
        timestamp = str(datetime.datetime.now())
        message_content = message.content
        message_data = f'Message : {message_content} | Auteur : {author_id} | Date/Heure : {timestamp}'
        Component_history = Node(message_data)
        my_list.append(Component_history.data)
        await message.channel.send(f'Le message "{Component_history.data}" est placé dans l\'historique.')
        
        
        user_history = HashTableUser.get(author_id)

        # dans le cas lhistory nexiste pas
        if not user_history:
            user_history = list_chained(f"Historique de {message.author.display_name}")
            HashTableUser.append(author_id, user_history)

        # ajout
        user_history.append(Component_history.data)

        await message.channel.send(f'Le message "{Component_history.data}" est placé dans l\'historique de {message.author.display_name}.')
        with open("history.txt", "a") as f:
            f.write(message_data + "\n")

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

#_________________________ABRE POUR PAPOTER __________________________________


#### COMMAND
@client.command(name="d")
async def start_discussion(ctx):
 
    global tree
    tree = Tree("What do you want to learn about Python?")

    tree.append_question("What is your current programming experience?", ["Beginner", "Intermediate", "Advanced"], "What do you want to learn about Python?")

    tree.append_question("What do you want to learn about Python?", ["Web development", "Data analysis", "Machine learning", "Game development"], "What is your current programming experience?")

    tree.append_question("Do you want to learn Python for web development?", ["Yes", "No"], "Web development")
    tree.append_question("Do you want to learn Python for data analysis?", ["Yes", "No"], "Data analysis")
    tree.append_question("Do you want to learn Python for machine learning?", ["Yes", "No"], "Machine learning")
    tree.append_question("Do you want to learn Python for game development?", ["Yes", "No"], "Game development")

    tree.append_question("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Yes")

    while True:
        # Send the current question to the user and wait for their response
        await ctx.send(f"{tree.get_question()} Valid responses: {', '.join(tree.current_node.responses)}")

        response = await client.wait_for('message')

        # Check if the response is valid for the current node
        valid_response = False
        for n in tree.current_node.next_nodes:
            if response.content.lower() in n.reponses:
                tree.current_node = n
                valid_response = True
                break

        # If the response is not valid, prompt the user to try again
        if not valid_response:
            await ctx.send("Sorry, I didn't understand your response. Please try again.")
            continue

        # If the current node is the initial question, skip checking responses
        if not tree.current_node.responses:
            tree.current_node = tree.current_node.next_nodes[0]
            await ctx.send(f"{tree.get_question()}")

        # If the current node has no further questions, end the discussion
        elif not tree.current_node.next_nodes:
            await ctx.send(tree.current_node.question)
            break

    await ctx.send("Thank you for using our Python learning bot. Have a great day!")



@client.command(name="topic")
async def discussion_topic(ctx):
    global tree
    await ctx.send("The current topic of the discussion is: " + tree.get_question())

@client.command(name="reset_python_discussion")
async def reset_discussion(ctx):
    global tree
    tree.reset()
    await ctx.send("The discussion has been reset.")

#________________Arbre_____________



tree.append_question("What is your current programming experience?", ["Beginner", "Intermediate", "Advanced"], "What do you want to learn about Python?")

tree.append_question("What do you want to learn about Python?", ["Web development", "Data analysis", "Machine learning", "Game development"], first_question)

tree.append_question("Do you want to learn Python for web development?", ["Yes", "No"], "Web development")
tree.append_question("Do you want to learn Python for data analysis?", ["Yes", "No"], "Data analysis")
tree.append_question("Do you want to learn Python for machine learning?", ["Yes", "No"], "Machine learning")
tree.append_question("Do you want to learn Python for game development?", ["Yes", "No"], "Game development")

tree.append_question("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "Yes")
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