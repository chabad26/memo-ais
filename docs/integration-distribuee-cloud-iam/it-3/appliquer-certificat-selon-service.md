# 3.7 | Appliquer le bon type de certificat selon le service

!!! info "Durée indicative : 1 h 30"
    Cette activité réutilise la PKI déjà construite dans le module On-premise
    et documente le choix d'un certificat public pour un service exposé.

## Objectif

Réutiliser son autorité de certification interne pour un service privé,
vérifier la confiance côté client et expliquer dans quelles conditions un site
public doit utiliser un certificat reconnu par les navigateurs.

!!! warning "Périmètre de la preuve"
    Les commandes ci-dessous sont des manipulations à retenir. Une commande
    présentée comme exécutée doit être remplacée par une sortie, une capture ou
    un lien de preuve réellement obtenu pendant le TP. Ne publie jamais de clé
    privée, de jeton DNS ou de secret d'AC.

## 1. Vérifier le chiffrement au repos

Le chiffrement au repos protège les données stockées sur les volumes et dans le
stockage objet. Il est distinct du certificat TLS, qui protège les échanges en
transit.

| Ressource | Vérification à effectuer | Preuve attendue |
| --- | --- | --- |
| Volume de VM | Ouvrir les détails du volume ou de l'instance chez le fournisseur | Capture de l'option de chiffrement, sans identifiant sensible |
| Bucket S3 | Ouvrir les informations générales du bucket | Capture indiquant le chiffrement actif |
| État OpenTofu | Vérifier que le backend utilise le bucket prévu | Nom du bucket et clé d'état, jamais les clés S3 |

Si le chiffrement n'est pas actif, ne pas modifier une ressource de production
pendant ce TP. Pour le laboratoire, activer l'option proposée par le
fournisseur, puis consigner la date et la portée de la modification.

!!! note "Limite de la démonstration"
    Le chiffrement côté fournisseur ne dispense pas de protéger les accès IAM,
    les sauvegardes et les clés utilisées pour accéder au stockage.

## 2. Émettre un certificat interne

Le service interne réutilise Step CA et le processus documenté dans le module
On-premise. Il ne faut pas recréer une nouvelle autorité pour chaque VM.

Exemple de préparation pour un service LDAP interne :

```bash
# Exemple à adapter au nom DNS réellement utilisé par le service
step ca certificate ldap.exemple-interne.test ldap.crt ldap.key \
  --provisioner infra
```

Le nom doit apparaître dans le `subjectAltName` du certificat. La clé privée
`ldap.key` doit être transmise au service par un moyen protégé et ne doit pas
être commitée dans Git.

Les noms, provisionneurs et chemins exacts doivent reprendre la configuration
réellement utilisée par la PKI du projet. La procédure complète de génération,
de distribution et de révocation reste documentée dans les fiches
[PKI On-premise](../../integration-distribuee-on-premise/it-6/index.md).

## 3. Configurer et vérifier le service interne

Installer la racine de l'AC sur le client qui doit faire confiance au service,
puis configurer le service avec le certificat et la clé correspondant au même
nom DNS. Le test doit être effectué depuis un client réel du réseau privé.

```bash
openssl s_client -connect ldap.exemple-interne.test:636 \
  -servername ldap.exemple-interne.test \
  -CAfile ca-root.crt </dev/null
```

La validation est satisfaisante si :

- la connexion TLS s'établit ;
- le nom demandé correspond au `subjectAltName` ;
- l'émetteur appartient à la chaîne Step CA attendue ;
- le client ne signale pas d'erreur de confiance ;
- le certificat expire à une date connue et son renouvellement est planifié.

Pour une preuve exploitable, masquer les numéros de série non nécessaires, les
noms de clients et tout contenu de clé privée. Conserver seulement les champs
`subject`, `issuer`, `notBefore`, `notAfter` et `subjectAltName`.

## 4. Documenter le certificat public

Le site exposé publiquement doit utiliser un nom de domaine contrôlé et un
certificat reconnu nativement. Si le laboratoire n'a pas de domaine disponible,
documenter la procédure sans l'exécuter sur une adresse IP.

Exemple avec Nginx et Certbot :

```bash
sudo certbot --nginx -d www.exemple.fr
sudo certbot renew --dry-run
```

Le challenge HTTP-01 nécessite que le domaine résolve vers le serveur et que le
port TCP 80 soit accessible pendant la validation. Le challenge DNS-01 utilise
un enregistrement TXT ; il est utile lorsque le serveur n'est pas directement
accessible, mais les identifiants DNS doivent alors être limités et protégés.

Le renouvellement doit être automatique, mais il faut aussi vérifier qu'il
fonctionne réellement :

```bash
systemctl list-timers | grep -i certbot
sudo certbot certificates
sudo certbot renew --dry-run
```

Ces commandes restent un exemple tant qu'aucun domaine réel du projet n'a été
utilisé et qu'aucune preuve correspondante n'est disponible.

## 5. Aller plus loin : preuve de renouvellement sur un site réel

En tant que développeur freelance, j'ai déjà des sites avec Let's Encrypt.
La capture suivante montre un certificat public actif et une connexion TLS
observée depuis le navigateur :
![Tâches cron d'un site freelance](../../assets/img/integration-distribuee-cloud-iam/it-3/Capture%20d’écran%20du%202026-09-02%2011-04-40.png)

*Preuve complémentaire : une tâche cron est planifiée sur un site freelance
réel. Cette capture montre l'automatisation d'une maintenance applicative ;
elle ne prouve pas à elle seule le renouvellement Let's Encrypt, qui doit être
validé avec `certbot certificates` ou `certbot renew --dry-run`.*

![Certificat Let's Encrypt et connexion TLS dans le navigateur](../../assets/img/integration-distribuee-cloud-iam/it-3/Capture%20d’écran%20du%202026-09-02%2011-12-45.png)

*Preuve complémentaire : le navigateur identifie Let's Encrypt comme autorité
de certification et indique une connexion chiffrée en TLS 1.3. Le site visible
appartient à un environnement freelance réel ; cette capture illustre le
résultat attendu pour un service public, sans constituer une preuve de
déploiement sur DIST-01b.*

> Preuve complémentaire : certificat Let's Encrypt actif sur un site freelance
> réel. Cette capture démontre le principe du renouvellement public ; elle ne
> constitue pas une preuve de déploiement sur l'infrastructure DIST-01b.

## 6. Justification finale

| Service | Choix | Justification |
| --- | --- | --- |
| Flux LDAP ou supervision entre VM | PKI interne Step CA | Les clients sont maîtrisés et peuvent recevoir la racine interne. |
| Site web public avec domaine réel | Let's Encrypt | Les visiteurs externes doivent faire confiance au certificat sans installation manuelle. |
| Site du laboratoire accessible uniquement par IP | Pas de certificat public exécuté | Il manque un nom de domaine validable ; la procédure est documentée seulement. |

## Résultat attendu

- le chiffrement au repos du volume et du bucket a été vérifié ;
- un service interne utilise un certificat de l'AC existante ;
- la confiance TLS est validée depuis un client autorisé ;
- la procédure Let's Encrypt et son renouvellement sont documentés ;
- le choix de certificat est justifié service par service ;
- les preuves sont lisibles et ne contiennent aucun secret.

## Ressources

- [PKI On-premise : vue d'ensemble](../../integration-distribuee-on-premise/it-6/index.md)
- [Let's Encrypt - Comment ça marche](https://letsencrypt.org/fr/how-it-works/)
- [Certbot - Documentation](https://eff-certbot.readthedocs.io/en/stable/)
