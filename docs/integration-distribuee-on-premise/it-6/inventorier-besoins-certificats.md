# Identifier les besoins en certificats numériques

## Objectif

Reprendre l'infrastructure construite lors des itérations précédentes afin
d'identifier les services qui devront utiliser un certificat numérique.

Cette activité est une analyse : aucun certificat n'est délivré, aucune
configuration TLS n'est modifiée et aucun service n'est redémarré. La
proposition doit être validée par le formateur avant la conception de la PKI.

## 1. Méthode d'analyse

Pour chaque service, identifier :

1. le nom DNS réellement utilisé par le client ;
2. le protocole qui doit être chiffré et authentifié ;
3. le certificat présenté par le serveur ou la confiance requise par le client ;
4. les clients, applications ou services qui doivent reconnaître la CA interne.

Un certificat ne protège pas un conteneur en lui-même. Il protège une connexion
TLS identifiée par un nom DNS figurant dans le SAN du certificat.

## 2. Inventaire des certificats nécessaires

| Service concerné | Protocole sécurisé utilisé | Utilisation du certificat | Clients ou services qui devront lui faire confiance |
| --- | --- | --- | --- |
| Step CA `ca.campus.test` | HTTPS, port 443 | Authentifie l'autorité de certification et protège les demandes de certificats. | Administrateurs PKI, hôtes Linux et automatisations qui interrogent la CA. |
| OpenLDAP | LDAPS, port 636, ou LDAP avec StartTLS | Authentifie l'annuaire et chiffre les recherches ainsi que les identifiants techniques. | Postfix, Dovecot, Samba avec `ldapsam`, LAM et administrateurs LDAP. |
| Postfix | SMTP Submission avec STARTTLS, port 587, et SMTP TLS | Authentifie le serveur d'envoi et protège les identifiants ainsi que les messages en transit. | Clients de messagerie, Roundcube, relais SMTP internes et Dovecot selon le flux. |
| Dovecot | IMAPS, port 993, ou IMAP avec STARTTLS | Authentifie le serveur de boîtes aux lettres et protège les identifiants et messages. | Clients de messagerie et Roundcube. |
| Roundcube | HTTPS, port 443 via un serveur Web ou reverse proxy | Authentifie le webmail et protège la session navigateur. | Navigateurs des utilisateurs et administrateurs. |
| LDAP Account Manager | HTTPS, port 443 via un serveur Web ou reverse proxy | Authentifie l'interface d'administration LDAP et protège les identifiants administrateur. | Navigateurs des administrateurs LDAP. |
| Kibana | HTTPS, port 443 ou port publié sécurisé | Authentifie l'interface de supervision et protège les recherches de journaux. | Navigateurs des administrateurs et exploitants. |
| Elasticsearch | HTTPS sur l'API | Authentifie l'API et chiffre les échanges avec Kibana et Filebeat. | Kibana, Filebeat et administrateurs qui utilisent l'API. |
| Nginx ou WordPress publié | HTTPS, port 443 | Authentifie le site Web et protège les sessions et formulaires. | Navigateurs des utilisateurs concernés. |

## 3. Services sans certificat serveur dans le périmètre initial

| Élément | Décision | Justification |
| --- | --- | --- |
| MariaDB interne | Pas de certificat serveur prévu dans un premier temps | La base reste sur le réseau Compose ; TLS pourra être ajouté si elle est exposée ou séparée de l'application. |
| Samba SMB | Pas de certificat X.509 prévu pour le partage SMB actuel | Le périmètre porte sur la sécurisation LDAP associée ; Kerberos ou SMB signing relèvent d'une analyse distincte. |
| Filebeat | Ne présente pas de certificat dans le laboratoire actuel | Il devient client TLS lorsqu'Elasticsearch est sécurisé et doit alors faire confiance à la CA. |

Cette distinction évite de confondre un service qui présente un certificat avec
un service client qui doit uniquement faire confiance à la CA interne.

## 4. Chaîne de confiance proposée

```text
Campus CA
  -> certificat racine public distribue aux clients concernes
     -> certificat de chaque service avec son nom DNS dans le SAN
        -> verification du nom, des dates et de la chaine par le client
```

Les clients reçoivent uniquement le certificat racine public et son empreinte
SHA-256 par un canal fiable. Les clés privées, les mots de passe de la CA et les
secrets de provisionneur ne quittent jamais le serveur Step CA.

## 5. Proposition à présenter au formateur

Présenter :

1. le tableau d'inventaire des services ;
2. les noms DNS à retenir pour les certificats ;
3. la liste des clients qui devront recevoir le certificat racine ;
4. les services explicitement exclus du premier périmètre ;
5. l'absence de déploiement pendant cette activité.

## Résultat

L'inventaire identifie les besoins de certificats pour la CA, l'annuaire,
la messagerie, les interfaces Web et la supervision. Il distingue les serveurs
qui présentent un certificat des clients qui doivent seulement faire confiance
à Campus CA.

## Termes à retenir

- **TLS** : protocole qui chiffre une connexion et vérifie l'identité du
  serveur grâce à un certificat.
- **Certificat numérique** : document signé qui associe une identité, telle
  qu'un nom DNS, à une clé publique.
- **Chaîne de confiance** : relation entre un certificat de service, son
  émetteur intermédiaire et le certificat racine reconnu par le client.
- **SAN** : liste des noms DNS ou adresses couverts par un certificat.

## Ressources

- [Concevoir l'architecture de certification](concevoir-architecture-certification.md)
- [Préparer la sécurisation TLS de la messagerie](../it-4/securiser-messagerie-tls.md)
- [Déployer Elasticsearch et Kibana](../it-7/deployer-elasticsearch-kibana.md)
