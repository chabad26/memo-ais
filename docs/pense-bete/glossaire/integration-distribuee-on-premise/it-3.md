# Glossaire Intégration distribuée on-premise — Itération 3

## Sujet

Authentification centralisée et partage de fichiers avec Samba et OpenLDAP.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Samba | Service qui fournit des partages de fichiers SMB/CIFS aux clients. |
| SMB/CIFS | Protocole de partage de fichiers utilisé notamment par Windows. |
| `ldapsam` | Backend Samba qui stocke les comptes Samba dans OpenLDAP. |
| Kerberos | Protocole d'authentification par tickets utilisé par Samba AD. |
| Contrôleur de domaine | Serveur qui gère un domaine, ses identités et ses politiques. |
| Partage | Répertoire publié par Samba avec des droits d'accès. |
| ACL | Liste de règles qui contrôle les accès à une ressource. |
| NSS | Mécanisme Linux qui résout les utilisateurs et groupes depuis LDAP. |
| `nslcd` | Service qui permet à NSS de consulter LDAP. |
| `smb.conf` | Fichier de configuration Samba. |

## Manipulations faites

| Manipulation | Commande ou action |
| --- | --- |
| Vérifier Samba | `docker compose exec samba testparm -s` |
| Vérifier LDAP | `docker compose exec openldap ldapsearch ...` |
| Lister les comptes Samba | `docker compose exec samba pdbedit -L` |
| Tester un partage | `docker compose exec samba smbclient -L //localhost -U utilisateur` |
| Vérifier les groupes | `docker compose exec samba getent group` |
| Recharger Samba | `docker compose restart samba` |

## Points de vigilance

- Samba AD et Samba avec `ldapsam` ne reposent pas sur le même backend.
- Les droits doivent être attribués aux groupes, pas directement aux personnes.
- Vérifier `testparm` avant de redémarrer Samba.
- Un mot de passe LDAP de service ne doit pas être écrit dans `smb.conf` ni dans Git.
- Le réseau Docker et les volumes Samba doivent être sauvegardés.

## Docs associées

- [Vue d'ensemble de l'itération 3](../../../integration-distribuee-on-premise/it-3/index.md)
- [Concevoir l'architecture Samba AD et LDAP](../../../integration-distribuee-on-premise/it-3/concevoir-architecture-samba-ad-ldap.md)
- [Intégrer Samba à OpenLDAP](../../../integration-distribuee-on-premise/it-3/integrer-samba-openldap.md)
- [Créer les espaces de partage Samba](../../../integration-distribuee-on-premise/it-3/creer-espaces-partage-samba.md)
