# Préparation d'un CTF facile

## Objectif

Cette feuille sert à préparer un mini-CTF simple sur l'infrastructure de l'atelier.

Le but est de proposer un parcours accessible à un autre apprenant, avec :

- un accès SSH initial ;
- un indice local ;
- un mot de passe faible ;
- un premier flag ;
- une recherche avec `find` ;
- un service FTP en configuration volontairement faible ;
- un flag final à décoder.

## Scénario proposé

Chaîne prévue :

```text
PC autre apprenant
        |
        | SSH vers R2:2222
        v
RH1 avec utilisateur visiteur
        |
        | indice rockyou
        v
utilisateur admin
        |
        | premier flag + indice
        v
scan réseau / recherche
        |
        | FTP anonymous
        v
flag final chiffré en ROT13
```

## Périmètre

| Élément | Rôle |
| --- | --- |
| `R2` | Publication SSH vers RH1 avec NAT |
| `RH1` | Machine d'entrée du CTF |
| `visiteur` | Compte initial facile |
| `admin` | Compte à découvrir avec l'indice `rockyou#26` |
| Machine FTP | Machine dans un autre VLAN ou autre segment |
| FTP anonymous | Service volontairement mal configuré pour le CTF |

## 1. Préparer l'accès initial vers RH1

Le joueur doit pouvoir se connecter depuis son PC vers `RH1` via `R2`.

Accès donné :

```text
ssh visiteur@192.168.122.218 -p 2222
mot de passe : visiteur
```

La redirection attendue est :

```text
PC joueur -> R2:2222 -> RH1:22
```

Sur `R2`, vérifier que la publication fonctionne :

```bash
sudo nft list ruleset
sudo tcpdump -ni ens4 tcp port 2222
```

Depuis un PC externe :

```bash
ssh visiteur@192.168.122.218 -p 2222
```

## 2. Créer le compte initial `visiteur` sur RH1

Sur `RH1` :

```bash
sudo adduser visiteur
```

Mot de passe conseillé pour le CTF facile :

```text
visiteur
```

Vérifier :

```bash
id visiteur
getent passwd visiteur
```

## 3. Ajouter le premier indice

Dans le home de `visiteur`, créer un pense-bête :

```bash
echo "admin" | sudo tee /home/visiteur/pensebete.txt
echo "rockyou#26" | sudo tee -a /home/visiteur/pensebete.txt
sudo chown root:root /home/visiteur/pensebete.txt
sudo chmod 644 /home/visiteur/pensebete.txt
```

Ce fichier donne deux informations :

```text
admin
rockyou#26
```

Interprétation attendue côté joueur :

```text
Utilisateur cible : admin
Mot de passe : ligne 26 de la wordlist rockyou
```

## 4. Créer le compte `admin`

Récupérer le mot de passe ligne 26 de `rockyou`.

Sur une machine Kali ou une machine qui possède la wordlist :

```bash
zcat /usr/share/wordlists/rockyou.txt.gz | sed -n '26p'
```

Si la wordlist est déjà décompressée :

```bash
sed -n '26p' /usr/share/wordlists/rockyou.txt
```

Sur `RH1`, créer l'utilisateur :

```bash
sudo adduser admin
```

Utiliser comme mot de passe la valeur trouvée à la ligne 26 de `rockyou`.

Vérifier :

```bash
id admin
getent passwd admin
```

## 5. Ajouter le premier flag

Sur `RH1` :

```bash
sudo tee /home/admin/flag.txt >/dev/null <<'EOF'
FLAG{premier_pas}
Bravo, tu as trouvé le premier flag.

Un deuxième flag existe dans un autre VLAN de ce réseau.
Mais comment y accéder...

Indice : si tu galères à trouver, utilise find.
EOF
```

Permissions :

```bash
sudo chown admin:admin /home/admin/flag.txt
sudo chmod 644 /home/admin/flag.txt
```

Vérification :

```bash
sudo -u admin cat /home/admin/flag.txt
```

## 6. Ajouter un indice vers la suite

Pour guider vers un autre service, ajouter un fichier accessible à `admin`.

Exemple :

```bash
sudo mkdir -p /home/admin/reseau
sudo tee /home/admin/reseau/indice-suite.txt >/dev/null <<'EOF'
Le second flag n'est pas sur cette machine.
Cherche les services accessibles sur les autres réseaux.
Indice : certains services gardent leurs identifiants par défaut.
EOF
sudo chown -R admin:admin /home/admin/reseau
sudo chmod 755 /home/admin/reseau
sudo chmod 644 /home/admin/reseau/indice-suite.txt
```

Le joueur devrait le trouver avec :

```bash
find /home -type f 2>/dev/null
find / -iname '*indice*' 2>/dev/null
```

## 7. Préparer le service FTP anonymous

Sur la machine qui portera le second flag, installer `vsftpd` :

```bash
sudo apt update
sudo apt install vsftpd
```

Créer le dossier FTP :

```bash
sudo mkdir -p /srv/ftp
```

Créer un flag final chiffré en ROT13.

Exemple de flag clair :

```text
FLAG{flag_final}
```

Le chiffrer :

```bash
echo 'FLAG{flag_final}' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Exemple de résultat :

```text
SYNT{synt_svany}
```

Créer le fichier FTP :

```bash
echo "SYNT{synt_svany}" | sudo tee /srv/ftp/flagfinal.txt
sudo chmod 644 /srv/ftp/flagfinal.txt
```

## 8. Configurer FTP anonymous

Éditer la configuration :

```bash
sudo nano /etc/vsftpd.conf
```

Paramètres attendus pour le CTF :

```text
anonymous_enable=YES
anon_root=/srv/ftp
no_anon_password=YES
local_enable=NO
write_enable=NO
```

Redémarrer :

```bash
sudo systemctl restart vsftpd
sudo systemctl status vsftpd --no-pager
```

Vérifier l'écoute :

```bash
sudo ss -tulnp | grep ':21'
```

## 9. Vérifier depuis une autre machine

Depuis une machine de test :

```bash
nmap -sV -p 21 <IP_MACHINE_FTP>
```

Connexion FTP :

```bash
ftp <IP_MACHINE_FTP>
```

Identifiants :

```text
anonymous
anonymous
```

Commandes FTP :

```text
pwd
ls
ls -la
get flagfinal.txt
bye
```

Lire le fichier :

```bash
cat flagfinal.txt
```

Décoder ROT13 :

```bash
cat flagfinal.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Résultat attendu :

```text
FLAG{flag_final}
```

## 10. Message à donner aux joueurs

Exemple de message :

```text
CTF facile disponible.

Connexion :
ssh visiteur@192.168.122.218 -p 2222

Mot de passe :
visiteur

Objectif :
Trouver 2 flags.

Thèmes :
- mot de passe faible ;
- wordlist rockyou ;
- recherche de fichiers avec find ;
- configuration FTP par défaut ;
- petit chiffrement classique.

Indices :
- rockyou#26 signifie ligne 26 de rockyou.
- En FTP, tester anonymous / anonymous.
- Si tu ne trouves pas, utilise find.
- Si le flag final ne commence pas par FLAG, pense à ROT13.

Périmètre :
Rester dans les machines et réseaux accessibles depuis l'environnement du CTF.
```

## 11. Solution attendue

Commandes attendues côté joueur :

```bash
ssh visiteur@192.168.122.218 -p 2222
cat pensebete.txt
zcat /usr/share/wordlists/rockyou.txt.gz | sed -n '26p'
ssh admin@<IP_RH1>
cat flag.txt
find /home -type f 2>/dev/null
nmap -sV -p 21,22,80,443,445,8080 <RESEAU_AUTORISE>
ftp <IP_MACHINE_FTP>
```

Dans FTP :

```text
anonymous
anonymous
ls -la
get flagfinal.txt
bye
```

Décodage :

```bash
cat flagfinal.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Flags attendus :

```text
FLAG{premier_pas}
FLAG{flag_final}
```

## 12. Points de sécurité

- Utiliser des comptes dédiés au CTF.
- Ne pas donner de droits `sudo` aux comptes joueurs.
- Ne publier qu'un port précis vers la machine d'entrée.
- Désactiver ou supprimer les comptes après l'exercice.
- Ne pas placer de vrai secret dans les fichiers d'indice.
- Limiter les règles pfSense au strict nécessaire.
- Surveiller les logs pendant le test.

Commandes de nettoyage possibles :

```bash
sudo deluser --remove-home visiteur
sudo deluser --remove-home admin
sudo systemctl stop vsftpd
sudo systemctl disable vsftpd
```

## Conclusion

Ce CTF facile reprend des notions simples et pédagogiques :

- lire un indice ;
- utiliser une wordlist ;
- se connecter à un compte avec mot de passe faible ;
- chercher des fichiers ;
- identifier un service exposé ;
- exploiter une configuration par défaut ;
- décoder un flag.

Le scénario reste volontairement guidé afin de servir de test d'infrastructure et d'exercice d'initiation.
