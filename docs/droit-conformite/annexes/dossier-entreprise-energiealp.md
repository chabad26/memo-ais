# Annexe — Dossier entreprise ÉnergieAlp

Ce dossier décrit l'infrastructure, les données traitées et les failles connues d'**ÉnergieAlp**, l'entreprise fictive utilisée comme fil rouge du module Droit et conformité. Il sert à l'audit organisationnel, à la matrice d'applicabilité, à l'analyse Cloud Act et à la simulation d'audit ANSSI.

!!! info "Mise en situation"
    Vous intégrez l'équipe Conformité d'ÉnergieAlp. Les éléments ci-dessous sont les faits du scénario pédagogique fourni, et non les résultats d'une inspection d'une entreprise réelle.

## 1. Présentation de l'entreprise

- **Activité :** gestionnaire de réseau de distribution d'électricité dans les Alpes : exploitation, entretien et développement du réseau moyenne et basse tension.
- **Zone de desserte :** plusieurs départements alpins ; environ **280 000 clients raccordés** (particuliers, professionnels, collectivités).
- **Chiffre d'affaires 2025 :** **30 millions d'euros**.
- **Effectif :** environ **650 salariés**, dont une **DSI de 12 personnes** et un **RSSI à temps plein**.
- ÉnergieAlp sous-traite une partie de son informatique et de la maintenance du réseau aux prestataires de la section 3.

## 2. Infrastructure et données traitées

| Système | Rôle | Données traitées |
| --- | --- | --- |
| **SCADA / supervision réseau** | Télésurveillance et télécommande des postes sources et disjoncteurs du réseau électrique | Données techniques d'exploitation : états, mesures, commandes |
| **Compteurs communicants** | Relève à distance de la consommation électrique des clients | Données de consommation, identifiants de compteur, adresses |
| **SI de gestion clientèle (CRM/facturation)** | Facturation, gestion des contrats, relation client | Données personnelles des clients : identité, adresse, IBAN, historique de consommation |
| **Plateforme data analytics** | Analyse des données de consommation, prévision de charge | Données de consommation agrégées et individuelles |
| **VPN technicien** | Accès distant des techniciens itinérants aux systèmes de supervision | Identifiants d'accès, journaux de connexion |

## 3. Sous-traitants et prestataires

| Prestataire | Rôle | Implantation |
| --- | --- | --- |
| **GridSoft Solutions** | Éditeur et intégrateur du système SCADA | France |
| **CloudPeak Americas** | Hébergement de la plateforme data analytics et d'une partie du CRM en cloud public | Filiale européenne d'un groupe américain |
| **RéseauTech Maintenance** | Maintenance des équipements terrain : postes sources et compteurs ; accès VPN aux systèmes de supervision | France, PME régionale |

## 4. Enjeux et failles connues

- Aucune matrice formalisée ne relie les obligations légales NIS2 à la situation de l'entreprise.
- Le VPN des techniciens et de RéseauTech Maintenance repose sur un identifiant et un mot de passe, **sans MFA**.
- Aucune analyse de risque documentée n'a été formalisée pour l'hébergement d'une partie du CRM et de la plateforme data analytics chez CloudPeak Americas, filiale d'un groupe soumis au Cloud Act. **Aucun contrat n'a été mis en place** pour cet hébergement dans le scénario.
- Le registre des actifs critiques existe mais reste **incomplet**.
- Les accès des prestataires externes GridSoft et RéseauTech sont fournis à la demande, sans stratégie particulière ni revue périodique documentée.

## 5. Contraintes d'exploitation

| Contrainte | Conséquence à intégrer au plan de remédiation |
| --- | --- |
| **Fenêtres de maintenance** | Interventions et mises à jour sur la supervision et le SI clientèle uniquement lors de fenêtres validées : nuit, hors pics de consommation, sauf urgence de sécurité avérée |
| **Disponibilité continue** | Le SI clientèle et la supervision doivent rester disponibles ; toute interruption non planifiée affecte le service rendu aux 280 000 clients |
| **Dérogation de sécurité** | Seul le RSSI est habilité à la valider |
| **Responsabilité opérationnelle de la supervision** | Responsable Production |
| **Responsabilité des systèmes de gestion** | DSI : CRM, VPN et plateforme data analytics |

## 6. Contexte pour la qualification juridique

Le dossier **ne tranche volontairement pas le statut d'ÉnergieAlp au regard de NIS2**. L'exercice du jour 1 doit argumenter cette qualification à partir des faits fournis.

Une désignation OIV, une certification, un transfert effectif de données vers les États-Unis ou l'utilisation d'un système d'intelligence artificielle ne sont pas documentés dans le dossier. Les traiter comme des points à vérifier, sans les ajouter aux faits du scénario.

[Retour au module](../README.md) · [Première fiche](../it-1/comprendre-conformite-reglementaire.md)
