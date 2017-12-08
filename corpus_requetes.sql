-- Donner les articles parus en 2011.
SELECT *
FROM public.titre
  LEFT JOIN public.date
    ON public.titre.fichier = public.date.fichier
WHERE public.date.annee = '2011';

--Voir article
SELECT DISTINCT *
FROM titre;

--Voir bulletin
SELECT DISTINCT *
FROM numero;

SELECT DISTINCT *
FROM titre
  LEFT JOIN date ON titre.fichier = date.fichier
WHERE date.annee = '2011';

SELECT DISTINCT *
FROM titre
  LEFT JOIN date ON titre.fichier = date.fichier;


SELECT COUNT(*)
FROM titre
  LEFT JOIN date ON titre.fichier = date.fichier
WHERE date.annee = '2013' AND titre.mot LIKE '%cancer%';


SELECT DISTINCT *
FROM titre
  LEFT JOIN date ON titre.fichier = date.fichier
  LEFT JOIN email ON titre.fichier = email.fichier
WHERE titre.mot LIKE '%robot%' AND date.annee = '2013';