# Relier les détections à MITRE ATT&CK

**Itération 8 — 8 octobre 2026 — Travail individuel**

## 🎯 Objectif

Utiliser MITRE ATT&CK pour décrire les comportements associés à certaines
détections, en partant des événements et des conditions des règles.
**Les rapprochements ci-dessous sont une analyse documentaire : aucune
technique d’attaque n’est démontrée par les seuls tests du laboratoire.**

## 1. Tactique, technique et vulnérabilité

| Notion | Signification | Exemple |
| --- | --- | --- |
| Tactique | Objectif poursuivi par l’adversaire : pourquoi il réalise une action | Initial Access : obtenir un premier accès à l’environnement |
| Technique | Manière d’atteindre un objectif : comment l’adversaire agit | T1190 : exploiter une application accessible publiquement |
| Vulnérabilité | Faiblesse d’un composant ou d’une configuration qui peut être exploitée sous certaines conditions | Défaut de contrôle d’un chemin de fichier |
| Alerte IDS | Correspondance entre le trafic visible et les conditions d’une signature | Présence de `%2e%2e` dans une URI brute |

Les [tactiques Enterprise](https://attack.mitre.org/tactics/enterprise/) et les
[techniques Enterprise](https://attack.mitre.org/techniques/enterprise/)
décrivent respectivement l’objectif et la manière d’agir. Une technique peut
être associée à plusieurs tactiques : retenir celle que le contexte justifie.
Une CVE ne suffit pas à attribuer une technique ; une alerte ne prouve pas
à elle seule l’intention, la réussite ou l’identité d’un attaquant.

## 2. Rapprochements avec les activités du laboratoire

Suricata observe `virbr0` sur l’hôte ; File Browser est joint sur
`192.168.122.229:8080`. Les preuves sont conservées dans la
[feuille de règles locales](rechercher-adapter-regles-detection.md) et les
[observations J7](../it-7/observer-activite-file-browser.md).

| Activité / règle | Technique ATT&CK | Tactique | Pourquoi ce rapprochement ? |
| --- | --- | --- | --- |
| Marqueur `%2e%2e` dans un GET vers File Browser ; SID 1008001 déclenché | [T1190 — Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/), piste conditionnelle uniquement | Initial Access, si tentative d’accès initial par exploitation d’une application publique | Une tentative réelle de traversée visant à exploiter une application publique pourrait relever de T1190. Ici, paramètre inerte et réponse 200 : ni exploitation ni exposition Internet démontrées. Aucun rattachement confirmé |
| Motifs de traversée et `<script` ; signatures génériques J7 sur serveur temporaire 18080 | Non déterminée | Non déterminée | Les signatures reconnaissent des chaînes. Le serveur de test ne démontre ni accès à un fichier sensible ni exécution de script. Un motif XSS ne permet pas à lui seul de choisir une technique |
| Cinq GET `/` successifs ; règle 1008002 | Aucun rapprochement retenu | Non déterminée | Accès normaux répétés ; aucune alerte 1008002 visible dans la capture actuelle. Ni recherche de services ni déni de service démontrés par ce faible volume |
| Réponse `/api/renew` 401 au J7 ; règle 1008003 destinée aux réponses 401 | [T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/), hypothèse écartée avec les preuves actuelles | Credential Access serait pertinente pour une recherche répétée de secrets | Un refus de renouvellement ne prouve pas des essais de mots de passe. Il faudrait des tentatives d’authentification répétées et leur contexte ; aucune alerte 1008003 prouvée ici |
| Accès ponctuel à un autre port de la VM, activité proposée au J7 | [T1046 — Network Service Discovery](https://attack.mitre.org/techniques/T1046/), piste conditionnelle | Discovery, dans un contexte de découverte de services | Un accès isolé peut être une vérification normale. Il faudrait établir une recherche de services, par exemple des sondes sur plusieurs ports ou machines ; pas de campagne de découverte démontrée |
| DNS normal, HTTPS externe et accès usuels aux ressources File Browser | Aucun rapprochement retenu | Non déterminée | Les protocoles et les connexions normales ne prouvent ni commande et contrôle, ni exfiltration, ni utilisation abusive d’un compte |

T1190 décrit l’exploitation pour obtenir un accès initial à un système
accessible depuis Internet ; T1110 décrit la recherche de secrets par essais ;
T1046 décrit la recherche de services réseau. Ces descriptions proviennent des
pages MITRE liées dans le tableau, consultées le **8 octobre 2026**.
Les rapprochements avec notre laboratoire sont des hypothèses analysées,
pas une validation de couverture complète de ces techniques par les règles.

## 3. Informations à réunir avant de conclure

Pour le marqueur encodé, examiner le chemin demandé, la réponse et les
journaux applicatifs ; établir également la réelle exposition publique avant
de retenir T1190. Une réponse HTTP 200 ne démontre pas l’accès à un fichier
interdit ou l’exécution de code.

Pour une suspicion de force brute, corréler les événements réseau avec les
journaux d’authentification : endpoint, horaires, résultats, compte ciblé et
répétition. Ne pas conserver de mots de passe ou de jetons dans les preuves.
Un code 401 isolé ou cinq GET sur la racine ne suffisent pas.

Pour une suspicion de découverte réseau, examiner les ports et destinations
contactés, la séquence temporelle, les réponses et le contexte de la source.
Une vérification réalisée par l’administrateur doit rester identifiée comme
test contrôlé. Si des sondes externes de reconnaissance étaient étudiées,
rechercher la technique correspondante plutôt que d’appliquer T1046 par défaut.

Le chiffrement HTTPS masque les URI et les statuts à ce point d’observation,
sans déchiffrement ; les actions internes à la VM ou au conteneur peuvent
également nécessiter des journaux hôte et applicatifs.

## 4. Méthode à reprendre pour chaque détection

1. Décrire l’action réellement visible, avec son SID ou son type d’événement EVE.
2. Lire la fiche MITRE candidate et vérifier son objectif et ses conditions.
3. Séparer fait observé, hypothèse et informations manquantes.
4. Justifier le rapprochement ou écrire « informations insuffisantes ».
5. Conserver l’événement original et le contexte du test ; réexaminer le choix si de nouvelles preuves apparaissent.

## Illustration complémentaire : vue MITRE dans Wazuh

![Dashboard MITRE Wazuh avec événements associés à vm-filebrowser](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2016-51-51.png)

Le dashboard MITRE affiche des agrégations pour vm-filebrowser, avec les
filtres manager.name=wazuh.manager et présence de rule.mitre.id.
Les catégories affichées sont des associations des règles Wazuh : elles
ne prouvent pas une attaque, une compromission ou une alerte File Browser
sur /api/renew. Les événements détaillés doivent être examinés pour
distinguer les opérations normales du laboratoire des activités suspectes.

Cette illustration concerne les associations des règles Wazuh après
l’installation de l’agent sur la VM. Elle ne valide pas rétroactivement
les rapprochements conditionnels proposés pour les signatures Suricata.

## 📦 Livrable

Conserver le tableau, les liens MITRE, la date de consultation et les preuves
associées. Pour l’alerte 1008001, reprendre l’événement du
**8 octobre à 11:53:20.484380 +0200**, flux `105860300332322` : détection
confirmée du marqueur sur 8080, rapprochement T1190 seulement conditionnel.

**Bilan :** aucune attribution d’attaque confirmée. Les refus de rapprochement
sont justifiés et les données supplémentaires nécessaires sont identifiées.
Cette feuille ne modifie pas les règles Suricata ni leur configuration.

- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
