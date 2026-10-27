"""Source commune SVG / draw.io, export PDF A3 et dossier formateur V2."""
from pathlib import Path
from xml.etree import ElementTree as ET
import html
import cairosvg
from pypdf import PdfReader, PdfWriter
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-1'
STEM='Schema-architecture-OT-J1-Olivier-HIMBLOT-Visio'
svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','width':'1500','height':'1060','viewBox':'0 0 1500 1060'})
defs=ET.SubElement(svg,'defs')
for col,name in [('#2563a6','blue'),('#66788a','gray'),('#b26b14','orange'),('#008477','teal')]:
 mk=ET.SubElement(defs,'marker',{'id':name,'viewBox':'0 0 10 10','refX':'9','refY':'5','markerWidth':'8','markerHeight':'8','orient':'auto-start-reverse'})
 ET.SubElement(mk,'path',{'d':'M 0 0 L 10 5 L 0 10 z','fill':col})
mx=ET.Element('mxfile',{'host':'app.diagrams.net','type':'device','version':'24.7.17'})
dia=ET.SubElement(mx,'diagram',{'id':'ot-j1','name':'Architecture OT — J1'})
model=ET.SubElement(dia,'mxGraphModel',{'dx':'1500','dy':'1060','grid':'1','gridSize':'10','page':'1','pageScale':'1','pageWidth':'1500','pageHeight':'1060','math':'0','shadow':'0'})
rt=ET.SubElement(model,'root');ET.SubElement(rt,'mxCell',{'id':'0'});ET.SubElement(rt,'mxCell',{'id':'1','parent':'0'})
count=0
def cell(value,style,x,y,w,h):
 global count
 count+=1;n=ET.SubElement(rt,'mxCell',{'id':str(count+1),'value':value,'style':style,'vertex':'1','parent':'1'})
 ET.SubElement(n,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'});return n

def rect(x,y,w,h,fill='#ffffff',stroke='#c7d4e2',radius=0):
 ET.SubElement(svg,'rect',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'rx':str(radius),'fill':fill,'stroke':stroke,'stroke-width':'1.5'})
 cell('',f'rounded={int(radius>0)};arcSize=5;fillColor={fill};strokeColor={stroke};strokeWidth=1.5;',x,y,w,h)

def text(x,y,lines,size=16,color='#20364d',bold=False,width=900):
 if isinstance(lines,str):lines=lines.split('\n')
 t=ET.SubElement(svg,'text',{'x':str(x),'y':str(y+size),'fill':color,'font-family':'DejaVu Sans, Arial, sans-serif','font-size':str(size),'font-weight':'700' if bold else '400'})
 for i,line in enumerate(lines):ET.SubElement(t,'tspan',{'x':str(x),'dy':'0' if i==0 else str(size*1.4)}).text=line
 cell('<br>'.join(html.escape(z) for z in lines),f'text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;overflow=hidden;fontFamily=Arial;fontSize={size};fontColor={color};fontStyle={int(bold)};spacing=0;',x,y,width,len(lines)*size*1.4+3)

def edge(points,label,x,y,color='blue',dashed=False,both=False,wide=False):
 cols={'blue':'#2563a6','gray':'#66788a','orange':'#b26b14','teal':'#008477'};c=cols[color]
 attrib={'points':' '.join(f'{a},{b}' for a,b in points),'fill':'none','stroke':c,'stroke-width':'3' if wide else '2','marker-end':f'url(#{color})'}
 if dashed:attrib['stroke-dasharray']='8 5'
 if both:attrib['marker-start']=f'url(#{color})'
 ET.SubElement(svg,'polyline',attrib)
 global count
 count+=1;n=ET.SubElement(rt,'mxCell',{'id':str(count+1),'value':'','style':f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={c};strokeWidth={3 if wide else 2};dashed={int(dashed)};endArrow=block;endFill=1;startArrow={"block" if both else "none"};startFill=1;','edge':'1','parent':'1'})
 g=ET.SubElement(n,'mxGeometry',{'relative':'1','as':'geometry'})
 for pt,which in [(points[0],'sourcePoint'),(points[-1],'targetPoint')]:ET.SubElement(g,'mxPoint',{'x':str(pt[0]),'y':str(pt[1]),'as':which})
 if len(points)>2:
  ar=ET.SubElement(g,'Array',{'as':'points'})
  for a,b in points[1:-1]:ET.SubElement(ar,'mxPoint',{'x':str(a),'y':str(b)})
 if label:text(x,y,label,14,c,width=360)

def icon(x,y,kind):
 if kind=='monitor':
  rect(x,y,40,27,'#ffffff','#42668e',2);rect(x+17,y+27,6,7,'#42668e','#42668e');rect(x+8,y+34,24,3,'#42668e','#42668e')
 elif kind=='server':
  for off in (0,13,26):
   rect(x,y+off,40,10,'#ffffff','#42668e',1);rect(x+5,y+off+3,4,4,'#008477','#008477',1)
 elif kind=='sensor':
  rect(x+15,y,10,27,'#ffffff','#008477',3);rect(x+11,y+23,18,15,'#dcf2ec','#008477',7)
 elif kind=='plc':
  rect(x,y,42,36,'#ffffff','#42668e',2)
  for i in range(4):rect(x+5+i*8,y+6,4,5,'#008477','#008477')
  rect(x+6,y+19,30,9,'#ecf3fa','#42668e')
 elif kind=='plant':
  rect(x,y,40,38,'#ffffff','#008477',1);rect(x+6,y+5,28,25,'#edf7f3','#008477');rect(x+30,y+17,3,6,'#008477','#008477')
 elif kind=='motor':
  rect(x,y+5,34,28,'#ffffff','#008477',6);rect(x+34,y+14,8,10,'#008477','#008477');text(x+8,y+5,'M',17,'#008477',True,30)

def node(x,y,w,h,title,body,kind):
 rect(x,y,w,h,'#ffffff','#849db7',5);icon(x+16,y+19,kind)
 text(x+75,y+13,title,18,bold=True,width=w-85);text(x+75,y+43,body,15,width=w-85)

rect(0,0,1500,1060,'#ffffff','#ffffff')
rect(0,0,1500,112,'#153653','#153653')
text(38,20,'J1 — Architecture OT de l’installation frigorifique',31,'#ffffff',True,1410)
text(40,70,'Olivier HIMBLOT  |  AIS 2026 • Grenoble  |  26 octobre 2026',17,'#dbeaf5',False,1380)
rect(35,143,1430,194,'#f0f5fb','#b7cce1',6)
text(52,153,'SUPERVISION ET MAINTENANCE — fonctions OT sur infrastructure informatique',18,'#24527c',True,1380)
node(65,218,300,94,'Poste opérateur','Navigateur web', 'monitor')
node(475,218,380,94,'Service de supervision','lab.dashboard • lecture seule\nHTTP 127.0.0.1:18080','server')
node(1085,218,350,94,'Poste de maintenance','lab.client • lectures / écritures','monitor')
rect(35,392,1430,485,'#fafcfd','#95acbf',6)
text(52,401,'CONTRÔLE ET PROCÉDÉ SIMULÉS — même processus lab.server, même instance Plant',18,'#24527c',True,1380)
node(930,463,450,100,'Interface de communication','lab/modbus.py\nModbus TCP 127.0.0.1:15020','server')
node(475,463,350,100,'Contrôleur local Python','Régulation + alarme\nHystérésis • défaut • mode auto','plc')
text(55,599,'Échanges internes au modèle Python.\nAucun réseau capteur–PLC matériel.',15,'#61758b',False,390)
node(65,717,300,98,'Procédé frigorifique','Enceinte • ambiance\nPorte et température','plant')
node(475,717,350,98,'Mesure de température','Valeur simulée Plant.temp\nAucun capteur matériel','sensor')
node(1085,717,350,98,'Actionneur simulé','Commande compresseur\nBooléen marche / arrêt','motor')
edge([(365,265),(475,265)],'HTTP',382,239,both=True)
edge([(665,312),(665,365),(1110,365),(1110,463)],'Modbus TCP • lecture',760,341,both=True)
edge([(1260,312),(1260,463)],'Modbus TCP\nlecture / écriture',1280,352,both=True)
edge([(930,513),(825,513)],'Variables\npartagées',839,468,'gray',both=True)
edge([(650,717),(650,563)],'Mesure',665,664,'gray')
edge([(365,766),(475,766)],'Température',370,736,'gray')
edge([(790,563),(790,653),(1260,653),(1260,717)],'Commande marche / arrêt',885,624,'orange',True)
edge([(1260,815),(1260,851),(215,851),(215,815)],'Refroidissement simulé',750,827,'teal',wide=True)
text(40,899,'LÉGENDE DES CONNECTEURS',15,'#20364d',True,420)
edge([(40,942),(135,942)],'Réseau (requêtes / réponses)',150,930,'blue',both=True)
edge([(650,942),(745,942)],'Données internes',760,930,'gray')
edge([(40,981),(135,981)],'Commande',150,969,'orange',True)
edge([(650,981),(745,981)],'Effet physique simulé',760,969,'teal',wide=True)
text(40,1010,'Périmètre : laboratoire fictif ; zones fonctionnelles, pas une segmentation réseau. OpenPLC et FUXA ne sont pas connectés au procédé.',14,'#52677d',False,1430)
text(40,1033,'Source : ot-refrigeration-poc — lab/model.py, lab/modbus.py, lab/server.py, lab/dashboard.py et lab/client.py.',12,'#52677d',False,1430)
ET.indent(mx);ET.ElementTree(mx).write(OUT/(STEM+'.drawio'),encoding='utf-8',xml_declaration=True)
ET.ElementTree(svg).write(OUT/(STEM+'.svg'),encoding='utf-8',xml_declaration=True)
cairosvg.svg2pdf(url=str(OUT/(STEM+'.svg')),write_to=str(OUT/(STEM+'.pdf')),output_width=1587.4,output_height=1122.5)
cairosvg.svg2png(url=str(OUT/(STEM+'.svg')),write_to='/tmp/schema-ot-visio.png',output_width=1500,output_height=1060)
writer=PdfWriter();writer.append(str(OUT/(STEM+'.pdf')))
old=PdfReader(str(OUT/'Schema-architecture-OT-J1-Olivier-HIMBLOT.pdf'))
for page in old.pages[1:]:writer.add_page(page)
writer.add_metadata({'/Title':'J1 — Architecture OT annotée — V2 style Visio','/Author':'Olivier HIMBLOT'})
with open(OUT/'Schema-architecture-OT-J1-Olivier-HIMBLOT-V2.pdf','wb') as f:writer.write(f)
print(OUT/(STEM+'.drawio'))
