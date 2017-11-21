-- Donner les articles parus en 2011.
SELECT *
FROM public.titre
  LEFT JOIN public.date
    ON public.titre.fichier = public.date.fichier
WHERE public.date.annee='2011';


--Voir article
SELECT DISTINCT * FROM titre;

--Voir bulletin
SELECT DISTINCT * FROM numero;


-- Objectif: gérer toutes les requetes portant sur les articles.

-- Exemples:
-- Affiche-moi les articles qui contiennent des actualités.
-- Afficher les articles plus vieux que 2013.
-- Articles parlant d'innovation.
-- Donner les articles parus en 2011.
-- Donnez moi les articles sur le diabète

