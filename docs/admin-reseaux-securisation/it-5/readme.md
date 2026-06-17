# Réponse à incident et automatisation sécurité

## Contexte de l'itération

Une des machines Linux utilisées pour l'analyse de données commence à se comporter de manière étrange :

    forte lenteur,
    ventilateur constamment actif,
    services qui répondent difficilement,
    charge CPU très élevée.

Un administrateur système senior regarde rapidement la machine puis revient vers vous :

« Un cryptomineur. Encore une installation Spark non sécurisée...
Nous sommes en situation de crise. Une bonne occasion de formation pour vous, ceci dit, puisque ce n'est pas un système de production.
Vous avez une journée pour un exercice de gestion de crise. »

« L'installation Spark a été laissée quasiment dans son état par défaut.
Regardez ce que recommande le guide de sécurisation de Spark. Rien de tout cela n'a été fait. »

L'administrateur vous laisse :

    une machine Linux pour l'installation du Spark,
    le guide de sécurité Spark,
    le guide ANSSI de remédiation : [ANSSI](https://messervices.cyber.gouv.fr/guides/cyberattaques-et-remediation-les-cles-de-decision)

Votre rôle :

    analyser les risques liés à l'installation Spark,
    reproduire une situation vulnérable,
    identifier les problèmes de sécurité,
    sécuriser le système,
    appliquer une démarche de réponse à incident,
    mettre en place des mécanismes simples d'automatisation défensive.
