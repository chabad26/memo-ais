# Diagrammes finaux et résumé

## Objectif

Produire des diagrammes propres, lisibles et compréhensibles, puis savoir expliquer pourquoi l'architecture proposée est crédible.

Un bon diagramme doit pouvoir être compris sans explication orale. Il doit donc avoir :

- un titre clair ;
- peu d'éléments ;
- des flèches directionnelles ;
- une légende ;
- des hypothèses explicites.

Message à défendre :

**Le SI hospitalier est critique parce qu'il relie les soins, les utilisateurs, les applications, les données, les droits d'accès et les sauvegardes. Un ransomware devient grave quand il atteint ces points de concentration.**

## Versions draw.io

Les diagrammes sont aussi disponibles au format diagrams.net / draw.io :

- [00 - Schéma complet du SI hospitalier](drawio/00-schema-complet-si-hospitalier.drawio.png)
- [01 - Vue réseau simplifiée](drawio/01-vue-reseau-simplifiee.drawio.png)
- [02 - Flux de données critiques](drawio/02-flux-donnees-critiques.drawio.png)
- [03 - Utilisateurs et autorisations](drawio/03-utilisateurs-autorisations.drawio.png)
- [04 - Chemin d'attaque ransomware](drawio/04-chemin-attaque-ransomware.drawio.png)
- [05 - Vue hardware simplifiée](drawio/05-vue-hardware-simplifiee.drawio.png)
- [06 - Cartographie applicative](drawio/06-cartographie-applicative.drawio.png)

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

### Hypothèses flux

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

### Hypothèses user/auth

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

### Hypothèses attaque

- Le scénario est volontairement simplifié.
- L'attaque peut entrer par un poste utilisateur, un accès distant ou un service exposé.
- Le risque augmente si les droits sont trop larges et si les sauvegardes sont accessibles depuis le SI compromis.

## Diagramme 5 : vue hardware simplifiée

Ce schéma donne une idée matérielle du chemin entre Internet, les équipements réseau, les serveurs et quelques postes représentatifs.

Il ne cherche pas à montrer tous les postes : les machines dessinées servent seulement d'exemples.

```mermaid
flowchart LR
    INTERNET["Internet"]
    ROUTER["Routeur / box<br/>accès opérateur"]
    FW["Pare-feu<br/>filtrage"]
    SWITCH["Switch coeur réseau<br/>réseau local"]

    subgraph SRV["Salle serveur"]
        direction TB
        APP["Serveur applicatif<br/>DPI, métiers"]
        AD["Serveur AD / DNS<br/>comptes, noms"]
        BACKUP["Serveur sauvegarde<br/>copies"]
    end

    subgraph POSTS["Postes / machines"]
        direction TB
        P1["Poste soins<br/>exemple"]
        P2["Poste accueil<br/>exemple"]
        P3["Poste admin IT<br/>exemple"]
        PRN["Imprimante / équipement<br/>exemple"]
    end

    INTERNET --> ROUTER
    ROUTER --> FW
    FW --> SWITCH
    SWITCH --> APP
    SWITCH --> AD
    SWITCH --> BACKUP
    SWITCH --> P1
    SWITCH --> P2
    SWITCH --> P3
    SWITCH --> PRN
    P1 -->|"accès applicatif"| APP
    P2 -->|"accès applicatif"| APP
    P3 -->|"administration"| AD
    APP -->|"authentification"| AD
    APP -->|"copies"| BACKUP

    classDef internet fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#111827;
    classDef network fill:#e0f2fe,stroke:#0369a1,stroke-width:2px,color:#111827;
    classDef server fill:#fef3c7,stroke:#ca8a04,stroke-width:2px,color:#111827;
    classDef workstation fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#111827;
    classDef admin fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#111827;

    class INTERNET internet;
    class ROUTER,FW,SWITCH network;
    class APP,AD,BACKUP server;
    class P1,P2,PRN workstation;
    class P3 admin;

    linkStyle 0,1,2 stroke:#2563eb,stroke-width:2px;
    linkStyle 3,4,5,6,7,8,9 stroke:#0369a1,stroke-width:2px;
    linkStyle 10,11 stroke:#16a34a,stroke-width:2px;
    linkStyle 12,13 stroke:#7c3aed,stroke-width:2px;
    linkStyle 14 stroke:#ca8a04,stroke-width:2px;
```

### Hypothèses sur le hardware

- Le routeur, le pare-feu et le switch représentent les équipements réseau principaux.
- Les serveurs sont regroupés pour montrer le principe, pas le nombre réel de machines.
- Les postes affichés sont des exemples : il peut y en avoir beaucoup plus dans un vrai hôpital.
- Le chemin à retenir est : **Internet -> périmètre réseau -> réseau local -> serveurs et postes**.

## Résumé de présentation

| Partie | Message à faire passer | Diagramme à utiliser |
| --- | --- | --- |
| Structure du SI | Le SI est découpé en zones : utilisateurs, applications, administration, données, sauvegardes. | Vue réseau simplifiée |
| Données critiques | Les données patient, examens, droits et sauvegardes sont les cibles prioritaires. | Flux de données critiques |
| Utilisateurs et accès | Les profils métier ont des contraintes réelles et des droits différents. | Utilisateurs et autorisations |
| Risque ransomware | Une attaque peut partir d'un poste ou d'un accès distant puis se propager. | Chemin d'attaque |
| Vue matérielle | Internet arrive sur des équipements réseau, puis dessert les serveurs et quelques postes représentatifs. | Vue hardware simplifiée |

## Points critiques à défendre

| Point critique | Pourquoi c'est important |
| --- | --- |
| Active Directory / IAM | concentre l'authentification et les droits |
| DPI | porte le dossier patient et les soins informatisés |
| VPN / prestataires | peut devenir une entrée distante vers le SI |
| Données patient et examens | indispensables aux soins et très sensibles |
| Sauvegardes | dernière solution pour restaurer après chiffrement |
| Biomédical | équipements critiques, parfois difficiles à mettre à jour |

## Pourquoi c'est crédible ?

- Les zones retenues correspondent aux usages réels d'un hôpital : soigner, administrer, maintenir, restaurer.
- Les flux représentés sont les flux essentiels : accès applicatif, droits, données, sauvegardes.
- Les points critiques sont des points de concentration : comptes, données, applications, accès distant.
- Les hypothèses sont annoncées comme telles et restent vérifiables.
- Les limites sont identifiées : droits exacts, segmentation réelle, accès prestataires, isolation des sauvegardes.

## Limites à annoncer

| Limite | À vérifier |
| --- | --- |
| Accès distants | quels VPN, quels prestataires, quels droits |
| Segmentation | quelles zones sont réellement séparées |
| Droits applicatifs | qui lit, écrit ou administre |
| Sauvegardes | isolation, fréquence, tests de restauration |
| Biomédical | équipements connectés et niveau de cloisonnement |

## Questions possibles

| Question | Réponse courte |
| --- | --- |
| Pourquoi l'AD/IAM est critique ? | Parce qu'il contrôle les comptes et les droits. |
| Pourquoi les sauvegardes sont centrales ? | Parce qu'elles conditionnent la reprise après ransomware. |
| Pourquoi parler des utilisateurs ? | Parce que les accès et contraintes métier influencent la sécurité. |
| Pourquoi un prestataire est sensible ? | Parce qu'il peut avoir un accès distant et technique. |
| Pourquoi cette architecture est crédible ? | Elle part des usages réels et identifie clairement les hypothèses. |

## À retenir

Finaliser un diagramme, ce n'est pas ajouter plus de détails.

C'est choisir ce qui doit rester visible pour qu'un tiers comprenne :

- les zones principales ;
- les flux essentiels ;
- les points critiques ;
- les hypothèses ;
- les risques majeurs.
