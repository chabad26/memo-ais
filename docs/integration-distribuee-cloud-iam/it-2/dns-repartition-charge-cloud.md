# DNS et répartition de charge cloud

!!! info "Durée indicative : 1 h 15"
    La partie obligatoire porte sur un enregistrement DNS et sa vérification.
    Le load balancer est une extension conditionnelle.

## Objectif

Faire pointer un nom de domaine vers une ressource cloud et vérifier la
résolution. Comprendre ensuite la différence entre DNS et répartition de charge.

## Pré-requis et état réel

Préparer une zone DNS administrable, l'adresse publique de la VM et un service
HTTP ou HTTPS réellement démarré si un test applicatif est prévu.

Dans le prototype OVH, les VM sont joignables par Ansible mais aucun domaine ni
enregistrement DNS réel n'est documenté. La résolution reste donc à réaliser et
à prouver.

!!! warning "Adresse publique et pare-feu"
    Une adresse publique peut changer. Le DNS ne corrige pas un pare-feu qui
    bloque le service. Le prototype autorise actuellement SSH uniquement avec
    UFW : ouvrir HTTP/HTTPS nécessite une décision explicite.

## Types d'enregistrements

| Type | Exemple | Usage |
| --- | --- | --- |
| A | `web.example.tld -> 203.0.113.10` | Pointer vers une IPv4. |
| AAAA | `web.example.tld -> 2001:db8::10` | Pointer vers une IPv6. |
| CNAME | `www.example.tld -> web.example.tld` | Créer un alias vers un nom. |

Pour la VM OVH, un enregistrement A est le choix pédagogique le plus direct.

## Étape 1 - Créer l'enregistrement DNS

Dans le gestionnaire DNS du domaine, ou dans la zone OVHcloud :

1. ouvrir la zone DNS ;
2. ajouter un enregistrement A ;
3. choisir un nom, par exemple `cloud` ou `web` ;
4. renseigner l'IPv4 publique de la VM ;
5. choisir un TTL, par exemple 300 secondes pour un laboratoire ;
6. enregistrer la modification.

Fiche à compléter avec les valeurs réelles :

| Élément | Valeur |
| --- | --- |
| Zone DNS | `A_COMPLETER` |
| Nom complet | `A_COMPLETER` |
| Type | `A` ou `CNAME` |
| Cible | `IP_PUBLIQUE_VM` ou `NOM_CIBLE` |
| TTL | `A_COMPLETER` |
| Date et heure | `A_COMPLETER` |

Ne pas publier une adresse ou une information de compte inutile à la preuve.

## Étape 2 - Vérifier la résolution

Depuis le poste d'administration :

```bash
dig +short cloud.example.tld A
dig cloud.example.tld A
nslookup cloud.example.tld
```

Comparer avec deux résolveurs publics :

```bash
dig @1.1.1.1 +short cloud.example.tld A
dig @8.8.8.8 +short cloud.example.tld A
```

La réponse attendue contient la cible configurée. En cas d'absence, contrôler
la zone autoritative, le nom complet, le TTL et la propagation.

Si HTTP est volontairement exposé :

```bash
curl -I http://cloud.example.tld
```

Une résolution réussie ne prouve pas que le service HTTP répond. Conserver les
sorties `dig` et `curl` comme deux preuves distinctes.

## Étape 3 - Documenter une bascule

Pour un test contrôlé :

1. relever l'ancien enregistrement et son TTL ;
2. modifier la cible vers une seconde adresse de laboratoire ;
3. relever l'heure de modification ;
4. interroger plusieurs résolveurs ;
5. remettre la cible initiale.

Pendant la propagation, différents clients peuvent encore recevoir l'ancienne
adresse. Cette bascule DNS ne constitue pas une haute disponibilité complète.

## DNS et load balancer

Plusieurs enregistrements A peuvent produire une répartition DNS rudimentaire,
mais le DNS ne suit pas chaque connexion et ne retire pas automatiquement une
VM défaillante sans mécanisme de santé.

| Besoin | Solution |
| --- | --- |
| Nom stable vers une VM | DNS A ou CNAME |
| Plusieurs cibles simples | Plusieurs A, avec limites documentées |
| Santé des backends et distribution des connexions | Load balancer |
| Bascule conditionnelle | DNS avec health checks et failover |

## Extension - Deux VM derrière un load balancer

Avec deux services web actifs, placer les VM derrière un load balancer OVH ou
un service équivalent. Vérifier l'état de santé des backends, le port contrôlé,
le protocole, le TLS et le comportement après arrêt d'une VM.

Cette extension est optionnelle et peut consommer un quota ou générer une
facturation. Elle n'est pas réalisée tant que sa configuration et ses tests ne
sont pas prouvés.

## État final attendu

| Point de contrôle | Statut initial |
| --- | --- |
| Zone DNS contrôlée | À confirmer |
| Enregistrement A ou CNAME | À réaliser |
| Résolution avec `dig` | À prouver |
| Résolution avec un second résolveur | À prouver |
| Réponse HTTP/HTTPS | Conditionnelle |
| Bascule d'adresse | Optionnelle |
| Load balancer avec deux VM | Extension non obligatoire |

## Preuves à conserver

- capture de l'enregistrement DNS sans secret ;
- sortie `dig` ou `nslookup` datée ;
- test depuis au moins deux résolveurs ;
- sortie `curl` séparée si le service est exposé ;
- TTL, heure et observations lors d'une bascule ;
- pour l'extension, état des backends et test après arrêt d'une VM.

## Ressources

- [OVHcloud - documentation DNS](https://help.ovhcloud.com/)
- [AWS Route 53 - choix des enregistrements avec health checks](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-how-route-53-chooses-records.html)
- [AWS Route 53 - configuration du failover DNS](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring.html)
