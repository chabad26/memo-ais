# Chiffrement

Le chiffrement consiste à transformer une information lisible en information illisible sans la bonne clé.

Il sert à protéger les données, par exemple pendant leur stockage ou pendant leur transmission sur un réseau.

Il existe deux grandes familles de chiffrement :

- le chiffrement **symétrique**, où la même clé sert à chiffrer et déchiffrer. Il est rapide et adapté aux gros volumes de données. Exemple : **AES**, utilisé pour protéger des fichiers, des connexions Wi-Fi ou des VPN.
- le chiffrement **asymétrique**, où deux clés différentes sont utilisées : une clé publique et une clé privée. Il est utile pour sécuriser les échanges sur Internet. Exemples : **RSA** et **ECC**.

![Types de chiffrement](../assets/img/intro-ais/type_chiffrement.png)

## Cryptographie

La cryptographie est l'ensemble des techniques qui permettent de protéger une information.

Elle sert notamment à assurer :

- la confidentialité,
- l'intégrité des données,
- l'authentification.

Le chiffrement fait partie de la cryptographie.

## Autres notions liées

- **FPE** : chiffrement avec préservation du format. Les données restent dans le même format, par exemple un numéro de téléphone garde la forme d'un numéro de téléphone.
- **Hachage** : ce n'est pas vraiment du chiffrement, car on ne peut pas revenir au texte d'origine. Il sert surtout à vérifier l'intégrité d'une donnée ou à stocker des mots de passe de manière plus sûre.

## HTTPS

HTTPS est la version sécurisée de HTTP.

Il chiffre les échanges entre le navigateur et le site web, ce qui limite les risques d'interception ou de modification des données pendant le trajet.

## Le cadenas dans le navigateur

Le cadenas affiché dans le navigateur indique que la connexion avec le site utilise HTTPS.

Il ne veut pas dire que le site est forcément fiable, mais il montre que la communication est chiffrée et que le navigateur a pu vérifier le certificat du site.
