"""Génère le livrable formateur J1 à partir du laboratoire et des captures fournies."""
from pathlib import Path
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT.pdf'
IMG=ROOT/'docs/assets/img/informatique-industrielle/it-1'
pdfmetrics.registerFont(TTFont('Lato','/usr/share/fonts/truetype/lato/Lato-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LatoBold','/usr/share/fonts/truetype/lato/Lato-Bold.ttf'))
W,H=landscape(A4); M=34
INK=HexColor('#152238'); MUTED=HexColor('#526277'); TEAL=HexColor('#00695c'); PALE=HexColor('#edf7f4'); LINE=HexColor('#cbd7df')
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('J1 — Schéma d’architecture OT annoté — Olivier HIMBLOT')
c.setAuthor('Olivier HIMBLOT')
style=ParagraphStyle('body',fontName='Lato',fontSize=10,leading=14,textColor=INK)
def para(text,x,y,width,size=10,color=INK,bold=False):
 st=ParagraphStyle('p',parent=style,fontName='LatoBold' if bold else 'Lato',fontSize=size,leading=size*1.35,textColor=color)
 p=Paragraph(text,st);_,h=p.wrap(width,H);p.drawOn(c,x,y-h);return h

def header(n,title,sub):
 c.setFillColor(INK);c.rect(0,H-79,W,79,fill=1,stroke=0)
 para('INFORMATIQUE INDUSTRIELLE · AIS 2026 · GRENOBLE',M,H-15,W-2*M,9,HexColor('#97f0d7'),True)
 para(title,M,H-34,W-2*M,20,white,True)
 para(sub,M,H-65,W-2*M,9,HexColor('#e5eefc'))
 c.setStrokeColor(LINE);c.line(M,36,W-M,36)
 para('Olivier HIMBLOT · 26 octobre 2026 · Installation frigorifique fictive',M,27,660,8,MUTED)
 para(f'{n} / 3',W-65,27,35,8,MUTED)

def box(x,y,w,h,title,body,fill=PALE):
 c.setFillColor(fill);c.setStrokeColor(TEAL);c.setLineWidth(.9);c.roundRect(x,y,w,h,6,fill=1,stroke=1)
 para(title,x+9,y+h-8,w-18,10,INK,True)
 para(body,x+9,y+h-25,w-18,9,INK)

def arrow(points,label=None,lx=0,ly=0,lw=140,kind='data'):
 c.setStrokeColor(TEAL);c.setFillColor(TEAL);c.setLineWidth(2.3 if kind=='phys' else 1)
 c.setDash(4,3) if kind=='cmd' else c.setDash()
 p=c.beginPath();p.moveTo(*points[0])
 for pt in points[1:]:p.lineTo(*pt)
 c.drawPath(p);c.setDash()
 x,y=points[-1];px,py=points[-2];a=math.atan2(y-py,x-px);r=6
 p=c.beginPath();p.moveTo(x,y);p.lineTo(x-r*math.cos(a-.45),y-r*math.sin(a-.45));p.lineTo(x-r*math.cos(a+.45),y-r*math.sin(a+.45));p.close();c.drawPath(p,fill=1,stroke=0)
 if label:para(label,lx,ly,lw,8,MUTED)

header(1,'J1 — Schéma d’architecture OT annoté','Critère : identifier les composants, leurs fonctions et interactions ; distinguer contrôle local et supervision.')
para('Architecture du laboratoire de référence Python/Modbus',M,501,770,12,TEAL,True)
# Functional grouping, not separate physical machines.
c.setFillColor(HexColor('#f6f8fb'));c.setStrokeColor(LINE);c.roundRect(246,116,350,337,8,fill=1,stroke=1)
para('CONTRÔLE LOCAL — processus lab.server',258,443,325,11,TEAL,True)
para('Une instance Plant : physique + contrôle + variables',258,426,325,9,MUTED)
box(34,362,176,53,'Navigateur opérateur','Consulte la vue web.')
box(34,232,176,79,'Supervision — lab.dashboard','Serveur HTTP : 127.0.0.1:18080<br/>Lit le contrôleur par Modbus.<br/>Aucune écriture depuis la page.')
box(266,353,310,48,'Interface Modbus TCP — lab/modbus.py','127.0.0.1:15020 · lectures / écritures des variables')
box(266,255,139,63,'Mesure simulée','Température de Plant<br/>Pas de capteur matériel.')
box(437,255,139,63,'Contrôleur Python','Hystérésis, défaut,<br/>mode auto et alarme.')
box(266,143,139,63,'Procédé thermique','Enceinte, ambiance,<br/>porte et température.')
box(437,143,139,63,'Actionneur simulé','Commande compresseur<br/>Booléen marche / arrêt.')
box(632,353,176,67,'Maintenance — lab.client','Lit les états ; écrit consigne,<br/>porte, défaut et mode auto.')
arrow([(120,362),(120,311)],'HTTP : page / valeurs',127,346,100)
arrow([(210,275),(232,275),(232,375),(266,375)],'Modbus TCP<br/>requêtes / réponses',44,220,170)
arrow([(632,376),(576,376)],'Modbus TCP',632,438,155)
arrow([(507,353),(507,318)],'Accès internes<br/>aux variables',514,347,100)
arrow([(405,285),(437,285)],'T',416,302,20)
arrow([(335,206),(335,255)],'Mesure interne',269,242,130)
arrow([(507,255),(507,206)],'Commande',514,241,80,kind='cmd')
arrow([(437,174),(405,174)],'Froid',408,164,38,kind='phys')
para('<b>Réseau :</b> seuls navigateur, supervision et client de maintenance utilisent les services HTTP / Modbus. Les flèches internes représentent des variables et appels Python, pas des liaisons capteur–PLC matérielles.',632,320,176,10)
para('<b>Lecture :</b> traits fins = données / échanges ; pointillés = commande ; trait épais = effet physique simulé. Les requêtes et réponses réseau empruntent la même liaison logique.',34,100,774,9)
para('<b>Périmètre :</b> fonctions OT exécutées sur informatique Linux. Ce schéma n’est pas un plan de segmentation. OpenPLC, FUXA et la passerelle optionnelle ne sont pas intégrés au chemin démontré.',34,67,774,9)
c.showPage()
header(2,'Composants, régulation et dépendances','Analyse du fonctionnement à partir des fichiers du laboratoire et des essais J1.')
rows=[['Composant / fonction','Rôle et interaction identifiés'],
['Enceinte / processus','Plant.advance() calcule une température unique. L’ambiance réchauffe ; le compresseur refroidit. La porte ouverte double l’apport thermique du modèle.'],
['Capteur simulé','Plant.temp est la mesure utilisée par le contrôle et publiée en registre. Un défaut injecté ne fait pas disparaître la température calculée.'],
['Contrôleur local','Plant.advance() décide de la commande. À consigne 4 °C : marche ≥ 4,5 °C ; arrêt ≤ 3,5 °C ; conservation de l’état entre les seuils, en mode automatique.'],
['Compresseur / actionneur','Plant.compressor active le terme de refroidissement. Il s’agit d’une commande simulée, sans retour matériel indépendant.'],
['Alarme haute','Le modèle exige T > 8 °C pendant au moins 10 s calculées. Le compteur et l’alarme reviennent à zéro lorsque T ≤ 8 °C.'],
['Supervision / IHM','lab.dashboard interroge Modbus et sert la page web : température, consigne, compresseur, porte et alarme. Le défaut capteur n’est pas affiché.'],
['Maintenance / communications','lab.client lit les états et écrit des paramètres. Consigne : holding 0 (dixièmes de °C) ; température : input 0 ; compresseur : input 1 ; alarme : input 2 ; porte : coil 0. Adresses PDU à partir de zéro.']]
data=[[Paragraph(v,ParagraphStyle('cell',parent=style,fontName='LatoBold' if i==0 else 'Lato',fontSize=9,leading=12)) for v in row] for i,row in enumerate(rows)]
t=Table(data,colWidths=[171,603]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));_,th=t.wrap(774,H);t.drawOn(c,M,498-th)
y=498-th-18
para('Contrôle local ≠ supervision',M,y,774,13,TEAL,True)
y-=26
h1=para('<b>Arrêter seulement lab.dashboard :</b> perte de la vue web. Si lab.server reste actif, sa boucle continue à calculer et commander. Cette autonomie est établie par le code ; aucun essai de coupure de supervision n’est capturé.',M,y,370,10)
h2=para('<b>Redémarrer la machine qui héberge les deux :</b> interruption du contrôle comme de la supervision. Relancer lab.server recrée les valeurs initiales ; la simulation arrêtée ne reproduit pas une enceinte réelle qui continue à se réchauffer.',438,y,370,10)
y-=max(h1,h2)+12
para('<b>Essais J1 :</b> changement de consigne 4 → 6 → 4 °C, porte ouverte / fermée, défaut capteur et modification des seuils ±0,5 → ±1 °C observés en captures. La variante élargie est documentée ; sa restauration n’est pas encore attestée.',M,y,774,9)
c.showPage()
header(3,'Preuves visuelles et portée des résultats','J1 — défaut capteur : distinguer l’affichage de supervision et la décision du contrôleur.')
for x,time,title,caption in [
(34,'11-25-05','Défaut injecté : le compresseur reste arrêté','À 5 °C, pour une consigne de 4 °C, le compresseur est OFF : le seuil normal de 4,5 °C est dépassé. La commande sensor-fault 1 est acceptée. L’affichage ne montre pas le défaut et indique encore « Alarm: none ». La priorité au défaut est cohérente avec le code.'),
(434,'11-25-31','Défaut supprimé : la commande reprend','À 5,2 °C, après sensor-fault 0 accepté, le compresseur est ON. La température ne revient pas instantanément à la consigne. Les deux images montrent des états successifs ; elles ne mesurent pas précisément le délai de reprise.')]:
 para(title,x,497,374,12,TEAL,True)
 f=IMG/f'Capture d’écran du 2026-10-26 {time}.png';im=ImageReader(str(f));iw,ih=im.getSize();h=374*ih/iw;c.drawImage(im,x,466-h,width=374,height=h,preserveAspectRatio=True)
 para(caption,x,466-h-12,374,10)
 para(f'Capture utilisateur : 26/10/2026 {time.replace("-", ":")} (nom du fichier).',x,466-h-94,374,8,MUTED)
para('Ce que le travail établit',34,166,374,12,TEAL,True)
para('Composants et interactions repérés ; régulation localisée dans le serveur Python ; supervision identifiée comme lectrice ; distinction entre consigne, commande et température ; réaction au défaut et reprise documentées.',34,144,374,10)
para('Limites à conserver',434,166,374,12,TEAL,True)
para('Installation fictive, sans capteur ni automate matériel. Aucun OpenPLC ou FUXA connecté au procédé. Pas de validation de sûreté frigorifique, de conformité alimentaire ou de segmentation réseau. Le choix d’arrêt sur défaut est propre au scénario.',434,144,374,10)
para('<b>Sources de la preuve :</b> laboratoire ot-refrigeration-poc : README.md, lab/model.py, lab/server.py, lab/modbus.py, lab/client.py, lab/dashboard.py et docs/REGISTER_MAP.md ; captures utilisateur J1. Le détail des essais est conservé dans les fiches 1.3 à 1.7 du mémo.',34,76,774,8,MUTED)
c.save();print(OUT)
