"""Architecture cible Montval 3.5, SVG et draw.io ; aucune configuration appliquée."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import escape
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/assets/files/informatique-industrielle/it-2';OUT.mkdir(parents=True,exist_ok=True)
W,H=1800,1270
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#245b83"/></marker></defs><rect width="1800" height="1270" fill="white"/>']
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
label('title',30,20,1740,40,['MONTVAL — Architecture IT/OT cible pour préparer J4'],27,True)
label('sub',30,62,1740,28,['Proposition 3.5 — manuel MAN-OT-01 v1.0 — zones fonctionnelles, pas un plan IP/VLAN déployé'],17)
for id,x,y,w,h,lines in [
 ('ext',30,120,350,210,['EXTÉRIEUR — FrigoMaint']),('it',30,420,350,210,['IT MAGASIN — EXP-IT']),('dmz',450,120,400,510,['DMZ INDUSTRIELLE PROPOSÉE','Filtrage aux frontières IT / DMZ / OT']),('super',950,120,800,240,['OT — SUPERVISION ET CONDUITE']),('services',950,450,800,200,['SERVICES OT','PROPOSÉS']),('ctrl',450,810,1300,310,['OT — CONTRÔLE','FRIGORIFIQUE'])]:box(id,x,y,w,h,lines,fill='#f2f5f8')
box('maint',65,205,280,85,['MAINT-01','Diagnostic / intervention autorisée'])
box('admin',65,505,280,85,['Administration IT','Poste et dépendances à confirmer'])
box('access',490,225,320,90,['Point d’accès distant sécurisé','Identité / ouverture contrôlées'],fill='#fff3df',dash=True)
box('bast',490,440,320,105,['BASTION proposé','Sessions et actions tracées','Cibles autorisées seulement'],fill='#fff3df',dash=True)
box('ops',990,215,275,90,['OPS-01','Consultation / acquittements'])
box('sup',1420,215,290,110,['SUP-01 — serveur unique','Supervision + historisation','90 jours / ≥ 1 valeur par min'])
box('time',990,525,300,95,['S-TEMPS proposé','Référence locale si compatible','Source / autonomie à confirmer'],dash=True)
box('back',1390,525,320,95,['S-SAUVEGARDE proposé','Données + configurations','Pertes / reprise à fixer'],dash=True)
for i,x in enumerate([500,930,1360],1):
 box('reg'+str(i),x,905,340,60,[f'REG-0{i} — consigne locale +4 °C'])
 box('field'+str(i),x,1020,340,75,[f'ZF-0{i} — sonde, contact de porte', 'Groupe frigorifique / avertissement'])
edge('A01','maint','access',[(345,247),(490,270)],['A01 — accès autorisé'],355,202,True)
edge('A02','access','bast',[(650,315),(650,440)],['A02 — session relayée','Protocole à confirmer'],665,350,True)
edge('A03','admin','bast',[(345,545),(490,490)],['A03 — administration'],350,565,True)
edge('A04','bast','sup',[(810,470),(890,470),(890,390),(1730,390),(1730,270),(1710,270)],['A04 — administration SUP-01'],1040,365,True)
edge('A05','bast','reg1',[(650,545),(650,905)],['A05 — maintenance REG autorisés','Lecture / écriture séparées'],665,710,True)
edge('C02','ops','sup',[(1265,260),(1420,260)],['C02 — interface','À confirmer'],1275,280)
edge('S01','sup','time',[(1480,325),(1480,415),(1150,415),(1150,525)],['S01 — temps','Si compatible'],1165,478,True)
edge('S02','sup','back',[(1610,325),(1610,525)],['S02 — sauvegarde','Protocole à confirmer'],1620,425,True)
for i,x in enumerate([670,1100,1530],1):
 edge('C01'+str(i),'sup','reg'+str(i),[(1560,325),(1770,325),(1770,760),(x,760),(x,905)],['C01 — collecte Modbus TCP'] if i==1 else [],980,730)
 edge('C00'+str(i),'reg'+str(i),'field'+str(i),[(x,965),(x,1020)],['C00 — terrain'] if i==1 else [],690,978)
label('note1',30,1150,1730,35,['Traits pleins : besoins documentés ; pointillés : chemins et services proposés. Réponses réseau implicites.'],17,True)
label('note2',30,1185,1730,55,['A05 illustre REG-01 ; règles distinctes possibles vers REG-02/03 selon autorisation. Aucun accès externe direct aux REG.', 'Historique interne à SUP-01 ; C03 sans flux réseau supplémentaire présumé. S03/S04 : restauration / temps REG à confirmer.'],16)
label('note3',30,1240,1730,25,['À confirmer avant J4 : topologie/IP, ports, droits, protocoles, outillage, sauvegardes, autonomie et recette.'],15)
svg.append('</svg>');(OUT/'Montval-architecture-IT-OT-J4.svg').write_text(''.join(svg));ElementTree(mx).write(OUT/'Montval-architecture-IT-OT-J4.drawio',encoding='utf-8',xml_declaration=True)
print(OUT)
