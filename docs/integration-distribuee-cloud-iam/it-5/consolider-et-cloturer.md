# Consolider et clôturer

!!! info "Itération 5 - Synthèse finale"
    Cette feuille met à jour la matrice de décision du Kit 1 avec les
    observations réellement faites pendant le module. Elle ajoute le serveur
    **bare metal OVHcloud** comme option d'architecture, en distinguant ce qui
    a été déployé de ce qui a seulement été étudié.

## Objectif

Consolider les résultats du module, comparer les solutions sur des éléments
observés et formuler une recommandation adaptée à un contexte métier.

La comparaison porte sur :

- **OVHcloud Public Cloud**, réellement déployé et automatisé ;
- **Infomaniak Public Cloud**, réellement déployé et restauré ;
- **bare metal OVHcloud**, étudié comme cible dédiée mais non déployé dans ce
  module ;
- **AWS**, conservé comme référence de la matrice initiale et cas de
  comparaison pour la recommandation métier.

## Bilan des preuves disponibles

| Solution | Ce qui a été réellement constaté | Limite à signaler |
| --- | --- | --- |
| OVHcloud Public Cloud | VM, OpenTofu, Ansible, réseau privé, services distribués, stockage objet et nettoyage de fin d'exercice. | Les ressources ont été détruites ; les montants restent des estimations de laboratoire, pas une facture complète. |
| Infomaniak Public Cloud | Trois VM, OpenTofu, Ansible, services Docker, accès web et restauration après perte avec un RTO de 31 minutes. | Les VM ont utilisé une interface publique ; le RPO n'est pas calculable faute d'horodatage de sauvegarde. |
| Bare metal OVHcloud | Procédure d'installation, durcissement, Ansible, sauvegarde et réinstallation définie. | Aucun serveur dédié n'a été commandé ni testé ; il n'y a donc pas de coût ou de SLA observé. |
| AWS | Référence documentaire et estimation initiale. | Aucun déploiement AWS réalisé dans le module ; les constats sont théoriques. |

## Matrice de décision mise à jour

Les colonnes cloud reprennent les résultats du module. La colonne bare metal
concerne une offre serveur dédié OVHcloud et non un troisième fournisseur. Les
mentions « non observé » sont volontaires : elles indiquent une preuve à
produire lors d'un futur déploiement.

| Critère | OVH Public Cloud (constat) | Infomaniak Public Cloud (constat) | Bare metal OVHcloud (constat) | Écart avec la matrice initiale |
| --- | --- | --- | --- | --- |
| Facilité de prise en main | Bonne après préparation des variables OpenStack ; le Manager, OpenTofu et Ansible ont été utilisés. | Bonne pour un environnement OpenStack ; `clouds.yaml` et les règles Security Group demandent une adaptation. | Plus complexe au départ : commande, installation, partitionnement, SSH et réseau sont gérés depuis le Manager. | La matrice sous-estimait l'écart entre un cloud OpenStack et une installation physique. |
| Coût réel observé | Coût estimé sur les VM `d2-4`/`d2-2` ; ressources supprimées après validation pour éviter la facturation. | Coût non chiffré par facture dans les preuves disponibles ; ressources supprimées après validation. | Aucun coût observé : serveur non commandé. Le coût doit intégrer engagement, installation et stockage/sauvegarde. | L'estimation initiale devient un ordre de grandeur, pas un coût réellement facturé. |
| Portabilité du code OpenTofu | Bonne pour les objets OpenStack, mais variables, images, flavors et réseaux restent spécifiques. | Bonne : même provider OpenStack et mêmes playbooks Ansible, avec adaptation des paramètres. | Faible pour le provisionnement matériel : l'installation passe par le Manager ; bonne portabilité après installation avec Ansible. | La portabilité est forte pour la configuration, mais partielle pour le provisionnement. |
| Souveraineté / juridiction | Fournisseur européen et région GRA9 retenue ; choix cohérent pour le prototype, à compléter par l'analyse contractuelle. | Fournisseur suisse et région européenne utilisée ; la localisation et les sous-traitants doivent rester documentés. | Hébergement physique OVHcloud en région choisie ; contrôle matériel accru, sans supprimer les responsabilités contractuelles. | Le bare metal ajoute le contrôle physique, mais ne remplace pas l'analyse juridique du fournisseur. |
| Qualité du support / SLA | Exploitation validée, mais aucun ticket support observé ; SLA à vérifier selon l'offre. | Exploitation et restauration validées ; aucun ticket support observé ; SLA exact non mesuré. | Support matériel et délai de remplacement deviennent déterminants ; non observés dans le module. | La matrice initiale notait le SLA sur la documentation, pas sur une expérience d'incident support. |
| Reprise après incident | Recréation automatisable avec OpenTofu/Ansible ; modèle adapté aux VM éphémères. | Restauration testée : RTO constaté de 31 minutes ; RPO non calculable. | Réinstallation plus longue et dépendante du matériel ; prévoir sauvegardes hors serveur et procédure de remplacement. | Le test de restauration apporte un constat concret absent de la matrice initiale. |
| **Adéquation au besoin DIST01b** | **Favorable** pour un prototype reproductible et une architecture multi-VM. | **Favorable avec réserves** sur le réseau privé et le contrôle des flux inter-VM. | **À étudier** pour une charge stable ou exigeante, mais surdimensionné pour le prototype actuel. | La décision passe d'une comparaison théorique à une recommandation fondée sur les validations réalisées. |

## Lecture de la matrice

### OVHcloud Public Cloud

OVHcloud reste le meilleur choix pour le prototype DIST01b : le socle a été
provisionné, automatisé, réparti sur plusieurs VM, connecté par réseau privé,
puis nettoyé. Le code OpenTofu n'est pas universel, mais la configuration
Ansible et les services restent largement réutilisables.

### Infomaniak Public Cloud

Infomaniak confirme que la méthode est transférable : le même socle a été
reproduit avec OpenTofu et Ansible, puis restauré après suppression des VM. Le
principal écart constaté est réseau : les VM ont utilisé leurs interfaces
publiques, avec filtrage UFW et Security Group, au lieu d'un réseau privé
comparable à celui d'OVHcloud.

### Bare metal OVHcloud

Le bare metal est pertinent lorsque la charge est stable, que les ressources
physiques sont importantes ou que la performance prévisible compte davantage
que la création rapide d'une VM. Il impose toutefois une discipline plus forte
sur la réinstallation, le remplacement matériel, la sauvegarde et la
supervision. Dans ce module, il reste une option documentée et non une preuve
de déploiement.

## Recommandation métier

### Cas concret : PME industrielle avec annuaire, fichiers et supervision

Pour une PME industrielle qui veut migrer DIST01b avec un budget contrôlé,
des données européennes et une équipe qui doit pouvoir recréer rapidement son
infrastructure, je choisirais **OVHcloud Public Cloud** :

- les VM sont rapides à créer et à supprimer ;
- OpenTofu et Ansible permettent de rejouer le socle ;
- le réseau privé convient à une architecture distribuée ;
- la restauration Infomaniak a confirmé qu'un socle OpenStack automatisé peut
  être reconstruit, avec un RTO mesuré de 31 minutes sur le scénario testé ;
- les ressources peuvent être détruites en fin d'exercice pour maîtriser les
  coûts.

Je choisirais **AWS** plutôt qu'OVHcloud dans un contexte différent : une
entreprise internationale qui prévoit plusieurs régions, une forte croissance
et des services managés AWS, par exemple RDS, S3, IAM avancé, CloudWatch et
répartition multi-AZ. Le coût et la complexité sont alors acceptables si la
priorité est l'écosystème, la disponibilité multi-région et l'intégration avec
les services managés. Il faut intégrer dans la décision le stockage EBS,
le trafic sortant, le support et les enjeux Cloud Act/RGPD ; une simple VM EC2
ne suffit pas à reproduire le calcul initial.

Le **bare metal OVHcloud** serait préférable si la même PME hébergeait une
charge persistante et lourde, par exemple une base de données ou un traitement
qui utilise en permanence CPU, mémoire et I/O. Je ne le retiendrais pas comme
première cible du prototype : la rapidité de recréation et la réversibilité des
VM sont plus utiles à ce stade.

## Décision finale

| Besoin | Choix recommandé | Justification |
| --- | --- | --- |
| Prototype DIST01b et validation pédagogique | OVH Public Cloud | Solution réellement déployée, automatisée et documentée. |
| Reproduction chez un second fournisseur | Infomaniak Public Cloud | Bonne portabilité OpenStack/Ansible, avec réserve sur le réseau privé. |
| Charge stable et intensive | Bare metal OVHcloud | Ressources physiques prévisibles, à condition de tester PRA et remplacement matériel. |
| Architecture internationale managée | AWS | Large écosystème et services managés, malgré un coût et une complexité supérieurs. |

## Preuves de clôture à joindre

- matrice initiale du Kit 1 et présente matrice annotée ;
- sorties ou captures OpenTofu et Ansible OVHcloud et Infomaniak ;
- preuve du RTO de 31 minutes sur Infomaniak ;
- preuve de destruction des ressources et contrôle FinOps ;
- fiche bare metal avec la mention « non déployé » ;
- hypothèses tarifaires datées et limites de comparaison AWS ;
- recommandation finale validée et date de clôture.

## État final attendu

- les constats sont séparés des hypothèses ;
- OVHcloud, Infomaniak et le bare metal sont comparés ;
- le RTO constaté et le RPO non calculable sont explicités ;
- le choix OVHcloud ou AWS est relié à un cas métier concret ;
- les ressources cloud d'exercice sont clôturées ;
- les limites du bare metal sont documentées ;
- le module est prêt à être présenté et défendu.
