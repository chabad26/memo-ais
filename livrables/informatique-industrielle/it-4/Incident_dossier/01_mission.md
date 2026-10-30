# Montval — Fiche de mission J5

**Date des événements :** jeudi 8 octobre 2026. **Zone :** ZF-02 « produits laitiers » ; régulateur REG-02.

À 10 h 04, le responsable d'exploitation demande à l'équipe IT de contribuer à l'investigation d'une alarme de température élevée. Une consigne inhabituelle a été observée. Le responsable du magasin n'a connaissance d'aucune demande de dérogation applicable à ZF-02.

REG-02 utilise Modbus TCP et ne bénéficie plus de support constructeur ni de correctifs de sécurité. Il doit rester en service faute de budget de remplacement. Le prestataire FrigoMaint assure certaines interventions, dont l'accès à distance. Les informations de contrôle, de maintenance et de supervision proviennent de sources distinctes.

Votre mission est de :
1. Reconstituer les événements et séparer faits établis, hypothèses et inconnues.
2. Identifier les conséquences possibles sur les fonctions OT et la continuité d'exploitation.
3. Proposer une réponse conservatoire coordonnée avec l'exploitation et FrigoMaint.
4. Comparer la situation aux protections proposées en J4 ; tester sur le PoC simplifié les corrections techniquement possibles.

**Attention :** ces documents sont fictifs. Le laboratoire PoC n'est pas relié à un équipement réel et utilise une temporisation d'alarme accélérée. Ne transposez pas ses durées aux données ci-dessous.

**Exigences pertinentes du manuel :** EXP-01, EXP-02, EXP-04 à EXP-12, MAI-01 à MAI-08.

**Périmètre des preuves initiales :** températures par minute, journal de SUP-01, maintenance/accès, et communications Modbus échantillonnées sur le segment de REG-02. La capture PCAP ne garantit pas l'exhaustivité du trafic du site.
