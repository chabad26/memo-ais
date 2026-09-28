# Glossaire Sécurité des données - Itération 5

| Terme | Définition courte |
| --- | --- |
| Cycle de vie d'une clé | Étapes de création, usage, sauvegarde, rotation, révocation et destruction. |
| Rotation | Remplacement planifié d'une clé par une nouvelle clé. |
| Révocation | Retrait de la confiance ou de l'autorisation accordée à une clé. |
| TPM2 | Composant matériel pouvant protéger et mesurer des secrets. |
| `systemd-cryptenroll` | Outil systemd pour associer des moyens d'ouverture à un volume LUKS. |
| Clevis | Client d'autodéverrouillage de volumes chiffrés. |
| Tang | Service réseau fournissant une liaison de récupération pour Clevis. |
| KMS | Service de gestion de clés cryptographiques. |
| HSM | Matériel spécialisé pour protéger et utiliser des clés cryptographiques. |
| Coffre-fort de secrets | Service contrôlant le stockage et la délivrance de secrets avec authentification et audit. |
| Keyslot de secours | Emplacement LUKS contenant un moyen d'ouverture indépendant du mécanisme normal. |
| PCR | Registre du TPM contenant une mesure de l'état de composants du démarrage. |
| vTPM | TPM virtuel présenté à une machine virtuelle avec un état qui doit rester persistant. |
| Double approbation | Règle imposant l'accord de deux personnes distinctes pour une opération sensible. |
| Séparation des responsabilités | Répartition des droits afin qu'une seule personne ou un seul outil ne contrôle pas toute la chaîne. |
| Secret commun | Même secret réutilisé sur plusieurs machines, créant un impact collectif en cas de compromission. |
