"""Import documentaire des livrables Modules ; ne lance aucun laboratoire.

Copies de consultation expurgées, originaux inchangés. Les lignes susceptibles de
contenir des identifiants sont volontairement retirées de manière conservatrice.
"""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib, json, re, os

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'Modules'
DOC = ROOT / 'docs/livrables-modules'
ASSET = ROOT / 'docs/assets/files/livrables-modules'
GROUPS = {
 'on-premise': ('on-premise', 'Infrastructure on-premise', 'integration-distribuee-on-premise/README.md'),
 'cloud-iam': ('cloud-iam', 'Cloud et IAM', 'integration-distribuee-cloud-iam/README.md'),
 'observabilite': ('observabilite', 'Supervision et observabilité', 'supervision-optimisation-performances/README.md'),
 'lab-securisation-avancee': ('securisation', 'Audits Greenbone et Trivy', 'securisation-avancee-infrastructures/README.md'),
 'preuves-trivy-filebrowser': ('securisation', 'Audits Greenbone et Trivy', 'securisation-avancee-infrastructures/README.md'),
 'GNS3': ('reseaux', 'Configurations réseau GNS3', 'admin-reseaux/index.md'),
}
KEY = re.compile(r'password|passwd|passphrase|secret|token|credential|mot[s]? de passe|bindpw|rootpw|api[_ -]?key|authorization\s*[:=]|--auth|\s-w\s+\S+|enable secret', re.I)
PRIVATE = re.compile(r'-----BEGIN (?:[A-Z ]*PRIVATE KEY|OPENSSH PRIVATE KEY)-----')
known=set()
# Valeurs sensibles connues : utilisées uniquement en mémoire, jamais journalisées.
for f in SOURCE.rglob('*'):
 if not f.is_file() or any(x in ('.git','.terraform') for x in f.parts):continue
 if f.name=='.env' or f.suffix=='.env' or f.name=='openrc.sh':
  for line in f.read_text(errors='replace').splitlines():
   if '=' in line and KEY.search(line.split('=',1)[0]):
    v=line.split('=',1)[1].strip().strip('\"\'')
    if len(v)>=6 and '$' not in v:known.add(v)

def clean(text):
 lines=[];removed=0
 for line in text.splitlines():
  if KEY.search(line) or any(v in line for v in known) or re.search(r'https?://[^\s/@:]+:[^\s/@]+@',line):
   # Preserve table width and code fence balance.
   if line.strip().startswith('|'):
    line='| '+' | '.join('VALEUR RETIRÉE' for _ in line.strip().strip('|').split('|'))+' |'
   else: line='[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]'
   removed+=1
  lines.append(line)
 return '\n'.join(lines)+'\n',removed

rows=[];selected={};dups={};bygroup=defaultdict(list)
allowed={'.md','.txt','.yaml','.yml','.tf','.hcl','.sh','.json','.ndjson','.conf','.ext','.ini','.example','.ldif','.py','.cfg','.template','.tsv','.status','.log','.gns3'}
for f in sorted(SOURCE.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(SOURCE);parts=rel.parts;item={'source':rel.as_posix(),'octets':f.stat().st_size}
 reason=None
 if f.is_symlink():reason='Lien symbolique conservé localement'
 elif any(x in ('.git','.terraform','__pycache__') for x in parts):reason='Métadonnées, cache ou dépendance générée'
 elif parts[0] not in GROUPS:reason='Dépôt de sauvegarde, accès cloud privé ou dossier hors publication'
 elif any(x in ('borg-demo','borg-repository-demo','secrets','issued','logs','ldap-import') for x in parts[1:]) and not (parts[1]=='ldap-import' and f.name=='README.md'):reason='Données de travail, identités, secrets ou preuves brutes conservés localement'
 elif 'files/site' in rel.as_posix():reason='Copie du portfolio déployé, hors livrable pédagogique de cette sélection'
 elif f.name=='.env' or (f.name.startswith('.env') and f.suffix!='.example') or f.suffix in ('.env','.key','.pem','.csv') or 'tfstate' in f.name or f.name=='terraform.tfvars':reason='Configuration privée, état ou identité'
 elif '.bak' in f.name or '.avant-' in f.name or '.before-' in f.name or 'sauvegarde-avant-' in rel.as_posix():reason='Sauvegarde intermédiaire, original conservé'
 elif not item['octets']:reason='Fichier vide'
 elif f.suffix.lower() not in allowed and f.name not in ('Dockerfile','inventory','README.MD'):reason='Image disque, archive, certificat ou autre binaire conservé localement'
 if reason:item['statut']=reason;rows.append(item);continue
 try:text=f.read_text(encoding='utf-8')
 except (UnicodeError,OSError):item['statut']='Contenu binaire conservé localement';rows.append(item);continue
 if PRIVATE.search(text):item['statut']='Clé privée : non publiée';rows.append(item);continue
 text,n=clean(text);slug,title,module=GROUPS[parts[0]]
 digest=hashlib.sha256(text.encode()).hexdigest();key=(slug,digest)
 ismd=f.suffix.lower()=='.md'
 if key in dups:
  target=dups[key];item['statut']='Doublon exact de la copie de consultation';item['copie']=target.relative_to(ROOT/'docs').as_posix();selected[rel.as_posix()]=target;rows.append(item);continue
 target= DOC/slug/Path(*parts) if ismd else ASSET/slug/Path(*parts).with_name(f.name.lstrip('.')+'.txt')
 if ismd:target=target.with_suffix('.md')
 selected[rel.as_posix()]=target;dups[key]=target
 item.update(statut='Copie de consultation expurgée' if n else 'Copie documentaire',lignes_retirees=n,copie=target.relative_to(ROOT/'docs').as_posix(),sha256_copie=digest)
 rows.append(item);bygroup[slug].append((f,target,text,n,item))

# Rewrite internal source links to imported documents / text downloads.
def link_from(target,dest):return Path(os.path.relpath(dest,target.parent)).as_posix()
for slug,files in bygroup.items():
 for f,target,text,n,item in files:
  target.parent.mkdir(parents=True,exist_ok=True)
  if target.suffix=='.md':
   def repl(m):
    label,url=m.group(1),m.group(2)
    if re.match(r'(https?://|mailto:)',url):return m.group(0)
    if url.startswith('#'):return label
    path=url.split('#')[0]
    found=(f.parent/path).resolve()
    try:rel=found.relative_to(SOURCE).as_posix()
    except ValueError:return label+' (`'+url+'`, référence locale source)'
    dest=selected.get(rel)
    return '['+label+']('+link_from(target,dest)+')' if dest else label+' (`'+url+'`, conservé dans la source locale)'
   text=re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)',repl,text)
   header='\n\n> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/'+item['source']+'`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. '
   header+=('Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.' if n else 'Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.')+'\n\n'
   lines=text.splitlines(True);lines.insert(1,header);text=''.join(lines)
  target.write_text(text)
  item['sha256_copie']=hashlib.sha256(text.encode()).hexdigest()

DOC.mkdir(parents=True,exist_ok=True)
for slug in sorted(bygroup):
 files=bygroup[slug];title=next(v[1] for v in GROUPS.values() if v[0]==slug);module=next(v[2] for v in GROUPS.values() if v[0]==slug)
 s=f'# Livrables — {title}\n\n[Retour au catalogue](index.md) · [Module associé](../{module})\n\n'
 s+='Copies de consultation des livrables fournis dans `Modules`, classées le **28 octobre 2026**. Les documents conservent leurs dates et limites ; les configurations et procédures ne sont pas exécutées lors de cet import. Les fichiers techniques sont proposés en texte, éventuellement expurgé, et ne constituent pas un paquet prêt à déployer.\n\n'
 docs=[x for x in files if x[1].suffix=='.md'];tech=[x for x in files if x[1].suffix!='.md']
 for heading,entries in [('Documents et comptes rendus',docs),('Configurations, scripts et rapports techniques',tech)]:
  if not entries:continue
  s+='## '+heading+'\n\n| Livrable | Source | Copie |\n| --- | --- | --- |\n'
  for f,t,text,n,item in entries:
   h=re.search(r'^# (.+)',text,re.M);label=(h.group(1) if h and t.suffix=='.md' else f.name).replace('|','—')
   s+=f'| [{label}]({link_from(DOC/(slug+".md"),t)}) | `{item["source"]}` | '+(f'{n} ligne(s) retirée(s)' if n else 'Documentaire')+' |\n'
 (DOC/(slug+'.md')).write_text(s)
counts=Counter(x['statut'] for x in rows)
manifest=ASSET/'inventaire.json';manifest.parent.mkdir(parents=True,exist_ok=True);manifest.write_text(json.dumps({'date_import':'2026-10-28','source_locale':str(SOURCE),'fichiers':rows},ensure_ascii=False,indent=2)+'\n')
s='''# Livrables des modules

Livrables retrouvés dans `/home/oliv/Documents/entreprise/AIS/Modules`, classés par module le **28 octobre 2026**. Les sources restent à leur emplacement d’origine. Les copies intégrées au mémo permettent de relire les documents et les fichiers techniques sans dépendre de ce chemin local.

## Catalogue

| Ensemble | Contenu |\n| --- | --- |
| [Infrastructure on-premise](on-premise.md) | Architecture, annuaire, Samba, messagerie, PKI, sauvegarde, PCA/PRA, exploitation et validations. |
| [Cloud et IAM](cloud-iam.md) | Patrons OpenTofu et Ansible, inventaires et déploiement distribué. |
| [Supervision et observabilité](observabilite.md) | Stack, collecte, tableaux de bord, règles et injects pédagogiques. |
| [Audits Greenbone et Trivy](securisation.md) | Exports de rapports et configurations du laboratoire d’audit. |
| [Configurations réseau GNS3](reseaux.md) | Configurations initiales et projet du simulateur si exploitable en texte. |

## Portée des preuves

L’import rend les travaux consultables : il ne valide pas une infrastructure actuelle. Les résultats datés sont ceux des documents, les exercices simulés restent simulés, et les patrons de déploiement ne prouvent pas un déploiement. Les fiches pédagogiques existantes restent la référence de lecture contextualisée.

Les lignes susceptibles de contenir des identifiants ou des secrets sont retirées de manière conservatrice, y compris certains exemples. Les fichiers techniques sont donc des **copies de consultation**, pas une configuration directement réutilisable. Les originaux ne sont ni modifiés ni déplacés.

## Tri et conservation locale

Les doublons exacts des copies sont reliés à une seule copie par ensemble. Les variantes de contenu et les documents datés sont conservés séparément. Les historiques Git, caches fournisseurs, images disque, archives Docker, dépôts Borg, clés privées, accès cloud, états OpenTofu, fichiers d’environnement réels et listes d’identités restent locaux. Les sauvegardes intermédiaires et fichiers vides sont inventoriés sans être ajoutés au site. La copie du portfolio dans le rôle Ansible reste également locale.

[Inventaire complet du tri — JSON](../assets/files/livrables-modules/inventaire.json) : chaque fichier source, sa taille, la décision de tri et, pour les copies publiées, leur chemin et empreinte SHA-256. Les liens symboliques ne sont pas suivis comme livrables à publier.

| Décision | Nombre de fichiers |\n| --- | --- |\n'''
for status,count in sorted(counts.items()):s+=f'| {status} | {count} |\n'
s+='\nLe dossier `inject-backups` est vide au moment de l’inventaire. `cloud-iam-ovh` et les dépôts Borg sont référencés dans l’inventaire mais ne fournissent pas de copie publique.\n'
(DOC/'index.md').write_text(s)
for folder in (DOC, ASSET):
 for out in folder.rglob('*'):
  if out.is_file():
   content=out.read_text()
   assert not PRIVATE.search(content), str(out)
   assert not any(v in content for v in known), str(out)
print(json.dumps({'fichiers_inventories':len(rows),'copies':sum(len(v) for v in bygroup.values()),'decisions':dict(counts)},ensure_ascii=False))
