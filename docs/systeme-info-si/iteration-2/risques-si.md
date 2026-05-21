# Identifier et prioriser les risques d'un SI

## Objectif

Identifier des risques possibles dans un SI, puis choisir ceux qui méritent le plus d'attention.

Cette page est pensée comme un mémo personnel : je pars du cas CHU de Rouen, des enjeux vus avant et de mes propres exemples pour construire une liste de risques priorisés.

Un **risque** combine généralement :

- une cause possible ;
- un événement redouté ;
- un impact sur le SI ou l'activité.

Exemple :

| Cause | Événement redouté | Conséquence |
| --- | --- | --- |
| Compte prestataire compromis | accès distant utilisé par un attaquant | propagation vers les serveurs et données |

## Types de risques à identifier

| Type de risque | Définition | Exemples |
| --- | --- | --- |
| Technique | lié aux systèmes, réseaux, applications ou infrastructures | panne serveur, sauvegarde accessible, faille non corrigée, SPOF |
| Organisationnel | lié aux procédures, responsabilités ou décisions | absence de PRA, droits non revus, départ prestataire non désactivé |
| Humain | lié aux usages, contraintes ou erreurs possibles | phishing, partage de compte, contournement, clé USB |

## Méthode personnelle adaptée à l'exercice

Comme je travaille seul, je remplace le travail en sous-groupe par une analyse personnelle structurée :

1. identifier des risques techniques, organisationnels et humains ;
2. m'appuyer sur le cas CHU de Rouen et les cartographies précédentes ;
3. distinguer la cause, l'événement redouté et l'impact ;
4. relier chaque risque à un ou plusieurs enjeux ;
5. sélectionner mes 3 risques majeurs.

## Phase d'analyse et recherche

Je pars de trois sources :

| Source | Ce que j'en retire |
| --- | --- |
| Cas CHU de Rouen | un ransomware peut bloquer les applications métiers et forcer le mode dégradé |
| Cartographie SI | certains points concentrent les risques : DPI, AD/IAM, VPN, sauvegardes |
| Expérience générale | phishing, mots de passe, lenteur, accès partagés et manque de procédures reviennent souvent |

## Liste de risques possibles

### Risques techniques

| Risque | Cause possible | Impact possible | Enjeu lié |
| --- | --- | --- | --- |
| Ransomware sur postes et serveurs | faille, pièce jointe, compte compromis | arrêt des applications, mode dégradé, perte de temps | disponibilité, sécurité |
| Sauvegardes accessibles depuis la production | stockage mal isolé, droits trop larges | restauration impossible ou très lente | disponibilité, sécurité |
| DPI indisponible | panne serveur, base inaccessible, attaque | soins ralentis, accès difficile aux antécédents | disponibilité |
| Middleware ou API indisponible | panne d'interface, erreur de synchronisation | labo, imagerie ou pharmacie non synchronisés | intégration, disponibilité |
| Pic de charge non supporté | capacité insuffisante, architecture non scalable | lenteur, blocage des utilisateurs | évolutivité, disponibilité |

### Risques organisationnels

| Risque | Cause possible | Impact possible | Enjeu lié |
| --- | --- | --- | --- |
| Compte administrateur mal séparé | usage du même compte pour bureautique et administration | propagation rapide si le compte est compromis | sécurité |
| Accès VPN prestataire trop large | droits non limités, accès permanent | entrée distante vers plusieurs zones du SI | sécurité, intégration |
| Sauvegardes non testées | absence de test de restauration | fausse impression de sécurité, reprise impossible | disponibilité |
| Départs ou changements de rôle mal gérés | comptes non désactivés, droits non revus | accès non légitime aux applications | sécurité, conformité |
| Non-respect RGPD | données trop conservées, accès non tracés | sanctions, perte de confiance, correction obligatoire | conformité, sécurité |

### Risques humains

| Risque | Cause possible | Impact possible | Enjeu lié |
| --- | --- | --- | --- |
| Phishing via messagerie | pièce jointe ou lien malveillant | vol d'identifiants, infection initiale | sécurité |
| Partage de compte ou de carte | urgence, postes partagés, procédure trop lourde | traçabilité faible, accès non attribuable | sécurité, conformité |
| Contournement de sécurité | outil trop lent, authentification répétée | règles non respectées, exposition du SI | sécurité |
| Clé USB ou outil externe | maintenance biomédicale, transfert rapide | introduction de malware | sécurité, disponibilité |
| Mauvaise manipulation en crise | stress, manque de procédure | perte de temps, aggravation de l'incident | disponibilité |

## Ma sélection de risques majeurs

| Rang | Risque choisi | Type | Cause principale | Impact | Enjeu lié |
| --- | --- | --- | --- | --- | --- |
| 1 | Ransomware atteignant le DPI et les serveurs | technique / humain | phishing ou accès distant compromis | arrêt des soins informatisés, mode dégradé | disponibilité, sécurité |
| 2 | Sauvegardes non isolées ou non testées | technique / organisationnel | sauvegardes accessibles ou restauration non vérifiée | reprise lente ou impossible | disponibilité |
| 3 | Compte à privilèges compromis | technique / organisationnel | droits trop larges, compte admin mal séparé | propagation, accès aux données, désactivation de protections | sécurité |

### Description de mes 3 risques majeurs

#### 1. Ransomware atteignant le DPI et les serveurs

Le risque le plus important est qu'un ransomware parte d'un poste utilisateur, d'un mail de phishing ou d'un accès distant compromis, puis atteigne les serveurs métiers. Dans un hôpital, l'impact est immédiat : le DPI, les prescriptions, le laboratoire ou l'imagerie peuvent devenir indisponibles.

Impact principal :

- arrêt ou forte dégradation des soins informatisés ;
- retour au papier et au téléphone ;
- perte de temps pour les équipes ;
- risque de propagation vers les données et les sauvegardes.

#### 2. Sauvegardes non isolées ou non testées

Les sauvegardes sont la dernière ligne de défense après un incident grave. Si elles sont accessibles depuis le SI compromis, elles peuvent être chiffrées ou supprimées. Si elles ne sont pas testées, on ne sait pas vraiment si la restauration fonctionnera.

Impact principal :

- reprise très lente ;
- perte possible de données ;
- dépendance au mode dégradé plus longtemps ;
- pression plus forte en cas de ransomware.

#### 3. Compte à privilèges compromis

Un compte administrateur ou un compte à droits élevés peut donner accès à de nombreux systèmes. S'il est compromis, l'attaquant peut se déplacer plus vite, désactiver des protections ou atteindre des serveurs critiques.

Impact principal :

- élévation des privilèges ;
- propagation vers serveurs, AD/IAM, sauvegardes ;
- accès à des données sensibles ;
- difficulté à reprendre le contrôle.

## Priorisation simple

Pour prioriser seul, je peux noter chaque risque sur 3 critères :

- **impact** : faible, moyen, fort ;
- **vraisemblance** : faible, moyenne, forte ;
- **maîtrise actuelle** : bonne, partielle, faible.

| Risque | Impact | Vraisemblance | Maîtrise actuelle | Priorité |
| --- | --- | --- | --- | --- |
| Ransomware sur DPI et serveurs | fort | moyenne à forte | partielle | 1 |
| Sauvegardes non isolées ou non testées | fort | moyenne | inconnue | 2 |
| Compte administrateur compromis | fort | moyenne | partielle | 3 |
| Phishing via messagerie | moyen à fort | forte | partielle | 4 |
| Middleware/API indisponible | moyen | moyenne | inconnue | 5 |

## Notes personnelles

Ce qui ressort le plus pour moi :

- le ransomware est le risque le plus parlant, car il combine humain, technique et organisationnel ;
- les sauvegardes ne sont pas un détail technique : elles conditionnent la reprise ;
- les comptes administrateurs et l'AD/IAM sont des points de concentration ;
- un prestataire ou un accès VPN mal limité peut devenir un point d'entrée majeur ;
- il faut toujours relier le risque à un enjeu concret, sinon la liste reste trop abstraite.

## À retenir

- Un risque n'est pas seulement une panne : il relie une cause, un événement et un impact.
- Il faut distinguer **cause** et **conséquence**.
- Un ransomware est intéressant à analyser car il combine technique, humain et organisationnel.
- Prioriser sert à choisir où mettre l'effort en premier.
