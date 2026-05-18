# Menaces et attaques

## Les principales menaces

- **Hameçonnage ou phishing** : escroquerie où l'attaquant se fait passer pour un organisme connu afin de voler des informations ou pousser la victime à cliquer.
- **Malware** : programme malveillant conçu pour nuire à un système informatique sans le consentement de l'utilisateur.
- **Rançongiciel ou ransomware** : malware qui bloque un système ou chiffre des fichiers, puis demande une rançon pour rendre l'accès.

## Les types d'attaques

- **Attaques physiques** : elles visent directement le matériel ou les accès locaux. Exemple : vol d'un ordinateur, clé USB piégée, accès non autorisé à une salle serveur.
- **Attaques humaines** : elles exploitent surtout la confiance ou l'erreur humaine. Exemple : phishing, appel frauduleux, usurpation d'identité, mot de passe donné trop facilement.
- **Attaques réseau** : elles passent par les communications entre machines. Exemple : scan de ports, interception de données, attaque par déni de service, exploitation d'un service mal sécurisé.

!!! tip "À retenir"
    La sécurité ne concerne pas seulement les logiciels : elle dépend aussi des personnes, du matériel et du réseau.

## Cas concret : cyberattaque du CHU de Rouen

En novembre 2019, le CHU de Rouen a été touché par une attaque par rançongiciel.

L'attaque a fortement perturbé le système d'information de l'hôpital : plusieurs applications métiers sont devenues inaccessibles, des postes de travail ont été infectés et des fichiers présents sur des ordinateurs et des serveurs ont été chiffrés.

### Avant l'attaque

L'attaque est liée à un scénario classique de rançongiciel :

- une campagne d'hameçonnage peut servir de point d'entrée,
- un utilisateur ouvre un email ou une pièce jointe piégée,
- un malware s'installe discrètement sur une machine,
- les attaquants explorent ensuite le réseau interne,
- ils cherchent à obtenir plus de droits pour atteindre davantage de serveurs et de postes.

Dans le cas de Clop, l'ANSSI indique que le chiffrement est souvent précédé d'une phase de propagation manuelle dans le réseau, pendant plusieurs jours.

Cette phase est importante pour la défense, car elle peut laisser des traces détectables avant le déclenchement massif du rançongiciel.

### Pendant l'attaque

Le 15 novembre 2019 vers 19 h, l'attaque est détectée au CHU de Rouen.

Le rançongiciel chiffre des fichiers et bloque l'accès à de nombreuses applications.

Les premières actions de sécurité consistent à :

- identifier rapidement qu'il s'agit d'un rançongiciel,
- limiter la propagation dans le réseau,
- isoler les machines ou services touchés,
- protéger les sauvegardes,
- passer en mode dégradé pour continuer l'activité.

À l'hôpital, certains services ont dû fonctionner avec des procédures papier ou par téléphone, notamment pour les prescriptions, les comptes rendus et les admissions.

La DSI du CHU a mené les premières actions, puis l'ANSSI est intervenue en appui.

### Après l'attaque

Après la crise, l'objectif est de reconstruire progressivement le système d'information sans réinfecter les machines.

Les actions importantes sont :

- restaurer les services par ordre de priorité,
- vérifier les sauvegardes avant restauration,
- analyser les traces pour comprendre le chemin de l'attaque,
- changer les mots de passe et contrôler les comptes à privilèges,
- corriger les failles utilisées,
- renforcer la surveillance des logs,
- déposer plainte et documenter l'incident.

Le CHU de Rouen a indiqué qu'aucune fuite de données médicales ou personnelles n'avait été constatée à ce stade et qu'une plainte avait été déposée.

!!! tip "À retenir"
    Un rançongiciel ne se déclenche pas toujours dès l'entrée dans le réseau. Il peut y avoir une phase silencieuse où l'attaquant explore, se déplace et prépare le chiffrement.

## Autre exemple : WannaCry

WannaCry, aussi appelé WannaCrypt, est un rançongiciel qui s'est propagé massivement en mai 2017.

Il ciblait principalement des systèmes Windows qui n'avaient pas reçu le correctif de sécurité `MS17-010`.

Contrairement à certains rançongiciels qui demandent surtout une action humaine, WannaCry pouvait aussi se propager automatiquement sur le réseau en exploitant une faille du protocole SMB.

Une machine vulnérable pouvait donc infecter d'autres machines connectées au même réseau.

Les conséquences ont été importantes : fichiers chiffrés, postes bloqués, services perturbés et demande de rançon pour récupérer les données.

Cette attaque montre l'importance des mises à jour de sécurité, de la désactivation des services inutiles comme SMBv1, de la segmentation réseau et des sauvegardes isolées.

!!! tip "À retenir"
    WannaCry est un bon exemple d'attaque qui combine rançongiciel et propagation réseau automatique. Une seule machine non corrigée peut devenir un point d'entrée pour contaminer rapidement d'autres postes.

## Sources

- CHU de Rouen : [Le point sur l'attaque informatique du 15 novembre 2019](https://www.chu-rouen.fr/le-point-sur-lattaque-informatique-du-15-novembre-2019/)
- CERT-FR / ANSSI : [Informations concernant le rançongiciel Clop](https://cert.ssi.gouv.fr/cti/CERTFR-2019-CTI-009/)
- CERT-FR / ANSSI : [Propagation d'un rançongiciel exploitant les vulnérabilités MS17-010](https://www.cert.ssi.gouv.fr/alerte/CERTFR-2017-ALE-010/)
- Document apprenant : `cyberattaques_apprenant.pdf`
