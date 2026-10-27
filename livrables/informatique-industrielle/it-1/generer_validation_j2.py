"""Dossier C2 du formateur : synthèse des preuves utilisateur J1/J2, sans rejouer les essais."""
from pathlib import Path
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-1/J2-validation-jumeau-numerique-Olivier-HIMBLOT.pdf'
IMG=ROOT/'docs/assets/img/informatique-industrielle/it-1'
for name,file in [('Body','Lato-Regular.ttf'),('Bold','Lato-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/lato/'+file))
W,H=landscape(A4);M=34;CW=W-2*M
INK=HexColor('#18354c');TEAL=HexColor('#00695c');MUTED=HexColor('#516477');LINE=HexColor('#c7d4df');PALE=HexColor('#edf6f3')
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('J2-validation-jumeau-numerique');c.setAuthor('Olivier HIMBLOT');c.setSubject('C2 — Mettre en œuvre et valider un jumeau numérique simplifié')
style=ParagraphStyle('body',fontName='Body',fontSize=10,leading=14,textColor=INK)
def p(txt,x,y,w,size=10,bold=False,color=INK):
 st=ParagraphStyle('p',parent=style,fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.35,textColor=color)
 q=Paragraph(txt,st);_,h=q.wrap(w,H);q.drawOn(c,x,y-h);return y-h

def title(n,name,sub):
 c.setFillColor(INK);c.rect(0,H-83,W,83,fill=1,stroke=0)
 p('INFORMATIQUE INDUSTRIELLE · ITÉRATION 1 · JOURNÉE 2',M,H-15,CW,9,True,HexColor('#97f0d7'))
 p(name,M,H-34,CW,20,True,white);p(sub,M,H-65,CW,9,False,HexColor('#e1ebf3'))
 c.setStrokeColor(LINE);c.line(M,36,W-M,36)
 p('Olivier HIMBLOT · AIS 2026 · Grenoble · 27 octobre 2026',M,26,CW-50,8,False,MUTED)
 p(f'{n} / 7',W-66,26,36,8,False,MUTED)

def table(rows,widths,y,size=9):
 data=[[Paragraph(str(v),ParagraphStyle('cell',parent=style,fontName='Bold' if i==0 else 'Body',fontSize=size,leading=size*1.35)) for v in row] for i,row in enumerate(rows)]
 t=Table(data,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));_,h=t.wrap(CW,H);assert y-h>=45,(y,h);t.drawOn(c,M,y-h);return y-h

def shot(time,x,top,w,maxh=200,date='2026-10-27'):
 path=IMG/f'Capture d’écran du {date} {time}.png';r=ImageReader(str(path));iw,ih=r.getSize();scale=min(w/iw,maxh/ih);dw,dh=iw*scale,ih*scale;c.drawImage(r,x+(w-dw)/2,top-dh,width=dw,height=dh);return top-dh

def box(x,y,w,h,t,b):
 c.setFillColor(PALE);c.setStrokeColor(TEAL);c.roundRect(x,y,w,h,5,fill=1,stroke=1);p(t,x+9,y+h-9,w-18,11,True);p(b,x+9,y+h-29,w-18,9)
def arrow(points,label,x,y,w=160,dash=False):
 c.setStrokeColor(TEAL);c.setFillColor(TEAL);c.setLineWidth(1.2);c.setDash(4,3) if dash else c.setDash();path=c.beginPath();path.moveTo(*points[0])
 for z in points[1:]:path.lineTo(*z)
 c.drawPath(path);c.setDash();ex,ey=points[-1];sx,sy=points[-2];a=math.atan2(ey-sy,ex-sx);q=c.beginPath();q.moveTo(ex,ey);q.lineTo(ex-6*math.cos(a-.5),ey-6*math.sin(a-.5));q.lineTo(ex-6*math.cos(a+.5),ey-6*math.sin(a+.5));q.close();c.drawPath(q,fill=1,stroke=0);p(label,x,y,w,8,False,MUTED)

# 1 — Trainer-facing criterion and honest readiness assessment.
title(1,'J2-validation-jumeau-numerique','Dossier de validation du jumeau numérique simplifié · Preuve de travail C2')
y=p('Mettre en œuvre et valider un jumeau numérique simplifié',M,492,CW,16,True,TEAL)-12
y=p('<b>Critères :</b> met en œuvre les services du jumeau numérique ; vérifie les échanges Modbus et les comportements simulés. Ce dossier rassemble architecture, variables, captures représentatives, résultats et limites en un document unique.',M,y,CW,11)-18
y=table([['Critère','Éléments établis','Portée / limite'],['Services du modèle','Serveur Python, client, supervision web et chemin de passerelle utilisés ; lectures concordantes.','Fonctions attestées par captures et PCAP, sans relevé complet de démarrage et des écoutes.'],['Échanges industriels','FC03/FC04/FC01 repérés ; FC05 documenté ; FC06 direct accepté ; FC06 via proxy refusé.','Échanges locaux du laboratoire. La passerelle seule ne segmente pas le réseau.'],['Comportements simulés','Consigne modifiée, porte et défaut injectés, séries thermiques, état final restauré.','Certains scénarios restent partiels : cycles complets et versions de seuils non exhaustivement attestés.'],['Limites identifiées','Procédé fictif, physique simplifiée, absence de matériel et de synchronisation réelle.','La validation pédagogique ne vaut pas validation d’une installation réelle.']],[140,325,CW-465],y,9)-18
y=p('<b>Environnement :</b> Debian 13 x86_64, Python 3.13.5 (capture de préparation). VM déclarée : 2 vCPU, 2 Go RAM, disque 20 Go, accès SSH. Les ressources finales ne sont pas re-mesurées dans la série de validation.',M,y,CW,10)-12
p('<b>Statut :</b> dossier constitué sur les travaux individuels documentés. Le binôme, la restitution collective et l’appréciation finale du formateur restent à confirmer. Aucune signature ni décision de validation n’est inventée.',M,y,CW,10)
c.showPage()
# 2 — Actual connected architecture.
title(2,'1 — Architecture du modèle assemblé','Composants réellement utilisés et protocoles · Fonctions Python distinctes des équipements physiques')
box(34,402,196,65,'Navigateur du poste','Vue web de supervision')
box(310,402,230,65,'lab.dashboard','HTTP : 18080<br/>Client Modbus en lecture seule')
box(610,402,198,65,'lab.client','Maintenance / consultation')
box(70,222,286,85,'lab.gateway — 15021','Autorise FC01–FC04<br/>Refuse les autres fonctions<br/>Relais vers 15020')
box(520,222,288,85,'lab.server — 15020','Serveur Modbus TCP<br/>Accès direct en écriture disponible')
box(520,104,288,65,'Plant — lab/model.py','Physique + régulation + alarme<br/>Même état pour les deux chemins')
arrow([(230,435),(310,435)],'HTTP via tunnel SSH',235,456,160)
arrow([(425,402),(425,346),(638,346),(638,307)],'Modbus : lecture directe',436,367,175)
arrow([(709,402),(709,307)],'Modbus direct',716,360,95)
arrow([(610,418),(580,418),(580,329),(216,329),(216,307)],'Modbus via passerelle',70,352,200)
arrow([(356,266),(520,266)],'Lectures relayées',373,287,150)
arrow([(665,222),(665,169)],'Appels / variables internes',675,202,130,dash=True)
p('<b>Repères :</b> les services écoutent par défaut sur 127.0.0.1 dans la VM. Le tunnel SSH transporte HTTP 18080 vers le navigateur du poste. Il ne remplace pas les échanges Modbus locaux.',34,183,415,10)
p('<b>Contrôle local :</b> lab.server héberge la simulation et la régulation. Arrêter seulement le dashboard ne supprime pas cette boucle ; redémarrer leur machine commune interrompt les deux. Le redémarrage du serveur recrée un nouvel état du processus.',34,119,415,10)
p('<b>Hors chemin démontré :</b> OpenPLC et FUXA ont été explorés séparément ; ni leur raccordement au procédé, ni le bastion/pare-feu de l’architecture cible ne sont présentés comme déployés ici.',M,69,CW,9,False,MUTED)
c.showPage()
# 3 — Complete mapping.
title(3,'2 — Table de variables Modbus','Adresses PDU à partir de zéro · Une donnée s’identifie par sa table et son adresse')
y=table([['Variable','Table / adresse','Lecture','Écriture','Unité / signification'],['Consigne','Holding 0','FC03','FC06','Dixièmes de °C : 40 = 4 °C, 60 = 6 °C. Serveur : 0..500 acceptés.'],['Température simulée','Input 0','FC04','Non','Dixièmes de °C ; mesure calculée et arrondie.'],['Compresseur','Input 1 ; aussi discrete 0','FC04 ; FC02','Non directe','0 arrêt / 1 marche. Commande simulée, sans retour matériel indépendant.'],['Porte','Coil 0','FC01','FC05','Vrai = ouverte : 0xFF00 à l’écriture ; faux = fermée : 0x0000.'],['Alarme haute','Input 2 ; aussi discrete 1','FC04 ; FC02','Non directe','T > 8 °C pendant au moins 10 s calculées ; 0 inactive / 1 active.'],['Défaut capteur','Coil 1 ; aussi input 3','FC01 ; FC04','FC05 sur coil 1','0 inactif / 1 injecté. L’input register reste en lecture seule.'],['Mode automatique','Holding 2','FC03','FC06','1 actif / 0 régulation suspendue ; 0 ne garantit pas l’arrêt du compresseur.'],['Limite conseillée','Holding 1','FC03','Non','80 = 8 °C, information non imposée comme borne de consigne.']],[124,146,72,106,CW-448],490,9)-18
p('<b>Codage et droits :</b> un bit FC05 s’écrit 0xFF00 ou 0x0000 ; ce n’est pas une température. FC06 écrit un registre numérique. Les droits dépendent du serveur et du chemin utilisé : le proxy refuse les écritures, le port direct les accepte aux adresses/valeurs implémentées.',M,y,CW,10)
p('<b>Limite d’encodage :</b> le modèle peut calculer une température négative, mais l’implémentation de registre non signé ne la couvre pas correctement. Les essais documentés restent au-dessus de 0 °C.',M,y-58,CW,9,False,MUTED)
c.showPage()
# 4 — Communication evidence, packet numbers scoped to one PCAP.
title(4,'3 — Preuves de communication','Fichier assemblage-j2.pcap · Numéros propres à cette capture, distincts de ceux des ateliers précédents')
y=table([['Essai','Paquets','Résultat observé'],['Lecture via 15021','2554 → 2564','FC03 adresse 0, quantité 3 ; réponse [40, 80, 1].'],['Écriture directe via 15020','2734 → 2736','FC06 holding 0, valeur 60 ; écho sans exception, 494 µs.'],['Restauration directe','8204 → 8206','FC06 holding 0, valeur 40 ; écho sans exception, 473 µs.'],['Écriture refusée via 15021','11574 → 11576','FC06 holding 0, valeur 60 ; réponse 86 01, Illegal Function.']],[180,130,CW-310],490,9)
p('Lecture relayée : valeurs du serveur',34,309,370,11,True,TEAL)
p('Écriture bloquée par la passerelle',438,309,370,11,True,TEAL)
shot('10-53-42',34,284,370,190);shot('10-54-37',438,284,370,190)
p('Réponse 2564 : consigne 4 °C, limite conseillée 8 °C et mode auto actif. Le délai de 793 µs concerne l’échange applicatif.',34,87,370,9)
p('Réponse 11576 : exception active, code 01 ; le PCAP confirme le sens 15021 → client. Ce refus n’empêche pas un accès direct à 15020.',438,87,370,9)
c.showPage()
# 5 — Validation matrix.
title(5,'4 — Résultats des six scénarios','Résultats attendus et observés · Critères limités aux conditions et preuves disponibles')
rows=[['ID / scénario','Attendu (modèle initial)','Observé / preuve','Conclusion limitée'],['V1 — Normal','Consigne 4 °C, porte fermée ; cycles vers 3,5–4,5 °C.','J1 : états et températures capturés ; calcul local de cycles distinct des essais utilisateur.','Partiel : pas de cycle complet horodaté à 4 °C dans la série 2.6.'],['V2 — Consigne','Écriture à 6 °C ; seuils 5,5 / 6,5 °C ; température progressive.','Écriture acceptée et relue ; 11:12:54 : lectures à 4,1 °C / consigne 6 °C sur les deux ports. Supervision à consigne 6 °C en 2.5.','Écriture et visibilité établies ; cycle complet vers la nouvelle bande non enregistré.'],['V3 — Porte','Porte ouverte : apport thermique augmenté ; effet dépend du compresseur.','À consigne 6 °C, compresseur arrêté : porte ouverte, 4,8 → 5,4 °C en 25 s ; fermée, 6,0 → 6,3 °C en 25 s.','Effet cohérent ; températures initiales différentes, donc facteur thermique deux non validé quantitativement.'],['V4 — Défaut','Défaut actif : commande arrêtée ; reprise selon température après retrait.','2.6 : défaut 1, compresseur 0, 5,8 → 6,1 °C ; puis défaut 0 et compresseur 1 à 6,3 °C. J1 : OFF à 5 °C / consigne 4 °C.','États cohérents. Bascule marche → arrêt et délai exact non capturés ; essai 2.6 à consigne 6 °C.'],['V5 — Lecture proxy','Lectures autorisées et cohérentes avec le serveur.','PCAP 2554/2564 ; 11:17:17 : deux lectures à 6,3 °C / consigne 6 °C, mêmes états.','Établi pour les chemins testés ; décalage temporel possible entre lectures.'],['V6 — Refus proxy','FC06 refusée, consigne inchangée après tentative.','86 01 dans le PCAP ; 11:17:47 : exception 01 puis relectures à 4 °C, porte fermée, défaut 0 et auto 1.','Refus et état final établis. Aucune segmentation démontrée.']]
y=table(rows,[98,180,285,CW-563],490,8.7)-14
p('<b>Version et temporalité :</b> le fichier de référence utilise ±0,5 °C ; la variante ±1 °C a été explorée en J1. Son empreinte chargée pendant cette série et sa restauration ne sont pas capturées. Le serveur calcule avec un pas nominal de 0,1 s ; les délais TCP ne mesurent pas une réponse thermique.',M,y,CW,9)
c.showPage()
# 6 — Four readable user evidence extracts.
title(6,'Annexe intégrée — Essais fonctionnels','Captures utilisateur 2.6 · Consigne 6 °C pendant porte/défaut, puis restauration finale à 4 °C')
for x,top,time,name,caption in [
(34,491,'11-13-54','V3 — Porte ouverte','Porte 1, défaut 0, auto 1, compresseur arrêté ; 4,8 °C à 11:13:18 → 5,4 °C à 11:13:43.'),
(438,491,'11-14-46','V3 — Porte fermée','Porte 0, compresseur arrêté ; 6,0 °C à 11:14:14 → 6,3 °C à 11:14:39. Conditions initiales différentes.'),
(34,263,'11-16-37','V4 — Défaut actif','Défaut 1, compresseur 0 ; le relevé 5,8 → 6,1 °C ne montre pas la bascule depuis la marche. La supervision seule ne signale pas ce défaut.'),
(438,263,'11-17-47','V6 — Refus et restauration finale','Écriture via 15021 refusée ; deux lectures à consigne 4 °C, porte 0, défaut 0, auto 1. Température 5,8 °C et compresseur 1 : retour thermique progressif.')]:
 p(name,x,top,370,12,True,TEAL);bottom=shot(time,x,top-22,370,145);p(caption,x,min(bottom-9,top-174),370,9)
c.showPage()
# 7 — Limits, reproducibility and J3 readiness.
title(7,'5 — Limites, cohérence et conservation','Préparer J3 sans confondre simulation, filtrage applicatif et sécurité d’une installation réelle')
y=table([['Limite','Conséquence pour une transposition au réel'],['Physique simplifiée','Température unique, coefficients non calibrés ; absence de représentation détaillée des produits, pressions, humidité, dégivrage et consommation.'],['Capteur / actionneur simulés','Pas de câblage, d’étalonnage ni de retour mécanique indépendant. Une commande ON ne prouve pas un refroidissement matériel.'],['Défauts / protections partiels','L’arrêt sur défaut est une hypothèse pédagogique ; les sécurités et toutes les défaillances industrielles ne sont pas modélisées.'],['Temps et synchronisation','Pas de lien actualisé à un équipement réel ; délais du modèle et du réseau ne garantissent pas ceux d’une installation physique.'],['Sécurité du chemin','Modbus conventionnel sans authentification native ; 15020 reste accessible en écriture. Le bastion/pare-feu dessiné reste une proposition.']],[175,CW-175],490,9)-16
y=p('<b>Contrôle de cohérence :</b> composants limités au laboratoire utilisé ; adresses et fonctions vérifiées dans le mapping et le code ; observations rapportées depuis captures et PCAP ; calculs locaux antérieurs clairement distincts. Aucune observation nouvelle n’est inventée par la génération de ce PDF.',M,y,CW,10)-12
y=p('<b>Conservation :</b> PCAP original copié dans livrables/informatique-industrielle/it-1/validation-j2/assemblage-j2.pcap. Captures dans docs/assets/img/informatique-industrielle/it-1/. Conserver programme, sauvegarde initiale et version réellement utilisée dans la VM avant J3.',M,y,CW,9)-10
y=p('<b>SHA-256 du PCAP :</b><br/>02cc2db1c138ec8389a8e79196bfc7ea24a6a21d6dbb9581d269ad190d345988',M,y,CW,8.5)-10
y=p('<b>Sources :</b> README.md, docs/REGISTER_MAP.md, docs/NETWORK.md, lab/model.py, lab/modbus.py, lab/client.py, lab/dashboard.py et lab/gateway.py du PoC ; captures utilisateur des 26–27 octobre 2026 ; PCAP assemblage-j2.pcap. Les références, commandes et limites sont détaillées dans les fiches du mémo.',M,y,CW,9)-10
p('<b>Bilan C2 :</b> mise en œuvre et échanges documentés ; comportements observés avec les réserves de la matrice. Validation collective, cycles complets et version chargée à confirmer. Site de la convention de nommage à confirmer avant remise finale ; aucun visa du formateur n’est prérempli.',M,y,CW,9)
c.save();print(OUT)
