"""Emballe le compte-rendu Markdown et ses annexes sans altérer les preuves.
La page MkDocs reste la source de contenu ; les liens sont rendus relatifs au ZIP.
Les scripts d'analyse joints sont des sources à exécuter dans le dépôt d'origine.
"""
from pathlib import Path
from urllib.parse import unquote,quote
import re,hashlib,json,zipfile,shutil,tempfile
R=Path(__file__).resolve().parents[3];A=R/'docs/assets/files/informatique-industrielle/it-4';PAGE=R/'docs/informatique-industrielle/it-4/finaliser-compte-rendu-investigation-remediation.md';NAME='J5-investigation-remediation-OT';MD=NAME+'.md';MAN=NAME+'-inventaire.json'
source=PAGE.read_text();source=source.replace('sont joints pour reproduire les analyses hors ligne, avec les sources et captures nécessaires ; ils n’effectuent aucune connexion au modèle.','sont joints comme sources pour reproduire les analyses hors ligne **dans l’arborescence du dépôt d’origine**, avec ses dépendances et chemins ; ils n’effectuent aucune connexion au modèle. Ils ne sont pas des exécutables autonomes du ZIP.')
PAGE.write_text(source)
with tempfile.TemporaryDirectory(prefix='livrable-j5-') as tmp:
    out=Path(tmp);attached={}
    # Retirer les liens de téléchargement du livrable lui-même dans sa copie portable.
    portable='\n'.join(line for line in source.splitlines() if '[Télécharger le livrable complet' not in line)+'\n'
    def rewrite(m):
        raw=m.group(1)
        if not raw.startswith('../../assets/'):return m.group(0)
        path=(PAGE.parent/unquote(raw)).resolve();assert path.is_file(),path
        if 'assets/img/' in str(path):dest=Path('annexes/captures')/path.name
        else:dest=Path('annexes/fichiers')/path.name
        (out/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,out/dest);attached[str(dest)]=path
        return ']('+quote(str(dest),safe='/')+')'
    portable=re.sub(r'\]\(([^)]+)\)',rewrite,portable)
    (out/MD).write_text(portable)
    extras=[(R/'docs/informatique-industrielle/it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md',Path('annexes/fichiers/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md'))]
    for name in ['analyser_traces_j5.py','analyser_capture_poc_54.py']:
        extras.append((Path(__file__).with_name(name),Path('annexes/scripts-sources')/name))
    pdf=A/'J5-investigation-remediation-OT-Olivier-HIMBLOT.pdf'
    if pdf.is_file():extras.append((pdf,Path(pdf.name)))
    for path,dest in extras:
        (out/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,out/dest)
    inventory={'document':NAME,'date_preparation':'2026-10-30','auteur':'Olivier HIMBLOT','statut':'Compte-rendu pédagogique : scénario fictif et tests de laboratoire ; pas validation opérationnelle Montval','mode_emploi':'Décompresser puis ouvrir '+MD+' ; liens et images relatifs aux annexes. Scripts sources à exécuter dans le dépôt d’origine, pas directement depuis le ZIP.','empreintes':'SHA-256 des contenus annexés et du rapport ; cet inventaire ne se hache pas lui-même et ne certifie pas les faits historiques.','fichiers':[{'chemin':str(p.relative_to(out)),'octets':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.rglob('*')) if p.is_file()]}
    (out/MAN).write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    shutil.copy2(out/MAN,A/MAN);shutil.copy2(out/MD,Path(__file__).with_name(MD))
    with zipfile.ZipFile(A/(NAME+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(out)))
    # Vérifier contenu et liens de la copie distribuée, sans exécuter les annexes.
    for raw in re.findall(r'\]\(([^)]+)\)',portable):
        if not raw.startswith(('http://','https://','#')):assert (out/unquote(raw)).is_file(),raw
    with zipfile.ZipFile(A/(NAME+'.zip')) as z:
        for f in inventory['fichiers']:assert hashlib.sha256(z.read(f['chemin'])).hexdigest()==f['sha256']
    print(str(A/(NAME+'.zip')));print(len(inventory['fichiers']),'fichiers hachés, liens locaux vérifiés.')
