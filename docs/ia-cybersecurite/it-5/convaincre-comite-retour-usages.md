# Convaincre le comité et revenir sur ses usages

**Séquence 5.6 — Présentiel — Trois minutes par groupe, sans diaporama**

> **Nadia [16:15]** Trois minutes par groupe pour me convaincre. Imaginez que je suis le comité de vendredi 😄

## Mission 1 — Convaincre le comité

Présenter les cinq règles à retenir ; défendre la règle dont le groupe est le plus fier et une situation étudiée qui justifie cette règle ; expliquer ce que la politique aurait changé la nuit du 24 septembre.

La [politique V0.1 et son PDF de quatre pages](la-politique-utilisation-ia.md) sont disponibles. Le texte ci-dessous est une **trame orale proposée**, à adapter au choix et aux contributions du groupe. La présentation réelle n’est pas attestée.

### Trame de trois minutes — sans diaporama

**0:00–0:50 — Les cinq règles.**

« Notre politique permet d’utiliser l’IA avec un cadre clair. Première règle : choisir un outil et un compte professionnels approuvés pour l’usage. Deuxième : retirer les secrets et limiter les données avant toute demande. Troisième : faire relire et tester le code, les commandes et les configurations avant la production. Quatrième : faire approuver les extensions, connecteurs et agents, avec des droits limités. Cinquième : signaler immédiatement un envoi ou un accès suspect, sans sanction pour le seul fait d’avoir signalé de bonne foi. »

**0:50–1:45 — La règle à défendre.**

« Nous proposons de défendre le paragraphe 11 : une demande d’outil reçoit un accusé sous un jour ouvré et une décision sous dix jours ouvrés, avec une alternative métier. Le silence ne vaut pas autorisation. En urgence, manager et RSSI arbitrent une solution interne. Cela répond au problème du J2 : une personne avait attendu trois semaines et commencé à utiliser un outil sans validation. Une interdiction seule n’aurait pas couvert son besoin. Cette règle oblige aussi l’organisation à répondre et à fournir une solution. »

« La situation du J2 a guidé notre relecture : attendre trois semaines sans réponse ne couvre pas le besoin métier. Le paragraphe 11 fixe donc un responsable, un délai et une solution transitoire. »

**1:45–2:40 — Ce qui aurait changé le 24 septembre.**

« Julien aurait eu un chemin de dépannage interne et un référent d’astreinte, au lieu d’utiliser son compte personnel. Les paragraphes 4 et 5 imposent de retirer les deux secrets et de minimiser les journaux et données clients. Le paragraphe 8 exige une seconde relecture et des tests avant d’appliquer une commande en production ; le paragraphe 10 garde la trace du changement. Les paragraphes 2 et 5 excluent le partage public de la conversation métier. Si une exposition survient malgré tout, le paragraphe 12 organise immédiatement l’alerte, le confinement et les personnes à informer. »

**2:40–3:00 — La décision demandée.**

« Nous demandons d’approuver le cadre et ses moyens : catalogue, compte professionnel, support, relecteurs et contrôles vérifiés. L’ouverture de l’espace IA reste conditionnée à ces vérifications ; les outils internes permettent de travailler en attendant. Nous ne prétendons pas que le texte suffit à déployer les contrôles. »

### Correction de la consigne

**Coquille confirmée par l’apprenant : le module ne comporte pas de crash-test.** La présentation s’appuie sur la relecture de la politique et sur les situations étudiées au J2 et dans l’incident de Julien. Aucun résultat de crash-test ni correction associée n’est attendu au carnet.

## Mission 2 — Retour sur mes usages du J1

Source : [inventaire personnel du 19 octobre](../it-1/le-message-de-nadia.md). Deux usages de **Codex**, un seul outil, sont documentés ; aucun autre outil personnel n’est ajouté par supposition. L’évaluation ci-dessous applique la politique proposée comme grille de lecture, sans prétendre qu’elle régit déjà la formation.

| Usage observé | Ce que la politique en dirait | Pourquoi et conditions | Changement proposé dès lundi |
| --- | --- | --- | --- |
| **Codex pour rédiger et structurer le mémo** | **À valider** | Codex n’a pas d’entrée autorisée dédiée dans la liste A ; type de compte, offre et garanties non vérifiés. §2/3/4/11 : faire valider outil, compte et classes de données avant emploi professionnel | Vérifier compte et périmètre autorisé ; préparer des contenus fictifs ou publics minimaux ; ne pas envoyer de pièces internes en attendant l’accord |
| **Codex comme agent dans le dépôt** | **À valider** | Même outil, avec lecture/édition/exécution supplémentaires. §5/7/8/10 : vérifier fichiers accessibles, permissions, commandes, traces et validation des actions à impact. Un accès au dépôt ne prouve pas un accès à une production | Limiter l’espace accessible ; retirer secrets et fichiers sans rapport ; relire les différences et commandes ; vérifier la séparation entre documentation locale et production |

**Interdit dans les deux usages :** fournir des secrets ou traiter des informations Hexalp avec un compte personnel (§3/4), même si l’outil est ensuite approuvé. Le compte n’étant pas identifié, on ne transforme pas cette condition en constat d’écart réel. Un usage non validé ne devient pas autorisé parce que son résultat semble utile.

### Mes pratiques dès lundi — engagements proposés à confirmer

- Vérifier le type de compte et l’autorisation pour le contexte professionnel avant tout envoi.
- Décrire le problème avec un exemple fictif minimal ; garder configurations, journaux bruts et coordonnées internes dans les outils internes.
- Définir le périmètre de fichiers accessible à l’agent ; contrôler ses changements avant de les conserver.
- Faire relire par une seconde personne habilitée toute proposition destinée à la production, avec tests et retour arrière ; pour une modification documentaire locale, conserver une relecture adaptée et les vérifications du dépôt.
- Signaler immédiatement une exposition suspectée, sans recopier le secret ni attendre une preuve d’exploitation.

Ces points sont des engagements de pratique proposés, pas la preuve qu’ils ont déjà été mis en place. L’inventaire personnel reste limité aux usages observés.

## Paragraphe final du carnet — proposition à personnaliser

> Aujourd’hui, je sais mieux distinguer un modèle fondé sur l’apprentissage d’une règle automatisée et expliquer ce qu’ajoutent les outils d’un agent. Je sais analyser un usage d’IA en regardant le fournisseur, le compte, les données, les permissions et les preuves disponibles. Les exercices m’ont appris à regarder les faux positifs, les faux négatifs et la charge de qualification plutôt qu’un pourcentage global. Pour un incident, je peux distinguer exposition, exploitation démontrée et mesure seulement proposée, puis transformer le risque en une règle avec un responsable, un contrôle et une solution métier. Il me reste à vérifier mon propre compte et les garanties des outils, à pratiquer la validation des permissions et la révocation, et à vérifier l’application de la politique sur des situations concrètes. Je dois aussi pouvoir expliquer ces choix sans reprendre aveuglément le texte de l’assistant.

Ce bilan est proposé à partir des travaux documentés ; il ne mesure pas les compétences initiales ni une maîtrise autonome. L’apprenant le corrige selon ce qu’il peut personnellement expliquer et reproduire.

## Remise et limites

Le [PDF de politique](../../assets/files/ia-cybersecurite/it-5/Politique-IA-Hexalp-proposition.pdf) est prêt comme **proposition V0.1**. Le carnet `livrables/ia-cybersecurite/it-5/ia01-j5/carnet_J5.md` contient désormais la préparation orale, le retour sur les deux usages et un bilan proposé. La partie **résultats du relecture et corrections éventuelles** est explicitement à compléter : l’ensemble demandé au formateur ne peut pas encore être annoncé comme entièrement réalisé.

[Retour au J5](index.md) · [Pense-bête](../../pense-bete/glossaire/ia-cybersecurite/it-5.md)
