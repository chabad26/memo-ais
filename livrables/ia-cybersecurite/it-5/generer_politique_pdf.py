"""Rendu A4 reproductible du Markdown de la politique ; dépendance : reportlab."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(__file__).parent / 'ia01-j5/politique_ia_hexalp.md'
OUTPUT = ROOT / 'docs/assets/files/ia-cybersecurite/it-5/Politique-IA-Hexalp-proposition.pdf'
for name, file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
styles = {
 'body': ParagraphStyle('body', fontName='DV',fontSize=9.5,leading=12.4,spaceAfter=6,textColor=colors.HexColor('#192b3a')),
 'h1': ParagraphStyle('h1',fontName='DV-Bold',fontSize=17,leading=21,spaceAfter=9,textColor=colors.HexColor('#123f5d')),
 'h2': ParagraphStyle('h2',fontName='DV-Bold',fontSize=11,leading=14,spaceBefore=6,spaceAfter=5,textColor=colors.HexColor('#123f5d'),keepWithNext=True),
 'cell': ParagraphStyle('cell',fontName='DV',fontSize=8.7,leading=11,spaceAfter=0),
}
def inline(s):
    s=escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'<link href="\2" color="#185b80">\1</link>',s)
    return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)

def footer(c, doc):
    c.setStrokeColor(colors.HexColor('#a7bac5')); c.line(38,31,A4[0]-38,31)
    c.setFont('DV',8); c.setFillColor(colors.HexColor('#465b69'))
    c.drawString(38,19,'Hexalp · Proposition V0.1 · 23/10/2026')
    c.drawRightString(A4[0]-38,19,f'{doc.page} / 4')

story=[]
blocks=SOURCE.read_text().split('\n\n')
for block in blocks:
    block=block.strip()
    if not block: continue
    if block=='<!-- pagebreak -->': story.append(PageBreak()); continue
    if block.startswith('|'):
        rows=[]
        for line in block.splitlines():
            if re.match(r'^\|[\s:|\-]+\|$',line): continue
            rows.append([Paragraph(inline(x.strip()),styles['cell']) for x in line.strip('|').split('|')])
        t=Table(rows,colWidths=[154,A4[0]-76-154],hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eff5')),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#aabdc8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story += [t,Spacer(1,6)]; continue
    level=len(block)-len(block.lstrip('#'))
    if level and block[level:level+1]==' ':
        story.append(Paragraph(inline(block[level:].strip()),styles['h1' if level==1 else 'h2'])); continue
    if block.startswith('>'):
        content=[]
        for line in block.splitlines():
            line=re.sub(r'^>\s?', '',line)
            if line: content.append(Paragraph(inline(line),styles['body']))
        box=Table([[content]],colWidths=[A4[0]-76])
        box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#edf5fa')),('BOX',(0,0),(-1,-1),0.6,colors.HexColor('#8aaec5')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.extend([box,Spacer(1,6)])
        continue
    story.append(Paragraph(inline(block.replace('\n',' ')),styles['body']))
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUTPUT),pagesize=A4,leftMargin=38,rightMargin=38,topMargin=33,bottomMargin=41,title='Politique IA Hexalp — Proposition V0.1',author='Olivier HIMBLOT — rédaction avec assistance').build(story,onFirstPage=footer,onLaterPages=footer)
print(OUTPUT)
