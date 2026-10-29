"""Protection compensatoire REG-02 — 4.3, SVG et draw.io ; aucune configuration appliquée."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import escape
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/assets/files/informatique-industrielle/it-3';OUT.mkdir(parents=True,exist_ok=True)
W,H=1700,1250
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#245b83"/></marker></defs><rect width="1700" height="1250" fill="white"/>']
mx=Element('mxfile',host='app.diagrams.net');dg=SubElement(mx,'diagram',name='Montval — Architecture cible J4');md=SubElement(dg,'mxGraphModel',grid='1',gridSize='10',page='1',pageWidth=str(W),pageHeight=str(H));root=SubElement(md,'root');SubElement(root,'mxCell',id='0');SubElement(root,'mxCell',id='1',parent='0')

def label(id,x,y,w,h,lines,size=16,bold=False):
 svg.append(f'<text x="{x}" y="{y+size}" font-family="Arial,sans-serif" font-size="{size}" fill="#18354c" font-weight="{"bold" if bold else "normal"}">')
 for i,line in enumerate(lines):svg.append(f'<tspan x="{x}" dy="{0 if not i else size+7}">{escape(line)}</tspan>')
 svg.append('</text>');c=SubElement(root,'mxCell',id=id,value='\n'.join(lines),style=f'text;html=0;align=left;verticalAlign=top;whiteSpace=wrap;fontSize={size};fontColor=#18354c;fontStyle={1 if bold else 0};',vertex='1',parent='1');SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
def box(id,x,y,w,h,lines,fill='#edf6f3',dash=False):
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#38718a" stroke-width="1.5"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
 c=SubElement(root,'mxCell',id=id,value='\n'.join(lines),style=f'rounded=1;html=0;whiteSpace=wrap;align=left;spacing=12;verticalAlign=top;fillColor={fill};strokeColor=#38718a;fontColor=#18354c;fontSize=16;'+('dashed=1;' if dash else ''),vertex='1',parent='1');SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
 svg.append(f'<text x="{x+12}" y="{y+27}" font-family="Arial,sans-serif" font-size="16" fill="#18354c">')
 for i,line in enumerate(lines):svg.append(f'<tspan x="{x+12}" dy="{0 if not i else 23}">{escape(line)}</tspan>')
 svg.append('</text>')
def edge(id,s,t,pts,caption,x,y,dash=False):
 svg.append('<path d="M'+' L'.join(f'{a} {b}' for a,b in pts)+'" fill="none" stroke="#245b83" stroke-width="2" marker-end="url(#arrow)"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
 c=SubElement(root,'mxCell',id=id,value='',style='edgeStyle=orthogonalEdgeStyle;html=0;endArrow=block;strokeColor=#245b83;'+('dashed=1;' if dash else ''),edge='1',parent='1',source=s,target=t);g=SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});a=SubElement(g,'Array',attrib={'as':'points'})
 for px,py in pts[1:-1]:SubElement(a,'mxPoint',x=str(px),y=str(py))
 if caption:label(id+'label',x,y,390,55,caption,14)
label('title',30,20,1640,40,['MONTVAL — Protection compensatoire proposée pour REG-02'],26,True)
label('sub',30,65,1640,35,['REG-02 reste obsolète et sans authentification Modbus ; passerelle et cloisonnement ne corrigent pas son logiciel.'],16)
for id,x,y,w,h,ls in [
 ('external',30,130,400,200,['EXTÉRIEUR — FrigoMaint']),('dmz',30,410,400,220,['DMZ PROPOSÉE']),
 ('super',560,130,430,200,['SUPERVISION OT']),('prot',560,410,1060,300,['OT-PROTECTION','GW-02 proposé']),
 ('regzone',560,880,1060,210,['REG-02 — ISOLÉ','GW-02 seul en réseau'])]:box(id,x,y,w,h,ls,fill='#f2f5f8')
box('maint',65,210,330,85,['MAINT-01','Session externe autorisée'])
box('bast',65,495,330,100,['Point d’accès / BASTION','Identité, autorisation et traces','Pas de connexion directe REG-02'],fill='#fff3df',dash=True)
box('sup',600,210,350,85,['SUP-01','Lecture des mesures et alarmes'])
box('read',600,520,390,100,['GW-02-LECT — proposé','Lecture seule, fonctions/adresses utiles','TCP 502 hypothèse H8'],fill='#fff3df',dash=True)
box('write',1180,520,390,130,['GW-02-MAINT — proposé','Lecture puis écritures ciblées autorisées','P_MAINT_02 à confirmer','Fermé hors intervention'],fill='#fff3df',dash=True)
box('reg',600,965,410,95,['REG-02 — Modbus TCP 502','Aucune authentification, support terminé','Pas de correctif ni remplacement immédiat'])
box('field',1180,965,390,95,['ZF-02 : sonde / porte / groupe','Régulation et avertissement locaux','Comportement de sortie à confirmer'])
edge('M0','maint','bast',[(230,295),(230,495)],['Accès contrôlé'],245,355,True)
edge('Q10','sup','read',[(775,295),(775,520)],['Q10 — consultation via GW','Pas de direct SUP → REG-02'],795,350,True)
edge('Q12','bast','write',[(395,545),(475,545),(475,780),(1375,780),(1375,650)],['Q12 — maintenance bornée','Fermeture / révocation des sessions'],1080,795,True)
edge('U1','read','reg',[(795,620),(795,965)],['Q11 — GW-02 → REG-02 (TCP 502)'],1010,850,True)
edge('U2','write','reg',[(1260,650),(1260,845),(960,845),(960,965)],[],0,0,True)
edge('LOCAL','reg','field',[(1010,1010),(1180,1010)],['Terrain local','Technologie inconnue'],1030,1040)
label('guard',30,700,430,170,['IT, STOCK, ORDER, BACKUP, fournisseurs,','MAINT-01, SUP-01 et bastion :','direct vers REG-02 REFUSÉ (Q00).','Pas de pont ou bypass permissif.'],16,True)
label('limits',30,1115,1630,100,['GW-02 unique sur le dessin : deux rôles applicatifs, pas deux régulateurs. Son réseau d’administration est à définir.', 'Panne GW : collecte/maintenance dégradées ; contrôle local attendu si indépendant, à qualifier. Aucun bypass automatique.', 'Hypothèse d’architecture : aucune règle chargée, capacité de passerelle et résilience non testées.'],16)
svg.append('</svg>');(OUT/'Montval-REG02-protection-compensatoire.svg').write_text(''.join(svg));ElementTree(mx).write(OUT/'Montval-REG02-protection-compensatoire.drawio',encoding='utf-8',xml_declaration=True)
print(OUT)
