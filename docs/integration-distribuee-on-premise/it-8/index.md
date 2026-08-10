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
- [Traiter la compromission du certificat Roundcube](traiter-compromission-certificat-roundcube.md)
- [Retour d'expérience et mise à jour PCA/PRA](retour-experience-pca-pra.md)

## Documentation opérationnelle associée

Le livrable de crise est conservé dans le dépôt d'exploitation :

- `/home/oliv/on-premise/documentation/incident-majeur-ldap.md`
- `/home/oliv/on-premise/documentation/rapport-restauration-pra.md`
- `/home/oliv/on-premise/documentation/gestion-certificats-roundcube.md`
- `/home/oliv/on-premise/documentation/retour-experience-pca-pra.md`

Les documents PCA/PRA, inventaire, sauvegardes, restauration et supervision
utilisés pendant l'exercice se trouvent aussi dans `/home/oliv/on-premise`.
