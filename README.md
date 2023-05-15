# Projet Bot Discord
## Les fonctionnalités

Dans ce bot privé se trouvent plusieurs fonctionnalités :

    - Historique : avec liste chaînée, nous pouvons stocker tous les messages, naviguer en avant et en arrière et supprimer des messages à un index donné, le dernier message ou tous les messages. L'historique est également stocké dans un fichier texte.
    - Image du net : une commande permettant d'obtenir une image directement du web.
    - Lancer une vidéo YouTube : une commande pour lancer une vidéo YouTube.
    - Arbre de discussion : un arbre binaire permettant d'interagir avec le sujet de la cuisine en utilisant les emojis pour naviguer et obtenir une réponse.
    - Système de vote de suggestion : un système permettant de voter, de regarder et d'afficher les suggestions, toutes stockées dans un fichier JSON.

## La "tech utilisée"

### A. Structure faite à la main : liste chaînée, hashtable, file (FIFO), arbre binaire.
### B. Technologies : Asyncio, JSON, BS et autres bibliothèques de Discord.

## Description d'ensemble
 ### Historique

Tous les messages sont stockés dans un historique et placés dans un fichier texte. Nous pouvons naviguer en avant et en arrière, voir tous les messages et supprimer des messages à un index donné, le dernier message ou tous les messages. Pour accéder à cette commande, il y a le principe de queue pour éviter le problème de threading. Pour la sécurité, nous hachons l'ID de l'utilisateur via une Hashtable : chaque utilisateur a un ID hashé, rendant plus complexe l'observation de l'historique. Enfin, nous pouvons regarder l'historique de chaque utilisateur (via son ID hashé).

 ### Arbre binaire

Nous pouvons interagir avec l'arbre sur le sujet de la cuisine. Nous utilisons les emojis (add reaction) pour naviguer dans ce dernier et obtenir une réponse.

 ### Système de suggestion

Nous pouvons voter, regarder les suggestions, afficher les suggestions (on ne peut voter qu'une fois), toutes les suggestions sont stockées dans un fichier JSON.

### Scrappe

Nous pouvons entrer la commande "!scrap" + un nom et le bot part scrapper sur le web une image correspondante. ( les images sont stockés en json ( non pas lurl , mais les recherches faites))

### YouTube

Nous pouvons entrer un lien YouTube, et cela lance une vidéo YouTube en adéquation sur l'ordinateur.
Reminder

Il y a une fonction reminder qui envoie un message en fonction du temps que l'on souhaite mettre (en secondes). Malheureusement, je n'ai pas réussi à gérer le côté de loop.task (loop le reminder chaque seconde pour voir si le temps défini (du rappel) correspond au temps actuel).

N'hésitez pas à me faire un retour ou à proposer d'autres options sympa si vous avez des idées !