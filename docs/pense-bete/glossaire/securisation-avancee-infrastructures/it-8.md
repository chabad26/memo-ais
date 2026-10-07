# Itération 8 — Suricata sur l’hôte

Route par virbr0 et quatre alertes sur le serveur temporaire/18080 documentées ;
les autres trajets et File Browser/8080 restent à vérifier.

| Terme / contrôle | À retenir |
| --- | --- |
| IDS réseau | Alerte sur le trafic visible ; ne prouve pas une compromission et ne remplace pas le filtrage |
| Point d’observation | Emplacement de capture ; visibilité limitée aux flux qui y passent |
| Interface de capture | Prouver le trajet VM/hôte avant d’interpréter l’absence d’alerte |
| SID / rev | Identifier chaque signature et sa version ; dix signatures maximum |
| HTTP brut / normalisé | Lire le buffer réellement inspecté ; le chiffrement masque les motifs HTTP |
| `suricata -T -c ...` | Valider configuration et bilan de chargement avant redémarrage |
| EVE | Corréler timestamp, IP/ports, signature et flow_id aux tests |

- [Contexte de la journée](../../../securisation-avancee-infrastructures/it-8/index.md)
- [Identifier le point d’observation](../../../securisation-avancee-infrastructures/it-8/identifier-point-observation.md)
- [Installer et tester les règles](../../../securisation-avancee-infrastructures/it-8/installer-tester-regles-suricata.md)

- [Comprendre les événements produits](../../../securisation-avancee-infrastructures/it-8/comprendre-evenements-produits.md) : lecture EVE, activité normale, flow_id et distinction événement/alerte.

- [Observer l’activité autour de File Browser](../../../securisation-avancee-infrastructures/it-8/observer-activite-file-browser.md) : essais contrôlés, corrélation et limites des déductions.

- [Bilan du dispositif de détection](../../../securisation-avancee-infrastructures/it-8/bilan-dispositif-detection.md) : capacités prouvées, bruit, angles morts et réglage à préparer.
