"""Analyse reproductible des sources pédagogiques reçues ; aucune connexion réseau.
Lecteur limité à ce PCAP Ethernet/IPv4/TCP avec un ADU complet par paquet.
Rejette les formats, fragments et tailles non pris en charge ; pas de réassemblage TCP.
"""
from pathlib import Path
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
import csv,struct,json,hashlib
ROOT=Path(__file__).resolve().parents[3];SRC=Path(__file__).with_name('Incident_dossier');OUT=ROOT/'docs/assets/files/informatique-industrielle/it-4';OUT.mkdir(parents=True,exist_ok=True)
PARIS=ZoneInfo('Europe/Paris')
def write(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
b=(SRC/'modbus_REG02_capture.pcap').read_bytes();assert b[:4]==bytes.fromhex('d4c3b2a1');assert struct.unpack_from('<I',b,20)[0]==1
pos=24;packets=[]
while pos<len(b):
 sec,usec,size,orig=struct.unpack_from('<IIII',b,pos);pos+=16;d=b[pos:pos+size];pos+=size
 assert len(d)==size==orig and d[12:14]==b'\x08\x00';ip=14;assert d[ip]>>4==4 and d[ip+9]==6
 assert struct.unpack_from('!H',d,ip+6)[0]&0x3fff==0
 end=ip+struct.unpack_from('!H',d,ip+2)[0];t=ip+(d[ip]&15)*4;sport,dport=struct.unpack_from('!HH',d,t);payload=d[t+(d[t+12]>>4)*4:end]
 assert len(payload)>=8
 tid,proto,length,unit=struct.unpack_from('!HHHB',payload);assert proto==0 and len(payload)==6+length
 fc=payload[7];request=dport==502;address='';value='';count='';note=''
 if fc==6:address,value=struct.unpack_from('!HH',payload,8)
 elif fc==3 and request:address,count=struct.unpack_from('!HH',payload,8)
 elif fc==3:
  count_bytes=payload[8];assert count_bytes==len(payload[9:]) and count_bytes%2==0
  value=';'.join(str(x) for x in struct.unpack('!'+'H'*(count_bytes//2),payload[9:]));count=count_bytes//2
 else:raise ValueError('Fonction non prise en charge : '+str(fc))
 time=datetime.fromtimestamp(sec,timezone.utc)+timedelta(microseconds=usec)
 packets.append(dict(trame=len(packets)+1,utc=time.isoformat(),heure_locale=time.astimezone(PARIS).isoformat(),source='.'.join(map(str,d[ip+12:ip+16])),port_source=sport,destination='.'.join(map(str,d[ip+16:ip+20])),port_destination=dport,transaction=tid,unite=unit,fonction=fc,sens='requete' if request else 'reponse',adresse_pdu=address,valeur=value,quantite=count,observation=note))
assert len(packets)==18
for q,r in zip(packets[::2],packets[1::2]):
 assert q['sens']=='requete' and r['sens']=='reponse' and q['transaction']==r['transaction'] and q['fonction']==r['fonction']
 assert q['source']==r['destination'] and q['port_source']==r['port_destination']
 if q['fonction']==6:assert q['adresse_pdu']==r['adresse_pdu'] and q['valeur']==r['valeur']
 elif q['quantite']!=r['quantite']:
  for row in (q,r):row['observation']='Incohérence synthétique : quantité FC03 demandée '+str(q['quantite'])+', retournée '+str(r['quantite'])
write('Montval-5.2-modbus-decode.csv',packets)
vpn=[]
for num,r in enumerate(csv.DictReader((SRC/'acces_distants_VPN.csv').open()),2):
 vpn.append({'ligne_source':num,**r,'timestamp_reference_sup':(datetime.fromisoformat(r['timestamp_horloge_vpn'])-timedelta(minutes=2,seconds=10)).isoformat(),'correction':'soustraction 00:02:10 selon 02_sources_et_horloges.md'})
write('Montval-5.2-vpn-normalise.csv',vpn)
measures=list(csv.DictReader((SRC/'temperatures_ZF02_2026-10-08.csv').open()));peak=max(measures,key=lambda r:float(r['temperature_c']))
summary={'date_analyse':'2026-10-30','pcap_sha256':hashlib.sha256(b).hexdigest(),'trames':len(packets),'clients_observes':sorted({r['source'] for r in packets if r['sens']=='requete'}),'fonctions':[3,6],'lectures_incoherentes':sum(r['fonction']==3 and r['sens']=='requete' for r in packets),'mesures':len(measures),'pic_mesure':peak,'premier_echantillon_superieur_8':next(r for r in measures if float(r['temperature_c'])>8),'limites':['Trace synthétique partielle, pas de réassemblage TCP nécessaire pour ce fichier','Quantités FC03 incompatibles avec les réponses à un registre','Pas d’attribution humaine, pas de preuve de température des produits']}
(OUT/'Montval-5.2-synthese-analyse.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
# Figure autonome : mesures originales, consigne en escalier et seuil documentaire.
from html import escape
W,H=1000,470;left,right,top,bottom=75,965,65,330
x=lambda i:left+(right-left)*i/(len(measures)-1)
y=lambda t:bottom-(bottom-top)*t/14
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>','<g font-family="sans-serif" font-size="13" fill="#18354c">','<text x="75" y="25" font-size="20">Montval ZF-02 — traces pédagogiques du 8 octobre 2026</text>','<text x="75" y="47">Mesures à la minute ; heures locales CEST (UTC+02:00), pas températures produit</text>']
for t in (0,4,8,12,14):parts += [f'<path d="M {left} {y(t)} H {right}" stroke="#dae2e8"/>',f'<text x="35" y="{y(t)+4}">{t} °C</text>']
for i in range(0,len(measures),30):parts += [f'<text x="{x(i)-18}" y="353">{measures[i]["timestamp_local"][11:16]}</text>']
parts += [f'<path d="M {left} {y(8)} H {right}" stroke="#bd4747" stroke-dasharray="5 4"/>']
pts=' '.join(f'{x(i):.2f},{y(float(r["temperature_c"])):.2f}' for i,r in enumerate(measures));parts += [f'<polyline points="{pts}" fill="none" stroke="#136d9b" stroke-width="2.5"/>']
path=f'M {x(0)} {y(float(measures[0]["consigne_c"]))}'
for i,r in enumerate(measures[1:],1):path+=f' H {x(i):.2f} V {y(float(r["consigne_c"])):.2f}'
parts += [f'<path d="{path}" fill="none" stroke="#a35a0a" stroke-width="2"/>']
for minutes,label in [(44,'09:14 écriture 12 °C'),(82,'09:52 alarme'),(111,'10:21 retour 4 °C')]:
 parts += [f'<path d="M {x(minutes)} {top} V {bottom}" stroke="#8d9ca7" stroke-dasharray="2 4"/>',f'<text x="{x(minutes)+5}" y="{top+15+(minutes%3)*18}">{escape(label)}</text>']
parts += ['<text x="75" y="385" fill="#136d9b">Bleu : température enregistrée</text>','<text x="365" y="385" fill="#a35a0a">Orange : consigne</text>','<text x="610" y="385" fill="#bd4747">Pointillé rouge : seuil 8 °C</text>','<text x="75" y="415">Premier échantillon &gt; 8 °C : 09:42 (8,13 °C) ; alarme enregistrée à 09:52.</text>','<text x="75" y="441">Source : temperatures_ZF02_2026-10-08.csv — analyse documentaire du 30 octobre 2026.</text>','</g></svg>']
(OUT/'Montval-5.2-evolution-ZF02.svg').write_text('\n'.join(parts))
print(json.dumps(summary,ensure_ascii=False,indent=2))
# Chronologie de travail : événements sélectionnés, références aux traces et statut explicite.
events=[
('08:22','FM-426 ouvert ; lecture paramètres autorisée 08:30–09:00','maintenance ligne 2','Autorisation consignée'),
('08:39–08:52','Session maint-shared ; source 198.51.100.44','VPN lignes 2–3 corrigées ; maintenance lignes 3–5','Session enregistrée ; identité humaine déclarée dans ticket'),
('08:46:00','FC06 PDU 0 = 40, réponse normale ; réécriture à 4 °C','PCAP 3/4 ; maintenance ligne 4 ; SUP ligne 3','Échange établi dans la trace ; portée exacte de l’autorisation à confirmer'),
('09:11:00','Réponse FC03 contenant 40 (4 °C)','PCAP 7/8','Valeur encodée ; incohérence quantité FC03'),
('09:12–09:19','Session maint-shared ; source 203.30.113.77, ticket non fourni','VPN lignes 4–5 corrigées','Session enregistrée ; auteur et autorisation non établis'),
('09:14:00','MAINT-01 écrit PDU 0 = 120 ; réponse identique +30 ms','PCAP 9/10 ; SUP ligne 4 ; mesures ligne 46','Modification confirmée par sources du scénario'),
('09:15:00','Réponse de lecture SUP contenant 120','PCAP 11/12','Corroboration de valeur ; incohérence quantité FC03'),
('09:42','Premier échantillon > 8 °C : 8,13 °C','Mesures ligne 74','Premier échantillon disponible ; instant exact de franchissement inconnu'),
('09:45','8,55 °C et régulation locale déclarée active','SUP ligne 5 ; mesures ligne 77','Valeur et événement enregistrés'),
('09:50','INC-881 ouvert pour anomalie de température','Maintenance ligne 6','Signalement consigné'),
('09:52','Alarme haute active ; mesure 9,55 °C','SUP ligne 6 ; mesures ligne 84','Déclenchement enregistré, cohérent avec 10 minutes depuis premier échantillon haut'),
('10:04','Acquittement OPS-01 et sollicitation IT','SUP ligne 7 ; mission','Prise en compte, pas correction de consigne'),
('10:07','Premier maximum enregistré : 11,55 °C','Mesures ligne 99','Mesure d’enceinte ; pas température produit'),
('10:11','FrigoMaint ne déclare pas de changement à 12 °C','Maintenance ligne 7','Déclaration à confronter aux traces'),
('10:18','Retour à 4 °C autorisé, contrôle sur place requis','Maintenance ligne 8','Autorisation consignée'),
('10:19–10:26','Session maint-oncall ; source 198.51.100.51','VPN lignes 6–7 corrigées','Session enregistrée, correspondance INC-881'),
('10:21:00','MAINT-01 écrit 40 ; réponse normale +30 ms ; commande compresseur = 1','PCAP 15/16 ; SUP ligne 8 ; maintenance ligne 9 ; mesures ligne 113','Retour à 4 °C confirmé dans sources ; contrôle terrain à vérifier'),
('10:22:00','Réponse de lecture SUP contenant 40','PCAP 17/18','Valeur encodée ; incohérence quantité FC03'),
('10:45','Mesure 8,00 °C ; alarme encore active dans export','Mesures ligne 137','Observation ; règle de disparition non détaillée'),
('10:46','Alarme effacée ; mesure 7,85 °C','SUP ligne 9 ; mesures ligne 138','Fin d’alarme enregistrée ; pas décision de conformité des produits'),
('11:15','Mesures en baisse et consigne à 4 °C','SUP ligne 10','Suivi enregistré'),
('11:30','Dernière mesure disponible : 4,18 °C','Mesures ligne 182','Fin de l’export, pas fin de toute investigation')]
write('Montval-5.2-chronologie.csv',[dict(heure_locale_2026_10_08=h,evenement=e,source=s,statut=t) for h,e,s,t in events])
