# Sécurité des données

## Objectif global

Ce module étudie les mécanismes cryptographiques qui protègent les données
d'une infrastructure : données en transit, données au repos, sauvegardes et
clés nécessaires à leur récupération.

L'objectif n'est pas de concevoir des algorithmes, mais de comprendre leurs
principes et leurs limites afin de configurer, administrer et vérifier des
solutions cryptographiques. Le module réutilise les infrastructures Linux,
réseau, sauvegarde et cloud construites précédemment.

## En fin de module

Vous serez capables de :

- expliquer les principaux mécanismes cryptographiques et choisir celui qui
  répond à un besoin de confidentialité, d'intégrité ou d'authenticité ;
- vérifier une configuration TLS et sa chaîne de confiance ;
- mettre en œuvre et récupérer un stockage chiffré avec LUKS ;
- identifier les conditions nécessaires à une génération et une conservation
  sûres des clés ;
- organiser le cycle de vie des clés à l'échelle d'un parc.

## Progression

1. **Comprendre** les fondamentaux cryptographiques et les recommandations de
   sécurité applicables.
2. **Observer et vérifier** la protection des données en transit avec TLS.
3. **Mettre en œuvre** le chiffrement des données au repos avec LUKS.
4. **Casser et récupérer** un stockage chiffré, puis étudier l'aléa et la
   génération des clés.
5. **Industrialiser** la gestion des clés avec TPM2, Clevis/Tang et les
   services de gestion de clés cloud.

## Livrables

- analyse cryptographique d'une configuration existante au regard des
  recommandations ANSSI ;
- stockage chiffré LUKS sur périphérique loop, documenté et vérifié ;
- procédure de sauvegarde du header, destruction contrôlée et récupération ;
- architecture de gestion des clés d'un parc, avec cycle de vie,
  responsabilités et moyens de récupération.

## Feuille du module

- [Itération 1 - Fondamentaux cryptographiques](it-1/index.md)
- [Itération 2 - Données en transit et TLS](it-2/index.md)
  - [Analyser une configuration avec les recommandations ANSSI](it-2/analyser-configuration-anssi.md)
  - [Comprendre et vérifier une connexion TLS](it-2/connexion-tls.md)
- [Itération 3 - Données au repos et LUKS](it-3/index.md)
  - [Mettre en œuvre et comprendre un stockage chiffré avec LUKS](it-3/mettre-en-oeuvre-stockage-chiffre-luks.md)
  - [Administrer les accès et préparer la récupération d'un volume LUKS](it-3/administrer-acces-preparer-recuperation-luks.md)
- [Itération 4 - Récupération et génération des clés](it-4/index.md)
  - [Provoquer et restaurer un incident LUKS sur openSUSE Leap 16.0](it-4/provoquer-restaurer-incident-luks-opensuse.md)
- [Itération 5 - Gestion des clés à l'échelle d'un parc](it-5/index.md)

## Glossaire

- [Glossaire - fondamentaux cryptographiques](../pense-bete/glossaire/securite-donnees/it-1.md)
- [Glossaire - données en transit et TLS](../pense-bete/glossaire/securite-donnees/it-2.md)
- [Glossaire - données au repos et LUKS](../pense-bete/glossaire/securite-donnees/it-3.md)
- [Glossaire - récupération et génération des clés](../pense-bete/glossaire/securite-donnees/it-4.md)
- [Glossaire - gestion des clés à l'échelle d'un parc](../pense-bete/glossaire/securite-donnees/it-5.md)
