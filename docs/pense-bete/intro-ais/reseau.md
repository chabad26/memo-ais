# Pense-bête Réseau

## Rappels rapides

- Une **adresse IP** identifie une machine sur un réseau.
- Le **masque** indique la partie réseau et la partie machine.
- La **passerelle** permet de sortir du réseau local.
- Le **DNS** traduit un nom de domaine en adresse IP.
- Le **DHCP** distribue automatiquement les paramètres réseau.
- Un **port** identifie un service sur une machine.
- Un **pare-feu** filtre les communications autorisées ou bloquées.

## Vérifier le réseau

```bash
ip a
ip route
ping 8.8.8.8
ping google.com
ss -tulpn
```

- `ip a` affiche les adresses IP.
- `ip route` affiche la passerelle et les routes.
- `ping 8.8.8.8` teste la connectivité Internet.
- `ping google.com` teste aussi la résolution DNS.
- `ss -tulpn` affiche les ports en écoute.

!!! tip "Diagnostic réseau rapide"
    Si `ping 8.8.8.8` fonctionne mais pas `ping google.com`, le problème vient probablement du DNS.

## Ordre simple de diagnostic

1. Vérifier l'adresse IP.
2. Vérifier la passerelle.
3. Tester une IP externe.
4. Tester un nom de domaine.
5. Vérifier les ports et services.
6. Vérifier le pare-feu si besoin.
