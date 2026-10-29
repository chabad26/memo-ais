"""Architecture étendue Montval 4.1, SVG et draw.io ; aucune configuration appliquée."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import escape
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/assets/files/informatique-industrielle/it-3';OUT.mkdir(parents=True,exist_ok=True)
W,H=1900,1510
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#245b83"/></marker></defs><rect width="1900" height="1510" fill="white"/>']
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
label('title',30,20,1800,40,['MONTVAL — Intégration des services IT et des échanges métier'],27,True)
label('sub',30,65,1800,30,['4.1 — cible fonctionnelle proposée : protocoles, ports et authentification à confirmer ; aucun déploiement attesté'],17)
for id,x,y,w,h,ls in [
 ('suppliers',30,130,340,340,['FOURNISSEURS COMMERCIAUX','Pas de droit de maintenance OT']),
 ('it',450,130,380,890,['IT MAGASIN — EXP-IT']),
 ('dmz',930,130,380,890,['DMZ INDUSTRIELLE PROPOSÉE','Filtrage et médiation']),
 ('ot',1410,130,380,890,['SUPERVISION / SERVICES OT']),
 ('maintzone',30,650,340,370,['MAINTENANCE — FrigoMaint','Interventions autorisées seulement']),
 ('ctrl',930,1160,860,240,['CONTRÔLE OT','EXP-01'])]:box(id,x,y,w,h,ls,fill='#f2f5f8')
box('portal',65,250,270,110,['SUPPLIER-01','Commandes / confirmations','Portail externe commercial'])
box('stock',490,240,300,100,['STOCK-01','Produits / lots / stocks','Consulte les données de froid'])
box('order',490,450,300,100,['ORDER-01','Commandes / réassort'])
box('admin',490,670,300,90,['IT-ADMIN','Administration IT'])
box('backup',490,850,300,100,['BACKUP-01','Sauvegarde IT + copies OT','Périmètre / restauration à fixer'])
box('relay',970,240,300,100,['RELAIS-DONNÉES proposé','Températures / alarmes','Pas de commande régulateur'],fill='#fff3df',dash=True)
box('bast',970,660,300,110,['Accès sécurisé + BASTION','Services proposés en DMZ','Rôles / sessions / cibles limités'],fill='#fff3df',dash=True)
box('depot',970,850,300,100,['DÉPÔT-OT proposé','Copies de sauvegarde','Séparé des données STOCK'],fill='#fff3df',dash=True)
box('sup',1440,240,310,100,['SUP-01','Supervision + historique','Publication des données de froid'])
box('ops',1440,450,310,90,['OPS-01','Conduite / alarmes'])
box('time',1440,680,310,110,['Services OT de J3','Référence de temps proposée','Support / autonomie à confirmer'],dash=True)
box('maint',65,780,270,100,['MAINT-01','Prestataire frigorifique','Accès ponctuel autorisé'])
for i,x in enumerate([960,1230,1500],1):box('reg'+str(i),x,1240,250,125,[f'REG-0{i} / ZF-0{i}','Sonde / porte / groupe','Boucle locale et avertissement'])
edge('B01','sup','relay',[(1440,290),(1270,290)],['B01 — publication'],1280,250,True)
edge('B02','stock','relay',[(790,290),(970,290)],['B02 — lecture'],800,250,True)
edge('B03','order','stock',[(640,450),(640,340)],['B03 — stock'],650,375,True)
edge('B04','order','portal',[(490,500),(210,500),(210,360)],['B04 — commandes / confirmations'],80,510,True)
edge('M01','maint','bast',[(335,825),(395,825),(395,805),(900,805),(900,715),(970,715)],['M01 — accès dédié autorisé'],470,805,True)
edge('A01','admin','bast',[(790,715),(970,715)],['A01 — admin OT'],795,675,True)
edge('M02','bast','reg1',[(1120,770),(1120,790),(910,790),(910,1300),(960,1300)],['M02 — maintenance REG autorisés'],1140,1080,True)
edge('A02','bast','sup',[(1270,715),(1350,715),(1350,385),(1595,385),(1595,340)],['A02 — admin SUP'],1430,390,True)
edge('L02','ops','sup',[(1595,450),(1595,340)],[],0,0)
edge('S01','sup','depot',[(1750,290),(1830,290),(1830,1060),(1340,1060),(1340,900),(1270,900)],['S01 — copie OT publiée'],1420,1070,True)
edge('S02','backup','depot',[(790,900),(970,900)],['S02 — collecte'],795,860,True)
for i,x in enumerate([1085,1355,1625],1):edge('L01'+str(i),'sup','reg'+str(i),[(1635,340),(1805,340),(1805,1135),(x,1135),(x,1240)],['L01 — Modbus TCP / collecte'] if i==1 else [],1390,1140)
label('note1',30,1420,1830,30,['Traits pleins : fonctions du manuel ; pointillés : intégration et chemins proposés. Réponses réseau implicites.'],17,True)
label('note2',30,1455,1830,50,['Pas de flux STOCK/ORDER/fournisseurs vers les commandes REG. B03 : lecture ; B04 : transactions métier, pas maintenance.', 'IT-ADMIN administre les services IT ; BACKUP-01 sauvegarde les services IT (liaisons internes non dessinées).'],16)
svg.append('</svg>');(OUT/'Montval-J4-integration-services.svg').write_text(''.join(svg));ElementTree(mx).write(OUT/'Montval-J4-integration-services.drawio',encoding='utf-8',xml_declaration=True)
print(OUT)
