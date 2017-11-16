See `environment.yml` for dependencies.

Generate `antlr4` classes from our grammar:
```bash
antlr4 -o gen -listener -visitor -Dlanguage=Python3 GrammaireSQL.g4
```

TODOs:
- In Python, deal with the new grammar rules for handling request with time restriction
- Adapt table names to reality

Questions:
- Comment traiter les mots non connus du lexique que notre lexique transforme ?
- How to handle words not existing in Lexicon during lemmatisation?
- Tables names? Que faire de article/bulletin ?
- Peut-on avoir les accès à la bdd ?

Tables de la base de données
http://www4.utc.fr/~lo17/faq.html#faq10

Structure de la phrase
- veux - afficher ... => selection
- paru ... => date
- contienne ... => mot
- écrit par ... => email

Si on tombe sur 'veux', alors s'il existe 'afficheur' ensuite, il ne sera pas transformer car c'est une information non liée à la structure.


VS
Paramétrage
biologie
02/12/2004
email@gmail.fr


Deux lexiques différents: un pour la structure et un pour les paramètres.

SELECT COUNT(*) FROM public.titre, public.date WHERE public.titre.fichier = public.date.fichier AND YEAR(public.date) = 2011
