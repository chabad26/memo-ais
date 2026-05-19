# Pense-bête Cybersécurité

## Réflexes de base

- Éviter d'utiliser `root` directement.
- Utiliser `sudo` seulement quand c'est nécessaire.
- Garder le système à jour.
- Ne pas ouvrir de ports inutiles.
- Utiliser des mots de passe solides.
- Activer la MFA quand c'est possible.
- Privilégier SSH avec des clés quand c'est possible.
- Lire les logs en cas de comportement anormal.
- Documenter les changements importants.

## Points à surveiller

| Point | Pourquoi c'est important |
| --- | --- |
| Comptes utilisateurs | Limiter les droits réduit l'impact d'une compromission. |
| Comptes administrateurs | Ils doivent être protégés et utilisés seulement pour l'administration. |
| Mises à jour | Elles corrigent des failles connues. |
| Sauvegardes | Elles permettent de restaurer après panne ou rançongiciel. |
| Logs | Ils aident à comprendre ce qui s'est passé. |
| Ports ouverts | Chaque service exposé augmente la surface d'attaque. |

## Phrase à retenir

La sécurité repose souvent sur des gestes simples, mais réguliers :

- limiter,
- vérifier,
- surveiller,
- sauvegarder,
- corriger.
