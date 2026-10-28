# Validation de la stratégie de sauvegarde


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/backup-strategy-validation.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Scénario

Corruption de la base OpenLDAP avec indisponibilité de l'authentification
centralisée et impact sur Samba et la messagerie.

| Élément | Résultat de l'analyse |
|---|---|
| Archive de référence | `embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` |
| Sauvegardes | LDIF OpenLDAP, volumes `ldap_data` et `ldap_config`, Compose et paramètres protégés |
| Objectif PRA | Authentification rétablie en 2 heures |
| Objectif PCA | Interruption maximale de 4 heures |
| Temps estimé | 1 h 20 |
| Perte maximale actuelle | Jusqu'à 24 heures de modifications LDAP |
| Conclusion | RTO compatible sur estimation ; stratégie globalement partielle |

## Procédure proposée

1. dater l'incident et geler les écritures LDAP ;
2. conserver les volumes corrompus ;
3. sélectionner la dernière archive saine antérieure à la corruption ;
4. vérifier le dépôt, le journal et le contenu de l'archive ;
5. extraire les LDIF et les volumes dans un emplacement temporaire ;
6. restaurer dans des volumes Docker isolés ;
7. démarrer un OpenLDAP de test sans remplacer la production ;
8. vérifier l'administrateur, la base, les unités, groupes et utilisateurs ;
9. basculer vers les données validées ;
10. redémarrer LAM, Samba et la messagerie puis réaliser les tests fonctionnels.

Les commandes d'extraction et de contrôle sont détaillées dans
`documentation/restore-procedure.md`.

## Évaluation PCA/PRA

Le temps estimé de 1 h 20 est inférieur aux objectifs de 2 heures du PRA et de
4 heures du PCA. Ce résultat reste une estimation tant que le service restauré
n'a pas été démarré et chronométré de bout en bout.

La sauvegarde complète est prévue une fois par jour. La perte maximale est donc
proche de 24 heures, conformément à la sauvegarde nocturne issue du PCA. Cette
valeur doit néanmoins être acceptée comme RPO par le responsable métier. La
copie chiffrée hors de l'hôte principal doit également être prouvée.

## Conclusion

La stratégie est partiellement validée : automatisation, chiffrement,
journalisation, contrôle et extraction sont opérationnels. Pour la déclarer
conforme, il reste à observer une exécution planifiée sur un hôte disponible,
effectuer une copie hors hôte et mesurer un exercice complet de restauration
LDAP.
