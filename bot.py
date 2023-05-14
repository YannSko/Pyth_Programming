import discord
from discord.ext import commands
import asyncio
from Liste_chained import list_chained, Node, fifo
from question_tree import Tree
import datetime
from Hashtable_user import HashTableUser
import json

intents = discord.Intents.all()

client = commands.Bot(command_prefix ="!", intents = intents)


my_list = list_chained("historique=liste chainée") 
nod = Node("Ne")
fifo = fifo(None)

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
### Fonction Pour handle la conv



### Création de l'abre
@client.command(name="love")
async def love(ctx):
    tree = Tree("Bienvenue dans cette discussion sur l'amour. Pour commencer, pouvez-vous me dire ce qui vous amène ici ?")
    tree.append_question("Êtes-vous en couple ?", ["Oui", "Non"], "Bienvenue dans cette discussion sur l'amour. Pour commencer, pouvez-vous me dire ce qui vous amène ici ?")
    tree.append_question("Comment avez-vous rencontré votre partenaire ?", ["En ligne", "À travers des amis", "Au travail", "Dans un lieu public", "Autre"], "Êtes-vous en couple ?")
    tree.append_question("Qu'est-ce que vous appréciez le plus chez votre partenaire ?", ["Son physique", "Sa personnalité", "Son sens de l'humour", "Sa gentillesse", "Autre"], "Comment avez-vous rencontré votre partenaire ?")
    tree.append_question("Comment entretenez-vous votre relation amoureuse ?", ["En communiquant ouvertement et régulièrement", "En passant du temps ensemble", "En faisant des choses spéciales pour l'autre", "En respectant l'autre et ses besoins"], "Qu'est-ce que vous appréciez le plus chez votre partenaire ?")
    tree.append_question("Quelles sont les clés pour maintenir une relation amoureuse saine ?", ["La communication", "La confiance", "Le respect", "Le compromis", "La passion"], "Comment entretenez-vous votre relation amoureuse ?")
    tree.append_question("Avez-vous déjà vécu une rupture amoureuse ?", ["Oui", "Non"], "Quelles sont les clés pour maintenir une relation amoureuse saine ?")
    tree.append_question("Comment avez-vous surmonté cette rupture ?", ["En prenant du temps pour moi-même", "En parlant à mes amis et ma famille", "En cherchant l'aide d'un professionnel", "Autre"], "Avez-vous déjà vécu une rupture amoureuse ?")
    tree.append_leaf("Si vous avez besoin d'aide pour surmonter une rupture amoureuse ou pour améliorer votre relation amoureuse actuelle, je vous recommande de consulter ce site : https://www.psychologytoday.com/us/topics/relationships")
   





#####__________________________Option++___________________________________

#________________Sondage_____________________________
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




client.run("MTA5MTI2Mjc0NjI1MjgwNDEyNg.GllGTP.3YWLuyn8VsxMbsjL2KkGOVCr_FJO7rWOt02uBE")