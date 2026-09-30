# Comprendre CVSS

**Durée prévue : 30 minutes.**

## Objectif

Lire les principales informations fournies par CVSS et distinguer la sévérité
d'une vulnérabilité de sa priorité de traitement dans une infrastructure.

**Statut : synthèse documentaire préparée par l'assistant le 30 septembre 2026.**
Les scores ont été relevés dans l'API officielle de la NVD et recoupés avec les
JSON CVE lorsqu'ils contiennent des métriques. Les exemples de priorité sont
hypothétiques ; ils ne décrivent pas des constats sur la VM du laboratoire.

## Ce que fournit CVSS

CVSS signifie **Common Vulnerability Scoring System**. Le score de base, de
**0 à 10**, exprime la sévérité technique selon les caractéristiques de la
vulnérabilité. Le **vecteur** indique les valeurs retenues pour le calcul.
Conserver ensemble **version, score, vecteur, source et date** permet de relire
et de comparer les évaluations.
[Source : spécification FIRST CVSS 3.1](https://www.first.org/cvss/v3.1/specification-document).

Un score de base ne constitue ni une probabilité d'exploitation ni un ordre de
correction automatique. FIRST demande de le compléter par l'analyse de la
menace et de l'environnement.
[Source : guide FIRST CVSS 4.0](https://www.first.org/cvss/v4.0/user-guide).

## Relevé des trois vulnérabilités

### Scores de base CVSS 3.1

Les trois évaluations ci-dessous sont attribuées à **NVD / NIST**
(`source: nvd@nist.gov` dans l'API), avec la même version de CVSS.

| Vulnérabilité et source | Version | Score de base | Sévérité | Vecteur |
| --- | --- | --- | --- | --- |
| [CVE-2008-0166 — Debian OpenSSL](https://nvd.nist.gov/vuln/detail/CVE-2008-0166) | 3.1 | **7,5** | Élevée | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| [CVE-2014-0160 — Heartbleed](https://nvd.nist.gov/vuln/detail/CVE-2014-0160) | 3.1 | **7,5** | Élevée | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| [CVE-2021-44228 — Log4Shell](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) | 3.1 | **10,0** | Critique | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |

Sources structurées effectivement consultées :
[API NVD — Debian OpenSSL](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2008-0166),
[API NVD — Heartbleed](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2014-0160),
[API NVD — Log4Shell](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-44228).
Lire `vulnerabilities[].cve.metrics.cvssMetricV31[]`, puis `source` et `cvssData`.

### Évaluations CVSS 2.0 également disponibles

Les mêmes réponses NVD contiennent ces scores dans `cvssMetricV2` :

| Vulnérabilité | Version | Score de base | Sévérité en v2 | Vecteur |
| --- | --- | --- | --- | --- |
| CVE-2008-0166 | 2.0 | **7,8** | Élevée | `AV:N/AC:L/Au:N/C:C/I:N/A:N` |
| CVE-2014-0160 | 2.0 | **5,0** | Moyenne | `AV:N/AC:L/Au:N/C:P/I:N/A:N` |
| CVE-2021-44228 | 2.0 | **9,3** | Élevée | `AV:N/AC:M/Au:N/C:C/I:C/A:C` |

Ces valeurs sont des évaluations selon une autre version du référentiel.
Ne pas mélanger, par exemple, le score v2 de Heartbleed et le score v3.1 de
Log4Shell pour établir un classement présenté comme homogène.

**Disponibilité dans les autres sources :** les
[JSON de l'activité précédente](lire-analyser-entrees-cve.md#retrouver-les-entrees-et-leurs-enregistrements-json)
contiennent également les scores 3.1 de Heartbleed et Log4Shell dans
`containers.adp[].metrics[].cvssV3_1`, fournis par **CISA-ADP**. Celui de Debian
OpenSSL ne contient pas de score CVSS au moment de la consultation.
Aucune métrique CVSS 4.0 n'a été trouvée dans ces trois JSON ni dans les trois
réponses NVD consultées : cela ne justifie pas d'en inventer une.

## Interpréter un vecteur — Log4Shell

Vecteur choisi : **CVE-2021-44228, CVSS 3.1, score de base 10,0**.

```text
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
```

| Élément | Signification | Interprétation |
| --- | --- | --- |
| `AV:N` | Attack Vector : Network | L'exploitation est possible par le réseau ; aucun accès physique n'est nécessaire. |
| `AC:L` | Attack Complexity : Low | Pas de condition particulière hors du contrôle de l'attaquant, dans la configuration vulnérable évaluée. |
| `PR:N` | Privileges Required : None | Aucun privilège préalable n'est requis. |
| `UI:N` | User Interaction : None | Aucune action d'un autre utilisateur n'est nécessaire. |
| `S:C` | Scope : Changed | Les impacts peuvent dépasser l'autorité de sécurité du composant vulnérable. |
| `C:H` | Confidentiality : High | Fort impact possible sur la confidentialité des informations. |
| `I:H` | Integrity : High | Fort impact possible sur l'intégrité : modification de données ou de ressources. |
| `A:H` | Availability : High | Fort impact possible sur la disponibilité du service. |

Lecture des métriques selon la
[spécification FIRST CVSS 3.1](https://www.first.org/cvss/v3.1/specification-document).
Ces valeurs décrivent des possibilités techniques, pas une exploitation observée.
`AV:N` ne prouve pas que **notre** instance est accessible depuis Internet :
son exposition réelle doit être vérifiée.

## Utiliser le calculateur avec la bonne version

Pour reproduire l'évaluation retenue, ouvrir le
[calculateur FIRST CVSS 3.1 avec le vecteur Log4Shell](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).
Vérifier les huit métriques et le score de base attendu **10,0**, en conservant
les métriques temporelles et environnementales non définies.

Le [calculateur CVSS 4.0 fourni dans le sujet](https://www.first.org/cvss/calculator/4.0)
permet d'étudier la version 4.0, mais ne reçoit pas directement ce vecteur 3.1.
La version 4.0 introduit notamment **`AT`** pour les conditions préalables
d'attaque et distingue les impacts sur le système vulnérable (**`VC/VI/VA`**)
de ceux sur les systèmes affectés ensuite (**`SC/SI/SA`**), à la place de `S`.
Une cotation 4.0 demande donc une nouvelle analyse, pas un changement du préfixe.
[Source : guide FIRST CVSS 4.0](https://www.first.org/cvss/v4.0/user-guide).

Cette manipulation du calculateur est proposée à l'apprenant ; aucune capture
de son exécution n'est encore fournie.

## Le score le plus élevé impose-t-il de corriger en premier ?

**Non.** Le score aide à apprécier la sévérité technique ; la priorité dépend
de l'applicabilité de la faille, de l'exposition réelle, de la menace et des
conséquences pour l'organisation. Un score élevé reste un signal important,
mais doit être contextualisé.
[Source : guide FIRST — score de base et risque](https://www.first.org/cvss/v4.0/user-guide).

### Deux informations de contexte qui peuvent modifier la priorité

| Information | Exemple hypothétique | Effet possible sur la priorité |
| --- | --- | --- |
| **Exposition et accessibilité réelles** | Un service Heartbleed à 7,5 est accessible depuis Internet ; une instance Log4Shell à 10,0 est arrêtée et isolée, avec cet isolement vérifié. | Traiter d'abord le service exposé peut être justifié ; corriger l'autre avant toute remise en service. |
| **Criticité métier et sensibilité des données** | Une faille à score plus faible affecte un service indispensable contenant des données sensibles ; une faille à score supérieur concerne un environnement de test sans données réelles ni dépendance de production. | L'impact métier peut donner la priorité au service essentiel, avec une intervention préparée pour maintenir son fonctionnement. |

Ces exemples sont des raisonnements de priorisation, pas des changements du
score de base publié. Documenter les éléments qui justifient l'ordre retenu
et le réexaminer si l'exposition ou la menace évolue.

## Résultat attendu et preuves à conserver

- Le relevé version, score, vecteur et source pour les trois CVE.
- L'interprétation du vecteur choisi et, après manipulation, une capture du
  calculateur montrant sa version, les métriques et le score de base.
- Une réponse argumentée sur la priorité, avec deux éléments de contexte.

- [Activité précédente — Lire et analyser trois entrées CVE](lire-analyser-entrees-cve.md)
- [Activité suivante — Observer la cible](observer-cible.md)
- [Retour à l'itération 1](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Retour au module](../README.md)
