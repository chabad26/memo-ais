# Samba autonome avec OpenLDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/samba-ad/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Le rôle détaillé du `Dockerfile`, des configurations et de `entrypoint.sh` est
décrit dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

Cette configuration remplace le contrôleur Samba AD de la première tentative
par un serveur Samba classique utilisant OpenLDAP comme backend `ldapsam`.

## Démarrage

OpenLDAP doit être démarré en premier :

```bash
cd ~/on-premise/openldap
docker compose up -d

cd ~/on-premise/samba-ad
docker compose up -d --build
```

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
doit pas être ajouté à Git.

## Vérifications

```bash
docker compose ps
docker compose exec samba testparm -s
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
docker compose exec samba pdbedit -L -b ldapsam:ldap://openldap:3890
docker compose exec samba smbclient -L //localhost -U amartin
docker compose exec samba smbclient //localhost/partage -U amartin -c 'ls'
```

Les ports SMB publiés sont `139` et `445`. OpenLDAP est joint sur le réseau
Docker `openldap_default` et reste publié sur le port hôte `389`.

## Persistance

- `samba_config` conserve les configurations de Samba, NSS et NSLCD ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- `samba_share` conserve les fichiers du partage ;
- les données et la configuration OpenLDAP restent dans ses trois volumes ;
- `compose.ad.yaml` conserve l'ancienne configuration Samba AD à titre
  historique, mais elle ne doit pas être démarrée avec cette configuration.

Ne pas utiliser `docker compose down -v` pendant les vérifications de
persistance.

## Gestion de la configuration

Les fichiers de référence sont intégrés à l'image depuis `config/`. Au premier
démarrage, l'entrypoint les copie dans le volume `samba_config`, puis copie les
versions persistantes vers `/etc`. Il ne construit plus les fichiers ligne par
ligne.

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
du conteneur.

Après une modification volontaire de `config/smb.conf`, synchroniser le modèle
dans le volume avant de redémarrer :

```bash
docker compose build samba
docker compose run --rm --entrypoint sh samba -c \
  'install -m 0644 /usr/local/share/samba-config/smb.conf /var/lib/samba-config/smb.conf'
docker compose up -d
docker compose exec samba testparm -s
```

Cette copie explicite évite d'écraser automatiquement une configuration
persistante qui aurait été adaptée et non encore reportée dans Git.

Au démarrage, l'entrypoint vérifie aussi la liaison avec le compte administrateur
LDAP avant de lancer Samba. En cas de refus, il affiche un message demandant de
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
