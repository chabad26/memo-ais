# Ce que dit la PSSI

## Le problème à résoudre

La PSSI d'Hexalp ne mentionne pas l'IA en 2022. Ses règles sur les informations, logiciels, services et comptes s'appliquent pourtant aux usages étudiés. L'objectif est de **rattacher chaque situation à une règle précise**, puis de distinguer l'écart démontré, l'information manquante et la règle insuffisamment précise.

Cette fiche traite l'étape **5. Règle PSSI** de la [méthode d'analyse](shadow-ia-de-quoi-parle-t-on.md). Elle ne réalise pas encore les trois qualifications de risque annoncées pour la séquence suivante.

## Référence — Extrait fourni de la PSSI Hexalp

**Version 3.2 — mars 2022.** Document du scénario pédagogique, et non constat d'une politique réellement déployée.

| Article | Règle |
| --- | --- |
| **2.1** | Toute information est classée C0 (public), C1 (interne), C2 (confidentiel) ou C3 (secret). |
| **2.3** | Les informations C2 et C3 ne peuvent être stockées, transmises ou traitées que sur des systèmes et des services validés par la DSI. |
| **4.1** | Seuls les logiciels du catalogue de la DSI peuvent être installés sur les postes. Toute autre installation est soumise à validation. |
| **4.4** | Tout abonnement à un service en ligne utilisé à des fins professionnelles est souscrit par la DSI ou avec son accord, quel que soit le mode de paiement. |
| **5.2** | Les comptes personnels (messagerie, stockage, services en ligne) ne doivent pas être utilisés pour traiter des informations d'Hexalp. |
| **5.5** | Les secrets (mots de passe, clés, jetons) sont conservés dans le coffre-fort de mots de passe d'Hexalp. Ils ne sont jamais transmis en clair ni écrits dans un script ou un fichier non chiffré. |
| **7.1** | Tout transfert de données personnelles vers un prestataire nécessite un contrat conforme au RGPD, validé par le DPO. |
| **8.1** | Tout incident de sécurité, ou toute suspicion d'incident, est signalé au RSSI sans délai. |
| **9.2** | Les demandes de dérogation sont adressées au RSSI, qui y répond sous 10 jours ouvrés. |

L'article 7.1 est ici une **exigence interne à vérifier** : l'absence de contrat dans l'énoncé ne démontre pas à elle seule son absence réelle ni une infraction au RGPD.

## Mission — Tableau de rattachement renseigné

Les huit premières lignes reprennent les [situations de 2.2](shadow-ia-de-quoi-parle-t-on.md). **Conforme** signifie conforme au périmètre documenté, sans certification globale. **Écart** suppose une condition démontrée ou une hypothèse annoncée. **Zone grise** signale ici soit une ambiguïté de règle, soit un fait manquant : la justification précise lequel.

| Situation | Article(s) applicable(s) | Conforme / écart / zone grise | Justification |
| --- | --- | --- | --- |
| **1 — Traduction du contrat fournisseur dans le navigateur** | **2.1**, **2.3** si C2/C3 ; **4.4** si abonnement ; **5.2** si compte personnel ; **7.1** si données personnelles transférées | **Zone grise — faits à vérifier ; écart si contrat C2 traité par un service non validé** | Le contrat peut contenir des données confidentielles, mais son contenu et le traitement local/distant doivent être établis. Le statut shadow retenu en 2.2 reposait sur une hypothèse. Un navigateur approuvé ne valide pas automatiquement son moteur de traduction ; ne pas inventer un abonnement ou un compte personnel. |
| **2 — Générateur d'images acheté par la DSI avec contrat** | **4.4** ; **4.1** si logiciel installé ; **2.1**, **2.3**, **5.2**, **7.1** selon compte et contenus | **Conforme pour la souscription et le périmètre approuvé retenu en 2.2** | L'achat par la DSI répond à 4.4 dans le scénario. Il ne démontre pas que toute donnée est autorisée ni qu'un contrat DPO existe pour un éventuel transfert de données personnelles. Utiliser le compte et les contenus prévus par la validation. |
| **3 — Photo du trieur envoyée depuis un téléphone personnel** | **2.1** ; **2.3** si C2/C3 ; **5.2** si compte personnel ; **7.1** si données personnelles ; **8.1** en cas de suspicion d'exposition | **Zone grise sur les faits ; écart si compte personnel ou données C2/C3 sur système/service non validé** | L'envoi est décrit, mais **téléphone personnel ≠ preuve de compte personnel**. Examiner la photo, le compte et les validations. Si la capture contient une configuration confidentielle envoyée à un service non validé, 2.3 est enfreint. Le périmètre de 4.1 sur un appareil personnel reste à préciser. |
| **4 — Assistant IA de paie activé par mise à jour** | **2.1**, **2.3** ; **4.1**, **4.4** pour le périmètre logiciel/service ; **7.1** si données personnelles transférées | **Zone grise — périmètre de validation et fonctionnement inconnus** | L'approbation de 2021 ne dit pas si la fonction ajoutée est couverte. L'activation seule ne prouve aucun transfert. Si des données de paie C2 sont traitées par un nouveau service non validé, l'écart à 2.3 est établi ; vérifier aussi le contrat et sa validation DPO. |
| **5 — Modèle local open source pour relire le code** | **4.1** ; **2.1**, **2.3** pour le code C2 | **Zone grise documentaire ; écart si installation hors catalogue sans validation** | Le fonctionnement hors ligne ne dispense pas de 4.1. Vérifier les installations effectivement réalisées, le catalogue et la validation du poste/outillage pour le code C2. Une installation non validée est un écart même sans fuite. L'absence de connexion décrite ne justifie pas d'appliquer 7.1 pour un transfert inexistant. |
| **6 — Transcription démarrée après trois semaines sans réponse DSI** | **4.4** si abonnement ; **2.1**, **2.3** selon réunions ; **5.2** selon compte ; **7.1** si données personnelles transférées ; **9.2** si demande de dérogation adressée au RSSI | **Usage non validé ; écart conditionnel sur les données/abonnement ; suivi organisationnel défaillant à examiner** | Déclarer ne vaut pas autoriser. Si abonnement professionnel sans accord, écart à 4.4 ; si réunion C2 traitée par un service non validé, écart à 2.3. Les trois semaines sont un signal d'alerte pour 9.2, mais l'énoncé parle d'une demande d'autorisation à la DSI, pas d'une dérogation reçue par le RSSI : voir l'analyse ci-dessous. |
| **7 — Service IA via « Se connecter avec Microsoft »** | **4.4** si abonnement ; **2.1**, **2.3** selon données ; **7.1** si transfert de données personnelles | **Zone grise — service, contrat et droits à vérifier** | Le compte Hexalp n'est pas un compte personnel au sens de 5.2, dans le périmètre décrit. Le SSO ne prouve ni validation du service ni consentement à des permissions Graph. Il faut examiner ces éléments séparément. |
| **8 — Transcription du standard prévue au contrat DSI** | **4.4** ; **2.1**, **2.3** ; **7.1** si données personnelles transférées au prestataire | **Conforme pour la fonction contractuellement approuvée ; 7.1 à vérifier** | La fonction est explicitement prévue dans le contrat signé par la DSI. Si les messages contiennent des données personnelles traitées par un prestataire, vérifier le contrat exigé par 7.1 et sa validation DPO. Une signature DSI ne prouve pas cette validation à elle seule. |
| **Thomas — Logs WMS et fichier `.env` préparés pour un assistant** | **2.1**, **2.3**, **5.5** ; **5.2** selon compte ; **7.1** si transfert des coordonnées personnelles ; **8.1** si exposition suspectée | **Écart à 5.5 dans le kit : secrets en clair ; envoi externe non établi** | L'extrait de 2.4 montre un mot de passe et un jeton en clair dans un bloc `.env`, contrairement à 5.5. Le copier-coller **préparé** ne prouve pas qu'il est parti. S'il est envoyé à un service non validé : écart à 2.3 ; avec compte personnel : 5.2 ; avec données personnelles, vérifier 7.1. Ne pas attendre une exploitation démontrée pour signaler une suspicion selon 8.1. |
| **InboxPilot — Écran de consentement à six permissions** | **2.1**, **2.3** pour les données accessibles ; **4.4** si abonnement ; **7.1** si transfert personnel ; **5.5** pour le stockage des jetons ; **8.1** si abus suspecté | **Zone grise — consentement non confirmé et règles de connecteurs incomplètes** | L'écran montre une demande, pas une acceptation ni une lecture. Si accord et traitement de C2/C3 par un service non validé : écart à 2.3. Aucune règle citée n'impose explicitement une validation DSI de chaque consentement OAuth ou le moindre privilège. L'éditeur non vérifié ne prouve pas seul un écart. Le stockage des jetons n'est pas visible dans l'écran : 5.5 ne peut pas être déclaré respecté ou enfreint. |

**Ce qui change depuis 2.2 :** le statut organisationnel et la conformité ne sont pas la même chose. Un usage peut être connu mais non autorisé ; un usage local peut enfreindre une règle d'installation ; un outil acheté peut encore être utilisé avec des données hors de son périmètre. Une zone grise documentaire se résout par une preuve ; une ambiguïté de règle demande une clarification de la PSSI.

## 1. Quels angles morts faut-il traiter ?

| Angle mort ou couverture insuffisante | Ce que la PSSI couvre déjà | Ce qu'il faudrait préciser pour l'IA |
| --- | --- | --- |
| **IA ajoutée à un outil approuvé** | Validation des logiciels et des services, protection de C2/C3 | Réévaluation lors d'une nouvelle fonction, d'un changement de fournisseur, de flux ou de conditions ; activation maîtrisée |
| **Consentements, connecteurs et agents** | Protection des informations ; conservation des secrets | Autorité pouvant accorder les droits, permissions minimales, durée, revue périodique, révocation et validation humaine avant actions à impact |
| **Services gratuits, sans abonnement ou sans compte** | 2.3 protège C2/C3 même sans paiement | 4.4 parle d'abonnement : préciser la validation de tout service professionnel, même gratuit et sans inscription, notamment pour C1 |
| **Contexte collecté automatiquement** | Classification générale des informations | Règles pour fichiers voisins d'un IDE, mémoire, pièces jointes, captures, métadonnées et indexation ; minimisation et exclusions |
| **Conservation et réutilisation par le fournisseur** | 7.1 pour le transfert de données personnelles | Critères de validation sur entraînement, historique, suppression, sous-traitants et continuité des comptes, y compris pour les données non personnelles |
| **Réponses générées et exécution** | Aucune règle explicite dans cet extrait sur ce point | Relecture des conseils techniques, validation du code et des commandes, contrôle des sorties réseau et traçabilité des actions d'agents |
| **Jetons OAuth gérés par une application** | 5.5 impose le coffre-fort et interdit les secrets en clair | Définir le stockage technique sécurisé approuvé des jetons renouvelables, leur cycle de vie et la frontière avec le coffre-fort de mots de passe ; ne pas déclarer les jetons exemptés sans décision |

Ces propositions nourriront la politique du J5 ; elles ne sont pas présentées comme des règles déjà adoptées. L'absence d'un article dans **l'extrait fourni** ne prouve pas son absence de toute autre procédure d'Hexalp.

### Une extension de navigateur est-elle un logiciel au sens de 4.1 ?

**Oui, l'interprétation opérationnelle retenue est qu'une extension installée ajoute du logiciel au poste.** Elle relève donc du catalogue ou d'une validation, même si son installation se fait depuis le navigateur. La PSSI devrait nommer explicitement extensions et modules complémentaires pour éviter une lecture restrictive.

Une fonction intégrée par mise à jour ou un service web utilisé sans installation n'est pas nécessairement une nouvelle installation au sens strict de 4.1. Cela ne le dispense pas des règles sur le service, les comptes et les données. Une extension validée n'autorise pas non plus tous les accès qu'elle peut demander ultérieurement.

## 2. Article 9.2 : Hexalp respecte-t-elle ses propres règles ?

### Ce que la situation permet d'établir

La manageuse a demandé à **la DSI** l'autorisation d'utiliser un outil et n'a pas eu de réponse depuis **trois semaines**. L'article 9.2 traite, lui, de **demandes de dérogation adressées au RSSI**, avec réponse sous **10 jours ouvrés**. Ces deux descriptions ne sont pas automatiquement équivalentes.

**Si la demande était bien une dérogation reçue par le RSSI et que plus de dix jours ouvrés se sont écoulés, Hexalp ne respecte pas 9.2.** Il faut vérifier date de réception, destinataire, nature de la demande et calendrier ouvré ; trois semaines civiles ne donnent pas à elles seules le décompte exact. Si c'était une simple demande d'ajout au catalogue restée à la DSI, l'écart à 9.2 n'est pas démontré, mais l'absence de traitement et de relais constitue un dysfonctionnement à corriger.

### Ce que cela change à l'analyse

Le problème ne peut pas être ramené au comportement de la manageuse. L'organisation doit instruire la demande, assurer son acheminement, répondre dans le délai applicable et proposer une solution qui couvre le besoin de transcription. **Le dépassement d'un délai ne vaut pas autorisation tacite** : aucune règle fournie ne le prévoit. Il n'efface pas non plus un éventuel traitement interdit de données.

**Actions proposées :** enregistrer la date et le propriétaire de chaque demande, distinguer validation ordinaire et dérogation, transmettre au RSSI si nécessaire, alerter avant l'échéance et communiquer une décision motivée ou une solution transitoire validée. Vérifier séparément le compte, les données des réunions et les contrats de l'outil déjà utilisé. Aucune de ces actions n'est attestée comme réalisée.

## Livrable obtenu et éléments à vérifier

Le tableau de **dix situations** est renseigné et les angles morts sont identifiés. Les principales pièces à rechercher sont les validations DSI et leur périmètre, comptes et abonnements, contrats validés par le DPO, traces de consentement et d'accès, preuve d'envoi éventuel de Thomas et historique de la demande de transcription.

**Source principale :** extrait de la PSSI v3.2 fourni dans la consigne, rapproché des situations fictives des sections [2.2](shadow-ia-de-quoi-parle-t-on.md), [2.4](quelles-donnees-sont-envoyees.md) et [2.5](connecteurs-quand-ia-a-les-cles.md). Cette analyse applique les règles internes du scénario ; elle ne constitue pas un audit de conformité réglementaire ni une qualification juridique de faute.

[Retour à l'itération 2](index.md)
