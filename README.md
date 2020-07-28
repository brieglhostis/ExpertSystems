# Pole IA - Systemes Experts

Ce projet S6 du pôle IA a pour objectif de faire un site web permettant d'enseigner ce qu'il y a à savoir sur les systèmes experts 
à travers des tutoriels et des exercices. Le projet est donc constitué de deux grosses parties :

* La programmation des systèmes experts et de l'interface utilisateur, entièrement en python (tous les dossiers sauf le dossier Website)
* Le site web, qui est fait avec la stack MEAN (MongoDB, Express, Angular, Node.js)

## Programmation python des systèmes experts

Afin de lancer toute l'interface utilisateur, il faut appeler la classe `DisplayUI(facts, rules, rules_fuzzy, fuzzy_sets)` présente dans le fichier
**User_interface/Main_menu.py**. Des tests sont proposés avec des règles et des faits déjà constitués dans le fichier **Test/Tests.py**.

Pour faire des tests plus précis, on peut trouver des fonctions spécifiques dans les dossiers correspondants aux différents types de systèmes experts
(forward, backward et fuzzy).

## Le site web

Le site web est constitué d'un front fait avec Angular, et d'un back fait avec le framework loopback (basé sur Express et Node.js) qui est connecté
à une base de donnée en MongoDB.

**Attention** : la base de donnée n'étant pas inclue dans le projet, il faut pour l'instant créer soi-même les parties et les tutoriels à inclure
dans la base de données.

### Faire tourner le site web en local

Il faut d'abord avoir Node.js, npm et mongoDB installés sur votre machine : si ce n'est pas le cas, faites le avant de continuer.

Pour faire tourner le site internet sur votre machine, ouvrez deux consoles de commande. Dans la première, rendez-vous dans le dossier 
**Website/backend**, puis exécutez la commande `npm install`. Ensuite, exécutez la commande `node .`.

Dans la deuxième console de commandes, rendez-vous dans le dossier **Website/front**, puis exécutez `npm install`. Ensuite, exécutez la commande 
`ng serve --open`, puis attendez un peu. Au bout d'un certain temps, votre navigateur devrait s'ouvrir tout seul sur le site web. Si ce n'est pas le 
cas, rendez-vous sur la page http://localhost:4200/ pour y accéder.

### Administrer la base de donnée

Assurez vous tout d'abord d'avoir MongoDB, Node.js et npm installés sur votre machine.
Ensuite, vous avez deux solutions :

Pour la première, lancez MongoDB Compass (que vous avez normalement installé au préalable), puis connectez
vous à la BDD en laissant les paramètres proposés par défaut. Il vous faut ensuite créer une database nommée "test", dans laquelle vous pourrez créer
 vos tutoriels et vos parties.

Pour la deuxième, effectuez la première étape de la partie précédente afin de lancer le backend du site. En ouvrant votre navigateur à 
l'adresse http://localhost:3000/explorer/, vous devriez alors avoir accès aux fonctions nécessaires pour administrer la BDD.


