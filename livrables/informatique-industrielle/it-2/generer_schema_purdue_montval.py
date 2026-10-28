"""Schéma fonctionnel proposé Montval : SVG et source draw.io, sans déploiement."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import escape
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-2'
OUT.mkdir(parents=True,exist_ok=True)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1380" height="1310" viewBox="0 0 1380 1310"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#245b83"/></marker></defs><rect width="1380" height="1310" fill="white"/>']
mx=Element('mxfile',host='app.diagrams.net');diagram=SubElement(mx,'diagram',name='Montval — cible Purdue');model=SubElement(diagram,'mxGraphModel',dx='1380',dy='1310',grid='1',gridSize='10',page='1',pageWidth='1380',pageHeight='1310');root=SubElement(model,'root');SubElement(root,'mxCell',id='0');SubElement(root,'mxCell',id='1',parent='0')
seq=1

def text(x,y,lines,size=16,bold=False,color='#18354c'):
 svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{color}">')
 for i,line in enumerate(lines):svg.append(f'<tspan x="{x}" dy="{0 if i==0 else size+6}">{escape(line)}</tspan>')
 svg.append('</text>')

def node(id,x,y,w,h,lines,fill='#edf6f3',dash=False):
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="#38718a" stroke-width="1.5"'+(' stroke-dasharray="6 4"' if dash else '')+'/>');text(x+12,y+25,lines,15)
 c=SubElement(root,'mxCell',id=id,value='\n'.join(lines),style='rounded=1;whiteSpace=wrap;html=0;fillColor='+fill+';strokeColor=#38718a;fontColor=#18354c;fontSize=15;'+('dashed=1;' if dash else ''),vertex='1',parent='1');SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})

def band(id,y,h,label,detail):
 node(id,25,y,1330,h,[],fill='#f2f5f8');text(40,y+28,[label],18,True);text(40,y+58,detail,13)

def edge(id,source,target,points,label,lx,ly,dash=False):
 path='M'+' L'.join(f'{x} {y}' for x,y in points);svg.append(f'<path d="{path}" fill="none" stroke="#245b83" stroke-width="2" marker-end="url(#a)"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
 text(lx,ly,label,13)
 c=SubElement(root,'mxCell',id=id,value=' / '.join(label),style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;strokeColor=#245b83;fontColor=#18354c;fontSize=12;endArrow=block;'+('dashed=1;' if dash else ''),edge='1',parent='1',source=source,target=target)
 g=SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});a=SubElement(g,'Array',attrib={'as':'points'})
 for x,y in points[1:-1]:SubElement(a,'mxPoint',x=str(x),y=str(y))

text(30,32,['MON TVAL — Architecture cible IT/OT proposée'.replace('MON TVAL','MONTVAL')],25,True)
text(30,61,['MAN-OT-01 v1.0 — fonctions documentées ; DMZ, bastion et filtrage proposés — aucun déploiement attesté'],15)
for args in [('n5',85,110,'N5 / Extérieur',['Prestataire externe']),('n4',220,105,'N4 / IT entreprise',['EXP-IT']),('dmz',355,160,'N3.5 / DMZ industrielle',['Zone et contrôles proposés']),('n3',560,90,'N3 / Opérations du site',['Fonction, sans nouvel actif']),('n2',695,140,'N2 / Supervision',['SUP-01 et OPS-01']),('n1',880,100,'N1 / Contrôle local',['REG-01 à REG-03']),('n0',1050,145,'N0 / Procédé',['Mesures et action physique'])]:band(*args)
node('maint',320,105,360,65,['FrigoMaint — MAINT-01','Poste distant autorisé'])
node('it',880,238,330,65,['EXP-IT — environnement magasin','Origine administration : à confirmer'])
node('vpn',320,382,230,95,['Accès distant sécurisé','Point d’entrée proposé','Identité et ouverture contrôlées'],fill='#fff3df',dash=True)
node('bast',690,382,340,95,['BASTION proposé','Sessions autorisées et tracées','Cibles et opérations limitées'],fill='#fff3df',dash=True)
text(320,503,['Filtrage IT/DMZ/OT proposé ; accès externe direct aux REG exclu.'],14,True)
text(320,588,['Historisation des trois zones portée par SUP-01 :','fonction de niveau 3, sans deuxième serveur ajouté.'],15)
node('ops',320,718,250,80,['OPS-01','Températures, états, alarmes'])
node('sup',690,718,340,80,['SUP-01 — serveur unique','Supervision + historique 90 jours'])
for i,x in enumerate([320,690,1060],1):
 node(f'r{i}',x,900,240,60,[f'REG-0{i} — régulateur local'])
 node(f'z{i}',x,1070,240,105,[f'ZF-0{i} — enceinte frigorifique','Sonde + contact porte','Groupe / compresseur'])
edge('e1','maint','vpn',[(435,170),(435,382)],['F4 — accès distant proposé','Protocole à confirmer'],445,210,True)
edge('e2','it','bast',[(1045,303),(1045,340),(860,340),(860,382)],['F6 — administration autorisée'],740,334,True)
edge('e3','vpn','bast',[(550,430),(690,430)],['Session relayée'],560,412,True)
edge('e4','bast','sup',[(860,477),(860,718)],['F6 — administration SUP-01','Protocole à confirmer'],880,626,True)
edge('e5','bast','r3',[(1030,430),(1320,430),(1320,930),(1300,930)],['F5 — maintenance vers REG autorisés','Chemin indicatif ; trois cibles possibles'],1055,670,True)
edge('e6','ops','sup',[(570,758),(690,758)],['F2 — consultation','Protocole inconnu'],575,812)
for i,x in enumerate([440,810,1180],1):
 edge(f'read{i}','sup',f'r{i}',[(810,798),(810,858),(x,858),(x,900)],['F1 — Modbus TCP'] if i==1 else [],330,852)
 edge(f'local{i}',f'r{i}',f'z{i}',[(x,960),(x,1070)],['F0 — mesure / commande','Liaison terrain à confirmer'] if i==1 else [],455,1002)
text(30,1230,['Trait plein : échange fonctionnel documenté (protocole parfois inconnu). Pointillé : chemin cible proposé.'],16,True)
text(30,1260,['F3 : historisation interne à SUP-01 ; aucun flux réseau distinct supposé. Boucles locales autonomes de l’IT sous EXP-01.'],15)
svg.append('</svg>');(OUT/'Montval-Purdue-cible.svg').write_text(''.join(svg))
ElementTree(mx).write(OUT/'Montval-Purdue-cible.drawio',encoding='utf-8',xml_declaration=True)
print(OUT)
