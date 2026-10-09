# Itération 9 — Reprise du dispositif de détection

**9 octobre 2026 — Travail individuel**

Reprendre l’environnement J8 avant son utilisation : contrôler les sources,
générer des activités connues et retrouver les informations attendues.

- [Reprendre le dispositif de détection](reprendre-dispositif-detection.md)
- [Construire une vue exploitable des événements — 1 h](construire-vue-exploitable-evenements.md)
- [Vérifier votre capacité de détection](verifier-capacite-detection.md)
- [Préparer l’analyse d’une situation inhabituelle](preparer-analyse-situation-inhabituelle.md)
- [Incident : premiers éléments](incident-premiers-elements.md)
- [Qualifier la situation et préparer la suite](qualifier-situation-preparer-suite.md)
- [Pense-bête](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-9.md)
- [État documenté en J8](../it-8/index.md)
- [Retour au module](../README.md)

**Statut : sorties J9 intégrées.** Suricata actif, sept règles acceptées et
alertes 1008001/1008002/1008003 observées. File Browser répond 200/401 ;
agent Wazuh reconnecté et deux messages applicatifs J9 reçus dans les archives
du manager avec décodeur JSON. Alerte Wazuh spécifique et contrôles
complémentaires à terminer.

**Vue exploitable :** capture de 11:25:32 intégrée ; nouveaux essais A2/A4/A5
et trois alertes Suricata observés, message A4 reçu dans Wazuh. Trois captures navigateur
à 11:27 documentent la session ouverte et la consultation de test/test2 ;
capture EVE à 11:30:13 intégrée avec cinq GET 200 à 11:27, dont
`/api/resources/test2`. Corrélation du fichier test et traces applicatives
des consultations réussies non fournies.

**Capacité de détection :** dix captures intégrées : scan Nmap (99 ports
fermés, 22/8080 ouverts), refus sur 65001–65003 et trois chemins HTTP 200.
EVE corrélé au scan de 11:41:48 et aux trois ports fermés de 11:42:16 ;
URI b/c documentées. Flux affichés sans alerte associée ; nouvelles règles
et déclenchements correspondants à valider. Une capture jointe confirme
ensuite dix règles acceptées, code 0 et service relancé à 11:46:12 ;
essais des nouveaux SID et contrôles négatifs à réaliser.

**Tests après adaptation à 12:07 :** alertes 1009001 (scan), 1009002
(trois ports refusés) et 1009003 (trois chemins HTTP) observées. Tests
positifs documentés ; contrôles négatifs et qualité du seuil à compléter.

**Contrôle normal de 12:12:35 :** GET 200 visible dans tcpdump ; recherche
1009001–1009003 vide sur 12:12:30–12:12:41, code 0. Quatre captures
intégrées ; objet HTTP EVE de ce GET encore à fournir.

**Contrôle négatif complété :** objet HTTP EVE du GET `/` de 12:12:35
retrouvé (flux 1056229479386453), corrélé à tcpdump et curl. Aucun nouveau
SID sur la fenêtre recherchée, code 0 : test normal validé pour ce scénario.
Deux captures complémentaires intégrées ; tests positifs et contrôle
négatif désormais documentés.

**Investigation :** méthode préparatoire, ordre des sources et chronologie
vide disponibles ; aucun élément de la situation inconnue encore fourni.

**Reproduction du scénario depuis l’hôte, 14:33:13–14:35:38 :** EVE
retrouve 22 GET 200 et 99 alertes 1009001 pendant le scan. Exploration
et répétition HTTP visibles sans alerte HTTP dans l’extrait ; scénario
pédagogique distinct de l’invocation initiale sur la VM.

**Bilan d’investigation consolidé :** cadrage, fréquences, chronologie,
hypothèses et conclusion complétés avec les pièces disponibles. Scénario
pédagogique expliqué ; incident réel non établi. Informations non obtenues
et limites de visibilité documentées, sans résultat supposé.

**Suite J10 :** état provisoire séparant faits, hypothèses, manques, risques
conditionnels et actions avec impacts. Préservation et investigation ciblée
retenues ; aucune coupure effectuée, situation non clôturée.
