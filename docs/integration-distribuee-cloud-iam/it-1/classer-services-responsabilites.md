# Classer les services et identifier les responsabilités

## Objectif

Savoir situer un service dans les modèles **IaaS**, **PaaS** ou **SaaS**, puis identifier qui est responsable de la mise à jour de sécurité de l'OS.

Cette compétence est essentielle avant une migration cloud : si tu ne sais pas qui administre quelle couche, tu risques soit de faire confiance au fournisseur sur un point qui reste à ta charge, soit de perdre du temps à gérer une couche déjà prise en charge.

## Ce que tu vas faire, et pourquoi

Pour chaque service, tu vas indiquer :

- le modèle cloud correspondant ;
- le responsable de la mise à jour de sécurité de l'OS ;
- la raison du classement.

Le but n'est pas seulement de remplir un tableau. Il faut être capable de justifier la frontière de responsabilité.

## Rappel rapide

| Modèle | Principe |
| --- | --- |
| IaaS | Tu gères les VM, l'OS, les services, les données et la configuration. Le fournisseur gère le matériel et la virtualisation. |
| PaaS | Le fournisseur gère aussi l'OS et la plateforme. Tu gères surtout la configuration, les données, les accès et parfois le code. |
| SaaS | Tu utilises une application complète. Tu gères surtout les comptes, les droits, les données et les paramètres de sécurité. |

## Exercice

Compléter le tableau suivant.

| Service | Modèle | Responsable OS | Justification |
| --- | --- | --- | --- |
| Une VM OVH nue avec Ubuntu 24.04 | IaaS | Client | Le fournisseur fournit la VM et l'infrastructure. Le client administre l'OS installé, donc les mises à jour de sécurité. |
| Une base de données managée, type RDS-like | PaaS | Fournisseur | Le fournisseur exploite l'OS et le moteur managé. Le client reste responsable de la configuration, des accès, des données et des paramètres de sécurité. |
| Un espace de stockage objet, type S3-like | PaaS | Fournisseur | Le client n'administre pas d'OS. Il configure les buckets, accès, politiques, chiffrement et cycle de vie des objets. |
| Une messagerie collaborative en ligne | SaaS | Fournisseur | Le fournisseur exploite l'application complète et son socle technique. Le client gère les comptes, droits, MFA, données et règles d'usage. |

!!! warning "Attention"
    Le responsable de l'OS n'est pas toujours le responsable de toute la sécurité. Même quand le fournisseur met à jour l'OS, le client reste responsable de ses accès, de ses données, de ses secrets et de ses mauvaises configurations.

## Lecture par responsabilité

| Couche | IaaS | PaaS | SaaS |
| --- | --- | --- | --- |
| Datacenter et matériel | Fournisseur | Fournisseur | Fournisseur |
| Hyperviseur et infrastructure physique | Fournisseur | Fournisseur | Fournisseur |
| OS | Client | Fournisseur | Fournisseur |
| Runtime ou moteur managé | Client | Fournisseur | Fournisseur |
| Application | Client | Variable selon le service | Fournisseur |
| Données | Client | Client | Client |
| IAM, comptes et droits | Client | Client | Client |
| Configuration de sécurité | Client | Client | Client |

## Pour aller plus loin

Chercher un exemple où la frontière de responsabilité a été ambiguë ou discutée publiquement.

Exemples de sujets possibles :

- une fuite de données liée à un bucket de stockage objet mal configuré ;
- une base managée exposée publiquement par erreur ;
- une faille sur un service managé où le fournisseur corrige la plateforme, mais où le client doit modifier sa configuration ;
- un bulletin ANSSI ou un retour d'incident qui distingue défaut fournisseur et mauvaise configuration client.

Pour ton analyse, répondre en quelques lignes :

1. Quel service était concerné ?
2. Quel modèle cloud semblait concerné : IaaS, PaaS ou SaaS ?
3. Quelle partie relevait du fournisseur ?
4. Quelle partie relevait du client ?
5. Pourquoi la frontière était-elle ambiguë ou mal comprise ?

## Preuves à conserver

- tableau complété ;
- justification courte pour chaque service ;
- source utilisée pour l'exemple avancé ;
- synthèse personnelle de la frontière fournisseur/client.

## État final attendu

À la fin de cette feuille, tu dois pouvoir expliquer :

- pourquoi une VM nue est classée en IaaS ;
- pourquoi une base de données managée est classée en PaaS ;
- pourquoi un stockage objet se rapproche d'un service managé ;
- pourquoi une messagerie collaborative en ligne est du SaaS ;
- pourquoi la sécurité de l'OS peut être côté fournisseur sans que toute la sécurité soit déléguée.
