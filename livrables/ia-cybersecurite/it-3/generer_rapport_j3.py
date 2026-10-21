"""Générer le rapport formateur J3 à partir des livrables locaux et captures."""
from pathlib import Path
from html import escape
import hashlib
import json
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
KIT = BASE / 'ia01-j3'
OUT = BASE / 'Entrainement-modele-SSH-Hexalp-Olivier-HIMBLOT.pdf'
IMG = ROOT / 'docs/assets/img/ia-cybersecurite/it-3'
for name, file in [('Lato', 'Lato-Regular.ttf'), ('LatoBold', 'Lato-Bold.ttf'), ('LatoItalic', 'Lato-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/lato/' + file))
pdfmetrics.registerFontFamily('Lato', normal='Lato', bold='LatoBold', italic='LatoItalic', boldItalic='LatoBold')
NAVY = colors.HexColor('#17324d')
TEAL = colors.HexColor('#087e8b')
PALE = colors.HexColor('#edf5f7')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyIA', fontName='Lato', fontSize=10, leading=14, spaceAfter=8))
styles.add(ParagraphStyle(name='CellIA', fontName='Lato', fontSize=9, leading=12))
styles.add(ParagraphStyle(name='HeadCellIA', parent=styles['CellIA'], fontName='LatoBold', textColor=colors.white))
styles.add(ParagraphStyle(name='SmallIA', fontName='Lato', fontSize=8, leading=11, textColor=NAVY, spaceAfter=7))
styles.add(ParagraphStyle(name='CodeIA', fontName='Courier', fontSize=7.2, leading=9.0))
for name in ['Title', 'Heading1', 'Heading2']:
    styles[name].fontName = 'LatoBold'
    styles[name].textColor = NAVY
styles['Title'].fontSize = 25
styles['Title'].leading = 31
styles['Heading1'].fontSize = 18
styles['Heading1'].leading = 23
styles['Heading2'].fontSize = 13
styles['Heading2'].leading = 17
story = []
def para(text, style='BodyIA'):
    text = escape(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    return Paragraph(text, styles[style])
def p(text, style='BodyIA'):
    story.append(para(text, style))
def h(text): p(text, 'Heading1')
def sub(text): p(text, 'Heading2')
def page(): story.append(PageBreak())
def table(rows, widths):
    data = [[para(str(c), 'HeadCellIA' if i == 0 else 'CellIA') for c in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [PALE, colors.white]), ('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),7), ('RIGHTPADDING',(0,0),(-1,-1),7), ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t); story.append(Spacer(1,12))
def capture(time, max_height):
    im = Image(str(IMG / f'Capture d’écran du 2026-10-21 {time}.png'))
    factor = min(511 / im.imageWidth, max_height / im.imageHeight)
    im.drawWidth = im.imageWidth * factor; im.drawHeight = im.imageHeight * factor
    story.append(im); story.append(Spacer(1,8))

story.append(Spacer(1,28))
p('IA ET CYBERSÉCURITÉ • ITÉRATION 3', 'SmallIA')
p('Entraîner un modèle simple à partir de journaux d’infrastructure', 'Title')
p('Détection SSH chez Hexalp', 'Heading1')
p('Preuve de travail destinée au formateur\nOlivier HIMBLOT • 21 octobre 2026')
sub('Critère évalué')
p('Un modèle Scikit-learn est entraîné de façon reproductible sur des journaux préparés et des caractéristiques justifiées, via un script commenté.')
sub('Preuves présentées')
p('Script detection_ssh.py et requirements.txt ; CSV d’alertes ; fiche du modèle ; résultats des notebooks observés en captures. Le code complet du script figure en annexe.')
sub('Périmètre établi')
p('Données fictives du bastion Hexalp. Captures de travail de l’apprenant dans Jupyter et exécution du script dans sa VM à graine 7. Vérification séparée par l’assistant à graines 42 et 7, dont deux exécutions identiques à 42. Le script a été rédigé avec assistance : commentaires à relire et expliquer personnellement.')
sub('Pièces à compléter avant remise')
notebooks = []
for name in ['00_python_survie.ipynb','01_detection_ssh.ipynb']:
    obj = json.loads((KIT/name).read_text())
    code = [c for c in obj['cells'] if c['cell_type'] == 'code']
    counts = sum(c.get('execution_count') is not None for c in code)
    notebooks.append((name, counts, len(code)))
for name, counts, total in notebooks:
    p(f'{name} : fichier local contrôlé, {counts}/{total} cellules de code avec compteur d’exécution. Les captures attestent des résultats, mais ne remplacent pas le notebook complet sauvegardé.', 'SmallIA')
p('Les deux notebooks complétés et exécutés de la VM sont à rapatrier. Aucune exécution de tous les notebooks n’est revendiquée à partir des seuls originaux. Aucun déploiement hebdomadaire ni blocage automatique n’est réalisé.')

page(); h('1. Critère, livrables et préparation')
table([
 ['Attendu du critère','Travail fourni et portée de la preuve'],
 ['Journaux préparés','CSV fictif inspecté ; valeurs manquantes localisées ; retrait documenté, sans assimiler absence de mesure à zéro.'],
 ['Caractéristiques justifiées','Sept variables de comportement ; étiquette exclue de X, contrôle fail2ban réservé à la comparaison ; date/IP conservées pour l’analyste.'],
 ['Modèle entraîné','Captures fit et matrice du notebook ; script complet relançable. Arbre profondeur 3 et Isolation Forest sans y.'],
 ['Reproductibilité','Deux exécutions à 42 identiques dans l’environnement de vérification ; essai distinct à 7. Versions et empreintes conservées.'],
 ['Preuve de travail','Script, requirements, CSV de 111 alertes et fiche modèle disponibles. Notebooks exécutés complets de la VM à récupérer.'],
], [119,392])
sub('Données et nettoyage')
p('Source : hexalp_ssh_sept2026.csv, 14–27 septembre 2026. Une ligne résume une IP pendant une heure. Brut : 1 704 observations, 11 colonnes, 117 attaques (6,87 %). Les étiquettes sont attribuées à Hugo dans le scénario.')
p('90 volumes sont absents pendant deux pannes NetFlow : 19 septembre, tranches 0–11 h (20 lignes), et 22 septembre, 10–15 h (70 lignes). Retrait de ces 90 lignes, dont 9 attaques ; restent 1 614 observations et 108 attaques (6,69 %). Ces lignes restent hors couverture : ce choix ne résout pas la panne de collecte.')
sub('Variables d’entrée et exclusions')
p('Retenues : heure, externe (origine validée puis codée 0/1), echecs_auth, succes_auth, comptes_distincts, duree_session_min, octets_sortants_mo. Elles décrivent l’activité de la tranche terminée ; elles ne permettent pas de prétendre détecter avant la fin de cette tranche.')
p('Exclues : etiquette, réponse réservée à l’apprentissage supervisé/évaluation ; fail2ban_ban, pour éviter de recopier un contrôle qu’on compare ; ip_source et date, pour limiter la mémorisation dans ce premier modèle. La date et l’IP restent dans les alertes pour les retrouver.')

page(); h('2. Entraînement et résultats')
p('Séparation stratifiée à graine 42 : 1 129 lignes d’entraînement (76 attaques) et 485 de test (32 attaques). Une attaque de plus ou de moins modifie le rappel de 3,125 points sur ce test.')
table([
 ['Périmètre','FP','FN','VP','Précision','Rappel'],
 ['Arbre, test 485','0','4','28','100 %','87,50 %'],
 ['fail2ban, même test','0','15','17','100 %','53,125 %'],
 ['Isolation Forest, ajustement 1 614','5','64','44','89,80 %','40,74 %'],
 ['Union, descriptive sur tout X','5','2','106','95,50 %','98,15 %'],
], [196,35,35,35,105,105])
p('Les deux dernières lignes utilisent le jeu d’ajustement d’Isolation Forest ; l’union inclut les données d’entraînement de l’arbre. Elles ne constituent pas un résultat de généralisation comparable directement au test supervisé.', 'SmallIA')
sub('Lecture de l’arbre : explicable mais fragile')
p('Profondeur 3, six feuilles. Avec au plus trois comptes : durée ≤0,5 minute ou >64 minutes → attaque ; sinon normal. À partir de quatre comptes : externe → attaque ; interne → attaque jusqu’à 19 h, normal dès 20 h. Le seuil horaire interne est un raccourci appris, pas une autorisation métier.')
p('Les quatre attaques manquées ont un seul compte et des sessions de 24 à 57 minutes. Cet arbre ne teste directement ni le volume sortant ni les échecs, malgré leur présence dans les variables proposées.')
sub('Anomalies : classement utile, coût de détection')
p('À contamination 0,03 : 49 signalées, dont 44 attaques de référence et 5 normales — scanner 3, sauvegarde 2. Le top 15 est entièrement étiqueté attaque ; les qualifications analyste écrites avant révélation ne sont pas montrées. Les trois lignes SSH de Julien pendant l’incident WMS ne sont pas signalées ; le CSV ne contient pas les données envoyées à son chatbot.')
table([['Contamination','Alertes / 2 sem.','VP','FP','FN'],['0,03','49','44','5','64'],['0,05','81','64','17','44'],['0,10','162','104','58','4']], [116,160,78,78,79])
p('Choisir après comparaison sur le même jeu fragilise une évaluation finale : prévoir un nouveau test temporel et suivre les pratiques qui changent.')

page(); h('3. Script reproductible et charge réelle')
sub('Chaîne du script')
p('Paramètres regroupés ; chemins relatifs au fichier du script ; contrôles de schéma et de valeurs ; nettoyage ; construction X/y ; partage ; entraînement et évaluation ; export des lignes anomalie OU avis_arbre=1. Le CSV est trié de manière déterministe. Le code ne réalise ni appel réseau, ni ban, ni modification de compte.')
sub('Essais effectués par l’assistant, distincts de la VM')
p('Venv temporaire Linux/x86_64, Python 3.14.4, pandas 3.0.6, scikit-learn 1.9.1, matplotlib 3.11.2, JupyterLab 4.6.4, NumPy 2.5.4 et SciPy 1.18.1. Les versions directes du kit sont respectées ; pip check : aucune incompatibilité signalée. Les dépendances transitives sont relevées, pas protégées par un fichier de hachages approuvé.')
p('Deux exécutions à graine 42 : console et CSV identiques octet par octet. Essai à graine 7 dans un autre fichier : règles différentes malgré 0 FP et 4 FN également pour l’arbre sur son nouveau test ; IF : 4 FP/63 FN/45 VP. Les exports ont 107 observations communes, 4 propres à 42 et 1 propre à 7.')
sub('Empreinte du CSV final à graine 42')
p(hashlib.sha256((KIT/'alertes_a_qualifier.csv').read_bytes()).hexdigest(), 'SmallIA')
sub('L’union dépasse le budget de 30 alertes/semaine')
table([['Semaine','IF seules, graine42','Union42 exportée','Union7'],['14–20 septembre','20','45','44'],['21–27 septembre','29','66','64']], [161,132,132,86])
p('Le CSV final contient 111 lignes, plus l’en-tête. La file union moyenne est 55,5/semaine, pas 24,5. Diminuer la contamination ne supprime pas les alertes de l’arbre seul. Aucun plafond caché n’a été appliqué. Une file IF seule respecterait ici la capacité, mais manquerait 64 attaques : arbitrage RSSI requis, pas acceptation automatique.')
p('Avant exploitation : évaluer regroupement, priorités et détection sur données indépendantes ; séparer entraînement validé et prédiction sans étiquettes ; versionner le modèle ; superviser qualité de collecte, dérive, tâche planifiée et file analyste. Aucun cron n’a été créé.')

page(); h('4. Fiche du modèle — Prototype J3')
table([
 ['Rubrique','Fiche synthétique — 21 octobre 2026'],
 ['Données','Bastion Hexalp fictif, 14–27/09/2026 ; 1 704 lignes, 117 attaques (6,87 %). Après nettoyage : 1 614 lignes, 108 attaques (6,69 %).'],
 ['Préparation','90 volumes manquants retirés, dont neuf attaques ; hors couverture explicite. Origine vérifiée puis codée interne0/externe1. Aucun volume inconnu remplacé par zéro.'],
 ['Caractéristiques','Heure, externe, échecs, succès, comptes, durée et volume. Exclusions : étiquette (réponse), fail2ban (indépendance), date/IP (mémorisation). Identifiants conservés pour l’analyste.'],
 ['Modèles et réglages','DecisionTreeClassifier max_depth=3, test stratifié30 % ; IsolationForest contamination=0,03, sans y, sur tout X ; graine42. Export union.'],
 ['Résultats','Arbre test : 0FP/4FN, précision100 %, rappel87,5 %. IF ajustement : 5FP/64FN, précision89,80 %, rappel40,74 %. Union descriptive : 5FP/2FN ; 111 alertes, 45 puis66/semaine ; dépassement du budget.'],
 ['Limites','90 lignes hors couverture ; pas de contenu web dans les agrégats SSH ; branche interne fragile ; audits/sauvegardes atypiques ; test réutilisé pour réglages ; IF/union non évalués sur données nouvelles ; dérive possible.'],
 ['Conditions d’utilisation','Analyste SOC/astreinte qualifie ; Nadia arbitre charge et risques. Aucun blocage. Réévaluer avant production et après changement des données, règles ou usages ; conserver modèle, paramètres, versions, preuves et retour arrière.'],
], [119,392])
sub('Statut de remise des fichiers')
p('Disponibles dans ia01-j3 : detection_ssh.py, requirements.txt, alertes_a_qualifier.csv, carnet_J3.md et preuves de vérification. À joindre après récupération : les deux notebooks complets sauvegardés depuis la VM. L’évaluation finale appartient au formateur ; ce document ne la présume pas.')

page(); h('5. Preuve visuelle — Notebook supervisé')
capture('10-48-58', 220)
p('Capture apprenant 10:48:58 : nettoyage, partage 1 129/485, entraînement profondeur3 et accuracy0,992.', 'SmallIA')
capture('10-49-21', 390)
p('Capture apprenant 10:49:21 : matrice 453VN/0FP/4FN/28VP et rapport sur 32 attaques. Les résultats ne prouvent ni exécution complète ni sauvegarde du notebook dans les fichiers remis.', 'SmallIA')

page(); h('6. Preuve visuelle — Exécution dans la VM')
capture('11-20-40', 460)
p('Capture 11:20:40 : commande à graine7 dans le venv Debian ; préparation, règles et rapports. Résultats visibles concordants avec l’essai séparé de l’assistant.', 'SmallIA')
capture('11-20-55', 166)
p('Capture 11:20:55 : 44 puis64 alertes/semaine, avertissement budget et retour au prompt. Pas de preuve par ces captures de deux relances42 dans la VM ou d’identité des CSV entre machines.', 'SmallIA')

page(); h('Annexe — Script commenté complet')
p('Version fournie dans ia01-j3/detection_ssh.py. Code rédigé avec assistance ; l’apprenant doit pouvoir expliquer les choix. Squelette d’origine conservé. Les seuls effets sont lecture du CSV, calculs, affichage et écriture du CSV demandé.', 'SmallIA')
source=(KIT/'detection_ssh.py').read_text()
# Keep exact source lines without wrapping into invalid Python; long lines split visually only.
import textwrap
visual=[]
for i,line in enumerate(source.splitlines(),1):
    chunks=textwrap.wrap(line, width=103, replace_whitespace=False, drop_whitespace=False) or ['']
    visual.append(f'{i:03d} '+chunks[0])
    visual.extend('    '+c for c in chunks[1:])
story.append(Preformatted('\n'.join(visual), styles['CodeIA']))
page(); h('Références et pièces de preuve')
p('Pièces du dossier : kit fictif fourni, captures du 21 octobre et essais séparés de l’assistant. Référence technique : Scikit-learn, guide utilisateur, documentation consultée le 21 octobre 2026 : https://scikit-learn.org/stable/user_guide.html')
p('Répertoire de preuves : ia01-j3/preuves/ — verification_script.md, execution_graine42.txt, execution_graine7.txt, alertes_graine7.csv, dependances_verification.txt. Les lignes de sortie et hachages servent au rapprochement ; pas d’entraînement supplémentaire pendant la génération du PDF.')
table([['Fichier','SHA-256']], [150,361])
for name in ['detection_ssh.py','requirements.txt','hexalp_ssh_sept2026.csv','alertes_a_qualifier.csv']:
    p(name, 'Heading2'); p(hashlib.sha256((KIT/name).read_bytes()).hexdigest(), 'SmallIA')
p('Les empreintes correspondent aux fichiers locaux au moment de la génération. Des sorties réexécutées ou des notebooks remplacés doivent être conservés avec leur propre version et une date de vérification. Les deux notebooks restent à récupérer ; cette étape de remise n’est pas attestée par les captures seules.')
def footer(canvas, doc):
    canvas.saveState();canvas.setStrokeColor(TEAL);canvas.line(42,38,553,38)
    canvas.setFont('Lato',8);canvas.setFillColor(NAVY)
    canvas.drawString(42,25,'Hexalp • Données fictives • Preuve J3 • Olivier HIMBLOT')
    canvas.drawRightString(553,25,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=42,bottomMargin=52,title='Entraîner un modèle simple — Détection SSH Hexalp',author='Olivier HIMBLOT',subject='Critère : entraînement reproductible Scikit-learn, données préparées, script commenté')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
