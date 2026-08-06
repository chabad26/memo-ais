# Valider la stratégie de sauvegarde

## Objectif

Vérifier, à partir d'un scénario de corruption OpenLDAP, si les sauvegardes et
les procédures permettent de respecter les objectifs du PCA et du PRA.

## 1. Scénario retenu

La base LDAP est corrompue après une mauvaise opération d'administration. Les
utilisateurs ne peuvent plus être recherchés et les services dépendants
(Samba et messagerie) ne peuvent plus authentifier correctement les comptes.

| Élément | Réponse |
|---|---|
| Incident | Corruption de la base OpenLDAP |
| Service prioritaire | Authentification centralisée |
| Objectif PCA | Interruption maximale de 4 heures |
| Objectif PRA | Reprise de l'authentification en 2 heures |
| Dernière archive validée | `embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` |
| Fréquence réellement automatisée | Quotidienne à 02 h 00 |
| Perte maximale actuelle | Jusqu'à 24 heures de modifications LDAP |
| Temps de reprise estimé | 1 h 20 |

L'archive choisie doit obligatoirement être antérieure au début de la
corruption. L'archive indiquée sert de référence à l'exercice ; lors d'un
incident réel, l'administrateur sélectionne la dernière archive saine.

## 2. Sauvegardes nécessaires

La sauvegarde Borg contient plusieurs moyens de reprise complémentaires :

- `openldap-data.ldif` : export logique des entrées LDAP ;
- `openldap-config.ldif` : export logique de la configuration `cn=config` ;
- `openldap_ldap_data.tar.gz` : copie du volume de données ;
- `openldap_ldap_config.tar.gz` : copie du volume de configuration ;
- `openldap_ldap_backups.tar.gz` : sauvegardes internes OpenLDAP ;
- `openldap/compose.yaml`, `.env.example` et la documentation versionnée ;
- fichier `.env` protégé et clé Borg conservés séparément.

Pour une corruption logique limitée, l'export LDIF est privilégié. Pour une
perte complète de l'hôte ou des volumes, les archives des volumes permettent
de reconstruire une instance identique dans un environnement isolé.

## 3. Procédure de restauration proposée

### Étape 1 - Déclarer et contenir l'incident

1. relever l'heure présumée de la corruption ;
2. empêcher les modifications LDAP ;
3. arrêter temporairement Samba, Postfix et Dovecot si leurs écritures peuvent
   aggraver l'incident ;
4. conserver les volumes corrompus pour l'analyse ;
5. ne jamais exécuter `docker compose down -v`.

### Étape 2 - Choisir une archive saine

```bash
cd ~/on-premise/backup
set -a
source .env
set +a

borg check "$BORG_REPO"
borg list "$BORG_REPO"

ARCHIVE_NAME=embedded-infra-ubuntu-oliv-2026-08-05T12-55-10
borg list "$BORG_REPO::$ARCHIVE_NAME" | grep -E \
  'openldap-(data|config)\.ldif|openldap_ldap_(data|config)\.tar\.gz'
```

Vérifier le journal associé, son code retour et l'absence d'incident connu au
moment de la création de l'archive.

### Étape 3 - Restaurer dans un environnement isolé

1. extraire les exports LDIF et les archives des volumes dans `/tmp` ;
2. créer des volumes de test distincts des volumes de production ;
3. restaurer les données dans ces volumes ;
4. démarrer une instance OpenLDAP de test sans publier le port `389` de la
   production ;
5. ne remplacer les volumes actifs qu'après validation.

Les commandes détaillées d'extraction sont conservées dans la feuille
[Restaurer une sauvegarde BorgBackup](restaurer-sauvegarde-borg.md).

### Étape 4 - Vérifier l'annuaire restauré

```bash
ldapwhoami -x \
  -H ldap://<serveur-test>:<port-test> \
  -D "cn=admin,dc=embedded,dc=local" -W

ldapsearch -x \
  -H ldap://<serveur-test>:<port-test> \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "dc=embedded,dc=local" \
  '(uid=amartin)' dn uid cn
```

Contrôler également les unités d'organisation, les six groupes, les six
utilisateurs, les appartenances et les attributs Samba.

### Étape 5 - Remettre en service

1. effectuer une dernière sauvegarde des volumes corrompus ;
2. arrêter l'instance OpenLDAP défaillante ;
3. substituer les volumes validés ou importer le LDIF sain ;
4. démarrer OpenLDAP puis LAM ;
5. redémarrer Samba et les services de messagerie ;
6. tester LDAP, SMB, SMTP, IMAP et Roundcube ;
7. informer les utilisateurs et consigner les horaires réels.

## 4. Estimation du temps de reprise

| Opération | Durée estimée |
|---|---:|
| Détection, décision et gel des écritures | 10 min |
| Choix et contrôle de l'archive | 10 min |
| Extraction des LDIF et volumes | 15 min |
| Démarrage de l'environnement isolé | 15 min |
| Contrôles LDAP et groupes | 10 min |
| Bascule et redémarrage des dépendances | 10 min |
| Tests fonctionnels et communication | 10 min |
| **Total estimé** | **1 h 20** |

Cette estimation laisse une marge de 40 minutes par rapport à l'objectif PRA
de 2 heures. Elle doit être remplacée par une mesure réelle lors d'un exercice
complet de restauration.

## 5. Données éventuellement perdues

La sauvegarde automatique actuelle est quotidienne. Dans le pire cas, les
modifications réalisées depuis la sauvegarde de 02 h 00 sont perdues : comptes
créés, changements de groupes, mots de passe et attributs LDAP.

La fréquence nocturne limite le RPO technique à environ 24 heures. Elle répond
à l'exigence historique du PCA, mais cette perte maximale doit encore être
acceptée par le responsable métier.

## 6. Respect du PCA et du PRA

| Exigence | Évaluation | Justification |
|---|---|---|
| Priorité donnée à OpenLDAP | Conforme | LDAP est restauré avant Samba, la messagerie et LAM. |
| Reprise en moins de 2 heures | Conforme sur estimation | La procédure est estimée à 1 h 20, mais le temps réel reste à mesurer. |
| Interruption inférieure à 4 heures | Conforme sur estimation | La marge estimée est de 2 h 40 par rapport au PCA. |
| Sauvegarde quotidienne contrôlée | Conforme | Cron, journal, état `SUCCESS` et contrôle `CONFORME` ont été vérifiés. |
| Sauvegarde LDAP nocturne | Conforme à l'exigence historique | Le script exporte les LDIF et les volumes dans l'archive quotidienne. |
| Restauration fonctionnelle complète | Partiellement conforme | Les fichiers et volumes ont été extraits, mais un OpenLDAP restauré n'a pas encore été démarré et chronométré. |
| Copie chiffrée hors de l'hôte | À confirmer | Le dépôt est chiffré, mais la copie externe n'est pas prouvée. |

### Conclusion

La stratégie répond **partiellement** aux exigences. Les sauvegardes sont
automatisées, chiffrées, journalisées et extractibles. Le RTO LDAP semble
compatible avec le PCA/PRA, mais il ne sera déclaré validé qu'après un exercice
chronométré. La copie hors hôte reste à mettre en œuvre et le RPO de 24 heures
doit être validé par le responsable métier.

## 7. Actions correctives

1. faire valider le RPO LDAP de 24 heures par le responsable métier ;
2. répliquer le dépôt Borg chiffré sur un support hors hôte ;
3. démarrer une instance OpenLDAP à partir des volumes restaurés ;
4. mesurer le temps réel jusqu'au rétablissement de Samba et de la messagerie ;
5. inscrire les résultats et les écarts dans le PCA, le PRA et le journal.

## Autres scénarios possibles

| Incident | Sauvegarde principale | Objectif de reprise |
|---|---|---:|
| Suppression d'un partage Samba | Volume `samba_share` | 8 heures |
| Perte de l'hôte de messagerie | Dovecot, Roundcube, configurations et Git | 24 heures |
| Suppression d'une configuration | Git puis archive Borg | selon le service concerné |

## Livrables

- analyse du scénario de corruption LDAP ;
- liste des sauvegardes nécessaires ;
- procédure de restauration proposée ;
- estimation du temps et des pertes ;
- conclusion argumentée sur le respect du PCA et du PRA.
