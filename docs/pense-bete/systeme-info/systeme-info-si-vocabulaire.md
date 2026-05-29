# Vocabulaire SI

| Terme | Définition simple | Pourquoi c'est important |
| --- | --- | --- |
| SI | système d'information : personnes, outils, données, procédures, infrastructures | dépasse la technique pure |
| Incident | événement qui perturbe le SI : panne, attaque, fuite, erreur de configuration | point de départ d'une analyse de risque |
| Mitigation | ensemble de mesures pour réduire un risque ou son impact | on ne supprime pas toujours le risque, mais on peut le rendre moins grave |
| Cause racine | vraie cause profonde d'un problème, pas seulement le symptôme visible | évite de corriger seulement la conséquence |
| Symptôme | ce qu'on voit quand l'incident arrive | peut cacher une cause plus profonde |
| Impact | conséquence concrète sur la technique, le métier ou l'organisation | permet de mesurer la gravité |
| Risque | scénario possible qui peut nuire au SI | aide à décider quoi protéger en priorité |
| Mesure technique | action basée sur un outil ou une configuration | exemple : MFA, segmentation, sauvegarde, supervision |
| Mesure organisationnelle | action basée sur une procédure, une règle ou une responsabilité | exemple : procédure de crise, validation, contrôle régulier |
| Mesure humaine | action qui aide les personnes à mieux agir | exemple : formation, consignes claires, simplification d'un outil |
| Confidentialité | seules les personnes autorisées peuvent accéder aux données | enjeu majeur en cas de fuite de données |
| Intégrité | les données restent exactes, complètes et non modifiées sans autorisation | important pour éviter erreurs, fraude ou données fausses |
| Disponibilité | le service reste accessible quand on en a besoin | enjeu central lors d'une panne ou d'un ransomware |
| Indisponibilité | service, application ou poste inutilisable | bloque le travail même si les données ne sont pas volées |
| Dépendance critique | élément dont beaucoup de services dépendent | si cet élément tombe, l'impact peut être massif |
| Rollback | retour à une version précédente après problème | limite l'impact d'une mise à jour défectueuse |
| DPI | dossier patient informatisé | coeur des données de soins |
| SPOF | Single Point of Failure : point unique de panne | un seul composant peut bloquer beaucoup de services |
| Middleware | couche logicielle qui connecte applications, données et utilisateurs | explique les dépendances entre systèmes |
| API | interface permettant à deux applications d'échanger | rend les flux applicatifs visibles |
| Flux | circulation d'une donnée ou demande entre deux éléments | base des diagrammes |
| Segmentation | découpage réseau en zones ou VLAN | limite les chemins possibles |
| Cloisonnement | séparation fonctionnelle ou technique des zones | limite la propagation |
| AD / Active Directory | annuaire central de comptes, groupes et droits | point critique pour l'authentification |
| IAM | gestion des identités et des accès | répond à qui a droit à quoi |
| VPN | accès distant sécurisé au SI | utile mais sensible pour prestataires |
| MFA | authentification multifacteur | réduit l'impact d'un mot de passe volé |
| PACS | stockage et consultation des images médicales | critique pour l'imagerie |
| RIS | système de radiologie : demandes, planning, comptes rendus | souvent lié au PACS et au DPI |
| SIEM | centralisation et corrélation des journaux de sécurité | aide à détecter les incidents |
| ToIP | téléphonie sur IP | peut aider en crise si isolée |
| PRA | plan de reprise d'activité | redémarrer après incident |
| PCA | plan de continuité d'activité | continuer malgré l'incident |
| Mode dégradé | fonctionnement réduit sans SI complet | papier, téléphone, procédures manuelles |
