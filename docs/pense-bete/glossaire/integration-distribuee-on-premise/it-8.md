# Glossaire Integration distribuee on-premise - Iteration 8

## Sujet

Gestion de crise LDAP, restauration depuis sauvegarde et reprise progressive des
services dependants. La partie certificats Roundcube n'a pas ete traitee dans ce
poste ; elle est seulement mentionnee comme cas conditionnel.

## Termes a retenir

| Terme | Definition courte |
| --- | --- |
| Crise | Incident majeur qui impose une coordination avant les actions techniques. |
| Serveur compromis | Systeme considere non fiable et conserve pour analyse. |
| Forensique | Analyse des traces apres incident, sans modifier les preuves. |
| PCA | Plan qui organise la continuite minimale pendant l'incident. |
| PRA | Plan qui organise la reprise des services apres incident. |
| RTO | Duree maximale ou observee avant retour d'un service. |
| RPO | Perte de donnees maximale ou observee depuis la derniere sauvegarde saine. |
| Archive saine | Sauvegarde anterieure a la compromission et utilisable pour restaurer. |
| LDIF | Format texte utilise pour exporter/importer des entrees LDAP. |
| Reprise progressive | Remise en service dans l'ordre des dependances, avec verification a chaque etape. |
| Certificat compromis | Cas non realise ici : certificat a revoquer et a remplacer si sa cle n'est plus fiable. |

## Manipulations faites

| Manipulation | Commande ou action |
| --- | --- |
| Declarer la crise | Reunir l'equipe, attribuer les roles et valider le plan avant intervention. |
| Isoler LDAP | Arreter ou isoler le serveur compromis sans nettoyer ses donnees. |
| Preserver les preuves | Conserver volumes et journaux pour une analyse ulterieure. |
| Lire les journaux | Extraire les logs dans un fichier externe pour rechercher la date de compromission. |
| Chercher la sauvegarde | Identifier l'archive Borg la plus recente consideree saine. |
| Verifier la sauvegarde | Controler la presence de la configuration `.tar.gz` et des exports `.ldif`. |
| Extraire l'archive | Utiliser `borg extract` dans un repertoire temporaire controle. |
| Controler les LDIF | Verifier taille et contenu des fichiers utilisateurs/groupes avant import. |
| Reconstruire LDAP | Relancer un conteneur LDAP sain, puis importer utilisateurs et groupes. |
| Tester LAM | Verifier la connexion LAM vers LDAP et la presence de l'arborescence restauree. |
| Redemarrer les services | Reprendre Samba, messagerie, applications, sauvegarde et supervision sous surveillance. |
| Annoncer le cas certificats | Si des certificats avaient ete compromis : revoquer, regenerer, redeployer, verifier cote client. |

## Points de vigilance

- Ne pas reparer directement le serveur compromis : il peut contenir des preuves.
- Ne pas ecraser les volumes compromis avant isolement ou copie controlee.
- `borg extract` reconstruit l'arborescence dans le repertoire courant.
- Une sauvegarde recente n'est pas forcement saine ; elle doit etre comparee a
  la chronologie de compromission.
- LDAP revient avant les services qui dependent de ses comptes et groupes.
- Documenter ce qui n'a pas ete traite : ici, les certificats Roundcube sont
  seulement annonces comme cas possible, pas comme manipulation realisee.

## Docs associees

- [Vue d'ensemble de l'iteration 8](../../../integration-distribuee-on-premise/it-8/index.md)
- [Gestion de crise LDAP](../../../integration-distribuee-on-premise/it-8/gestion-crise-ldap.md)
- [Restaurer l'infrastructure avec le PRA](../../../integration-distribuee-on-premise/it-8/restaurer-infrastructure-pra.md)
- [Retour d'experience et mise a jour PCA/PRA](../../../integration-distribuee-on-premise/it-8/retour-experience-pca-pra.md)
