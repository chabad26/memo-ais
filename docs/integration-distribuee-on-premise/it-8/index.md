# Itération 8 - Gestion de crise

Cette itération met en situation l'exploitation du PCA/PRA face à un incident
majeur. L'objectif n'est pas de lancer directement des commandes, mais de
qualifier la crise, préserver les preuves, mesurer les impacts, répartir les
rôles et faire valider un plan d'actions avant toute intervention.

Le scénario porte sur la compromission du service OpenLDAP, devenu une
dépendance centrale pour l'authentification, Samba, la messagerie et
l'administration des identités.

## Feuilles de l'itération

- [Gestion de crise - incident majeur LDAP](gestion-crise-ldap.md)
- [Restaurer l'infrastructure avec le PRA](restaurer-infrastructure-pra.md)
- [Retour d'expérience et mise à jour PCA/PRA](retour-experience-pca-pra.md)

!!! note "Perimetre de l'exercice"
    Le poste realise porte sur la gestion de crise LDAP et la restauration du
    service depuis une sauvegarde saine. La partie compromission/remplacement de
    certificats Roundcube n'a pas ete faite. Si des certificats avaient aussi
    ete declares compromis, il aurait fallu isoler les anciennes cles, revoquer
    les certificats concernes, generer de nouvelles paires cle/certificat,
    redeployer les services TLS et verifier la chaine depuis un client.

## Documentation opérationnelle associée

Le livrable de crise est conservé dans le dépôt d'exploitation :

- `/home/oliv/on-premise/documentation/incident-majeur-ldap.md`
- `/home/oliv/on-premise/documentation/rapport-restauration-pra.md`
- `/home/oliv/on-premise/documentation/retour-experience-pca-pra.md`

Les documents PCA/PRA, inventaire, sauvegardes, restauration et supervision
utilisés pendant l'exercice se trouvent aussi dans `/home/oliv/on-premise`.
