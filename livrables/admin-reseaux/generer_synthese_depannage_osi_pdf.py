"""Fiche formateur synthétique : uniquement les constats et essais documentés."""
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
R=Path(__file__).resolve().parents[2]
OUT=R/'docs/assets/files/admin-reseaux/Synthese-depannage-OSI-Packet-Tracer-Olivier-HIMBLOT.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
CAP=R/'docs/assets/img/admin-reseau/tppackettracer'
for name,f in [('Lato','Lato-Regular.ttf'),('LatoBold','Lato-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/lato/'+f))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold')
INK=HexColor('#18354c');TEAL=HexColor('#00695c');LINE=HexColor('#c7d4df');W,H=A4;M=36;AW=W-2*M
st={k:ParagraphStyle(k,fontName='LatoBold' if k in ('title','head') else 'Lato',fontSize=sz,leading=ld,textColor=TEAL if k=='head' else INK,spaceAfter=gap) for k,sz,ld,gap in [('title',18,22,10),('head',11,14,7),('body',9.4,12.5,7),('small',7.8,10,6),('cell',8.1,10.4,0)]}
story=[]
def p(t,k='body'):story.append(Paragraph(t,st[k]))
def head(t):p(t,'head')
def table(rows,weights):
    data=[[Paragraph(c,st['cell']) for c in row] for row in rows]
    t=Table(data,colWidths=[AW*x/sum(weights) for x in weights],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#edf6f3')),('GRID',(0,0),(-1,-1),.35,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.extend([t,Spacer(1,9)])
def chrome(c,d):
    c.saveState();c.setFillColor(INK);c.setFont('LatoBold',9);c.drawString(M,H-25,'AIS · ADMINISTRATION DES RÉSEAUX · PREUVE L5 / RES-01a')
    c.setFont('Lato',8);c.drawString(M,21,'Olivier HIMBLOT · 2 novembre 2026 · Laboratoire Packet Tracer');c.drawRightString(W-M,21,f'Page {d.page}');c.restoreState()
def img(t,maxw,maxh):
    f=CAP/f'Capture d’écran du 2026-11-02 {t}.png'
    with PILImage.open(f) as im:w,h=im.size
    k=min(maxw/w,maxh/h);return Image(str(f),width=w*k,height=h*k,hAlign='CENTER')
p('Fiche de dépannage réseau','title')
p('<b>Compétence :</b> Diagnostiquer une panne réseau par démarche descendante OSI et produire une fiche structurée.')
p('<b>Critères :</b> démarche par couches · hypothèse avant chaque test · cause identifiée · correctif validé · fiche complète. <b>Restitution :</b> présenter la fiche et expliquer le raisonnement pour la panne traitée. La décision de validation appartient au formateur.','small')
head('1 — Symptôme, périmètre et état final')
p('<b>Symptôme fourni :</b> Laptop4 et Laptop5, sur le site principal, n’accèdent pas à <b>https://tracer.co</b>. L’investigation et les manipulations ont été réalisées par l’apprenant dans le projet fourni ; l’analyse repose sur les captures transmises. Les hypothèses de test ont été proposées avant leur exécution, dans l’accompagnement.')
p('<b>État final observé :</b> les deux laptops identifiés affichent la page HTTPS. Une nouvelle capture identifie explicitement Laptop4 ; PC2 affiche également la page après correction. Les premiers échecs et les réserves de preuve sont conservés.')
head('2 — Cartographie utile au diagnostic')
table([['<b>Équipement / liaison</b>','<b>Paramètres relevés et sources</b>'],['Laptop4 / Laptop5 → ASW4','Ports Fa0/13 / Fa0/20, VLAN 999 MANAGEMENT (ports déclarés, tables ASW4). Initial : Laptop4 10.99.0.10/24 en DHCP ; Laptop5 10.0.99.10/24 statique.'],['ASW4 → DSW1 → DR1','Po4 transporte le VLAN 999. DSW1 Vlan999 = 10.99.0.1/24 ; Gi0/1 = 172.16.0.129/28. DR1 Fa0/0 = 172.16.0.142/28 ; prochain saut DSW1 confirmé par ping.'],['DR1 → R0 → WAN','DR1 Fa0/1 = 9.9.9.1/30, défaut via 9.9.9.2 (R0). R0 apprend le réseau DNS 9.9.9.8/30 par OSPF ; pas de route de retour interne ni défaut dans son relevé.'],['Services','SRV-DHCP 10.30.0.10/24 ; SRV-TFTP 10.30.0.11/24, tous deux derrière ASW4 en VLAN 30. SRV-DNS 9.9.9.10/30, passerelle 9.9.9.9 ; service On, enregistrement tracer.co → 9.9.9.34.']],[1,2.3])
head('3 — Trois défauts identifiés')
table([['<b>Défaut précis</b>','<b>Lien avec le symptôme</b>'],['C01 — Sélection NAT incomplète sur DR1','ACL 1 utilisée pour PAT : réseaux 10.10/10.20/10.30 autorisés, pas 10.99.0.0/24. Les paquets du VLAN 999 restent non traduits ; R0 ne dispose pas du retour vers ces sources.'],['C02 — DNS erroné dans POOL-ROUGE','DNS annoncé : 9.9.9.1 (interface WAN DR1), au lieu du serveur observé 9.9.9.10. Le client Laptop4 reçoit cette mauvaise option.'],['C03 — Adressage statique incohérent de Laptop5','10.0.99.10/24 et passerelle 10.0.99.1, alors que son VLAN utilise 10.99.0.0/24 et la passerelle DSW1 10.99.0.1.']],[1,2.3])
p('Cartographie du chemin examiné, pas inventaire exhaustif de toute la topologie. L’IP de la cible web est corroborée par DNS et le service rendu ; son écran IP n’a pas été relevé directement.','small')
story.append(PageBreak())
p('Journal de diagnostic — hypothèses puis tests','title')
p('Le point de départ est l’application (L7). L’échec de sa dépendance DNS conduit à isoler le transport et l’acheminement, puis à examiner les paramètres réseau. Les relevés physiques/VLAN avaient été collectés lors de la cartographie. Les références ci-dessous reprennent les heures des noms de captures, pas un horodatage certifié des commandes.','small')
rows=[['<b>Couche / hypothèse préalable</b>','<b>Test ou lecture</b>','<b>Observation → conclusion</b>'],
['L7 — Les clients présentent le symptôme annoncé.','Navigateur, https://tracer.co, sur les deux laptops.','Page vide déclarée sur les deux ; capture commune 10:47:04. Aucun message explicitant la cause.'],
['L7 — Le DNS configuré résout le nom.','nslookup tracer.co, Laptop4 puis Laptop5.','Timeout vers 9.9.9.1 et vers 9.9.9.10. Deux destinations différentes ; ne pas conclure à un serveur globalement arrêté.'],
['L7 — Le DNS réel répond depuis Laptop4.','nslookup tracer.co 9.9.9.10','Timeout également (11:04:56). Le mauvais résolveur configuré ne suffit pas à expliquer tout l’échec.'],
['L3 — La passerelle locale répond.','Laptop4 : ping 10.99.0.1','4/4 réponses (11:09:46). Poste non totalement isolé.'],
['L3 — Le DNS est joignable en ICMP.','Laptop4 : ping 9.9.9.10','0/4 réponse (11:09:46). Continuer au-delà du segment local.'],
['L3 — DSW1 possède une route vers le DNS.','DSW1 : show ip route','Défaut via 172.16.0.142 (11:11:56). Route candidate présente ; chemin non encore validé.'],
['L3 — DSW1 atteint le DNS.','DSW1 : ping 9.9.9.10','0/5 réponse (11:11:56). L’échec ne touche pas uniquement Laptop4.'],
['L3 — Le prochain saut de DSW1 répond.','DSW1 : ping 172.16.0.142','5/5 réponses (11:14:10). Vérifier ensuite le voisin et son routage.'],
['L3 — DR1 possède l’adresse attendue.','DR1 : show ip interface brief','Fa0/0 = 172.16.0.142 et Fa0/1 = 9.9.9.1, up/up (11:15:37).'],
['L3 — DR1 a une route vers le DNS.','DR1 : show ip route','Défaut via 9.9.9.2 ; retour 10/8 via DSW1 (11:15:37).'],
['L3 — Le prochain saut WAN répond depuis DR1.','DR1 : ping 9.9.9.2','5/5 réponses (11:23:17). Le lien WAN fonctionne pour cet essai.'],
['L3 — DR1 lui-même atteint le DNS.','DR1 : ping 9.9.9.10','5/5 réponses (11:23:17). Différence selon l’origine ; examiner retour et traitement de transit.'],
['L3 — R0 a les routes de retour internes.','R0 : show ip route','Ni route interne ni défaut (11:26:26). Les sources internes non traduites n’ont pas de retour dans ce relevé.'],
['L3 — DR1 traite différemment les sources internes.','DR1 : show running-config','PAT via ACL 1 ; réseau 10.99 absent. Défaut précis identifié, puis correction ciblée et recette.']]
table(rows,[1.05,1,1.35])
p('<b>Écart conservé :</b> les essais de 11:21:16 ont été lancés sur DSW1 au lieu de DR1, puis refaits sur DR1 ; ils ne sont pas attribués au mauvais équipement. Les commandes de consultation rejetées pour syntaxe ne sont pas des correctifs.','small')
story.append(PageBreak())
p('Corrections, validation et couverture OSI','title')
head('4 — Corrections appliquées séparément')
table([['<b>Correction et état initial</b>','<b>Action exacte</b>','<b>Validation après action</b>'],['C01 — 10.99 absent de l’ACL de sélection PAT.','DR1 : configure terminal<br/>access-list 1 permit 10.99.0.0 0.0.0.255<br/>end<br/>show access-lists 1','Hypothèses : le ping et le DNS réel répondent ; une traduction est créée. Laptop4 : ping 9.9.9.10 = 4/4 ; nslookup tracer.co 9.9.9.10 = 9.9.9.34. show ip nat translations : UDP 10.99.0.10:1030 → 9.9.9.1:1030, DNS :53.'],['C02 — POOL-ROUGE annonce DNS 9.9.9.1.','SRV-DHCP → Services → DHCP → POOL-ROUGE : DNS Server 9.9.9.10 → Save.<br/>Laptop4 : ipconfig /renew','Hypothèses : le DNS reçu résout le nom ; HTTPS fonctionne. Bail : IP 10.99.0.10/24, GW 10.99.0.1, DNS 9.9.9.10. nslookup tracer.co réussi, puis page HTTPS affichée.'],['C03 — Laptop5 statique hors du réseau de son VLAN.','Laptop5 → Desktop → IP Configuration → DHCP.','Hypothèse : les paramètres DHCP cohérents rétablissent l’accès. Bail reçu 10.99.0.11/24, GW 10.99.0.1, DNS 9.9.9.10. Ping passerelle 4/4 et DNS réussis après répétition, puis HTTPS affiché.']],[1,1.25,1.65])
p('<b>État initial préservé :</b> captures et projet original conservés. Les commandes NAT existantes ne sont pas supprimées ; seul le réseau manquant est ajouté. Le mode DHCP de Laptop5 corrige adresse et passerelle ensemble. Retours arrière possibles : retirer la seule entrée ACL ajoutée, restaurer l’option DNS initiale du pool, rétablir les paramètres statiques initiaux ; ces retours arrière n’ont pas été exécutés.','small')
head('5 — Lecture descendante des couches et limites des preuves')
table([['<b>Couche</b>','<b>Contrôle réellement disponible / résultat</b>'],['L7 — Application','Navigateur HTTPS et DNS : échecs initiaux puis résolution et contenu web après correction.'],['L6 — Présentation','Contenu HTTPS rendu dans le simulateur ; aucune vérification indépendante de chiffrement ou certificat.'],['L5 — Session','Échange applicatif abouti ; aucune observation séparée d’un mécanisme de session.'],['L4 — Transport','Traduction UDP/53 observée et réponse DNS reçue. Pas de capture détaillée TCP/443.'],['L3 — Réseau','Adresses, passerelles, routes, ICMP et NAT/PAT comparés ; causes précises et correctifs étayés.'],['L2 — Liaison','Ports/VLAN et trunks relevés sur ASW4 ; chemin local fonctionnel. Pas de trace ARP dédiée.'],['L1 — Physique','Interfaces up/up et liens simulés actifs. Aucun test matériel de câble.']],[.8,3.2])
p('<b>Point à expliquer à l’oral :</b> la démarche commence par L7 puis recherche la dépendance défaillante vers les couches inférieures ; elle ne démontre pas une série de sept tests indépendants dans un ordre strict. Les couches non observées séparément restent signalées. Un ping ne valide pas HTTPS, et un timeout seul ne désigne pas une cause.','small')
p('<b>Incidents de test :</b> Laptop5 présente d’abord des timeouts DNS et 0/4 au ping, puis 4/4 et une réponse DNS après répétition. Leur cause transitoire n’est pas démontrée ; aucune attribution automatique à ARP/STP. La commande « clear » rejetée n’a pas corrigé le réseau.','small')
story.append(PageBreak())
p('Preuves finales et restitution au formateur','title')
p('<b>Résultat :</b> accès à https://tracer.co affiché sur Laptop4 et Laptop5 identifiés ; contrôle positif sur PC2 après corrections. Aucun test initial sur PC2 n’est fourni : ce contrôle ne constitue pas une mesure avant/après exhaustive.')
# Deux preuves nommées, puis la preuve de la séquence du second poste.
imgs=[[img('11-48-27',AW/2-8,235),img('11-48-58',AW/2-8,235)],[Paragraph('<b>Laptop4 identifié</b> — 11:48:27',st['small']),Paragraph('<b>PC2 identifié</b> — 11:48:58',st['small'])]]
t=Table(imgs,colWidths=[AW/2,AW/2]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]));story.extend([t,Spacer(1,8)])
# Afficher le navigateur Laptop5 en format contenu, en explicitant le cadrage.
story.append(img('11-44-20',AW,195))
p('<b>Laptop5 identifié</b> — page HTTPS 11:44:20. Les captures 11:43:28 (DHCP) et 11:43:59 (CLI) complètent la preuve du rétablissement.','small')
head('6 — Synthèse orale et pièces conservées')
p('« J’ai commencé par l’application et le DNS. Le poste atteignait sa passerelle mais pas le DNS distant. DR1 atteignait le DNS : j’ai comparé le routage et la sélection NAT. Après ajout ciblé du réseau client au PAT, j’ai validé ICMP et DNS explicite. J’ai ensuite corrigé le DNS DHCP, puis l’adressage de Laptop5. J’ai enfin retesté le service HTTPS initial sur les deux séquences et contrôlé un autre poste. »','small')
p('<b>Pièces :</b> Fiche-depannage-TP-Diagnostic.md (journal détaillé et captures), TP Diagnostic.pdf (consigne), TP Diagnostic.pkt (original), TP Diagnostic corrigé.pkt (sauvegarde reçue), Inventaire-preuves-TP-Diagnostic.json (empreintes). Captures datées du 2 novembre 2026 ; les heures des noms de fichiers ne certifient pas l’heure exacte des tests. Deux originaux contenant des paramètres d’authentification sont conservés hors publication.','small')
p('<b>Réserves avant validation :</b> cartographie exhaustive des autres équipements et configuration directe du serveur HTTPS encore à compléter selon la consigne ; sauvegarde corrigée non réouverte ici. Le PDF résume les travaux réellement documentés et n’atteste pas des contrôles absents.','small')
SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=45,bottomMargin=38,title='Diagnostiquer une panne réseau — Fiche structurée OSI',author='Olivier HIMBLOT',subject='Défauts NAT, DNS DHCP et adressage ; tests avant et après correction').build(story,onFirstPage=chrome,onLaterPages=chrome)
print(OUT)
