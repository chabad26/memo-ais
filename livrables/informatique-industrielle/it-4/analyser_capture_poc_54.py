"""Décodage hors ligne limité au PCAP fourni (Ethernet/IPv4/TCP, ADU complets).
Pas de réassemblage TCP ; échec explicite sur les formats incomplets rencontrés.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo
import struct,json,csv,hashlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('capture',nargs='?',default=str(Path(__file__).with_name('j5-54-controle-lecture.pcap')));parser.add_argument('--prefix',default='Montval-5.4-reproduction-complete');args=parser.parse_args()
R=Path(__file__).resolve().parents[3];P=Path(args.capture);O=R/'docs/assets/files/informatique-industrielle/it-4';b=P.read_bytes()
assert b[:4]==bytes.fromhex('d4c3b2a1') and struct.unpack_from('<I',b,20)[0]==1
pos=24;frames=0;records=[];times=[]
while pos<len(b):
 sec,us,size,orig=struct.unpack_from('<IIII',b,pos);pos+=16;d=b[pos:pos+size];pos+=size;frames+=1
 assert len(d)==size==orig
 time=(datetime.fromtimestamp(sec,timezone.utc)+timedelta(microseconds=us)).astimezone(ZoneInfo('Europe/Paris')).isoformat();times.append(time)
 assert d[12:14]==b'\x08\x00';ip=14;assert d[ip]>>4==4 and d[ip+9]==6 and struct.unpack_from('!H',d,ip+6)[0]&0x3fff==0
 end=ip+struct.unpack_from('!H',d,ip+2)[0];t=ip+(d[ip]&15)*4;sp,dp=struct.unpack_from('!HH',d,t);payload=d[t+(d[t+12]>>4)*4:end]
 if not payload:continue
 assert len(payload)>=8
 tid,protocol,length,unit=struct.unpack_from('!HHHB',payload);assert protocol==0 and len(payload)==length+6
 fc=payload[7];request=dp==15020;address='';count='';value=''
 if fc==6:address,value=struct.unpack_from('!HH',payload,8)
 elif request:assert fc in (1,3,4);address,count=struct.unpack_from('!HH',payload,8)
 else:
  assert fc in (1,3,4);n=payload[8];assert n==len(payload[9:])
  if fc in (3,4):assert n%2==0;value=list(struct.unpack('!'+'H'*(n//2),payload[9:]));count=len(value)
  else:value=list(payload[9:])
 records.append(dict(trame=frames,heure_locale=time,source='.'.join(map(str,d[ip+12:ip+16])),port_source=sp,destination='.'.join(map(str,d[ip+16:ip+20])),port_destination=dp,transaction=tid,unite=unit,fonction=fc,sens='requete' if request else 'reponse',adresse_pdu=address,quantite=count,valeurs=value,adu_hex=payload.hex()))
assert len(records)%2==0
for q,s in zip(records[::2],records[1::2]):
 assert q['sens']=='requete' and s['sens']=='reponse' and q['transaction']==s['transaction'] and q['fonction']==s['fonction'] and q['unite']==s['unite'] and q['source']==s['destination'] and q['port_source']==s['port_destination']
 if q['fonction']==6:assert (q['adresse_pdu'],q['valeurs'])==(s['adresse_pdu'],s['valeurs'])
 elif q['fonction'] in (3,4):assert q['quantite']==s['quantite']
 else:assert len(s['valeurs'])==(q['quantite']+7)//8
summary=dict(source=P.name,sha256=hashlib.sha256(b).hexdigest(),octets=len(b),trames=frames,debut_local=times[0],fin_locale=times[-1],adu=len(records),transactions=len(records)//2,limites=['Capture aval GW/OT seulement ; pas de preuve de toutes les opérations en amont','Analyse de messages complets par paquet, pas de réassemblage TCP','Origine de chaque lecture avant le relais non identifiable à ce seul point'],echanges=records)
(O/(args.prefix+'-analyse.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
with (O/(args.prefix+'-decode.csv')).open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
print(json.dumps({k:v for k,v in summary.items() if k!='echanges'},ensure_ascii=False,indent=2))
# Figure de cette fenêtre : points FC04, écritures FC06 et première/dernière alarme vue.
from html import escape
rs=summary['echanges'];temps=[x for x in rs if x['fonction']==4 and x['sens']=='reponse'];writes=[x for x in rs if x['fonction']==6 and x['sens']=='requete']
start=datetime.fromisoformat(summary['debut_local']);end=datetime.fromisoformat(summary['fin_locale']);duration=(end-start).total_seconds();left,right,top,bottom=75,970,65,330
x=lambda t:left+(right-left)*(datetime.fromisoformat(t)-start).total_seconds()/duration
y=lambda temp:bottom-(bottom-top)*temp/14
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="485" viewBox="0 0 1000 485">','<rect width="100%" height="100%" fill="white"/>','<g font-family="sans-serif" font-size="13" fill="#18354c">','<text x="75" y="25" font-size="20">PoC J5 — montée à 12 °C et correction de consigne</text>','<text x="75" y="47">30 octobre 2026, heures de Paris ; points décodés de la capture réseau du laboratoire</text>']
for temp in (0,4,8,12,14):parts.extend([f'<path d="M {left} {y(temp)} H {right}" stroke="#dde3e8"/>',f'<text x="35" y="{y(temp)+4}">{temp} °C</text>'])
pts=' '.join(f'{x(t["heure_locale"]):.2f},{y(t["valeurs"][0]/10):.2f}' for t in temps);parts.append(f'<polyline points="{pts}" fill="none" stroke="#136d9b" stroke-width="2.5"/>')
initial=next(t['valeurs'][0]/10 for t in rs if t['fonction']==3 and t['sens']=='reponse');path=f'M {left} {y(initial)}'
for w in writes:path+=f' H {x(w["heure_locale"]):.2f} V {y(w["valeurs"]/10):.2f}'
path+=f' H {right}';parts.extend([f'<path d="{path}" fill="none" stroke="#ac6411" stroke-width="2"/>',f'<path d="M {left} {y(8)} H {right}" stroke="#bd4747" stroke-dasharray="5 4"/>'])
for i,w in enumerate(writes):parts.extend([f'<path d="M {x(w["heure_locale"])} {top} V {bottom}" stroke="#8899a7" stroke-dasharray="2 4"/>',f'<text x="{x(w["heure_locale"])+5}" y="{80+i*20}">{escape(w["heure_locale"][11:19])} : {w["valeurs"]/10:g} °C</text>'])
for i in range(0,22,3):
 tm=start+timedelta(minutes=i)
 if tm<=end:parts.append(f'<text x="{left+(right-left)*i*60/duration-16}" y="352">{tm.strftime("%H:%M")}</text>')
parts.extend(['<text x="75" y="386" fill="#136d9b">Bleu : température simulée</text>','<text x="360" y="386" fill="#ac6411">Orange : consigne écrite</text>','<text x="650" y="386" fill="#bd4747">Pointillé : seuil 8 °C</text>','<text x="75" y="415">Alarme vue active à 10:47:41 ; vue inactive à 10:57:53 (échantillonnage non continu).</text>','<text x="75" y="444">Mesures réseau arrondies au dixième ; pas température produit ni validation d’une installation réelle.</text>','</g></svg>'])
(O/(args.prefix+'-evolution.svg')).write_text('\n'.join(parts))
