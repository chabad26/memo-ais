# Réponse à incident, Spark et Fail2ban

## Démarche de réponse à incident

Logique à suivre :

```text
Identification -> Confinement -> Correction -> Durcissement -> Vérification
```

| Étape | Objectif | Exemples d'actions |
|---|---|---|
| Identification | Comprendre ce qui est exposé et ce qui s'est produit | Ports, processus, logs, charge CPU |
| Confinement | Empêcher de nouveaux accès non autorisés | Couper Spark, filtrer les ports, isoler la machine |
| Correction | Corriger la configuration dangereuse | Authentification, interfaces d'écoute, permissions |
| Durcissement | Réduire la surface d'attaque | Firewall, utilisateur dédié, SSH limité, mises à jour |
| Vérification | Prouver que le risque est réduit | Tests `curl`, `nc`, logs, scan contrôlé |

## Symptômes à investiguer

- lenteur forte ;
- charge CPU élevée ;
- services difficiles à joindre ;
- activité réseau inhabituelle ;
- interface Spark accessible depuis le réseau ;
- ports applicatifs ouverts sans justification.

## Ports Spark à connaître

| Port | Service | Risque si exposé |
|---|---|---|
| `7077` | Spark master standalone | Soumission de jobs si accès non contrôlé |
| `8080` | Web UI master | Fuite d'informations sur le cluster |
| `8081` | Web UI worker | Fuite d'informations sur les workers |
| `6066` | REST submission API | Soumission distante via API |
| `4040` | Web UI d'une application | Fuite d'informations sur un job |
| `18080` | History server | Exposition de l'historique |

Point important : même si `7077`, `8080`, `8081` et `6066` sont fermés, une interface `4040` accessible peut déjà exposer des informations utiles à une reconnaissance.

## Identifier l'exposition

Sur le serveur Spark :

```bash
ip -br addr
sudo ss -tulnp
sudo ss -tulnp | grep -E '7077|8080|8081|6066|4040|18080'
ps aux | grep -i spark
top
```

Depuis une machine de test :

```bash
nc -vz IP_PC_SPARK 8080
nc -vz IP_PC_SPARK 7077
nc -vz IP_PC_SPARK 8081
nc -vz IP_PC_SPARK 6066
nc -vz IP_PC_SPARK 4040
curl http://IP_PC_SPARK:4040
```

Capturer le trafic :

```bash
sudo tcpdump -i any host IP_LAPTOP and tcp
```

Filtres Wireshark utiles :

```text
ip.addr == IP_PC_SPARK
tcp.port == 4040
tcp.port == 7077
tcp.port == 8080
tcp.port == 6066
```

## Traces à consulter

```bash
ls -l $SPARK_HOME/logs
tail -n 100 $SPARK_HOME/logs/*
journalctl -n 100 --no-pager
journalctl -u ssh --no-pager -n 100
find /tmp /var/tmp /opt/spark -type f -mtime -1 2>/dev/null
```

À rechercher :

- processus Spark master, worker ou `spark-shell` ;
- job en cours ;
- port `4040` ouvert ;
- charge CPU/RAM anormale ;
- fichiers récents suspects ;
- connexions SSH inhabituelles.

## Confinement Spark

Arrêter Spark si nécessaire :

```bash
$SPARK_HOME/sbin/stop-worker.sh
$SPARK_HOME/sbin/stop-master.sh
```

Limiter l'exposition réseau :

```bash
sudo nft add rule inet spark_filter input tcp dport 4040 drop
```

Ou lancer Spark en écoute locale si l'interface n'a pas besoin d'être accessible à distance :

```bash
SPARK_LOCAL_IP=127.0.0.1 spark-shell
```

## Durcir Spark

Créer ou modifier :

```bash
cp $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf
nano $SPARK_HOME/conf/spark-defaults.conf
```

Exemple de paramètres :

```properties
spark.authenticate true
spark.authenticate.secretFile /etc/spark/spark.secret
spark.network.crypto.enabled true
spark.network.crypto.authEngineVersion 2
spark.io.encryption.enabled true
spark.acls.enable true
spark.admin.acls sparkadmin
spark.ui.view.acls sparkadmin
spark.modify.acls sparkadmin
spark.master.rest.enabled false
```

Créer le secret :

```bash
sudo mkdir -p /etc/spark
sudo openssl rand -base64 48 | sudo tee /etc/spark/spark.secret >/dev/null
sudo chmod 600 /etc/spark/spark.secret
```

Créer un utilisateur dédié :

```bash
sudo useradd --system --home /opt/spark --shell /usr/sbin/nologin spark
sudo chown -R spark:spark /opt/spark-* /opt/spark
sudo chown -R spark:spark /etc/spark
```

Note : les ACLs Spark ne remplacent pas le filtrage réseau. Elles doivent être combinées à une authentification et à un firewall.

## Filtrer les ports Spark avec nftables

Exemple : autoriser seulement `IP_LAPTOP` vers les ports Spark.

```nft
table inet spark_filter {
    chain input {
        type filter hook input priority 0; policy accept;

        ct state established,related accept
        iif "lo" accept

        tcp dport { 7077, 8080, 8081, 6066, 4040, 18080 } ip saddr IP_LAPTOP accept
        tcp dport { 7077, 8080, 8081, 6066, 4040, 18080 } drop
    }
}
```

Charger et vérifier :

```bash
sudo nft -f /etc/nftables.d/spark.nft
sudo nft list ruleset
```

## Vérifier la remédiation

Depuis une machine non autorisée :

```bash
curl http://IP_PC_SPARK:8080
nc -vz IP_PC_SPARK 7077
nc -vz IP_PC_SPARK 6066
nc -vz IP_PC_SPARK 4040
```

Résultat attendu :

```text
Connexion refusée ou timeout
```

Depuis une machine autorisée, seuls les ports explicitement nécessaires doivent répondre.

## Fail2ban SSH

Installer et activer :

```bash
sudo apt update
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
sudo systemctl status fail2ban
```

Créer `/etc/fail2ban/jail.local` :

```ini
[DEFAULT]
bantime = 10m
findtime = 5m
maxretry = 3
ignoreip = 127.0.0.1/8 ::1

[sshd]
enabled = true
port = ssh
backend = systemd
mode = aggressive
maxretry = 3
```

Valider et redémarrer :

```bash
sudo fail2ban-client -t
sudo systemctl restart fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

Tester depuis une machine de lab avec plusieurs mauvais mots de passe :

```bash
ssh user@IP_VICTIME
```

Vérifier le bannissement :

```bash
sudo fail2ban-client status sshd
sudo journalctl -u fail2ban --no-pager -n 50
sudo journalctl -u ssh --no-pager -n 50
```

Débannir si besoin :

```bash
sudo fail2ban-client set sshd unbanip IP_DU_LAPTOP
```

## Bannissement manuel avec nftables

Principe du script :

```text
IP fournie -> validation -> création table/chain/set -> ajout avec timeout -> log horodaté
```

Commandes utiles à retenir :

```bash
sudo nft add table inet lab_filter
sudo nft add chain inet lab_filter input '{ type filter hook input priority 0; policy accept; }'
sudo nft add set inet lab_filter banned_ips '{ type ipv4_addr; flags timeout; }'
sudo nft add element inet lab_filter banned_ips "{ IP_A_BANNIR timeout 10m }"
sudo nft add rule inet lab_filter input ip saddr @banned_ips drop
sudo nft list ruleset
```

Après `10m`, l'élément ajouté avec timeout disparaît automatiquement du set.

## UFW en complément

Politique simple :

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 4040/tcp
sudo ufw allow 18080/tcp
sudo ufw enable
sudo ufw status verbose
```

Attention : autoriser `4040` ou `18080` doit être justifié. Ces ports sont à limiter par IP source ou à fermer lorsqu'ils ne sont pas nécessaires.

## Apache2 avec Fail2ban

Fail2ban peut aussi protéger une zone Apache avec authentification.

Jail type :

```ini
[apache-auth]
enabled = true
port = http,https
logpath = /var/log/apache2/error.log
backend = auto
maxretry = 3
findtime = 5m
bantime = 10m
```

## Fail2ban vs script manuel

| Élément | Fail2ban | Script manuel |
|---|---|---|
| Déclenchement | Automatique après échecs | Manuel |
| Source de décision | Logs du service | IP fournie par l'administrateur |
| Durée | `bantime` | Timeout défini dans le script |
| Intérêt | Protection continue | Réaction rapide pendant un incident |
| Limite | Dépend des logs | Risque d'erreur de saisie |

## À documenter dans un rapport

- symptôme initial ;
- IP de la victime et IP du poste de test ;
- ports exposés avant correction ;
- processus et logs observés ;
- risque confirmé et risque non confirmé ;
- action de confinement ;
- règles firewall ou Fail2ban appliquées ;
- preuve de vérification après correction ;
- limites restantes.
