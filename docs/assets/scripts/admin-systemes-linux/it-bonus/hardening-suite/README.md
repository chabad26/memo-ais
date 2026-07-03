# AlpesNet Hardening Suite

Suite Bash modulaire pour durcir une Debian 12 fraichement installee.

## Usage

Adapter d'abord `config/alpesnet.conf`, surtout `SSH_ALLOW_USERS` et les regles `UFW_RULES`, puis lancer :

```bash
sudo ./main.sh --menu
sudo ./main.sh --all
sudo ./main.sh --modules 03,04,08
sudo ./main.sh --audit-only
sudo ./main.sh --all --dry-run
```

Le mode `--menu` affiche la liste des modules et accepte `all`, `audit`, `dry-run`, `1 2 3`, `01,02,03` ou `q`.

Le log principal est genere dans `/var/log/alpesnet/hardening-[date].log`. Les rapports d'audit sont generes dans `rapports/audit-[hostname]-[date].txt`.

## Configuration

Toutes les valeurs metier sont dans `config/alpesnet.conf` : comptes, groupes, sudo restreint, parametres SSH, regles UFW, Fail2ban, services autorises, chemins de logs et sauvegardes.

## Rapports

Le module `08-audit` produit un rapport lisible sans commande supplementaire. Chaque controle apparait en `PASS`, `FAIL` ou `WARN`, avec les sections comptes, SSH, pare-feu, services, logs, sauvegarde, execution et score.

## Ajouter un module

Creer `modules/09-nom.sh`, definir une fonction `run_module`, ajouter le fichier dans `MODULE_FILES`, son ordre dans `MODULE_ORDER` et ses prerequis dans `DEPENDANCES` dans `main.sh`.
