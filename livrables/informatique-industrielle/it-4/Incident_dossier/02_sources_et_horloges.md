# Inventaire des sources et fiabilité

| Source | Fichier | Précision / limite |
|---|---|---|
| SUP-01 / export mesures | `temperatures_ZF02_2026-10-08.csv` | 1 mesure/minute. `temperature_c` est une mesure enregistrée, non une température produit ; pas de donnée avant 08:30 ni après 11:30 dans cet export. |
| SUP-01 / événements | `evenements_SUP01.csv` | Horodatage local CEST ; journal de supervision, non authentification humaine. |
| FrigoMaint / tickets | `maintenance_FrigoMaint.csv` | Heures saisies par personnel et système de tickets ; déclarations qui peuvent être incomplètes. |
| Passerelle VPN | `acces_distants_VPN.csv` | **Horloge en avance de 2 min 10 s** sur SUP-01 ; convertir avant corrélation. Adresse du poste cible : MAINT-01. |
| REG-02 / trafic | `modbus_REG02_capture.pcap` | **Trace synthétique partielle** de quelques échanges TCP/Modbus. Horodatages de paquets en UTC, Wireshark les affiche selon le fuseau configuré. |
| Architecture | Dossier J3/J4 | La topologie effectivement déployée peut différer de la proposition des apprenants ; ne pas présumer que toutes les protections J4 existaient au moment de l'incident. |

**Définitions :** adresse REG-02 = `10.30.10.22:502` ; MAINT-01 = `10.30.20.15` ; supervision SUP-01 = `10.30.20.10` ; client de consultation = `10.30.20.30`. Ces adresses documentent le scénario, pas le PoC localhost.

**Registre :** holding register adresse PDU `0` = consigne en dixièmes de degré Celsius (40 ↔ 4,0 °C, 120 ↔ 12,0 °C). Fonction FC03 = lecture de holding register ; FC06 = écriture d'un registre. Dans cette installation fictive, le flux de supervision de SUP-01 consulte normalement REG-02 en lecture.

**Pour Wireshark :** filtre `modbus || tcp.port == 502`. Pour retrouver une écriture, examiner les requêtes Modbus de fonction 6. L'identifiant de transaction MBAP associe chaque requête à sa réponse.
