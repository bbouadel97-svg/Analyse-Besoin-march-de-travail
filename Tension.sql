-- Objectif : Afficher les 5 métiers avec le Taux de Tension le plus élevé pour la dernière année disponible.
SELECT
    T2.nom_metier,
    T1.annee,
    SUM(T1.projets_totaux) AS Total_Projets,
    SUM(T1.projets_difficiles) AS Projets_Difficiles,
    -- Calcul du taux de tension : (Projets Difficiles / Total Projets) * 100
    ROUND((CAST(SUM(T1.projets_difficiles) AS REAL) * 100) / SUM(T1.projets_totaux), 2) AS Taux_Tension_Pct
FROM
    ANALYSE T1
INNER JOIN
    METIER T2 ON T1.code_metier_fk = T2.code_metier
WHERE
    T1.annee = (SELECT MAX(annee) FROM ANALYSE) -- Sélection de la dernière année dans la base
GROUP BY
    T2.nom_metier, T1.annee
HAVING
    SUM(T1.projets_totaux) > 500 -- S'assurer d'analyser les métiers avec un volume suffisant
ORDER BY
    Taux_Tension_Pct DESC
LIMIT 5;