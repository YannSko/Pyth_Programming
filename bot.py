import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node, fifo
from question_tree import Tree

intents = discord.Intents.all()

client = commands.Bot(command_prefix ="!", intents = intents)


my_list = list_chained("historique=liste chainée") 
nod = Node("Ne")
fifo = fifo(None)
tree = Tree("Do you want to learn about Python?")
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

    if message.content.lower() == "yes" or message.content.lower() == "no":
        response = tree.traverse(message.content.lower())
        if response:
            await message.channel.send(response)

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
    if not message.content.startswith(tuple(str(i) for i in range(10))): # prevent le !menu
        global Component_history
        Component_history = Node(message.content)
        my_list.append(Component_history.data)
        await message.channel.send(f'Le message "{Component_history.data}" est placé dans l\'historique.')



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
@client.command(name="papote")
async def start(ctx):
    papote_tree.reset()
    await ctx.send(papote_tree.get_question())

    def check(author):
        def inner_check(message):
            return message.author == author
        return inner_check

    author = ctx.message.author
    while True:
        try:
            message = await client.wait_for('message', check=check(author), timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to respond.")
            break

        papote_tree.choice(message.content.lower())

        if papote_tree.current_node.answer_to_go_here == "Do you want to learn about Python?":
            papote_tree.append("What is your current programming experience?", ["Beginner", "Intermediate", "Advanced"], "Do you want to learn about Python?")
            await ctx.send(papote_tree.current_node.question)

        elif papote_tree.current_node.answer_to_go_here == "Beginner":
            papote_tree.append("Do you want to learn Python for web development?", ["Yes", "No"], "Beginner")
            await ctx.send(papote_tree.current_node.question)

        elif papote_tree.current_node.answer_to_go_here == "Intermediate":
            papote_tree.append("Do you want to learn Python for data analysis?", ["Yes", "No"], "Intermediate")
            papote_tree.append("Do you want to learn Python for machine learning?", ["Yes", "No"], "Intermediate")
            await ctx.send(papote_tree.current_node.question)

        elif papote_tree.current_node.answer_to_go_here == "Advanced":
            papote_tree.append("Do you want to learn Python for game development?", ["Yes", "No"], "Advanced")
            await ctx.send(papote_tree.current_node.question)

        elif papote_tree.current_node.answer_to_go_here == "Yes":
            await ctx.send("Great! You should check out resources for {}.".format(papote_tree.current_node.question))

            # Add final message and reset tree
            papote_tree.append("Python is a versatile language that can be used for many applications. Good luck with your Python journey!", [], "")
            await ctx.send(papote_tree.current_node.question)
            papote_tree.reset()
            break

        elif papote_tree.current_node.answer_to_go_here == "No":
            await ctx.send("No problem, feel free to explore other topics.")
            papote_tree.reset()
            break

        else:
            await ctx.send(papote_tree.current_node.question)
@client.command(name="help_papote")
async def helpme(ctx):
    tree.reset()
    await ctx.send(tree.current_node.question)

@client.command(name="reset_papote")
async def reset(ctx):
    tree.reset()
    await ctx.send("Conversation has been reset.")

@client.command(name="topic_papote")
async def speak_about(ctx, topic):
    # Modify this list to include the topics you want the bot to discuss
    topics = ["python", "DevWeb", "Machine Learning", "GameDev"]
    if topic.lower() in topics:
        await ctx.send("Yes, I can help you with {}.".format(topic))
    else:
        await ctx.send("Sorry, I don't have information on that topic.")

#________________Arbre_____________

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




client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.Gsebrp.cJdD2YSX_V6-VC_RuX39NwIxK8PD9INRiq2eSM")