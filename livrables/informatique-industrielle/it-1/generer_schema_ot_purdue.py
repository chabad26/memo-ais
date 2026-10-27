"""Source commune SVG / draw.io, export PDF A3 et dossier formateur V2."""
from pathlib import Path
from xml.etree import ElementTree as ET
import html
import cairosvg
from pypdf import PdfReader, PdfWriter
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-1'
STEM='Schema-architecture-OT-J1-Olivier-HIMBLOT-Purdue'
svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','width':'1100','height':'1555','viewBox':'0 0 1100 1555'})
defs=ET.SubElement(svg,'defs')
for col,name in [('#2563a6','blue'),('#66788a','gray'),('#b26b14','orange'),('#008477','teal')]:
 mk=ET.SubElement(defs,'marker',{'id':name,'viewBox':'0 0 10 10','refX':'9','refY':'5','markerWidth':'8','markerHeight':'8','orient':'auto-start-reverse'})
 ET.SubElement(mk,'path',{'d':'M 0 0 L 10 5 L 0 10 z','fill':col})
mx=ET.Element('mxfile',{'host':'app.diagrams.net','type':'device','version':'24.7.17'})
dia=ET.SubElement(mx,'diagram',{'id':'ot-j1','name':'Architecture OT — J1'})
model=ET.SubElement(dia,'mxGraphModel',{'dx':'1100','dy':'1555','grid':'1','gridSize':'10','page':'1','pageScale':'1','pageWidth':'1100','pageHeight':'1555','math':'0','shadow':'0'})
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


rect(0,0,1100,1555,'#ffffff','#ffffff')
rect(0,0,1100,126,'#153653','#153653')
text(35,20,'Installation frigorifique — architecture OT',29,'#ffffff',True,1030)
text(35,64,'Lecture par niveaux Purdue • Laboratoire Python/Modbus • J1',19,'#dbeaf5',False,1030)
text(35,99,'Olivier HIMBLOT | AIS 2026 | Grenoble | 26 octobre 2026',13,'#dbeaf5',False,1030)
text(35,144,'Placement fonctionnel pédagogique : ce n’est pas une segmentation réseau déployée.',16,'#52677d',False,1030)
# Reference-only upper levels: never claim nonexistent firewalls or enterprise services.
for y,level,title,example in [
(187,'5','SI entreprise / accès externes','Internet, accès distant de tiers : non décrits dans le laboratoire.'),
(281,'4','Gestion métier du site','ERP / logistique : aucune liaison documentée.'),
(375,'DMZ','Zone industrielle intermédiaire','Souvent notée 3.5 ; aucun bastion ou pare-feu déployé attesté.'),
(469,'3','Opérations du site','MES / historian : aucun service dédié documenté.')]:
 rect(35,y,1030,78,'#f5f6f8','#c6ccd4',8)
 text(52,y+10,'NIVEAU '+level if level!='DMZ' else 'DMZ INDUSTRIELLE',14,'#77818f',True,190)
 text(252,y+9,title,18,'#697481',True,760)
 text(252,y+39,example,14,'#77818f',False,760)
rect(35,582,1030,246,'#edf4fb','#5f8fbd',8)
text(52,593,'NIVEAU 2',16,'#24527c',True,190)
text(52,620,'Supervision\net maintenance',15,'#24527c',False,190)
node(250,631,315,83,'Poste opérateur','Navigateur web','monitor')
node(250,744,315,67,'Supervision Python','lab.dashboard • lecture seule','server')
node(693,672,335,102,'Maintenance','lab.client\nLectures / écritures','monitor')
edge([(407,714),(407,744)],'HTTP : 18080',428,719,'blue',both=True)
rect(35,876,1030,195,'#edf4fb','#5f8fbd',8)
text(52,890,'NIVEAU 1',16,'#24527c',True,190)
text(52,918,'Contrôle local',15,'#24527c',False,190)
node(460,921,360,114,'Contrôleur simulé','lab.server / Plant\nModbus TCP : 15020\nHystérésis + défaut + alarme','plc')
edge([(407,811),(407,851),(550,851),(550,921)],'Modbus TCP : lecture',260,851,'blue',both=True)
edge([(861,774),(861,848),(750,848),(750,921)],'Modbus TCP',884,813,'blue',both=True)
text(846,850,'Écritures de paramètres',13,'#2563a6',False,215)
rect(35,1110,1030,263,'#edf7f3','#59a997',8)
text(52,1121,'NIVEAU 0',16,'#08776b',True,190)
text(52,1148,'Procédé, capteur\net actionneur',15,'#08776b',False,190)
node(250,1144,310,80,'Capteur simulé','Température Plant.temp','sensor')
node(250,1261,310,80,'Enceinte froide','Ambiance / porte\nÉvolution thermique','plant')
node(741,1261,287,80,'Compresseur','Marche / arrêt simulés','motor')
edge([(405,1144),(405,1090),(640,1090),(640,1035)],'Mesure interne',660,1085,'gray')
edge([(405,1261),(405,1224)],'Température',426,1233,'gray')
edge([(820,994),(1048,994),(1048,1301),(1028,1301)],'Commande',872,1007,'orange',True)
edge([(741,1301),(560,1301)],'Refroidissement',573,1274,'teal',wide=True)
text(35,1396,'LECTURE DU SCHÉMA',15,'#20364d',True,450)
text(35,1423,'Bleu : HTTP / Modbus TCP (requêtes-réponses). Gris : données internes.\nOrange pointillé : commande. Vert épais : effet thermique simulé.',14,'#52677d',False,1030)
text(35,1470,'Les niveaux 0 et 1 sont regroupés dans le même processus Python. Aucun PLC matériel.\nLes bandes grisées sont des repères non documentés, sans liaison inventée vers le laboratoire.',14,'#52677d',False,1030)
text(35,1516,'OpenPLC et FUXA ont été explorés séparément ; aucune connexion au procédé n’est attestée.',13,'#52677d',False,1030)
text(35,1537,'Sources : laboratoire ot-refrigeration-poc ; repérage Purdue : Cisco Industrial Security 3.1, chap. 2.',11,'#52677d',False,1030)
ET.indent(mx);ET.ElementTree(mx).write(OUT/(STEM+'.drawio'),encoding='utf-8',xml_declaration=True)
ET.ElementTree(svg).write(OUT/(STEM+'.svg'),encoding='utf-8',xml_declaration=True)
cairosvg.svg2pdf(url=str(OUT/(STEM+'.svg')),write_to=str(OUT/(STEM+'.pdf')),output_width=1122.5,output_height=1587.4)
cairosvg.svg2png(url=str(OUT/(STEM+'.svg')),write_to='/tmp/schema-ot-purdue.png',output_width=1100,output_height=1555)
writer=PdfWriter();writer.append(str(OUT/(STEM+'.pdf')))
old=PdfReader(str(OUT/'Schema-architecture-OT-J1-Olivier-HIMBLOT.pdf'))
for page in old.pages[1:]:writer.add_page(page)
writer.add_metadata({'/Title':'J1 — Architecture OT annotée — V3 présentation Purdue','/Author':'Olivier HIMBLOT'})
with open(OUT/'Schema-architecture-OT-J1-Olivier-HIMBLOT-V3.pdf','wb') as f:writer.write(f)
print(OUT/(STEM+'.drawio'))
