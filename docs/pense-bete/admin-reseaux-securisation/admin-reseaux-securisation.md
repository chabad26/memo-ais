# Pense-bête Administration des réseaux - sécurisation

Cette section regroupe les rappels rapides du module **Administration des réseaux - sécurisation**.

Objectif : retrouver vite les réflexes de supervision, de corrélation et de réponse à incident sans relire tous les ateliers.

| Fiche | Contenu |
|---|---|
| [Zeek, scans et corrélation](zeek-correlation.md) | Placement du capteur, logs Zeek, scans Nmap, SYN flood et comparaison Zeek/Wireshark/pfSense |
| [Réponse à incident, Spark et Fail2ban](incident-spark-fail2ban.md) | Analyse d'exposition Spark, remédiation, durcissement, Fail2ban SSH et bannissement IP |

## À retenir

- Zeek observe et journalise, mais ne bloque pas.
- Wireshark détaille les paquets, pfSense montre les décisions firewall.
- Une absence d'alerte dans `notice.log` ne veut pas dire absence d'activité suspecte.
- Une réponse à incident suit une logique : identifier, confiner, corriger, durcir, vérifier.
- Fail2ban protège automatiquement à partir des logs, mais ne remplace pas une configuration SSH solide.
