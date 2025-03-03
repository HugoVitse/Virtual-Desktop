Ce projet a été réalisé par Bochu Axel, Chiadmi Yassine, Degraeve Rémi et Vitse Hugo.

Pour compiler le projet, lancez le fichier install.sh, puis activer l'environnement virtuel (source venv/bin/activate) aller sur la racine du projet et entrez la commande python manage.py runserver
Assurez vous de bien avoir une version de Python3 fonctionnelle.

Il est également possible du build une image Docker à partir du DockerFile.

Il est possible que le projet ne compile pas suite à une indisponibilité du modèle d'IA hébergé sur Hugging Face. Si un problème survient :
- Attendez quelques minutes et essayez de recompiler le projet
- Vous pouvez désactiver le module d'IA en commentant la ligne path("chatbot/", include("chat.urls")) dans /mysite/urls.py

Spécificité des modules :

Un module terminal est disponible, mais seulement certaines commandes sont accessibles. Ci dessous une liste des commandes authorisées :
- ls
- cat
- echo
- touch
- rm
- mkdir
- rmdir