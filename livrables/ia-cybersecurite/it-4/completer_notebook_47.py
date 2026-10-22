"""Compléter/exécuter le notebook 04 ; vérifier le modèle du kit avant chargement.

Inférence seule pour l'autoencodeur, fichier modèle conservé inchangé.
La référence vient du PDF du cours, séquence4.7 ; ce n'est pas une signature.
"""
from pathlib import Path
import hashlib
import json
import shutil
import nbformat
from nbclient import NotebookClient
BASE = Path(__file__).resolve().parent
KIT = BASE / 'IA_J4_ressources_apprenant/ia01-j4'
ATTENDUE = '01464c560c949742a4b832c1b615194971ce56e29c93f39fd98bda3169e38b00'
model_path = KIT / 'autoencodeur_hexalp.joblib'
if hashlib.sha256(model_path.read_bytes()).hexdigest() != ATTENDUE:
    raise ValueError('Empreinte différente du PDF : arrêt sans chargement')
p = KIT / '04_autoencodeur.ipynb'
source = KIT / '04_autoencodeur.source.ipynb'
if not source.exists():
    shutil.copyfile(p, source)
n = nbformat.read(source, as_version=4)
n.cells[1].source += '\n\n**Exécution locale avec assistance, hors VM.** Référence SHA-256 relevée dans le PDF du cours (4.7). Cette concordance vérifie la conformité au kit ; elle ne certifie pas la provenance réelle de Hugo ni l’innocuité du contenu. Comparaison principale : préparation pédagogique avec médiane et IF0,05 ; V2 à exclusion/0,03 distincte.'
n.cells[2].source = n.cells[2].source.replace('___', ATTENDUE)
# Verify again immediately before deserialization, including when running this cell alone.
n.cells[3].source = '''from pathlib import Path
if hashlib.sha256(Path("autoencodeur_hexalp.joblib").read_bytes()).hexdigest() != EMPREINTE_ATTENDUE:
    raise ValueError("Empreinte différente : aucun chargement")
''' + n.cells[3].source
n.cells[5].source = n.cells[5].source.replace('___','nb_parametres')
n.cells[6].source = n.cells[6].source.replace('Les 24 poids','Les 56 poids')
n.cells[9].source = n.cells[9].source.replace('___','SEUIL')
n.cells[14].source = n.cells[14].source.replace('___','0')
n.cells.append(nbformat.v4.new_markdown_cell('## Preuves complémentaires et comparaison au périmètre V2\nInférence du même autoencodeur sans réentraînement ; exclusion des 14 vrais volumes absents pour comparer sur les 2 105 mêmes observations que la V2.'))
n.cells.append(nbformat.v4.new_code_cell('''import json, sys, sklearn, numpy as np
from sklearn.metrics import confusion_matrix
from pathlib import Path
import hashlib
raw = pd.read_csv("hexalp_ssh_oct2026.csv")
volume = raw["octets_sortants_mo"].fillna(raw["octets_sortants_ko"] / 1024)
couverture = volume.notna()
def bilan(frame, col):
    y = (frame["etiquette"] == "attaque").astype(int)
    tn, fp, fn, tp = confusion_matrix(y, frame[col], labels=[0,1]).ravel()
    return {"VN":int(tn),"FP":int(fp),"FN":int(fn),"VP":int(tp),
            "precision":float(tp/(tp+fp)) if tp+fp else None,
            "rappel":float(tp/(tp+fn)), "alertes":int(tp+fp)}
groupes_stats = {nom:{"lignes":int(m.sum()),"IF":int(octobre.loc[m,"anomalie_if"].sum()),
    "AE":int(octobre.loc[m,"anomalie_ae"].sum())} for nom,m in groupes.items()}
resultat = {"origine":"Assistant, inférence locale hors VM", "python":sys.version.split()[0],
    "scikit_learn":sklearn.__version__, "pandas":pd.__version__,
    "empreinte_reference_PDF":EMPREINTE_ATTENDUE,
    "empreinte_apres_inference":hashlib.sha256(Path("autoencodeur_hexalp.joblib").read_bytes()).hexdigest(),
    "couches":[int(reseau.n_features_in_)]+list(reseau.hidden_layer_sizes)+[int(reseau.n_outputs_)],
    "parametres":int(nb_parametres),"seuil":float(SEUIL), "caracteristiques":list(CARACTERISTIQUES),
    "description":modele["description"],
    "bilan_AE_2119":bilan(octobre,"anomalie_ae"), "bilan_IF_2119":bilan(octobre,"anomalie_if"),
    "bilan_AE_2105":bilan(octobre.loc[couverture],"anomalie_ae"),"groupes_2119":groupes_stats,
    "attaques_IF_seul":int(((octobre.etiquette == "attaque") & (octobre.anomalie_if == 1) & (octobre.anomalie_ae == 0)).sum()),
    "attaques_AE_seul":int(((octobre.etiquette == "attaque") & (octobre.anomalie_ae == 1) & (octobre.anomalie_if == 0)).sum()),
    "detail_exfiltration":detail(exfiltration).to_dict(),
    "detail_premiere_sauvegarde":detail(sauvegarde).to_dict(),
    "date_premiere_sauvegarde":str(octobre.loc[sauvegarde,"date"]),
    "heure_premiere_sauvegarde":int(octobre.loc[sauvegarde,"heure"])}
Path("preuves/autoencodeur_47.json").write_text(json.dumps(resultat,ensure_ascii=False,indent=2)+"\\n")
print(json.dumps(resultat,ensure_ascii=False,indent=2))
'''))
n.metadata['kernelspec']={'display_name':'Python 3 (vérification locale)','language':'python','name':'python3'}
NotebookClient(n,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(KIT)}}).execute()
nbformat.write(n,p)
logs=[]
for i,c in enumerate(n.cells):
    for o in c.get('outputs',[]):
        if o['output_type']=='stream':logs.append(f'CELLULE {i}\n'+o.text)
        elif o['output_type'] in ('execute_result','display_data') and 'text/plain' in o['data']:
            logs.append(f'CELLULE {i}\n'+o['data']['text/plain'])
(KIT/'preuves/execution_autoencodeur_47.txt').write_text('\n'.join(logs))
assert hashlib.sha256(model_path.read_bytes()).hexdigest()==ATTENDUE
print('Notebook04 exécuté ; empreinte du modèle inchangée.')
