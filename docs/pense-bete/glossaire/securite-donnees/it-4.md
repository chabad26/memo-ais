# Glossaire Sécurité des données - Itération 4

| Terme | Définition courte |
| --- | --- |
| Aléa | Valeur imprévisible utilisée notamment pour produire des secrets. |
| Pseudo-aléa | Valeur produite par un algorithme déterministe à partir d'un état initial. |
| CSPRNG | Générateur pseudo-aléatoire conçu pour résister aux prédictions. |
| Entropie | Mesure de l'incertitude disponible pour produire un secret. |
| Seed | Valeur initiale qui détermine la suite produite par un générateur pseudo-aléatoire déterministe. |
| Espace de clés | Ensemble des clés qu'un mécanisme peut réellement produire ou qu'un attaquant doit explorer. |
| `getrandom(2)` | Appel système Linux permettant d'obtenir des octets depuis le générateur cryptographique du noyau. |
| `/dev/urandom` | Interface Linux fournissant des octets issus du générateur cryptographique du noyau. |
| `secrets` | Module Python destiné à produire des valeurs adaptées aux secrets, contrairement au module `random`. |
| Sauvegarde du header | Copie de secours des métadonnées nécessaires à la récupération d'un volume. |
| Header LUKS | Métadonnées du volume contenant notamment ses paramètres cryptographiques, son UUID et ses keyslots. |
| Keyslot | Emplacement du header protégeant une copie de la clé de volume à l'aide d'un moyen d'accès. |
| `luksErase` | Opération destructive qui efface les keyslots sans réécrire tous les blocs de données chiffrés. |
| `luksHeaderBackup` | Commande qui sauvegarde le header LUKS dans un fichier externe sensible. |
| `luksHeaderRestore` | Commande qui remplace le header d'un volume par une sauvegarde compatible. |
| qcow2 | Format d'image disque de QEMU prenant notamment en charge l'allocation dynamique et les instantanés. |
| NBD | Network Block Device, mécanisme exposant une image disque comme un périphérique bloc Linux. |
| `qemu-nbd` | Outil permettant de raccorder une image QEMU à un périphérique NBD lorsque la VM est arrêtée. |
| Fichier témoin | Fichier créé avant l'incident et contrôlé après restauration pour vérifier la récupération des données. |
| Empreinte SHA-256 | Condensat utilisé ici pour comparer l'intégrité du fichier témoin avant et après l'incident. |
| Récupération | Retour à un état permettant de relire les données après un incident. |
| Secret | Information qui doit rester connue des seules personnes ou fonctions autorisées. |
| Destruction contrôlée | Suppression planifiée et vérifiable d'une information sensible. |
