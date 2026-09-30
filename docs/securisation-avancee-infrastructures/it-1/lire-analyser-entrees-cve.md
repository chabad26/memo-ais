# Lire et analyser trois entrées CVE

## Objectif

Utiliser une entrée CVE et ses références pour comprendre rapidement une
vulnérabilité : produit, versions, mécanisme, conséquences et traitement.

**Statut : synthèse documentaire préparée par l'assistant le 30 septembre 2026.**
Les enregistrements JSON et les références citées ont été consultés. Ces trois
cas historiques ne constituent pas des vulnérabilités démontrées sur la VM
File Browser ; aucun scan ni correctif n'a été exécuté pour cette activité.

## Retrouver les entrées et leurs enregistrements JSON

| Vulnérabilité | Entrée CVE.org | Enregistrement dans `CVEProject/cvelistV5` |
| --- | --- | --- |
| Debian OpenSSL | [CVE-2008-0166](https://www.cve.org/CVERecord?id=CVE-2008-0166) | [Fichier GitHub](https://github.com/CVEProject/cvelistV5/blob/main/cves/2008/0xxx/CVE-2008-0166.json) · [JSON brut](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2008/0xxx/CVE-2008-0166.json) |
| Heartbleed | [CVE-2014-0160](https://www.cve.org/CVERecord?id=CVE-2014-0160) | [Fichier GitHub](https://github.com/CVEProject/cvelistV5/blob/main/cves/2014/0xxx/CVE-2014-0160.json) · [JSON brut](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2014/0xxx/CVE-2014-0160.json) |
| Log4Shell | [CVE-2021-44228](https://www.cve.org/CVERecord?id=CVE-2021-44228) | [Fichier GitHub](https://github.com/CVEProject/cvelistV5/blob/main/cves/2021/44xxx/CVE-2021-44228.json) · [JSON brut](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2021/44xxx/CVE-2021-44228.json) |

Les chemins regroupent les fichiers par année puis par tranche de numéros :
`0xxx` pour `0166` et `0160`, `44xxx` pour `44228`. CVE.org nécessite JavaScript
pour afficher ses fiches ; les liens JSON donnent accès au contenu structuré
utilisé pour cette lecture.

Dans chacun des fichiers consultés, les champs utiles sont :

| Champ JSON | Ce qu'il faut en tirer |
| --- | --- |
| `cveMetadata.cveId` et `state` | Identifiant et état de l'enregistrement ; les trois entrées sont `PUBLISHED` |
| `cveMetadata.dateUpdated` | Date de mise à jour de la fiche, à distinguer de la date du correctif |
| `containers.cna.descriptions` | Description du défaut et de ses conséquences |
| `containers.cna.affected` | Produit, plages de versions et éventuelles exceptions |
| `containers.cna.references` | Avis de l'éditeur, bulletins et autres références à recouper |

**Point de lecture :** pour les deux anciennes CVE OpenSSL, `affected` contient
des valeurs `n/a` dans les JSON consultés. Cela ne signifie pas qu'aucun produit
n'est affecté : la description et les avis de sécurité fournissent les précisions.
Les liens `main` peuvent évoluer ; conserver la date de consultation et, pour
une preuve figée, le JSON téléchargé ou un lien vers sa révision GitHub.

## CVE-2008-0166 — Génération aléatoire dans Debian OpenSSL

### Produit et versions concernés

Le paquet **OpenSSL modifié par Debian**, à partir de **`0.9.8c-1`**, est concerné
jusqu'à l'application du correctif de sa branche. Il ne faut pas étendre ce
constat à toutes les versions amont d'OpenSSL : une modification propre à Debian
est en cause. Les correctifs historiques sont **`0.9.8c-4etch3`** pour Etch et
**`0.9.8g-9`** pour Lenny/Sid.
[Source : avis Debian DSA-1571-1](https://lists.debian.org/debian-security-announce/2008/msg00152.html).

### Problème et conséquences en deux phrases

Une modification du paquet rend les nombres pseudo-aléatoires prévisibles,
affaiblissant les clés cryptographiques produites. Un attaquant peut plus
facilement retrouver ces clés, y compris lorsqu'elles ont ensuite été importées
sur un système non vulnérable.

### Référence consultée et traitement

La [référence DSA-1571 présente dans l'entrée](https://www.debian.org/security/2008/dsa-1571)
conduit à l'avis Debian cité ci-dessus. Il demande de **mettre à jour OpenSSL,
puis de régénérer les éléments cryptographiques concernés**. Les clés DSA
utilisées pour signer ou s'authentifier sur les systèmes affectés doivent aussi
être considérées compromises, même si elles ont été générées ailleurs.

**Conséquence pratique :** le correctif ne transforme pas les anciennes clés
faibles en clés sûres. Leur remplacement doit couvrir les services et les
machines où elles ont été distribuées.

## CVE-2014-0160 — Heartbleed

### Produit et versions concernés

La bibliothèque **OpenSSL**, dans le traitement de l'extension Heartbeat de
TLS/DTLS, est concernée : **`1.0.1` à `1.0.1f` incluses**, ainsi que la
préversion **`1.0.2-beta1`**. L'avis annonce les corrections **`1.0.1g`** et
**`1.0.2-beta2`**. Pour un paquet de distribution, vérifier aussi la révision
du paquet et son avis de sécurité.
[Source : avis OpenSSL du 7 avril 2014](https://openssl-library.org/news/secadv/20140407.txt).

### Problème et conséquences en deux phrases

Un contrôle de longueur manquant permet de lire au-delà d'un tampon mémoire
lors du traitement d'un message Heartbeat. Cette fuite peut exposer des clés
privées, des mots de passe, des éléments de session ou des données applicatives.
[Sources : avis OpenSSL](https://openssl-library.org/news/secadv/20140407.txt)
et [explications des découvreurs sur Heartbleed.com](https://heartbleed.com/).

### Références consultées et traitement

L'[avis OpenSSL référencé dans l'entrée](https://www.openssl.org/news/secadv_20140407.txt)
renvoie désormais vers le site `openssl-library.org`. Il prescrit une version
corrigée ; à défaut de mise à jour immédiate, il indique historiquement une
recompilation avec `-DOPENSSL_NO_HEARTBEATS`.

La référence [Heartbleed.com](https://heartbleed.com/), également présente dans
le JSON, complète le traitement : après correction du service, renouveler les
clés potentiellement compromises, faire révoquer et réémettre les certificats
associés, invalider les sessions concernées et renouveler les secrets exposés.

**Conséquence pratique :** arrêter la fuite ne rend pas confidentielles les
informations déjà récupérées par un attaquant. Changer un mot de passe avant de
corriger le service pourrait exposer à nouveau ce secret.

## CVE-2021-44228 — Log4Shell

### Produit et versions concernés

Le composant concerné est **`log4j-core` d'Apache Log4j 2** ; la présence de
`log4j-api` seul ne suffit pas. L'avis Apache distingue les plages suivantes :

| Plage affectée | Premier correctif historique pour cette CVE |
| --- | --- |
| `2.0-beta9` incluse à `2.3.1` exclue | `2.3.1` — Java 6 |
| `2.4` incluse à `2.12.2` exclue | `2.12.2` — Java 7 |
| `2.13.0` incluse à `2.15.0` exclue | `2.15.0` — Java 8 et suivants |

[Source : avis Apache CVE-2021-44228](https://logging.apache.org/security.html#CVE-2021-44228).

### Problème et conséquences en deux phrases

Des données contrôlées par un attaquant et journalisées par l'application peuvent
déclencher une résolution JNDI vers un service distant malveillant. Dans les
conditions d'exploitation, cela permet une exécution de code avec les droits
de l'application.
[Source : enregistrement JSON Log4Shell](https://github.com/CVEProject/cvelistV5/blob/main/cves/2021/44xxx/CVE-2021-44228.json).

### Référence consultée et traitement

La [page de sécurité Apache présente dans l'entrée](https://logging.apache.org/log4j/2.x/security.html)
redirige vers les avis cités ici. **`2.15.0` est un premier correctif historique,
pas une cible de mise à jour à retenir aujourd'hui** : Apache décrit une
correction incomplète dans certaines configurations sous
[CVE-2021-45046](https://logging.apache.org/security.html#CVE-2021-45046).
Choisir une version maintenue qui traite l'ensemble des avis applicables,
via la mise à jour du produit ou de sa dépendance.

!!! note "Un écart dans le JSON à recouper"
    Dans le JSON consulté, la description inclut `2.15.0` dans sa formulation
    générale, alors que `affected[].versions[].changes` la marque `unaffected`.
    L'avis Apache distingue le correctif de CVE-2021-44228 et le cas complémentaire
    CVE-2021-45046. Cette divergence justifie la consultation des références
    plutôt qu'une conclusion tirée d'une seule phrase.

**Conséquence pratique :** si une exploitation a précédé la correction,
rechercher une compromission et traiter les accès persistants ou les secrets
volés. À titre de référence complémentaire, le
[retour d'incident CISA AA22-320A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-320a)
décrit un cas Log4Shell avec vol d'identifiants, déplacements vers d'autres
machines et maintien d'accès par des relais installés sur plusieurs hôtes.
Ce retour d'incident complète l'avis Apache ; il n'est pas présenté comme une
référence issue du JSON étudié.

## Comparaison — Une mise à jour suffit-elle ?

**Non. Une mise à jour peut corriger le défaut logiciel sans supprimer les
conséquences d'une exploitation ou les éléments faibles déjà produits.**

| Cas | Ce que traite le correctif | Ce qui peut rester à traiter |
| --- | --- | --- |
| Debian OpenSSL | Génération de nouveaux éléments cryptographiques avec le défaut corrigé | Anciennes clés faibles et copies distribuées : les remplacer |
| Heartbleed | Lecture indue de la mémoire via Heartbeat | Secrets potentiellement divulgués : renouvellement, révocation des certificats et invalidation des sessions |
| Log4Shell | Voie d'exécution de code liée au défaut corrigé | Compromission antérieure : investigation, suppression des accès persistants et restauration d'un état de confiance |

Ce tableau reprend les traitements décrits par
[Debian](https://lists.debian.org/debian-security-announce/2008/msg00152.html),
[Heartbleed.com](https://heartbleed.com/) et le
[retour d'incident CISA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-320a).

Il faut donc distinguer **correction de la vulnérabilité**, **remplacement des
éléments affectés** et **traitement d'une éventuelle compromission**. La présence
d'une version vulnérable ne prouve pas, à elle seule, qu'un attaquant l'a exploitée.
Les versions de correction citées sont des repères historiques propres à ces
CVE, pas des recommandations de déploiement pour le laboratoire actuel.

## Résultat attendu et preuves à conserver

- Pour chaque CVE : lien CVE.org, chemin JSON, produit et versions, résumé court,
  référence effectivement lue et traitement identifié.
- Date de consultation et copie ou révision du JSON pour garder la lecture vérifiable.
- Réponse argumentée à la question comparative, en distinguant faits sourcés et
  conséquences déduites pour l'administration d'un service.

- [Activité précédente — Vulnérabilité ou autre problème ?](vulnerabilite-ou-autre-probleme.md)
- [Activité suivante — Comprendre CVSS](comprendre-cvss.md)
- [Retour à l'itération 1](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Retour au module](../README.md)
