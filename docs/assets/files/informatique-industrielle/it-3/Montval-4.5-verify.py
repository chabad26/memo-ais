#!/usr/bin/env python3
"""Vérifications réelles dans les namespaces du TP ; ne fabrique aucun succès."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser();p.add_argument('--phase',choices=['before','after'],required=True);p.add_argument('--poc',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
results=[]
def call(ns,arguments,timeout=15):
 cmd=['ip','netns','exec',ns,'python3',*arguments]
 try:
  x=subprocess.run(cmd,cwd=a.poc,text=True,capture_output=True,timeout=timeout)
  return {'commande':cmd,'retour':x.returncode,'stdout':x.stdout,'stderr':x.stderr}
 except subprocess.TimeoutExpired as exc:
  return {'commande':cmd,'retour':124,'stdout':str(exc.stdout or ''),'stderr':'Délai du vérificateur dépassé'}
def client(ns,ip,port,op='status',value=None):
 args=['-m','lab.client',op]
 if value is not None:args.append(str(value))
 return call(ns,[*args,'--host',ip,'--port',str(port)])
def record(id,expected,ok,detail):
 results.append({'test':id,'attendu':expected,'conforme':bool(ok),'observation':detail})
 print(f'{id}: {"OK" if ok else "ÉCHEC"} — {expected}',flush=True)

ot=client('ais45-gw','10.77.30.2',15020)
record('T01','GW lit le serveur OT',ot['retour']==0 and 'setpoint=' in ot['stdout'],ot)
gw=client('ais45-it','10.77.20.2',15021)
record('T02','IT lit par la passerelle',gw['retour']==0 and 'setpoint=' in gw['stdout'],gw)
if a.phase=='before':
 direct=client('ais45-it','10.77.30.2',15020)
 record('B00','Avant filtrage, direct IT/OT joignable dans le seul réseau privé du TP',direct['retour']==0,direct)
else:
 attempted=client('ais45-it','10.77.20.2',15021,'setpoint',6)
 record('T03','FC06 via passerelle rejeté avec exception 01',attempted['retour']!=0 and 'exception code 1' in attempted['stderr'],attempted)
 door=client('ais45-it','10.77.20.2',15021,'door',1)
 record('T05','FC05 via passerelle rejeté avec exception 01',door['retour']!=0 and 'exception code 1' in door['stderr'],door)
 before=json.loads(subprocess.check_output(['ip','netns','exec','ais45-fw','nft','-j','list','ruleset'],text=True))
 def counter(tree,name):
  for entry in tree.get('nftables',[]):
   obj=entry.get('counter',{})
   if obj.get('name')==name:return obj.get('packets',0)
  raise RuntimeError('Compteur absent : '+name)
 before_drop=counter(before,'it_direct_drop')
 direct=client('ais45-it','10.77.30.2',15020)
 after=json.loads(subprocess.check_output(['ip','netns','exec','ais45-fw','nft','-j','list','ruleset'],text=True))
 after_drop=counter(after,'it_direct_drop')
 # The successful authorized OT path above plus a matching drop counter distinguish filtering from a dead service.
 record('T04','Direct IT/OT impossible et compteur de refus augmenté, avec OT disponible',direct['retour']!=0 and after_drop>before_drop and ot['retour']==0,{'client':direct,'compteur_avant':before_drop,'compteur_apres':after_drop})
 reread=client('ais45-it','10.77.20.2',15021)
 def field(text,name):
  for part in text.split(';'):
   part=part.strip()
   if part.startswith(name+'='):return part.split('=',1)[1]
  return None
 record('T03-T05-relecture','Consigne et porte inchangées après les tentatives refusées',reread['retour']==0 and field(reread['stdout'],'setpoint')==field(gw['stdout'],'setpoint') and field(reread['stdout'],'door')==field(gw['stdout'],'door'),reread)
 http=call('ais45-it',['-c','import urllib.request; r=urllib.request.urlopen("http://10.77.20.2:18080/api",timeout=4); print(r.status); print(r.read().decode())'])
 record('T07','Supervision HTTP et collecte via GW disponibles',http['retour']==0 and http['stdout'].startswith('200\n') and 'temperature' in http['stdout'],http)
 record('COUNTERS','Règles de consultation et GW/OT réellement traversées',counter(after,'it_gateway_accept')>0 and counter(after,'gateway_ot_accept')>0 and counter(after,'replies_accept')>0,{'it_gateway_accept':counter(after,'it_gateway_accept'),'gateway_ot_accept':counter(after,'gateway_ot_accept'),'replies_accept':counter(after,'replies_accept')})

payload={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':a.phase,'resultats':results,'conforme':all(x['conforme'] for x in results),'non_testes':['T06 source supplémentaire','T08 panne du GW','T09 révocation session persistante','T10 reprise GW','REG-02 réel et GW-02 industriel']}
a.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('Résultats :',a.output)
sys.exit(0 if payload['conforme'] else 1)
