# Cybersécurité

La cybersécurité regroupe les moyens utilisés pour protéger les systèmes, les réseaux et les données.

Elle sert à limiter les risques liés aux attaques, aux erreurs humaines, aux pannes et aux mauvaises configurations.

## Organisation de cette partie

Pour éviter une page trop longue, la cybersécurité est séparée en plusieurs thèmes :

- [Bases de la cybersécurité](securite.md) : définition, chapeaux, équipes cyber et CVE.
- [Acteurs et rôles défensifs](securite-acteurs.md) : ANSSI, CERT-FR, CNIL, RSSI, SOC et place de l'AIS.
- [Menaces et attaques](securite-menaces.md) : phishing, malware, ransomware, CHU de Rouen et WannaCry.
- [Hygiène numérique](hygiene-numerique.md) : mots de passe, MFA, sauvegardes, pare-feu, mises à jour et logs.
- [Chiffrement](chiffrement.md) : cryptographie, chiffrement symétrique, asymétrique, HTTPS et cadenas.

## Les chapeaux

- **Black hat** : personne qui attaque illégalement, souvent pour l'argent, l'espionnage ou le sabotage.
- **White hat** : personne qui teste la sécurité avec autorisation pour aider une organisation à corriger ses failles.
- **Grey hat** : personne qui cherche des failles sans autorisation claire, puis peut prévenir l'organisation concernée.

## Les équipes cyber

- **Red team** : équipe qui simule des attaques pour tester la sécurité d'une organisation.
- **Blue team** : équipe qui défend, surveille, détecte et réagit aux incidents.
- **Purple team** : collaboration entre red team et blue team pour améliorer la défense.

## CVE

Une **CVE** (*Common Vulnerabilities and Exposures*) est une référence publique qui identifie une faille de sécurité.

Elle permet de nommer clairement une vulnérabilité, de suivre les correctifs et d'évaluer sa gravité.

## Score CVSS

Les failles sont souvent accompagnées d'un score de gravité de `0` à `10`.

- `0.0` : aucun risque
- `0.1` à `3.9` : faible
- `4.0` à `6.9` : moyen
- `7.0` à `8.9` : haut
- `9.0` à `10.0` : critique

Le score prend en compte plusieurs éléments :

- la facilité d'exploitation,
- les privilèges nécessaires,
- l'interaction ou non de l'utilisateur,
- l'impact sur la confidentialité, l'intégrité et la disponibilité,
- l'existence de correctifs ou d'exploits connus.

!!! tip "À retenir"
    Une CVE permet d'identifier une faille. Le score CVSS aide à prioriser les corrections.
