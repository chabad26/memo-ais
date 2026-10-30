"""Synthèse autonome de deux pages : connexion de maintenance et réponse OT."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-4/J5-synthese-connexion-maintenance-Olivier-HIMBLOT.pdf'
for name,file in [('Lato','Lato-Regular.ttf'),('LatoBold','Lato-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/lato/'+file))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold')
ink=HexColor('#18354c'); teal=HexColor('#00695c'); pale=HexColor('#edf6f3')
styles={k:ParagraphStyle(k,fontName='LatoBold' if k in ('title','head') else 'Lato',fontSize=size,leading=lead,textColor=teal if k=='head' else ink,spaceAfter=gap) for k,size,lead,gap in [('title',20,24,12),('head',12,16,8),('body',10,14,8),('small',8,11,7),('cell',9,12,0)]}
story=[]
def p(text,kind='body'): story.append(Paragraph(text,styles[kind]))
def h(text): p(text,'head')
def table(rows,widths):
    data=[[Paragraph(c,styles['cell']) for c in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),pale),('GRID',(0,0),(-1,-1),.4,HexColor('#c7d4df')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.extend([t,Spacer(1,12)])
def chrome(c,d):
    w,hh=A4;c.setFillColor(ink);c.setFont('LatoBold',9);c.drawString(40,hh-28,'AIS · J5 · INVESTIGATION ET REMÉDIATION OT')
    c.setFont('Lato',8);c.drawString(40,24,'Olivier HIMBLOT · 30 octobre 2026 · Scénario pédagogique fictif');c.drawRightString(w-40,24,f'{d.page} / 2')
p('Connexion externe et maintenance partagée','title')
p('Montval · ZF-02 / REG-02 — Complément au compte-rendu J5','head')
p('<b>Constat :</b> une session VPN utilise le compte partagé <b>maint-shared</b> depuis une adresse externe. Pendant cette fenêtre, MAINT-01 écrit une consigne de <b>12 °C</b> sur REG-02. Le rapprochement justifie une investigation, mais <b>n’identifie pas la personne ayant envoyé la commande</b>.')
h('Les traces disponibles')
table([['<b>Trace</b>','<b>Fait établi dans les sources du scénario</b>'],['VPN','Source <b>203.30.113.77</b>, compte <b>maint-shared</b>, cible <b>MAINT-01</b>. Session corrigée : <b>09:12–09:19</b> le 8 octobre 2026. Heures brutes : 09:14:10–09:21:10 ; horloge VPN en avance de 2 min 10 s.'],['Commande Modbus','À <b>09:14</b>, trames 9/10 : <b>10.30.20.15:41002 → 10.30.10.22:502</b>. FC06, registre PDU 0, valeur <b>120 = 12 °C</b>. Réponse normale du régulateur à +30 ms.'],['Exploitation','SUP et mesures corroborent le changement et la hausse de température. Alarme à <b>09:52</b>. Retour à 4 °C autorisé à 10:18, documenté à <b>10:21</b>.'],['Autorisation','FM-426 connu couvre <b>08:30–09:00</b>. Aucun ticket n’est fourni pour la session de 09:12 ; FrigoMaint ne déclare pas de changement à 12 °C. Cela ne prouve pas l’absence exhaustive de toute autorisation.']],[100,415])
h('Qui a utilisé l’accès ?')
p('Le <b>compte</b> est connu, l’<b>auteur humain reste inconnu</b>. Le technicien A est déclaré pour la session précédente ; le compte partagé ne permet pas de lui attribuer la suivante. Erreur, automatisation, usage abusif d’un accès légitime ou compromission restent à départager.')
p('L’IP externe désigne la source enregistrée par le VPN, éventuellement une sortie partagée ou un relais. Le PCAP montre ensuite <b>MAINT-01 → REG-02</b> : il ne démontre ni accès direct du régulateur depuis Internet, ni lien causal certain avec la session VPN. Aucun pays, opérateur ou propriétaire n’est attribué à cette IP.')
p('<b>Pièces :</b> acces_distants_VPN.csv (lignes 4–5), modbus_REG02_capture.pcap (trames 9/10), evenements_SUP01.csv, températures ZF-02, maintenance_FrigoMaint.csv et inventaire des horloges. PCAP synthétique partiel : 18 trames ; quantités FC03 incohérentes, signalées dans le rapport complet.','small')
story.append(PageBreak())
p('Agir maintenant, puis corriger durablement','title')
p('<b>Statut :</b> propositions pour Montval, à coordonner avec exploitation, maintenance, IT et FrigoMaint. Aucune suspension de VPN ni intervention sur une installation réelle n’est attestée ici.','small')
h('À l’instant T — préserver le froid, les preuves et les accès utiles')
for text in [
'<b>1. Vérifier le processus.</b> Lire consigne, température, alarmes et état du groupe ; prévoir une mesure indépendante et une surveillance sur place. L’exploitation décide des lots et de la poursuite d’activité.',
'<b>2. Conserver les traces en parallèle.</b> Exporter VPN, authentification, SUP, pare-feu, tickets et configurations ; conserver originaux, empreintes, fuseaux et écarts d’horloge. Préserver les traces volatiles utiles de MAINT-01 si compatible avec l’urgence. Éviter nettoyage et redémarrage par défaut.',
'<b>3. Contenir l’accès suspect.</b> Vérifier les sessions actives, fermer celles concernées et suspendre le compte partagé sur décision coordonnée. La session documentée finit à 09:19 : elle ne peut pas être coupée rétroactivement. Désactiver un compte ne ferme pas toujours une session déjà ouverte ; bloquer une seule IP ne suffit pas.',
'<b>4. Maîtriser la maintenance.</b> Restreindre MAINT-01 si nécessaire sans couper indistinctement la supervision. Prévoir un accès alternatif autorisé ; renouveler les secrets concernés depuis un environnement de confiance, sans les exposer au poste suspect.',
'<b>5. Restaurer et vérifier.</b> Corriger la consigne avec autorisation, tracer avant/après et suivre le refroidissement. Le retour à 4 °C est déjà documenté à 10:21. Vérifier aussi lectures, supervision et accès utiles ; la baisse de température ne clôt pas seule l’incident.'
]: p(text)
h('Ensuite — lever les incertitudes et réduire la récidive')
for text in [
'<b>Relier session et commande :</b> demander identifiants de session VPN, IP du tunnel, traces d’accès au poste, processus/outils et connexions sortantes. Recouper avec les intervenants, IP de sortie et tickets FrigoMaint ; vérifier l’intégrité de MAINT-01.',
'<b>Individualiser et limiter :</b> comptes nominatifs, MFA, accès temporaires liés à un ticket, VPN puis bastion en DMZ industrielle ; consultation séparée des modifications et procédure d’urgence tracée. Tester expiration et révocation.',
'<b>Surveiller et pérenniser :</b> centraliser journaux et horodatage, alerter sur écritures ou connexions hors fenêtre, qualifier le contrôle Modbus et préparer le remplacement de REG-02. Ces mesures ne corrigent pas ses défauts internes.'
]: p(text)
p('<b>Limite des essais :</b> C01 journalise les refus IT directs du PoC ; elle ne démontre pas la détection d’une écriture depuis une origine autorisée. La conformité des produits et la remise en service relèvent de l’exploitation avec les spécialistes concernés.','small')
SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=48,bottomMargin=40,title='J5 — Connexion externe et maintenance partagée',author='Olivier HIMBLOT').build(story,onFirstPage=chrome,onLaterPages=chrome)
print(OUT)
