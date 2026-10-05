# Vérifier l’état du système après remédiation

***Itération 5 — Travail individuel — Feuille préparée le 5 octobre 2026***

## 🎯 Objectif

Vérifier l’efficacité des remédiations en comparant l’état actuel du système
avec l’audit initial. Cette activité prolonge le compte-rendu J4 pour constituer
le **compte-rendu de durcissement et de vérification** utilisé pour C2.

**Statut J5 — 5 octobre 2026 : contrôles manuels, Greenbone et Lynis
refaits par Olivier ; résultats déclarés inchangés par rapport au vendredi
2 octobre.** Les nouvelles sorties et les nouveaux rapports ne sont pas encore
joints à cette feuille. Ce retour confirme une vérification réalisée selon
l’apprenant, sans permettre une comparaison détaillée indépendante des exports.
Trivy n’a pas été relancé : Olivier indique que l’image n’a pas changé. La
centralisation Wazuh reste une activité collective distincte.

## Retour de vérification J5 — résultats stables selon Olivier

| Vérification | Retour reçu le 5 octobre | Portée et preuve restante |
| --- | --- | --- |
| Contrôles manuels | Refaits ; aucun changement par rapport aux résultats de vendredi | Détail des commandes, fenêtre de test et sorties J5 non joints ; ne pas inventer un nouveau test particulier |
| Greenbone | Relancé ; résultats déclarés inchangés | Rapport J5, dates, filtres, cible et succès d’authentification à conserver ; les compteurs précis ne sont pas revalidés ici |
| Lynis | Relancé ; résultats déclarés inchangés | Journal J5, version/profil et détails des tests à conserver ; aucun nouveau score exact déduit du seul retour |
| Trivy | Non relancé, image déclarée inchangée | Choix ciblé pour éviter de répéter l’analyse du même artefact ; digest J5 non joint. Les bases de vulnérabilités peuvent évoluer même à image constante |

**Conclusion du retour J5 :** stabilité déclarée des résultats des trois
familles de contrôles effectuées. Aucun nouveau problème n’est signalé par
Olivier dans ce retour. Cela ne signifie ni disparition des alertes ni absence
globale de vulnérabilité : les risques résiduels et investigations du J4 sont
maintenus. Les dix HIGH de l’export Trivy précédent restent à qualifier ;
l’absence de rescan ne démontre pas l’absence de nouvelles associations CVE.
Un nouveau Trivy sera pertinent après changement d’image ou pour actualiser
l’analyse des vulnérabilités, avec version des bases et digest conservés.

Les verdicts par constat ci-dessous restent provisoires : le retour global
ne détaille pas quels tests manuels ont été refaits. Compléter les pièces J5
avant de présenter chaque ligne comme une validation indépendante documentée.

## 1. Reprendre les trois documents de référence

- [Rapport d’audit et plan de remédiation J3](../it-3/finaliser-rapport-plan-remediation.md) : constats C01–C13, contexte et priorités.
- [Préparation des remédiations J4](../it-4/preparer-remediations.md) : actions R01–R09, effets attendus et retours arrière.
- [Compte-rendu de durcissement J4](../it-4/finaliser-compte-rendu-durcissement.md) : changements, tests, diagnostics, adaptations et risques résiduels.
- [Journal détaillé et preuves J4](../it-4/mettre-en-oeuvre-verifier-remediations.md) : captures, commandes, inventaires et rapports conservés.

Conserver les identifiants des constats. Une mise à niveau, un compteur en
baisse ou un service healthy ne démontre pas à lui seul la correction de
chaque défaut. Pour chaque conclusion, retrouver la propriété initialement
signalée et choisir un contrôle qui mesure cette propriété.

## 2. Identifier la cible actuelle avant les tests

Relever la date, le nom de la machine, l’OS, le noyau et les versions des paquets
sur **la VM**, puis l’identité du conteneur et de l’image effectivement utilisés.
Le poste hôte et la VM avaient été confondus lors d’un inventaire J4 : vérifier
l’invite et le nom de machine avant toute attribution.

| Référence du 2 octobre | Contrôle J5 attendu |
| --- | --- |
| VM Ubuntu 26.04.1, noyau 7.0.0-38-generic | aucun changement |
| File Browser 2.63.23, principal sur 8080 | aucun changement |
| SSH administrateur par clé ; gvm-audit avec clé dédiée | aucun changement |
| Données persistantes config/base/documents | aucun changement |

Les commandes de collecte et de contrôle sont dans le
[journal J4](../it-4/mettre-en-oeuvre-verifier-remediations.md). Les reprendre
comme contrôles, sans rejouer les commandes de modification. Ne pas mettre
à jour ou recréer le service avant le relevé initial J5 : une nouvelle
intervention doit avoir sa propre chronologie.

## 3. Choisir les vérifications pertinentes

Il n’est pas nécessaire de relancer tous les outils. Justifier ceux retenus,
ainsi que ceux non relancés, d’après les changements à vérifier.

| Outil / contrôle | Quand le retenir | Pièce à conserver et limite |
| --- | --- | --- |
| Greenbone | Constats distants, protocoles, services et inventaire authentifié pertinents | Cible, tâche, profil, date, filtres, QoD, succès SSH et XML complet ; vérifier l’attribution de l’hôte |
| Lynis | Auditd, services, configuration hôte et sysctl | Version, profil, commande, journal complet et détails des tests ; score non assimilable à un pourcentage de sécurité |
| Trivy | Vulnérabilités de l’image réellement déployée | ImageID/digest, version outil et bases, options, JSON complet ; ne pas analyser seulement une étiquette latest |
| Vérifications manuelles | Accès SSH, processus Docker, audit, CUPS, sysctl et application | Sorties datées, état effectif, tests positifs/négatifs adaptés ; distinguer configuration et effet |

Pour SSH, conserver une session et une console disponibles pendant les essais
d’accès. Faire les tests en session distincte pour ne pas réutiliser une
connexion déjà ouverte. Tester les opérations File Browser sur un fichier de
test, avec secret masqué. Un nouveau reboot n’est utile que si la persistance
ou un changement récent le justifie ; en expliciter l’interruption.

## 4. Comparer les nouveaux résultats avec l’audit initial

Créer des pièces J5 sous des noms distincts : ne pas écraser les fichiers J3/J4.
La comparaison conserve le périmètre, le composant, le chemin et les conditions
du test ; noter toute différence de profil, de base, de filtre ou de version.

**Points déjà identifiés en J4 :**

- Greenbone final du 2 octobre, 13:38–13:44 : 204 résultats de sécurité et 44 Log, mêmes compteurs que le scan post-migration de 12:11. Ces deux scans ne forment pas à eux seuls une comparaison avec l’audit initial J3.
- L’adresse exportée était `127.0.0.1`, malgré une authentification `gvm-audit` réussie et Ubuntu 26.04 détecté. Sa cause reste à établir avant une attribution définitive.
- Certaines alertes de versions étaient contradictoires ou liées à des correctifs Ubuntu rétroportés : comparer la version complète et chaque copie, notamment dans les snaps.
- Trivy de la nouvelle image : dix HIGH et zéro CRITICAL dans l’export texte ; applicabilité et JSON complet à compléter.
- Lynis : indice 65 → 67 et écarts sysctl 15 → 9. Ces indicateurs corroborent certains changements, sans prouver une sécurité globale.

Pour une alerte disparue, vérifier que le contrôle a bien été exécuté et que
le filtre ne l’a pas masquée. Pour une alerte persistante, confronter version
complète, correctif éditeur, chemin et scénario ; ne pas conclure à l’échec
sur son seul nom. Garder les exclusions justifiées dans l’analyse.

## 5. Matrice de vérification après remédiation

Le bilan J4 ci-dessous prépare les tests. **Les verdicts détaillés J5 restent à
renseigner à partir des pièces des contrôles refaits.** Reprendre le libellé précis de
chaque constat dans le rapport J3, en conservant ses sous-scénarios.

| Constat initial | Vérification après remédiation | Référence J4 / limite | Résultat J5 |
| --- | --- | --- | --- |
| C01–C03 — Composants hôte et SSH | Versions complètes, correctifs applicables et contrôles Greenbone pertinents | OS et moteurs migrés ; quelques exclusions ciblées ; toutes les CVE non qualifiées | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C04–C05 — Configuration SSH / MAC | Paramètres effectifs avec contexte ; offre MAC ; refus password ; accès par clé | Premier lot validé ; options de transfert complémentaires différées | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C06 — CUPS | Unités service/socket/path et écoute 631 ; distinguer service et paquet | Masquage persistant validé, paquets conservés | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C07 — Maintenance OS | OS et dépôts actuels, statut de maintenance pertinent au constat | Ubuntu 26.04.1 relevé ; migration réalisée | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C08 — Audit ciblé | Règles chargées, événement test retrouvé, pertes et stockage | Sept règles b64 ; ais_ssh avant/après reboot ; rotation manuelle réussie | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C09 — sysctl | Valeurs effectives, fichiers persistants, décisions réseau et tests fonctionnels | Deux lots validés ; forwarding/rp_filter maintenus ; autres paramètres contextualisés | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C10 — Privilèges / montages Docker | UID du processus applicatif, CapEff/CapBnd, NoNewPrivs, inspect et droits utiles | UID 1000, capacités nulles, NoNewPrivs 1 ; écritures nécessaires conservées | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |
| C12 — Image ancienne et maintenance applicative | Trivy de l’image exacte, qualification des composants, décision de maintenance | Version 2.63.23 ; dix HIGH ; fin de maintenance annoncée | À investiguer — risques résiduels déjà identifiés |
| C13 — Identifiants administrateur | Refus de l’ancien identifiant en session privée, accès légitime ; sessions existantes si retenu | Ancien mot de passe refusé ; invalidation des jetons non vérifiée | À investiguer — contrôle refait déclaré ; preuve détaillée non jointe |

**C11 :** les arrêts initiaux ont été expliqués comme volontaires ; ils ne sont
pas présentés comme une panne spontanée corrigée. Conserver cette justification
hors du compteur des défauts corrigés. R08 complète le contrôle fonctionnel :
vérifier reprise et données persistantes si le test est pertinent.

### Règles de conclusion

| Résultat | Condition à documenter |
| --- | --- |
| Corrigé | La propriété initialement défaillante est conforme et son contrôle est attribuable au bon composant |
| Partiellement corrigé | Une partie du constat est traitée ; préciser la partie restant présente |
| Non corrigé | Le défaut reste démontré par un contrôle pertinent |
| À investiguer | Preuve manquante, attribution incertaine, comparaison insuffisante ou applicabilité non établie |

Pour chaque verdict, joindre **date, outil/commande, preuve, effet de sécurité,
test fonctionnel et limite**. Une mesure compensatoire ou l’arrêt d’un service
ne signifie pas nécessairement que le paquet vulnérable a été corrigé.

## 6. Contrôler le fonctionnement et les nouveaux problèmes

Vérifier l’accès SSH légitime, sudo selon le besoin, l’état des services retenus,
l’accès File Browser et téléchargement/téléversement/suppression d’un fichier
de test. Contrôler l’espace disponible et les pertes audit ; ne pas réutiliser
le simple état healthy comme preuve du parcours complet.

| Nouveau problème observé | Première observation et contexte | Diagnostic / comparaison J4 | Impact et suite | Preuve |
| --- | --- | --- | --- | --- |
| À renseigner si un problème apparaît | Date, machine, opération, message exact | Hypothèses distinguées des causes établies | Action, retour arrière ou investigation | Sortie/capture datée |

Ne pas attribuer automatiquement une nouvelle alerte à la remédiation : elle
peut venir d’une base de vulnérabilités actualisée ou d’un périmètre plus large.
Comparer les composants et la chronologie. S’il n’y a aucun nouveau problème
observé, préciser les tests et la fenêtre d’observation qui étayent ce bilan.

## 📦 Résultat attendu

Une matrice complétée, des preuves J5 distinctes et une conclusion par constat :
**Corrigé / Partiellement corrigé / Non corrigé / À investiguer**. Ajouter les
nouveaux problèmes et les risques résiduels au compte-rendu, avec leur impact,
leur justification et leur prochaine action. Ne pas déclarer l’absence globale
de vulnérabilité à partir d’un scan ou d’un score.

## 📚 Notions acquises

- **Re-scan :** nouveau contrôle après intervention, comparé à une référence en conservant les conditions et leurs différences.
- **Risque résiduel :** risque qui demeure après les mesures réalisées ; il doit être explicité, qualifié et traité ou faire l’objet d’une décision documentée.

- [Compte-rendu J4 à compléter pour C2](../it-4/finaliser-compte-rendu-durcissement.md)
- [Retour à l’itération 5](index.md)
- [Retour au module](../README.md)
