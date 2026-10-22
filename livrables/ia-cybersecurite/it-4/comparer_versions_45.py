"""Comparer A/B/C sur le protocole V2, sans modifier le script ni ses alertes.

Exécution de vérification distincte de la VM ; données fictives.
Les chiffres du tableau pédagogique ne sont pas supposés reproductibles à l'identique.
"""
from pathlib import Path
import importlib.util
import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
BASE = Path(__file__).resolve().parent
KIT = BASE / 'IA_J4_ressources_apprenant/ia01-j4'
OUT = KIT / 'preuves'
spec = importlib.util.spec_from_file_location('v2', KIT / 'detection_ssh_v2.py')
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)
s, _ = v2.preparer(KIT / 'hexalp_ssh_sept2026.csv', False, .1)
o, _ = v2.preparer(KIT / 'hexalp_ssh_oct2026.csv', True, .1)
X = s[v2.CARACTERISTIQUES]
y = (s.etiquette == 'attaque').astype(int)
Xt, _, yt, _ = train_test_split(X, y, test_size=.3, stratify=y, random_state=42)
arbre = DecisionTreeClassifier(max_depth=3, random_state=42).fit(Xt, yt)
preds = {'A': arbre.predict(o[v2.CARACTERISTIQUES])}
for version, taux in [('B', .10), ('C', .05)]:
    model = IsolationForest(contamination=taux, random_state=42).fit(X)
    pred = (model.predict(o[v2.CARACTERISTIQUES]) == -1).astype(int)
    preds[version] = pred if version == 'B' else (pred | preds['A'])
preds['D'] = [0] * len(o)
result = {'origine': 'Assistant, environnement local distinct de la VM', 'observations': len(o),
          'protocole': 'V2, septembre seul, graine42, profondeur3, ordre des 7 variables J3', 'versions': {}}
for version, pred in preds.items():
    tn, fp, fn, tp = confusion_matrix((o.etiquette == 'attaque').astype(int), pred, labels=[0,1]).ravel()
    frame = o.copy(); frame['prediction'] = pred
    misses = frame[(frame.etiquette == 'attaque') & (frame.prediction == 0)]
    misses.to_csv(OUT / f'comparaison_45_FN_{version}.csv', index=False)
    result['versions'][version] = {'VN':int(tn),'FP':int(fp),'FN':int(fn),'VP':int(tp),
        'FN_internes':int((misses.origine == 'interne').sum()),
        'FN_externes':int((misses.origine == 'externe').sum()),
        'alertes_par_semaine':{str(k):int(v) for k,v in frame.groupby(pd.to_datetime(frame.date).dt.to_period('W-SUN')).prediction.sum().items()},
        'exfiltration_9_oct_3h_detectee':bool(frame.loc[(frame.date == '2026-10-09') & (frame.heure == 3) & (frame.ip_source == '10.20.250.151'), 'prediction'].iloc[0])}
(OUT / 'comparaison_versions_45.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
