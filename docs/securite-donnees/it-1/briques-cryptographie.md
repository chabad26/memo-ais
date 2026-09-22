# Comprendre les briques de la cryptographie

## Objectif

La cryptographie ne sert pas seulement à « cacher des données ». Elle protège différents aspects de la sécurité de l’information :

- la confidentialité ;
- l’intégrité ;
- l’authenticité ;
- la disponibilité, indirectement, via la protection des clés et des moyens de récupération.

L’objectif de cette synthèse est de comprendre les mécanismes fondamentaux utilisés dans les services que vous administrez déjà : SSH, HTTPS, VPN, Wi‑Fi, sauvegardes, certificats, disques chiffrés, mots de passe, etc.

---

## 1. La triade CIA

La sécurité de l’information est souvent décrite avec trois propriétés :

| Propriété | Définition | Exemple |
| --- | --- | --- |
| Confidentialité | Seules les personnes ou systèmes autorisés peuvent accéder à l’information. | Chiffrement d’un disque, TLS, VPN |
| Intégrité | Les données ne peuvent pas être modifiées sans detection. | Contrôle de somme, signatures, hash |
| Disponibilité | Les données et services restent accessibles quand ils sont nécessaires. | Sauvegardes, redondance, clés de récupération |

### Cas pratiques

- Un disque chiffré protège surtout la confidentialité en cas de vol.
- Une sauvegarde chiffrée protège la confidentialité, mais si la clé est perdue, la disponibilité peut être menacée.
- Une mise à jour logicielle doit être vérifiée pour garantir son intégrité et son authenticité.

### Authenticité

La cryptographie sert aussi à vérifier l’origine d’une information ou d’une entité :

- l’auteur d’un message ;
- la provenance d’un certificat ;
- l’identité du serveur auquel on se connecte.

La confidentialité, l’intégrité et l’authenticité sont les piliers de la sécurité cryptographique moderne.

---

## 2. L’aléa : la base de la sécurité des clés

La cryptographie repose sur des valeurs difficiles à prévoir. On parle d’aléa.

### Problème de clé prévisible

Si un système choisit une clé dans seulement 100 possibilités, un attaquant peut tester toutes les valeurs. Le chiffrement peut être parfait en théorie, mais si la clé est prévisible, la sécurité est compromise.

### Exemples d’utilisations de l’aléa

- génération de clés de chiffrement ;
- génération de nonce ;
- création de vecteurs d’initialisation ;
- génération de tokens ;
- création de certificats et de clés de session.

### À retenir

L’aléa n’est pas une simple « valeur random ». Il faut un générateur cryptographiquement sûr, capable de produire des valeurs difficiles à prédire.

---

## 3. Le chiffrement symétrique

Le chiffrement symétrique utilise une seule clé secrète pour chiffrer et déchiffrer.

```text
Données en clair ── chiffrement ──> Données chiffrées
Données chiffrées ─ déchiffrement ─> Données en clair
```

### Caractéristiques

- même clé pour chiffrement et déchiffrement ;
- très rapide ;
- adapté à de grandes quantités de données ;
- exige que les deux parties partagent le secret.

### Exemple connu

- AES (Advanced Encryption Standard)

### Avantages

- performance élevée ;
- pratique pour protéger des fichiers volumineux ou des flux de données.

### Limite majeure

Le problème clé : si deux machines ne se connaissent pas, comment partagent-elles la même clé secrète sans la divulguer ?

Cela nécessite soit :

- un canal sécurisé pour l’échange de la clé ;
- un mécanisme de distribution sécurisé ou une autre approche cryptographique.

### Si la clé est obtenue par un attaquant

Il peut lire et déchiffrer toutes les données protégées par cette clé.

---

## 4. Le chiffrement asymétrique

La cryptographie asymétrique utilise une paire de clés :

- une clé publique ;
- une clé privée.

### Rôle des clés

| Élément | Peut-il être communiqué ? | Rôle |
| --- | --- | --- |
| Clé privée | Non | Doit rester secrète pour signer ou déchiffrer des données destinées à ce propriétaire. |
| Clé publique | Oui | Permet de chiffrer pour le propriétaire ou de vérifier une signature. |

### Pourquoi publier une clé publique ?

Parce qu’elle ne permet pas de déduire la clé privée associée. Elle est conçue pour être diffusée librement.

### Exemples d’algorithmes

- RSA ;
- ECC (courbes elliptiques).

### Cas d’usage courants

- chiffrement de données pour un destinataire connu ;
- signatures numériques ;
- authentification de serveurs ou d’utilisateurs ;
- échanges de clés sécurisés dans le cadre de protocoles comme TLS.

### Danger

Si la clé privée est compromise, l’attaquant peut :

- déchiffrer les données chiffrées pour cette clé ;
- signer de fausses informations ;
- usurper l’identité associée à cette clé.

---

## 5. Les fonctions de hachage

Une fonction de hachage transforme des données de taille variable en une valeur de taille fixe, appelée empreinte ou digest.

```text
Fichier ── hachage ──> empreinte
```

### Caractéristiques du hachage

- calcul déterministe pour un même input ;
- très sensible au moindre changement ;
- impossible de retrouver le message original à partir du hash ;
- souvent utilisée pour vérifier l’intégrité.

### Exemple

- SHA-256

### Questions clés

- Si le fichier est modifié, le hash change.
- Un hash ne garantit pas la confidentialité du contenu : il ne permet pas de lire le fichier.
- Un hash seul ne suffit pas à prouver qu’un fichier est authentique si un attaquant peut remplacer à la fois le fichier et le hash.

### Utilisations

- vérification de fichiers téléchargés ;
- stockage de mots de passe ;
- construction de MAC ;
- signatures numériques ;
- certificats numériques.

---

## 6. Le MAC : authentification avec un secret partagé

Un MAC (Message Authentication Code) permet de vérifier l’intégrité et l’authenticité d’un message à l’aide d’un secret partagé.

```text
Message + clé secrète ──> MAC
```

### À retenir sur le MAC

- le MAC ne chiffre pas le message ;
- le destinataire doit posséder la même clé secrète ;
- un attaquant qui ne connaît pas la clé ne peut pas produire un MAC valide si le message est modifié.

### Limite importante

Si beaucoup de machines doivent partager la même clé, le mécanisme devient plus complexe à administrer, car chaque participant doit disposer et protéger cette clé partagée.

---

## 7. La signature numérique

La signature numérique permet de vérifier l’origine et l’intégrité d’un document.

Elle combine plusieurs mécanismes :

- hachage du document ;
- chiffrement du hash avec la clé privée ;
- vérification avec la clé publique correspondante.

```text
Document ──> hash ──> chiffrement avec clé privée ──> Signature
```

### Quels éléments interviennent ?

- la fonction de hachage permet de créer une empreinte du document ;
- la clé privée sert à signer ;
- la clé publique permet de vérifier la signature ;
- la signature prouve que le document a bien été émis par le propriétaire de la clé privée et n’a pas été modifié.

### Ce que la signature ne fait pas

Une signature ne chiffre pas le contenu du document. Elle atteste surtout de son origine et de son intégrité.

---

## 8. Les certificats numériques

Une clé publique seule ne suffit pas toujours. Il faut savoir si cette clé appartient réellement à la personne ou au service annoncé.

### Problème

Je reçois une clé publique de `serveur.example.org` ; comment savoir qu’elle appartient bien à ce serveur ?

### Solution

Un certificat numérique associe :

- une identité ;
- une clé publique ;
- une date de validité ;
- un émetteur qui le signe.

### Composants d’un certificat

- identité présentée ;
- clé publique du serveur ou de l’entité ;
- émetteur du certificat ;
- signature du certificat ;
- période de validité.

### Pourquoi la clé privée n’est pas dans le certificat ?

Parce qu’elle doit rester secrète. Le certificat contient la clé publique, pas la clé privée.

### Pourquoi le certificat est-il signé ?

Pour attester que le certificat a bien été émis par une autorité de confiance reconnue.

### Pour vérifier une signature de certificat, il faut

- connaître ou posséder la clé publique de l’autorité de certification ;
- vérifier la chaîne de confiance jusqu’à une racine de confiance.

---

## 9. En résumé

Les mécanismes cryptographiques ne sont pas interchangeables :

- chiffrement symétrique : confidentialité des données, très performant ;
- chiffrement asymétrique : gestion des clés, signatures, échanges sécurisés ;
- fonctions de hachage : intégrité et empreintes ;
- MAC : intégrité et authenticité avec secret partagé ;
- signatures numériques : authenticité et intégrité sans secret partagé ;
- certificats : association d’une identité à une clé publique, validée par une autorité.

La cryptographie ne protège pas tout à elle seule. Elle protège des besoins précis, et le bon choix du mécanisme dépend du contexte.

---

## Ressources

- [Online Tools - Crypto](https://emn178.github.io/online-tools/)
- [Advanced Encryption Standard (AES)](https://www.geeksforgeeks.org/computer-networks/advanced-encryption-standard-aes/)
- [Synthèse AES 128](https://www.emse.fr/~dutertre/documents/synth_AES128.pdf)
- [Wikipedia - RSA](https://fr.wikipedia.org/wiki/Chiffrement_RSA)
- [Introduction to elliptic curves](https://ritzenth.pages.math.cnrs.fr/web/cours/elliptic-curve-course.pdf)

## Notions acquises

- Triade CIA : Confidentialité, Intégrité, Disponibilité
- Aléa
- Chiffrement symétrique
- Chiffrement asymétrique
- Fonction de hachage
- MAC
- Signature numérique
- Certificat numérique
