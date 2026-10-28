# Stratégie de sauvegarde


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/backup-strategy.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Principes

La stratégie cible la règle 3-2-1 : trois copies, deux emplacements ou supports
distincts et une copie hors de l'hôte principal. Le dépôt Borg local est
chiffré, contrôlé et testé par restauration. La copie hors hôte reste une
mesure à mettre en œuvre ; la règle 3-2-1 n'est donc pas encore entièrement
démontrée.

## Plan retenu

| Élément | Fréquence | Rétention | Chiffrement | Vérification |
|---|---|---|---|---|
| LDAP : LDIF et volumes | Chaque nuit | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles | Oui | Import mensuel isolé |
| Partages Samba | Chaque nuit | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles | Oui | Restauration mensuelle d'un fichier et de ses droits |
| Boîtes Dovecot | Chaque nuit | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles | Oui | Restauration mensuelle d'une boîte IMAP |
| Base Roundcube | Chaque nuit | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles | Oui | Import mensuel temporaire |
| Configurations | Après chaque modification et commit | Historique Git et 6 mensuelles | Archive chiffrée | Reconstruction trimestrielle |
| VALEUR RETIRÉE | VALEUR RETIRÉE | VALEUR RETIRÉE | VALEUR RETIRÉE | VALEUR RETIRÉE |
| Documentation et Git | À chaque commit | Historique Git et 6 mensuelles | Archive chiffrée | Restauration trimestrielle |

## Exclusions

- images et conteneurs Docker reconstructibles ;
- réseaux Docker ;
- caches et fichiers temporaires ;
- sessions Roundcube ;
- index Dovecot reconstructibles ;
- journaux arrivés à expiration ;
- file Postfix en fonctionnement normal, afin de ne pas réinjecter des
  messages anciens ou déjà délivrés.

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
reprise ne sont jamais exclus.

## Intégrité et restauration

Chaque sauvegarde doit produire un code retour, un journal, une date, une
taille et un contrôle d'intégrité. Le contrôle actuel retourne un code non nul
et écrit un journal en cas d'échec. Son raccordement à une supervision ou à
une alerte externe reste à réaliser.

- mensuellement : restauration d'un utilisateur LDAP, d'un fichier Samba,
  d'une boîte IMAP et de la base Roundcube ;
- trimestriellement : reconstruction des services depuis Git et les archives ;
- annuellement : exercice PRA complet avec mesure des délais ;
- après incident ou évolution majeure : nouveau test du service concerné.

## Compatibilité PCA/PRA

La sauvegarde LDAP nocturne respecte l'exigence historique du PCA et limite la
perte maximale à environ 24 heures. Les sauvegardes quotidiennes de Samba et de
la messagerie sont compatibles avec les objectifs de reprise de 8 heures et
24 heures uniquement si les tests confirment que les restaurations tiennent
ces délais. Le scénario LDAP estime la reprise à 1 h 20 pour un objectif PRA de
2 heures ; ce délai doit encore être mesuré lors d'un exercice complet.
