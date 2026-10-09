# Pense-bête — Itération 9 : reprendre la détection

| Terme | Sens dans la reprise |
| --- | --- |
| Source de détection | Trafic réseau, journal applicatif ou autre trace réellement observable |
| Contrôle de bout en bout | Générer une activité, retrouver sa trace à la source puis au point d’exploitation prévu |
| Contrôle positif / négatif | Vérifier la détection d’un marqueur et comparer avec une activité sans ce marqueur |
| EVE / flow_id | Journal JSON Suricata / identifiant reliant les événements d’un flux |
| Archives / alertes Wazuh | Messages archivés / événements répondant aux conditions de règles ; réception et alerte sont distinctes |
| Source Docker json-file | Journal stdout/stderr du conteneur ; chemin à recontrôler après recréation |
| Non vérifiable | Information manquante pour conclure sur le contrôle actuel |

**Ordre utile :** activité → trace locale → collecte → réception → règle → vue de recherche.
Un processus actif ou un agent connecté ne valide pas à lui seul toute la chaîne.
Conserver les heures et fuseaux ; ne pas publier les secrets.

L’agent fonctionnel documenté en J8 était sur la **VM File Browser**, pas dans
le conteneur. Si sa collecte manque en J9, poursuivre avec les sources disponibles
et noter la limite sans consacrer la séance à une nouvelle installation.

- [Reprendre le dispositif](../../../securisation-avancee-infrastructures/it-9/reprendre-dispositif-detection.md)
- [Itération 9](../../../securisation-avancee-infrastructures/it-9/index.md)
- [Tous les pense-bêtes](../../index.md)

## Construire une vue exploitable

**Signal :** information utile à la question de surveillance. **Bruit :**
événements peu utiles dans cette vue, à mesurer avant filtrage.
**Redondance :** plusieurs traces du même échange ou copie d’un message
Docker dans Wazuh ; conserver la provenance sans compter deux activités.

Corréler heure/fuseau, IP, URI, méthode et statut. `flow_id` est local à
Suricata ; aucun identifiant commun avec Wazuh n’est établi. Sur une alerte
de réponse 401, la source réseau est le serveur, pas l’initiateur.

- [Construire une vue exploitable — 1 h](../../../securisation-avancee-infrastructures/it-9/construire-vue-exploitable-evenements.md)

## Vérifier la capacité de détection

- **SYN / RST :** tentative d’ouverture TCP / réinitialisation ; un RST doit
  être rapproché du SYN et du contexte, pas assimilé automatiquement à un port fermé.
- **Closed / filtered :** refus établi par les réponses / filtrage ou absence
  de réponse compatible ; conserver l’état réellement observé.
- **Seuil SYN :** compte des paquets correspondants, pas des ports distincts.
- **Chemin inhabituel :** dépend des usages ; un motif pédagogique ne couvre
  pas tous les chemins et un 200 ne prouve pas un fichier existant.

[Vérifier votre capacité de détection](../../../securisation-avancee-infrastructures/it-9/verifier-capacite-detection.md) :
observer d’abord, adapter si nécessaire, tester positif/négatif et documenter
ce que les événements permettent de conclure. Comportement détecté et
intention sont deux informations distinctes.

## Préparer une investigation

**Fait observé :** information présente dans une pièce référencée.
**Interprétation :** sens donné au fait dans son contexte. **Hypothèse :**
explication possible à tester, avec éléments qui pourraient la contredire.
La confiance qualifie une proposition ; elle ne mesure pas la gravité.

Ordre : premier indice → source originale → corrélation → autorisation et
conséquences → chronologie → qualification provisoire. Conserver les fuseaux,
les références et les limites des recherches ; absence de résultat ≠ absence
d’activité. `allowed` dans l’IDS n’est pas une autorisation métier.

[Préparer l’analyse d’une situation inhabituelle](../../../securisation-avancee-infrastructures/it-9/preparer-analyse-situation-inhabituelle.md).

## Premiers éléments

Obtenir début/fin/fuseau avant de filtrer. Séparer tests connus et activité
signalée ; compter les transactions HTTP sans ajouter les copies d’alertes.
Premier événement retrouvé ≠ début certain. Conserver critères des recherches
vides et comparer avant/après. Chaque conclusion renvoie à ses pièces.

[Incident : premiers éléments](../../../securisation-avancee-infrastructures/it-9/incident-premiers-elements.md).

## Qualifier et préparer J10

**Risque conditionnel :** conséquence possible si une activité est réellement
malveillante, pas dommage déjà observé. **Mesure de confinement :** action
de limitation/isolation/arrêt à justifier par les faits et son impact sur
le service et les preuves. Qualification provisoire ≠ clôture.

Conserver les originaux utiles et les limites ; prioriser les lectures ciblées.
Ne pas appliquer toutes les mesures possibles ni certifier l’absence de
conséquences faute d’information.

[Qualifier la situation et préparer la suite](../../../securisation-avancee-infrastructures/it-9/qualifier-situation-preparer-suite.md).
