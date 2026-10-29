# Itération 3 — J4 : Concevoir et mettre en œuvre des protections réseau

## 🎯 Objectifs de la journée

Concevoir et mettre en œuvre des protections réseau adaptées aux besoins d’une installation industrielle, en tenant compte de ses contraintes d’exploitation et de ses interactions avec les systèmes informatiques de l’entreprise.

À partir de l’architecture Montval étudiée en J3, intégrer les services informatiques du magasin, définir les flux nécessaires, élaborer les règles de pare-feu et protéger un régulateur industriel obsolète qui ne peut plus recevoir de mises à jour.

Utiliser ensuite le laboratoire frigorifique pour mettre en œuvre et tester des mesures de protection, en vérifiant que les fonctions nécessaires au processus restent opérationnelles.

**Matinée accompagnée par le formateur ; après-midi en autonomie.** En fin de journée, pouvoir proposer et configurer une segmentation IT/OT, définir les communications autorisées, identifier les limites des protections et vérifier leur fonctionnement.

## Fiches disponibles

- [4.1 — Intégrer les services informatiques du magasin](integrer-services-informatiques-magasin.md) : nouveaux composants, données, initiateurs et dépendances ; schéma étendu avec fournisseurs et maintenance distincts.
- [4.2 — Définir les accès et les règles de pare-feu](definir-acces-regles-pare-feu.md) : zones, matrice, hypothèses de ports, règles ordonnées et CSV ; états de connexion et refus par défaut.
- [4.3 — Protéger un régulateur industriel obsolète](proteger-regulateur-industriel-obsolete.md) : REG-02, GW lecture/maintenance proposé, limites et règles Q ; R10/R22 retirées pour REG-02.
- [4.4 — Préparer les essais de segmentation](preparer-essais-segmentation.md) : composants du PoC, fiche de topologie à compléter et plan T00–T10 avec méthodes et attentes.
- [4.5 — Mettre en œuvre le filtrage IT/OT](mettre-en-oeuvre-filtrage-it-ot.md) : VM 192.168.122.105, quatre namespaces et filtrage appliqués ; 8 contrôles conformes, exports réels et douze captures utilisateur intégrées ; refus par défaut confirmé et PCAP de 39 trames.
- [4.6 — Tester les protections et le fonctionnement](tester-protections-fonctionnement.md) : sept captures, tests conformes, régulation locale observée pendant coupure et reprise des lectures/API attestée.
- [4.7 — Documenter les protections et leurs limites](documenter-protections-limites.md) : dossier C4 unique et PDF formateur ; architecture et 32 règles proposées, configuration appliquée, preuves et limites.
- [Pense-bête de l’itération 3](../../pense-bete/glossaire/informatique-industrielle/it-3.md).

## Référence et état du travail

[Dossier J3](../it-2/finaliser-dossier-analyse-it-ot.md) et [manuel MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md). Les nouveaux services métier sont fournis par la consigne 4.1, sans protocole, port ou authentification documentés.

Les fiches 4.1 à 4.3 présentent l’intégration, le filtrage et les protections compensatoires proposés : aucune configuration réseau ni recette J4 n’est encore attestée. La fiche 4.3 identifie désormais **REG-02** comme obsolète, sans nouveau correctif ni remplacement financé cette année ; cette nouvelle contrainte succède au scénario SIT-03 du J3. Le briefing 4.4 prépare les essais ; la documentation disponible ne fournit pas encore les noms/adresses de la topologie séparée. Le 4.5 propose maintenant une topologie privée à quatre namespaces pour la VM 192.168.122.105, avec fichiers déposés et exécution vérifiée après saisie sudo utilisateur : 8 contrôles conformes et exports réels récupérés. L’approbation du formateur et les tests hors périmètre restent distincts. Le dossier 4.7 réunit la proposition et les preuves de laboratoire, avec le PDF C4 ; aucune mise en œuvre Montval réelle n’est revendiquée.

[Retour au module](../README.md)
