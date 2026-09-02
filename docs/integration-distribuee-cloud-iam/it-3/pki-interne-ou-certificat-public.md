# 3.6 | PKI interne ou certificat public : comment choisir

!!! info "Durée indicative : 45 min"
    Cette fiche aide à choisir la bonne autorité de certification selon les
    clients du service, son exposition réseau et le niveau de contrôle attendu.

## Objectif

Savoir choisir entre une PKI interne et un certificat public comme Let's
Encrypt, puis justifier ce choix avec des éléments techniques vérifiables.

## 1. Le principe

Une PKI comprend notamment une autorité de certification (AC), une chaîne de
confiance, des certificats de serveurs et un cycle de vie : émission,
renouvellement, révocation et remplacement des certificats.

Dans le projet DIST-01a, une PKI interne avec Step CA existe déjà dans le
socle On-premise. Elle reste pertinente pour les services qui ne sont
accessibles qu'à des machines ou des utilisateurs ayant explicitement reçu le
certificat racine.

Un certificat public est signé par une AC déjà reconnue par les navigateurs et
les systèmes courants. Il convient à un service exposé à des clients que
l'organisation ne maîtrise pas, mais nécessite un nom de domaine réel et un
renouvellement automatisé.

## 2. Comparer les deux approches

| Critère | PKI interne | Certificat public |
| --- | --- | --- |
| Clients | VM, applications et postes maîtrisés | Navigateurs et clients externes |
| Confiance | Il faut distribuer la racine interne | Déjà reconnue par défaut |
| Noms utilisés | Domaine interne ou noms de laboratoire | Domaine public contrôlé |
| Contrôle | Contrôle complet de l'émission et de la révocation | Dépendance aux règles de l'AC publique |
| Accès Internet | Pas nécessaire pour les services internes | Nécessaire selon le challenge choisi |
| Exploitation | Renouvellement et distribution à gérer | Renouvellement à automatiser et surveiller |
| Exemple DIST-01b | LDAP, supervision ou flux privés entre VM | Site web réellement publié sur un domaine |

!!! warning "Une adresse IP seule ne suffit pas pour Let's Encrypt"
    L'accès à un site par une adresse IPv4 ne permet pas de demander un
    certificat public pour cette IP dans le cas général. Il faut d'abord un
    nom de domaine contrôlé et une méthode de validation compatible. Pour un
    laboratoire accessible uniquement par IP ou réseau privé, la PKI interne
    est le choix cohérent.

## 3. Méthode de décision

Pour chaque service, répondre aux questions suivantes :

1. Le service est-il accessible depuis Internet ou seulement depuis le réseau
   privé ?
2. Les clients sont-ils maîtrisés et capables de faire confiance à la racine
   interne ?
3. Le service possède-t-il un nom DNS stable figurant dans le SAN du
   certificat ?
4. Qui émet, renouvelle, révoque et remplace le certificat ?
5. Quelle preuve permettra de vérifier que le client contrôle bien la chaîne
   de confiance ?

| Réponse dominante | Choix conseillé |
| --- | --- |
| Réseau privé, clients maîtrisés, contrôle interne nécessaire | PKI interne |
| Service public, clients inconnus, domaine public disponible | Certificat public |
| Service hybride avec accès interne et externe | Deux noms et certificats adaptés, ou un certificat public si le risque est accepté |
| Nom temporaire, adresse IP ou environnement de test | PKI interne ou certificat de laboratoire |

## 4. Application à DIST-01b

Le choix de départ peut être documenté ainsi :

| Service | Exposition | Décision | Justification |
| --- | --- | --- | --- |
| OpenLDAP / LDAPS | Privée entre services | Certificat Step CA | Les clients sont les VM et applications du projet ; la racine peut être distribuée par Ansible. |
| Supervision | Privée ou tunnelisée par SSH | Certificat Step CA | Kibana et les interfaces d'administration ne sont pas destinés au public. |
| Administration de la PKI | Privée | Certificat Step CA | Le service doit rester limité aux administrateurs et aux hôtes autorisés. |
| Site web public | Internet avec nom DNS | Let's Encrypt ou autre AC publique | Les navigateurs externes doivent reconnaître le certificat sans installation manuelle. |

Cette décision ne remplace pas les procédures de la PKI On-premise : elle les
réutilise pour les services internes. Les fichiers de configuration, clés
privées et certificats non destinés à être publics restent hors du dépôt Git.

## 5. Validation attendue

### Vérifier un certificat interne

Depuis un client ayant reçu la racine de Step CA, contrôler le nom et la chaîne
du certificat :

```bash
openssl s_client -connect ldap.exemple-interne.test:636 \
  -servername ldap.exemple-interne.test -showcerts </dev/null

openssl s_client -connect supervision.exemple-interne.test:443 \
  -servername supervision.exemple-interne.test </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

La sortie doit présenter le bon nom dans `subjectAltName`, une période de
validité cohérente et un émetteur appartenant à la chaîne interne attendue.

### Préparer un certificat public

Pour un domaine réellement contrôlé et résolu vers le service, le principe est
le suivant. Ces commandes sont un exemple à adapter ; elles ne constituent pas
une preuve de déploiement tant qu'elles n'ont pas été exécutées et validées :

```bash
# Exemple HTTP-01 avec Certbot et Nginx
sudo certbot --nginx -d www.exemple.fr

# Vérifier le renouvellement sans modifier le certificat réel
sudo certbot renew --dry-run
```

Le port TCP 80 doit être accessible pour le challenge HTTP-01. Une alternative
DNS-01 utilise un enregistrement TXT et convient lorsque le service web n'est
pas directement accessible, mais elle demande de protéger les identifiants du
fournisseur DNS.

## 6. Résultat attendu et preuves

- chaque service possède une décision PKI justifiée ;
- les certificats internes sont reconnus par les clients prévus ;
- un certificat public n'est envisagé qu'avec un domaine réel et un mécanisme
  de renouvellement ;
- les dates d'expiration et les responsables du renouvellement sont identifiés ;
- les captures ne montrent ni clé privée, ni jeton DNS, ni secret AC.

Une preuve utile peut être une sortie `openssl` expurgée, une capture de la
chaîne de confiance ou un test de renouvellement réussi. Le contenu sensible
des certificats et des fichiers de clés doit rester masqué.

## Ressources

- [Let's Encrypt - Comment ça marche](https://letsencrypt.org/fr/how-it-works/)
- [Step CA - Documentation](https://smallstep.com/docs/step-ca/)
- [OVHcloud - Chiffrement des volumes](https://help.ovhcloud.com/csm/fr-public-cloud-compute-encryption?id=kb_article_view&sysparm_article=KB0051535)
- [AWS - Chiffrement EBS](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption.html)
