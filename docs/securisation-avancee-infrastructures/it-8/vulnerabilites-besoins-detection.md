# Des vulnérabilités aux besoins de détection

**Itération 8 — 8 octobre 2026 — Travail individuel — 1 h**

## 🎯 Objectif et méthode

Pour chaque constat d’audit, déterminer ce que Suricata pourrait observer
si une exploitation était tentée. Distinguer composant vulnérable, chemin
exploitable, trafic visible et preuve d’une action réussie.

Sources : [rapport J1–J3](../it-3/finaliser-rapport-plan-remediation.md),
[registre consolidé](../it-3/consolider-trois-sources-audit.md),
[qualification des CVE Trivy](../it-3/analyser-verifier-resultats-trivy.md) et
[bilan après remédiation](../it-5/finaliser-compte-rendu-durcissement-verification.md).
Les états J1–J3 sont **historiques** : migration, durcissement SSH/Docker,
auditd, arrêt CUPS et changement d’identifiants sont documentés ultérieurement.
Ne pas remettre ces anciens défauts dans le laboratoire pour les exploiter.

Le point actuel est **virbr0 sur l’hôte**, VM `192.168.122.229`.
HTTP/8080 et DNS/TLS sortants sont observés ; quatre signatures génériques
ont déclenché sur un serveur temporaire/18080. Aucune signature spécifique
aux constats ci-dessous n’est validée par ces seuls tests.

## 1. Composants et conditions nécessaires

| Constat sélectionné | Composant et état initial | Conditions d’exploitation à établir | Situation et portée |
| --- | --- | --- | --- |
| C01 — Correctifs containerd manquants | containerd 1.7.24 sur la VM Ubuntu, utilisé par Docker | Avis précis, fonction vulnérable, accès au runtime ou contenu traité ; socket restreint et absence d’exposition réseau directe relevés | Écart de version confirmé ; fonctions exploitables non démontrées. Relever version actuelle après migration |
| C02 — Docker/BuildKit | Docker 26.1.3 initial et moteur de construction potentiel | Construction effectivement utilisée, entrée/contextes non fiables et conditions de l’avis applicable | Usage BuildKit à vérifier ; ne pas assimiler une requête File Browser à une construction d’image |
| C03/C04 — SSH ancien et permissif | OpenSSH 8.2p1 initial, service TCP 22 ; mot de passe et transferts autorisés au relevé initial | Joignabilité ; pour attaque de compte, accès valide/faible ou répétition de tentatives ; pour CVE, version complète et options exactes. GSSAPI désactivé écarte les scénarios qui l’exigent | Écart/configuration historiques ; durcissement par clé réalisé ensuite. Aucun succès d’un tiers prouvé |
| C06 — CUPS sans usage identifié | Service initial limité à localhost | Accès local ou rebond/proxy autorisant de joindre cette écoute ; défaut précis à qualifier | Ne pas inventer une exposition distante sur 631 ; service arrêté/masqué dans les travaux suivants |
| C10 — Application root et montage RW | File Browser initial UID 0, capacités actives, documents accessibles en écriture | Compromission applicative ou compte disposant des fonctions utiles ; chemins/droits réellement accessibles | Amplifie l’impact plutôt qu’une CVE autonome ; privilèges réduits ensuite, accès aux données à contrôler |
| C12 — Image ancienne / Go, Alpine | File Browser 2.15.0, Alpine 3.13.4, Go 1.16.2 initiaux | Identifier la copie de composant, son usage réel et une entrée attaquable ; fin de support seule n’a pas de paquet d’exploitation reconnaissable | Migration vers 2.63.23 documentée ; maintenance et alertes résiduelles restent à qualifier |
| CVE-2022-23806 — résultat initial à vérifier | crypto/elliptic dans l’ancien binaire Go | Montrer l’appel de la fonction affectée à partir de valeurs contrôlées par un attaquant ; présence du symbole ne démontre pas ce chemin | Qualification J3 ouverte ; aucune applicabilité actuelle ni signature réseau démontrée |
| C13 — Identifiants initiaux | Compte administrateur File Browser initialement accessible par identifiants par défaut | Joindre le service et utiliser un compte encore configuré avec ces valeurs | Constat ajouté au bilan initial ; ancien accès ensuite refusé. Ne pas republier les secrets ni réactiver le défaut |

Les autres résultats Trivy déjà écartés dans leur périmètre (CVE-2020-26160,
CVE-2021-44716, CVE-2021-3711, CVE-2022-37434) ne sont pas réintroduits comme
failles exploitables : code/protocole/bibliothèque utilisés ne satisfaisaient
pas les conditions étudiées. Une exclusion reste à revoir si le contexte change.

## 2. Conclusions — Que pourrait observer Suricata ?

| Vulnérabilité / problème | Activité possible | Visible par Suricata ? | Élément potentiellement détectable |
| --- | --- | --- | --- |
| C01 — runtime containerd | Action locale contre le runtime ; éventuel téléchargement préalable ou connexion sortante après compromission | Non pour appels locaux/socket Unix ; seulement les échanges passant par virbr0 | Destination/protocole/volume sortant inhabituel ; indice indirect, pas preuve d’exploitation containerd |
| C02 — BuildKit | Construction avec entrée non fiable, accès indu à des fichiers, récupération distante de dépendances | Opérations locales non ; récupération distante éventuellement | Flux vers dépôts/destinations inhabituelles si visibles ; logs de build et runtime nécessaires pour qualifier |
| C03/C04 — SSH | Nombreuses connexions, tentative d’accès puis commandes/rebond | Connexions et négociation observables si trajet capturé ; identifiants/commandes chiffrés non lisibles | Source non attendue, fréquence de connexions, bannière/métadonnées SSH ; corréler auth.log/journald pour échecs et succès |
| C06 — CUPS localhost | Tentative locale ou depuis un tunnel de joindre le service | Trafic loopback VM absent de virbr0 ; tunnel extérieur visible mais pas forcément sa destination interne | Pas de détection directe fiable ici ; logs et écoute locale à vérifier |
| C10 — root et documents RW | Modification/suppression de documents après compromission ; éventuel téléchargement/exfiltration | Requête HTTP en clair sur 8080 potentiellement ; écritures locales non | Méthode/URI, volume, source et destination ; aucune preuve réseau directe d’UID, de droits ou de modification effective |
| C12 — image obsolète | Exploitation d’un défaut applicatif réellement applicable | Selon protocole, chemin et entrée ; obsolescence non détectable en soi | Motif précis si qualifié et décodable ; bannière éventuelle n’établit pas la version corrigée ni l’applicabilité |
| CVE-2022-23806 initiale | Entrée contrôlée atteignant la fonction cryptographique affectée, si chemin démontré | Non déterminable avec les preuves actuelles | Aucune signature proposée sans chemin d’appel et encodage réseau ; une anomalie/rupture de flux seule ne suffit pas |
| C13 — compte initial faible | Requête de connexion et opérations administratives via compte compromis | HTTP visible en clair ; TLS masque les détails | Endpoint /api/login, cadence, réponse et sources ; éviter de journaliser le corps contenant des secrets. Succès métier à confirmer par logs applicatifs |
| Complément résiduel — accès 8080 non filtré | Connexion depuis une source non prévue, sondes ou accès normal non autorisé | Oui si le trajet passe par virbr0 ; aucune portée Internet prouvée | Comparer source au périmètre autorisé, activité HTTP/flux ; le capteur n’applique pas lui-même le filtrage |

Le complément 8080 a été identifié après J3 : il est indiqué séparément pour
préparer la suite, sans l’attribuer aux audits initiaux.

## 3. Besoins retenus et sources complémentaires

| Besoin proposé | Source réseau | Complément indispensable / limite |
| --- | --- | --- |
| Accès à File Browser depuis sources inattendues | HTTP/flux sur 8080 | Liste de sources autorisées, NAT éventuel et matrice CV04 ; ne pas traiter toute nouvelle source comme malveillante |
| Séries de connexions SSH inhabituelles | Flux/négociation sur 22 | Logs d’authentification pour distinguer simple ouverture TCP, refus et connexion réussie |
| Répétition de refus applicatifs | HTTP sur endpoints concernés | Fonction exacte et logs applicatifs ; 401 sur /api/renew n’est pas un mauvais mot de passe prouvé |
| Sondes HTTP réellement pertinentes | URI/méthode et buffers inspectés | Démontrer l’applicabilité ; les motifs génériques ne prouvent ni exploitation ni lecture de fichier |
| Sorties inhabituelles ou volumes élevés | DNS/TLS/flow | Référence des sorties légitimes, contexte et traces hôte ; HTTPS n’expose pas le contenu téléchargé |
| Actions sur runtime et fichiers | Pas de couverture directe fiable sur virbr0 | auditd, journald, logs Docker/containerd, application et contrôles de droits |

Les accès répétés à `/` sont déjà observés sans alerte dans les bilans affichés.
Une ressource supposée absente retourne 200 ; ne pas baser une règle d’échec
sur une hypothèse de 404. GET /, chargements statiques et contrôles de connectivité
sont une base normale à conserver pour le réglage et les faux positifs.

## 4. Travail à réaliser pendant l’heure

1. Relever état J1–J3 et source de chaque constat, puis état actuel connu sans rescanner systématiquement ni modifier les services.
2. Pour les CVE retenues, lire l’avis primaire et vérifier version complète, fonction, options et chemin d’entrée. Conserver « À vérifier » si une condition manque.
3. Dessiner trajet de l’activité possible et indiquer interface, protocole, chiffrement, direction et buffer éventuel ; différencier absence de trafic et contenu inaccessible.
4. Choisir signal candidat, contexte normal, faux positifs possibles, source complémentaire et preuve attendue. Aucun exploit n’est nécessaire pour cette analyse.
5. Conserver le tableau ci-dessus comme conclusions documentaires ; les nouvelles règles seront lues et testées dans la suite de l’itération, pas déclarées installées ici.

## 📦 Livrable et limites

Sélection couvrant Ubuntu/runtime, services exposés, File Browser et composants
du conteneur ; conditions, activités possibles, visibilité et signaux proposés.
**Analyse documentaire préparée, pas preuve d’une tentative d’exploitation.**
Aucune CVE n’est déclarée détectable simplement parce qu’elle figure dans Trivy.
Les informations inconnues (versions actuelles, fonctions, chemins et trajets)
restent explicites. Détection, prévention et remédiation sont trois objectifs distincts.

- [Référence officielle SSH Suricata 8.0.3 : bannières et négociation](https://docs.suricata.io/en/suricata-8.0.3/rules/ssh-keywords.html)
- [Qualification locale des CVE et sources primaires associées](../it-3/analyser-verifier-resultats-trivy.md)
- [Rapport d’audit initial](../it-3/finaliser-rapport-plan-remediation.md)
- [Bilan actuel de la détection](../it-7/bilan-dispositif-detection.md)
- [Retour à l’itération 9](index.md)
- [Retour au module](../README.md)
