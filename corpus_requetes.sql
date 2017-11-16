-- Donner les articles parus en 2011.
SELECT *
FROM public.titre
  LEFT JOIN public.date
    ON public.titre.fichier = public.date.fichier
WHERE public.date.annee='2011';