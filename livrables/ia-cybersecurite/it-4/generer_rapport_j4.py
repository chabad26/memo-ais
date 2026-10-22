"""PDF formateur J4 : rapport complet 4.1 à 4.8 et annexes de preuve."""
from pathlib import Path
from html import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
KIT=BASE/'IA_J4_ressources_apprenant/ia01-j4'
OUT=BASE/'Evaluation-modele-SSH-Hexalp-Olivier-HIMBLOT.pdf'
for name,file in [('Lato','Lato-Regular.ttf'),('LatoBold','Lato-Bold.ttf'),('LatoItalic','Lato-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/lato/'+file))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold',italic='LatoItalic',boldItalic='LatoBold')
s=getSampleStyleSheet()
for name in ['Title','Heading1','Heading2']:
    s[name].fontName='LatoBold';s[name].textColor=colors.HexColor('#17324d')
s.add(ParagraphStyle(name='BodyIA',fontName='Lato',fontSize=9.2,leading=11.7,spaceAfter=5))
s.add(ParagraphStyle(name='CellIA',parent=s['BodyIA'],fontSize=8,leading=9.7,spaceAfter=0))
s['Heading1'].fontSize=17;s['Heading1'].leading=21
s['Heading2'].fontSize=12;s['Heading2'].leading=15;s['Heading2'].spaceBefore=8;s['Heading2'].spaceAfter=5
story=[]
def p(t,style='BodyIA'):
    t=escape(t);t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t);t=re.sub(r'`([^`]+)`',r'\1',t)
    return Paragraph(t,s[style])
def add(t,style='BodyIA'):story.append(p(t,style))
def table(rows,widths=None):
    t=Table([[p(c,'CellIA') for c in r] for r in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcecf0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f4f7f9'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.extend([t,Spacer(1,7)])
def page():story.append(PageBreak())
add('IA & CYBERSÉCURITÉ — ITÉRATION 4','Heading2')
add('Évaluer un modèle de détection SSH','Title')
add('Olivier HIMBLOT • 22 octobre 2026 • Dossier pour le formateur')
add('Compétence : **Évaluer les performances et les limites d’un modèle de détection d’anomalies.**')
add('Critère : mesure sur des données nouvelles au-delà du taux global ; explication des erreurs, biais, dérives et vulnérabilités ; définition des conditions d’exploitation.')
table([['Attendu','Preuve et état'],['Données nouvelles et métriques','Septembre entraîne, octobre évalue ; matrices, précision/rappel et charge documentés.'],['Erreurs, biais et dérives','Profils de FP/FN analysés ; exclusions, apprentissage court, étiquettes et évolution du SI explicités.'],['Vulnérabilités','Simulations4.6 exécutées : extraction locale, fractionnement, liste blanche et empoisonnement ; kit et V2 distingués.'],['Conditions d’exploitation','Conditions4.8 rédigées ; pilote4semaines et critères proposés, sans approbation RSSI/SOC ni déploiement revendiqués.'],['Exécution et reproductibilité','Deux captures VM ; tests de répétabilité et contrôles dans un environnement distinct de l’assistant.']],[140,371])
add('État de la preuve','Heading2')
add('Données fictives du scénario Hexalp. Rapport rédigé avec assistance à partir des sorties fournies et vérifiées. Les résultats, essais de vulnérabilité et conditions proposées sont documentés. Leur portée reste celle du TP ; la validation opérationnelle des conditions n’est pas établie. Ce dossier ne prétend ni à un déploiement réel ni à une validation globale du modèle.')
add('Fichiers de preuve associés','Heading2')
add('Dans IA_J4_ressources_apprenant/ia01-j4 : detection_ssh_v2.py ; requirements.txt ; alertes_octobre.csv (239 lignes de données) ; rapport_evaluation.md ; preuves/execution_v2.txt ; preuves/verification_v2.json. Le PDF présente les résultats ; conserver le script et le CSV comme fichiers exploitables joints à la remise.')
add('Organisation : rapport complet sur les trois pages suivantes ; annexes séparées pour la chaîne de décision et les captures sélectionnées.')
page()
lines=(KIT/'rapport_evaluation.md').read_text().splitlines()
i=0
while i<len(lines):
    line=lines[i].strip()
    if not line:i+=1;continue
    if line=='## Protocole et résultats' or line=='## Conditions d’exploitation':page()
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[:\- ]+',c) for c in cells):rows.append(cells)
            i+=1
        widths=[96,42,32,32,34,66,60,149] if len(rows[0])==8 else ([95,416] if len(rows[0])==2 else [335,45,131])
        # Keep all columns within the 511 pt content width.
        widths=[v*511/sum(widths) for v in widths]
        table(rows,widths);continue
    if line.startswith('# '):add(line[2:],'Heading1')
    elif line.startswith('## '):add(line[3:],'Heading2')
    else:add(line)
    i+=1
page()
add('Annexe — De la collecte à la décision','Heading1')
add('Chaîne cible proposée en4.8 ; la V2 existante produit un CSV. Les raccordements SOC, enrichissements supplémentaires et procédures ci-dessous ne sont pas démontrés comme déployés.')
table([['Maillon / pilote proposé','Fonction et comportement en cas de panne'],
['Journaux — administrateurs/supervision','Collecte automatique. Si sonde/journaux absents : incident de collecte, couverture dégradée ; jamais normal par défaut.'],
['Qualité — Sofia','Schéma, unités, périodes, doublons/manques ; revue du journal DSI. Lot modèle refusé si contrat invalide, traces conservées.'],
['fail2ban — administrateurs bastion','Branche indépendante : règle existante et bannissement déjà autorisé. Signaler toute panne ; le modèle ne le remplace pas.'],
['Préparation et modèles — supervision','Version validée, conversion et exclusion tracées, prédiction. Arrêter si échec ; retour arrière seulement compatible avec les données.'],
['Enrichissement et file — supervision/SOC','Mesures, avis, score, déclencheur ; ajouter version, identité/destination et contexte. Conserver le surplus, suivre âge et priorités ; pas de troncature à30.'],
['Qualification — Hugo/SOC','Analyse humaine, référence aux sources et décision tracée. Indisponibilité : escalade/renfort, pas de validation automatique.'],
['Décision — analyste habilité/RSSI','Réponse selon la procédure ; mise à jour du modèle approuvée et réversible. Aucun ban ou changement de configuration décidé par le modèle.']],[145,366])
add('Cinq questions à l’éditeur','Heading2')
add('1. Le99% désigne-t-il rappel ou accuracy, sur quels effectifs et quels profils, avec quelles incertitudes ?')
add('2. Quel test indépendant, quelles données/étiquettes, quelles exclusions et quelle séparation temporelle ?')
add('3. Quel volume d’alertes/FP et quel coût de qualification ; que se passe-t-il au-delà de30 et pendant une panne ?')
add('4. Quelle provenance, protection, version et résistance aux attaques ; comment valider et annuler une mise à jour ?')
add('5. Quelles données sortent, quels droits d’action sont nécessaires et comment imposer contrôle humain et réversibilité ?')
add('Rappels de preuve','Heading2')
add('Les notebooks03/04 sont exécutés localement avec assistance. Les captures de l’apprenant corroborent les exercices du kit ; elles ne prouvent pas toutes ses versions Python ni une répétabilité de la V2 dans la VM. Le hash de référence du modèle est fourni dans le PDF4.7 ; sa concordance ne certifie ni qualité ni innocuité. Les sources originales des notebooks sont conservées séparément.')
for name,title,caption in [
('09-37-46','Capture — Export V2 et charge','239 alertes annoncées,104 puis135/semaine ; budget30 dépassé. Sorties VM concordantes avec les contrôles locaux.'),
('09-59-44','Capture — Sondes et frontières du kit','Dix sondes et export de l’arbre pédagogique ; frontières locales4comptes à14h et9h avec2comptes. Ces seuils ne décrivent pas notre V2.'),
('10-04-43','Capture — Liste blanche corrigée','185 alertes avant,19 supprimées,166 après dans le kit. Le transfert synthétique9000Mo est signalé ; la dernière phrase sur son masquage est explicative.'),
('10-05-12','Capture — Empoisonnement des étiquettes','Kit : le profil préparé passe à partir de5lignes parmi les tailles testées ; rappel/erreurs changent. Les essais supplémentaires V2 sont conservés dans le JSON.'),
('10-03-02','Capture — Empoisonnement comportemental','Détections kit sur9VPN après0/10/20/40/80observations ajoutées :9/9/5/6/2. Effet non monotone, aucune durée réelle minimale démontrée.'),
('10-17-53','Capture — Réseau et paramètres','7→8→3→8→7,186 paramètres. La matrice7×8 comporte56poids : le commentaire source24 est une coquille.'),
('10-18-45','Capture — Inférence et comparaison','Périmètre pédagogique2119lignes : AE70VP,145FN,6FP,1898VN ;9/9VPN repérés,4FP sauvegarde. Distinct de la préparation V2.'),
('10-19-17','Capture — Expliquer la reconstruction','Exfiltration8690,075Mo : erreur volume normalisé928,97 ; sauvegarde1666,53Mo :0,15. Une erreur élevée n’établit pas seule une intention malveillante.')]:
    page();add(title,'Heading1');add(caption)
    im=Image(str(ROOT/'docs/assets/img/ia-cybersecurite/it-4'/f'Capture d’écran du 2026-10-22 {name}.png'))
    factor=min(511/im.imageWidth,625/im.imageHeight)
    im.drawWidth=im.imageWidth*factor;im.drawHeight=im.imageHeight*factor;story.append(im)
    if name=='10-17-53':
        story.append(Spacer(1,12))
        add('Contrôle préalable dans la VM : SHA-256 conforme à la référence du PDF4.7.')
        im=Image(str(ROOT/'docs/assets/img/ia-cybersecurite/it-4/Capture d’écran du 2026-10-22 10-14-57.png'))
        factor=min(511/im.imageWidth,65/im.imageHeight)
        im.drawWidth=im.imageWidth*factor;im.drawHeight=im.imageHeight*factor;story.append(im)
def footer(canvas,doc):
    canvas.setFont('Lato',8);canvas.setFillColor(colors.HexColor('#17324d'))
    canvas.drawString(42,24,'Olivier HIMBLOT • Hexalp fictif • Évaluation J4 • 22/10/2026')
    canvas.drawRightString(553,24,str(doc.page))
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42.28,topMargin=35,bottomMargin=40,title='Évaluation du modèle SSH Hexalp — Olivier HIMBLOT',author='Olivier HIMBLOT').build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
