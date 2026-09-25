# Itération 4 - Récupération et génération des clés

## Objectif

Expérimenter la perte contrôlée des informations nécessaires à l'ouverture d'un
volume LUKS, restaurer l'accès à partir d'une sauvegarde et comprendre le rôle
de l'aléa dans la génération des clés.

## Feuille de l'itération

- déployer une VM Linux et préparer un volume LUKS ;
- sauvegarder les éléments nécessaires à sa récupération ;
- provoquer une perte ou une corruption contrôlée ;
- restaurer l'accès et valider les données ;
- distinguer aléa, pseudo-aléa et générateur cryptographiquement sûr.

## Livrable attendu

Une procédure de récupération testée, avec preuves de sauvegarde et de
restauration, sans exposer de secret réel.

- [Provoquer et restaurer un incident LUKS sur openSUSE Leap 16.0](provoquer-restaurer-incident-luks-opensuse.md)
- [Termes à retenir](../../pense-bete/glossaire/securite-donnees/it-4.md)
