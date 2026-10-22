"""Compléter et exécuter le notebook 03 à partir de sa source conservée.

Utiliser un environnement isolé avec nbformat, nbclient, ipykernel, pandas,
matplotlib et Scikit-learn. Exécution locale de simulations fictives seulement.
"""
import nbformat, json, shutil
from pathlib import Path
from nbclient import NotebookClient
BASE=Path(__file__).resolve().parent
KIT=BASE/'IA_J4_ressources_apprenant/ia01-j4'
p=KIT/'03_attaquer_le_modele.ipynb'
source=KIT/'03_attaquer_le_modele.source.ipynb'
if not source.exists():shutil.copyfile(p,source)
n=nbformat.read(source,as_version=4)
n.cells[1].source+='\n\n**Portée : variante pédagogique du kit**, avec imputation par médiane, ordre des variables du kit et contamination 0,05. Elle diffère de notre V2 J3/J4 (exclusion des volumes absents, autre ordre, contamination 0,03). Exécution avec assistance dans un environnement local distinct de la VM. Les comparaisons V2 sont ajoutées en fin de notebook ; aucun modèle de production n’est remplacé.'
n.cells[7].source='''# Dichotomie sur 1..64 ; frontière à vérifier, sans prétendre extraire tout le modèle.
for comptes in [32, 16, 8, 4, 2, 3]:
    sonde(comptes_distincts=comptes, heure=14)'''
n.cells[9].source='''# Chercher la transition du matin ; 8 h et 9 h vérifient la frontière.
for h in [12, 6, 9, 8]:
    sonde(comptes_distincts=2, heure=h)'''
n.cells[13].source=n.cells[13].source.replace('ECHECS = ___','ECHECS = 10').replace('COMPTES = ___','COMPTES = 2').replace('HEURE = ___','HEURE = 14')
n.cells[16].source=n.cells[16].source.replace('___','5000')
n.cells[17].source+='''\n# Fractionnement fictif : vérifier chaque heure, pas seulement une moyenne.
print("Plan 5 x 1000 Mo, heures 9 à 13 :")
for h in range(9, 14):
    print(h, verdict(succes_auth=1, comptes_distincts=1, duree_session_min=45,
                     octets_sortants_mo=1000, heure=h, externe=0, afficher=False))'''
n.cells[20].source=n.cells[20].source.replace('___','"10.20.8.30"')+'''\nprint("Suppressions par semaine :")
print(octobre.loc[dans_liste].groupby(pd.to_datetime(octobre.loc[dans_liste, "date"]).dt.to_period("W-SUN"))["alerte"].sum())'''
for i,variable,values in [(25,'N_LIGNES',[0,2,4,5,10,20]),(27,'N_NUITS',[0,10,20,40,80])]:
    original=n.cells[i].source.replace('___',variable)
    original='\n'.join(original.splitlines()[1:])
    n.cells[i].source=f'for {variable} in {values}:\n'+ '\n'.join('    '+line for line in original.splitlines())
n.cells.append(nbformat.v4.new_markdown_cell('## Vérification séparée sur la V2 figée\nMême protocole que la remise ; essais synthétiques uniquement. Les matrices d’octobre de la V2 ne sont pas remplacées.'))
v2code='''import importlib.util
from pathlib import Path
import json, sys
spec = importlib.util.spec_from_file_location("v2", "detection_ssh_v2.py")
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)
s_v2, _ = v2.preparer(Path("hexalp_ssh_sept2026.csv"), False, .10)
o_v2, _ = v2.preparer(Path("hexalp_ssh_oct2026.csv"), True, .10)
cols = v2.CARACTERISTIQUES
Xs = s_v2[cols]
ys = (s_v2.etiquette == "attaque").astype(int)
xt, xv, yt, yv = train_test_split(Xs, ys, test_size=.3, stratify=ys, random_state=42)
a_v2 = DecisionTreeClassifier(max_depth=3, random_state=42).fit(xt, yt)
f_v2 = IsolationForest(contamination=.03, random_state=42).fit(Xs)
def avis_v2(**kwargs):
    row = dict(echecs_auth=0, succes_auth=1, comptes_distincts=1, duree_session_min=30,
               octets_sortants_mo=1, heure=14, externe=0)
    row.update(kwargs)
    obs = pd.DataFrame([row])[cols]
    return bool(a_v2.predict(obs)[0] == 1 or f_v2.predict(obs)[0] == -1)
resultats = {"origine": "Assistant, notebook exécuté localement hors VM", "python": sys.version.split()[0],
             "protocole": "V2 : exclusion, ordre J3, contamination0.03, graine42"}
resultats["spraying_2_comptes_10_echecs_par_heure"] = {
    str(h): avis_v2(echecs_auth=10, succes_auth=0, comptes_distincts=2,
                    duree_session_min=0, octets_sortants_mo=0, heure=h, externe=1) for h in range(24)}
resultats["plan_exfiltration_1000_mo_9_a_13"] = {str(h): avis_v2(succes_auth=1, comptes_distincts=1,
    duree_session_min=45, octets_sortants_mo=1000, heure=h, externe=0) for h in range(9,14)}
resultats["9000_mo_1h"] = avis_v2(succes_auth=1, comptes_distincts=1,
    duree_session_min=55, octets_sortants_mo=9000, heure=1, externe=0)
pred_o = (a_v2.predict(o_v2[cols]) == 1) | (f_v2.predict(o_v2[cols]) == -1)
wb = (o_v2.ip_source == "10.20.8.30")
resultats["liste_blanche_suppressions"] = int((pred_o & wb).sum())
resultats["empoisonnement_etiquettes"] = []
for count in [0,2,4,5,10,20]:
    rng = np.random.default_rng(42)
    fausses_v2 = pd.DataFrame({"echecs_auth":rng.integers(4,9,count), "succes_auth":0,
        "comptes_distincts":rng.integers(4,7,count), "duree_session_min":0,
        "octets_sortants_mo":0., "heure":rng.integers(9,18,count), "externe":1})[cols]
    poison = DecisionTreeClassifier(max_depth=3, random_state=42).fit(
        pd.concat([xt, fausses_v2]), pd.concat([yt, pd.Series(0,index=fausses_v2.index)]))
    test = pd.DataFrame([attaque_preparee])[cols]
    resultats["empoisonnement_etiquettes"].append({"lignes":count,
        "attaque_classee":int(poison.predict(test)[0]),
        "union_alerte":bool(poison.predict(test)[0] == 1 or f_v2.predict(test)[0] == -1),
        "matrice_test":confusion_matrix(yv, poison.predict(xv), labels=[0,1]).tolist()})
resultats["empoisonnement_comportement"] = []
vpn = o_v2[(o_v2.etiquette == "attaque") & o_v2.ip_source.str.startswith("10.20.250.")]
for count in [0,10,20,40,80]:
    rng = np.random.default_rng(42)
    nuits_v2 = pd.DataFrame({"echecs_auth":rng.integers(0,2,count), "succes_auth":1, "comptes_distincts":1,
        "duree_session_min":rng.integers(30,61,count), "octets_sortants_mo":rng.uniform(3000,9000,count),
        "heure":rng.choice([3,4,5,22,23],count),"externe":0})[cols]
    poison = IsolationForest(contamination=.03, random_state=42).fit(pd.concat([Xs, nuits_v2]))
    resultats["empoisonnement_comportement"].append({"nuits_synthetiques":count,
        "vpn_detectes_IF":int((poison.predict(vpn[cols]) == -1).sum()), "vpn_total":len(vpn)})
Path("preuves/attaques_46_v2.json").write_text(json.dumps(resultats,ensure_ascii=False,indent=2)+"\\n")
print(json.dumps(resultats,ensure_ascii=False,indent=2))
'''
n.cells.append(nbformat.v4.new_code_cell(v2code))
n.metadata['kernelspec']={'display_name':'Python 3 (vérification locale)','language':'python','name':'python3'}
client=NotebookClient(n, timeout=120, kernel_name='python3',resources={'metadata':{'path':str(KIT)}})
client.execute()
nbformat.write(n,p)
outputs=[]
for i,c in enumerate(n.cells):
    for out in c.get('outputs',[]):
        if out.get('output_type')=='stream':outputs.append(f'CELLULE {i}\n'+out.text)
(KIT/'preuves/execution_attaques_46.txt').write_text('\n'.join(outputs))
print('Notebook exécuté :',len(n.cells),'cellules')
