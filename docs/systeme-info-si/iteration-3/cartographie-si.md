# Cartographie du SI d'une mairie

## Objectif

Construire une cartographie lisible du système d'information étudié.

Le schéma doit montrer :

- les utilisateurs ;
- les postes et équipements ;
- les applications ;
- les données ;
- le réseau ;
- les flux principaux ;
- les dépendances ;
- les accès externes ;
- le type d'architecture SI.

## Type d'architecture SI

Le SI de la mairie est une architecture **hybride**.

Elle mélange :

- une partie **centralisée** : comptes utilisateurs, fichiers partagés, sauvegardes, administration ;
- une partie **cloud / SaaS** : messagerie, démarches en ligne, certaines applications métier ;
- des **accès externes** : citoyens, prestataires, portails administratifs publics.

## Version Mermaid

```mermaid
flowchart TB
    subgraph LEG["Légende"]
        direction LR
        L1["Bleu : accès externe"]
        L2["Vert : usage métier"]
        L3["Jaune : données"]
        L4["Violet : administration"]
        L5["Gris : réseau / équipements"]
    end

    subgraph EXT["Accès externes"]
        direction TB
        CIT["Citoyens<br/>demandes, démarches"]
        PORTAILS["Portails administratifs<br/>préfecture, service-public"]
        PRESTA["Prestataire informatique<br/>maintenance, support"]
        INTERNET["Internet<br/>web, mail, services cloud"]
    end

    subgraph USERS["Utilisateurs mairie"]
        direction TB
        ACCUEIL["Agents d'accueil<br/>état civil"]
        METIERS["Services métier<br/>urbanisme, finances,<br/>RH, scolaire"]
        ELUS["Élus / direction<br/>pilotage, décisions"]
        ADMIN["Admin SI / prestataire<br/>comptes, sauvegardes"]
    end

    subgraph EQUIP["Postes et équipements"]
        direction TB
        PCS["Postes agents<br/>PC fixes / portables"]
        PRINT["Imprimantes / scanners<br/>documents administratifs"]
        WIFI["Réseau interne<br/>LAN / Wi-Fi mairie"]
        FW["Pare-feu / routeur<br/>filtrage internet"]
    end

    subgraph APPS["Applications"]
        direction TB
        ETAT["État civil<br/>actes administratifs"]
        URBA["Urbanisme<br/>permis, déclarations"]
        FIN["Finances / comptabilité<br/>budget, factures"]
        RH["RH<br/>agents, congés, paie"]
        MAIL["Messagerie<br/>cloud ou hébergée"]
        WEB["Site web / démarches<br/>formulaires citoyens"]
    end

    subgraph DATA["Données"]
        direction TB
        DOCS["Documents partagés<br/>courriers, dossiers"]
        PERSO["Données personnelles<br/>habitants, agents"]
        ARCH["Archives / preuves<br/>actes, décisions"]
        BACKUP["Sauvegardes<br/>restauration"]
    end

    CIT -->|"formulaires / demandes"| WEB
    WEB -->|"dossiers transmis"| METIERS
    PORTAILS <-->|"échanges administratifs"| METIERS
    PRESTA -->|"accès distant contrôlé"| ADMIN
    INTERNET -->|"services externes"| FW

    ACCUEIL -->|"saisie / consultation"| PCS
    METIERS -->|"travail quotidien"| PCS
    ELUS -->|"consultation"| PCS
    ADMIN -->|"administration"| PCS

    PCS --> WIFI
    PRINT --> WIFI
    WIFI --> FW
    FW --> INTERNET

    PCS -->|"accès applicatif"| ETAT
    PCS -->|"accès applicatif"| URBA
    PCS -->|"accès applicatif"| FIN
    PCS -->|"accès applicatif"| RH
    PCS -->|"emails"| MAIL
    PCS -->|"mise à jour contenu"| WEB

    ETAT -->|"lecture / écriture"| PERSO
    URBA -->|"dossiers"| DOCS
    FIN -->|"factures / budget"| DOCS
    RH -->|"dossiers agents"| PERSO
    MAIL -->|"pièces jointes / échanges"| DOCS
    WEB -->|"demandes citoyens"| PERSO

    DOCS -->|"copie"| BACKUP
    PERSO -->|"copie"| BACKUP
    ARCH -->|"copie"| BACKUP
    ETAT -->|"archives légales"| ARCH

    ADMIN -->|"comptes / droits"| ETAT
    ADMIN -->|"comptes / droits"| URBA
    ADMIN -->|"comptes / droits"| FIN
    ADMIN -->|"comptes / droits"| RH
    ADMIN -->|"supervision sauvegardes"| BACKUP

    classDef external fill:#dbeafe,stroke:#2563eb,stroke-width:1px,color:#111827;
    classDef user fill:#ede9fe,stroke:#7c3aed,stroke-width:1px,color:#111827;
    classDef equip fill:#f1f5f9,stroke:#64748b,stroke-width:1px,color:#111827;
    classDef app fill:#dcfce7,stroke:#16a34a,stroke-width:1px,color:#111827;
    classDef data fill:#fef3c7,stroke:#ca8a04,stroke-width:1px,color:#111827;
    classDef admin fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#111827;

    class CIT,PORTAILS,PRESTA,INTERNET,L1 external;
    class ACCUEIL,METIERS,ELUS user;
    class ADMIN,L4 admin;
    class PCS,PRINT,WIFI,FW,L5 equip;
    class ETAT,URBA,FIN,RH,MAIL,WEB,L2 app;
    class DOCS,PERSO,ARCH,BACKUP,L3 data;
```

## Fichier draw.io

Le diagramme est aussi disponible au format diagrams.net / draw.io :

- [Cartographie du SI d'une mairie](drawio/cartographie-si-mairie.drawio.png)

## Lecture du schéma

| Élément | Rôle dans le SI |
| --- | --- |
| Utilisateurs | Agents, élus, direction et administrateur utilisent le SI selon leurs droits |
| Postes et équipements | Les PC, imprimantes, scanners, réseau interne et pare-feu permettent l'accès au SI |
| Applications | Les logiciels métier supportent l'état civil, l'urbanisme, les finances, les RH et les démarches |
| Données | Les documents, données personnelles, archives et sauvegardes sont les éléments à protéger |
| Réseau | Le LAN / Wi-Fi et le pare-feu relient les postes aux applications et aux services externes |
| Flux principaux | Saisie, consultation, échanges administratifs, emails, sauvegardes |
| Dépendances | Les applications dépendent du réseau, des comptes utilisateurs, des données et des prestataires |
| Accès externes | Citoyens, portails administratifs, prestataire informatique et services cloud |
