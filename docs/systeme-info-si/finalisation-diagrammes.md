# Finalisation des diagrammes

## Objectif

Produire des diagrammes propres, lisibles et compréhensibles par une personne qui n'a pas participé au travail.

Un bon diagramme doit pouvoir être compris sans explication orale. Il doit donc avoir :

- un titre clair ;
- peu d'éléments ;
- des flèches directionnelles ;
- une légende ;
- des hypothèses explicites.

## Diagramme 1 : vue réseau simplifiée

Ce schéma montre les grandes zones du SI hospitalier et les flux principaux.

```mermaid
flowchart TB
    subgraph LEG["Légende"]
        direction LR
        LBLUE["Bleu : accès externe"]
        LGREEN["Vert : usage métier"]
        LPURPLE["Violet : administration"]
        LYELLOW["Jaune : données / sauvegardes"]
        LRED["Rouge : attaque"]
    end

    subgraph EXT["Extérieur"]
        direction LR
        INTERNET["Internet<br/>web, mail"]
        VPN["Accès distant<br/>VPN, prestataires"]
        ATT["Attaquant<br/>phishing ou accès compromis"]
    end

    subgraph INT["SI interne"]
        direction LR
        USERS["Réseau utilisateurs<br/>soins, accueil, pharmacie"]
        APPS["Applications métiers<br/>DPI, prescriptions,<br/>labo, imagerie"]
        ADMIN["Administration SI<br/>AD, comptes, droits"]
    end

    subgraph CRIT["Zones critiques"]
        direction LR
        DATA["Données<br/>patient, résultats,<br/>comptes rendus"]
        BACKUP["Sauvegardes<br/>restauration"]
    end

    INTERNET -->|"flux filtrés"| USERS
    VPN -->|"accès contrôlé"| ADMIN
    USERS -->|"accès applicatif"| APPS
    ADMIN -->|"authentification / droits"| APPS
    APPS -->|"lecture / écriture"| DATA
    DATA -->|"copies"| BACKUP
    ATT -. "phishing" .-> USERS
    ATT -. "compte distant compromis" .-> VPN
    ADMIN -. "propagation si droits compromis" .-> DATA

    classDef external fill:#dbeafe,stroke:#2563eb,stroke-width:1px,color:#111827;
    classDef app fill:#dcfce7,stroke:#16a34a,stroke-width:1px,color:#111827;
    classDef admin fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#111827;
    classDef data fill:#fef3c7,stroke:#ca8a04,stroke-width:2px,color:#111827;
    classDef attack fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#111827;
    classDef legendBlue fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#111827;
    classDef legendGreen fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#111827;
    classDef legendPurple fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#111827;
    classDef legendYellow fill:#fef3c7,stroke:#ca8a04,stroke-width:2px,color:#111827;
    classDef legendRed fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#111827;

    class INTERNET,VPN external;
    class USERS,APPS app;
    class ADMIN admin;
    class DATA,BACKUP data;
    class ATT attack;
    class LBLUE legendBlue;
    class LGREEN legendGreen;
    class LPURPLE legendPurple;
    class LYELLOW legendYellow;
    class LRED legendRed;

    linkStyle 0,1 stroke:#2563eb,stroke-width:2px;
    linkStyle 2 stroke:#16a34a,stroke-width:2px;
    linkStyle 3 stroke:#7c3aed,stroke-width:2px;
    linkStyle 4,5 stroke:#ca8a04,stroke-width:2px;
    linkStyle 6,7,8 stroke:#dc2626,stroke-width:2.5px,stroke-dasharray:5 5;
```

### Hypothèses

- Les accès distants passent par un VPN ou une solution de télémaintenance.
- Les applications métiers s'appuient sur un système d'identité central.
- Les sauvegardes doivent être séparées de la production.

## Diagramme 2 : flux de données critiques

Ce schéma montre où se concentrent les données qu'un ransomware viserait en priorité.

```mermaid
flowchart TB
    subgraph USERS["Utilisateurs"]
        direction LR
        CARE["Soignants"]
        ADMINU["Administratif"]
        ITU["DSI / IT"]
    end

    subgraph APPS["Applications"]
        direction LR
        DPI["DPI<br/>dossier patient"]
        RDV["Admissions<br/>rendez-vous"]
        TOOLS["Outils techniques<br/>supervision, sauvegarde"]
    end

    subgraph DATA["Données critiques"]
        direction LR
        PATIENT["Données patient<br/>prescriptions, comptes rendus"]
        ADMINDB["Données administratives<br/>identité, facturation"]
        TECHDB["Données techniques<br/>logs, configurations"]
        BACKUP["Sauvegardes"]
    end

    CARE -->|"lecture / écriture soins"| DPI
    ADMINU -->|"admission / gestion"| RDV
    ITU -->|"exploitation"| TOOLS
    DPI -->|"stocke"| PATIENT
    RDV -->|"stocke"| ADMINDB
    TOOLS -->|"journalise"| TECHDB
    PATIENT -->|"copie"| BACKUP
    ADMINDB -->|"copie"| BACKUP
    TECHDB -->|"copie"| BACKUP
    PATIENT -. "cible prioritaire" .-> BACKUP

    classDef user fill:#e0f2fe,stroke:#0369a1,stroke-width:1px,color:#111827;
    classDef app fill:#dcfce7,stroke:#15803d,stroke-width:1px,color:#111827;
    classDef data fill:#fef3c7,stroke:#b45309,stroke-width:2px,color:#111827;
    classDef backup fill:#fee2e2,stroke:#b91c1c,stroke-width:2px,color:#111827;

    class CARE,ADMINU,ITU user;
    class DPI,RDV,TOOLS app;
    class PATIENT,ADMINDB,TECHDB data;
    class BACKUP backup;

    linkStyle 0,1,2 stroke:#16a34a,stroke-width:2px;
    linkStyle 3,4,5,6,7,8 stroke:#ca8a04,stroke-width:2px;
    linkStyle 9 stroke:#dc2626,stroke-width:2.5px,stroke-dasharray:5 5;
```

### Hypothèses

- Les données patient sont les plus sensibles et les plus critiques pour les soins.
- Les données techniques peuvent aider un attaquant à comprendre le SI.
- Les sauvegardes deviennent critiques si la production est chiffrée.

## Diagramme 3 : utilisateurs et autorisations

Ce schéma relie les profils utilisateurs aux systèmes d'autorisation.

```mermaid
flowchart LR
    subgraph PROFILES["Profils"]
        direction TB
        MED["Médecins"]
        INF["Infirmiers"]
        ADM["Administratif"]
        IT["DSI / IT"]
        EXT["Prestataires"]
    end

    subgraph AUTH["Autorisations"]
        direction TB
        IAM["Active Directory / IAM"]
        BADGE["Badge / carte pro"]
        VPN["VPN / télémaintenance"]
    end

    subgraph SYSTEMS["Systèmes"]
        direction TB
        DPI["DPI"]
        RDV["Rendez-vous / admissions"]
        ADMIN["Administration SI"]
        BIOMED["Biomédical"]
    end

    MED -->|"compte nominatif"| IAM
    INF -->|"compte ou poste partagé"| IAM
    ADM -->|"compte nominatif"| IAM
    IT -->|"compte admin séparé"| IAM
    EXT -->|"compte prestataire"| VPN
    BADGE -->|"accès physique / logique"| DPI
    IAM -->|"droits métier"| DPI
    IAM -->|"droits métier"| RDV
    IAM -->|"droits techniques"| ADMIN
    VPN -->|"maintenance"| BIOMED
    VPN -->|"support distant"| ADMIN

    classDef profile fill:#e0f2fe,stroke:#0369a1,stroke-width:1px,color:#111827;
    classDef auth fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#111827;
    classDef system fill:#dcfce7,stroke:#15803d,stroke-width:1px,color:#111827;

    class MED,INF,ADM,IT,EXT profile;
    class IAM,BADGE,VPN auth;
    class DPI,RDV,ADMIN,BIOMED system;

    linkStyle 0,1,2,3,5,6,7,8 stroke:#7c3aed,stroke-width:2px;
    linkStyle 4,9,10 stroke:#2563eb,stroke-width:2px;
```

### Hypothèses

- Les comptes prestataires doivent être séparés des comptes internes.
- Les comptes administrateurs doivent être séparés des comptes bureautiques.
- La carte professionnelle peut parfois servir à plusieurs usages.

## Diagramme 4 : chemin d'attaque ransomware

Ce schéma montre une lecture simple du scénario d'attaque.

```mermaid
flowchart LR
    ENTRY["1. Entrée<br/>phishing ou accès distant"]
    USER["2. Poste compromis<br/>utilisateur ou prestataire"]
    CREDS["3. Identifiants<br/>récupération de droits"]
    ADMIN["4. Administration<br/>AD, serveurs, partages"]
    APPS["5. Applications métiers<br/>DPI, labo, imagerie"]
    DATA["6. Données critiques<br/>patient, résultats"]
    BACKUP["7. Sauvegardes<br/>restauration"]
    CRISIS["8. Mode dégradé<br/>papier, téléphone"]

    ENTRY --> USER
    USER --> CREDS
    CREDS --> ADMIN
    ADMIN --> APPS
    APPS --> DATA
    DATA --> BACKUP
    DATA -. "SI indisponible" .-> CRISIS

    classDef attack fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#111827;
    classDef critical fill:#fef3c7,stroke:#ca8a04,stroke-width:2px,color:#111827;
    classDef crisis fill:#f1f5f9,stroke:#64748b,stroke-width:2px,color:#111827;

    class ENTRY,USER,CREDS,ADMIN attack;
    class APPS,DATA,BACKUP critical;
    class CRISIS crisis;

    linkStyle 0,1,2,3,4,5 stroke:#dc2626,stroke-width:2.5px;
    linkStyle 6 stroke:#64748b,stroke-width:2px,stroke-dasharray:5 5;
```

### Hypothèses

- Le scénario est volontairement simplifié.
- L'attaque peut entrer par un poste utilisateur, un accès distant ou un service exposé.
- Le risque augmente si les droits sont trop larges et si les sauvegardes sont accessibles depuis le SI compromis.

## À retenir

Finaliser un diagramme, ce n'est pas ajouter plus de détails.

C'est choisir ce qui doit rester visible pour qu'un tiers comprenne :

- les zones principales ;
- les flux essentiels ;
- les points critiques ;
- les hypothèses ;
- les risques majeurs.
