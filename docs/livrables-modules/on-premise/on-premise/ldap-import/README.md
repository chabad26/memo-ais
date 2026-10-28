# Imports CSV LDAP pour LAM


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/ldap-import/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Ces fichiers sont destinés à l'import **Tools > File upload** de LDAP
Account Manager. LAM vérifie d'abord le fichier et propose de visualiser le
LDIF avant de créer les entrées. Ne valide l'import qu'après avoir contrôlé
le résultat.

## Ordre d'import

1. Créer ou vérifier `ou=People` et `ou=Groups`.
2. Importer les groupes avec `lam-groups.csv`.
3. Importer les utilisateurs avec `lam-users.csv`.
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
5. Vérifier les groupes et les utilisateurs avec `ldapsearch`.

## Utilisateurs

Dans LAM, sélectionner **Utilisateurs**, puis activer les modules **Personal**
et **Unix**. Le fichier `lam-users.csv` utilise les colonnes nommées par LAM :

- `inetOrgPerson_firstName` ;
- `inetOrgPerson_lastName` ;
- `inetOrgPerson_email` ;
- `posixAccount_userName` ;
- `posixAccount_uid` ;
- `posixAccount_group` ;
- `posixAccount_additionalGroups` ;
- `posixAccount_homedir` ;
- `posixAccount_shell`.

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
passe temporaire dans LAM après l'import, puis le remplacer selon la procédure
du TP.

## Groupes

`lam-groups.csv` suit le modèle affiché par LAM avec les colonnes `dn_suffix`,
`dn_rdn`, `overwrite`, `posixGroup_description`, `posixGroup_cn`,
`posixGroup_gid` et `posixGroup_members`. La valeur `dn_rdn` est `cn` : elle
indique l'attribut utilisé pour construire le DN. Le nom réel du groupe est
fourni par `posixGroup_cn`.

Dans le schéma utilisé pendant le TP, `posixGroup` est auxiliaire et
`groupOfNames` est la classe structurelle. Si l'import affiche
`no structural object class provided`, ne relance pas l'import en boucle :

1. active le profil de groupe combinant `groupOfNames` et `posixGroup` si ce
   profil est disponible ;
2. sinon crée d'abord les groupes `groupOfNames` dans le Navigateur LDAP ;
3. ajoute ensuite `posixGroup` et `gidNumber` aux groupes ;
4. importe les utilisateurs avec `lam-users.csv`.

LAM recommande de télécharger son modèle CSV depuis la page d'import, car les
colonnes dépendent des modules activés. Ces fichiers correspondent au profil
utilisé dans ce TP ; le modèle affiché par LAM reste la référence si le profil
est modifié.

## Attention aux doublons

Les utilisateurs et groupes déjà présents dans l'annuaire provoqueront des
erreurs de doublon. Ces fichiers sont destinés à un annuaire vide ou à un
import après nettoyage contrôlé.

## Vérification

~~~bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "dc=embedded,dc=local" \
  "(|(objectClass=posixAccount)(objectClass=posixGroup))" \
  uid cn gidNumber memberUid
~~~
