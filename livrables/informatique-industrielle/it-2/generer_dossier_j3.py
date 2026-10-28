"""PDF formateur C3 depuis le dossier Markdown ; aucun essai technique exécuté."""
from pathlib import Path
from html import escape
import re
import markdown
from bs4 import BeautifulSoup, Comment
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, NextPageTemplate, KeepTogether
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg
ROOT=Path(__file__).resolve().parents[3]
SRC=Path(__file__).with_name('J3-analyse-exigences-architecture-IT-OT.md')
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-2/J3-analyse-exigences-architecture-IT-OT-Olivier-HIMBLOT.pdf'
for name,f in [('Lato','Lato-Regular.ttf'),('LatoBold','Lato-Bold.ttf'),('LatoItalic','Lato-Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/lato/'+f))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold',italic='LatoItalic',boldItalic='LatoBold')
INK=HexColor('#18354c');TEAL=HexColor('#00695c');LINE=HexColor('#c7d4df')
styles={
 'body':ParagraphStyle('body',fontName='Lato',fontSize=9.5,leading=12.3,textColor=INK,spaceAfter=7),
 'h1':ParagraphStyle('h1',fontName='LatoBold',fontSize=20,leading=24,textColor=INK,spaceAfter=12),
 'h2':ParagraphStyle('h2',fontName='LatoBold',fontSize=17,leading=21,textColor=TEAL,spaceBefore=5,spaceAfter=10),
 'h3':ParagraphStyle('h3',fontName='LatoBold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=8,spaceAfter=8),
 'cell':ParagraphStyle('cell',fontName='Lato',fontSize=8.5,leading=11.2,textColor=INK),
}
SIZES={'A4L':landscape(A4),'A3P':A3,'A3L':landscape(A3)};M=34

def chrome(c,doc):
 w,h=c._pagesize;c.saveState();c.setFillColor(INK);c.rect(0,h-44,w,44,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('LatoBold',10);c.drawString(M,h-21,'INFORMATIQUE INDUSTRIELLE · ITÉRATION 2 · J3 · DOSSIER C3');c.setStrokeColor(LINE);c.line(M,31,w-M,31);c.setFillColor(INK);c.setFont('Lato',8);c.drawString(M,18,'Olivier HIMBLOT · AIS 2026 · 28 octobre 2026 · Proposition documentaire, non déployée');c.drawRightString(w-M,18,f'Page {doc.page}');c.restoreState()

doc=BaseDocTemplate(str(OUT),pagesize=SIZES['A4L'],leftMargin=M,rightMargin=M,topMargin=58,bottomMargin=43,title='J3-analyse-exigences-architecture-IT-OT',author='Olivier HIMBLOT',subject='C3 — Analyser les exigences d’exploitation et les interactions IT/OT')
for name,(w,h) in SIZES.items():doc.addPageTemplates(PageTemplate(id=name,frames=[Frame(M,43,w-2*M,h-101,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=chrome,pagesize=(w,h)))

def inline(node):
 s=node.decode_contents();s=re.sub(r'<code>(.*?)</code>',r'<font name="Courier">\1</font>',s,flags=re.S);return s

def widths(headers,available):
 n=len(headers)
 if n==6:weights=[.075,.14,.14,.18,.22,.245]
 elif n==5:weights=[.13,.19,.21,.28,.19]
 elif n==4:weights=[.13,.25,.32,.30]
 elif n==3:weights=[.20,.37,.43]
 else:weights=[1/n]*n
 return [available*x/sum(weights) for x in weights]

html=markdown.markdown(SRC.read_text(),extensions=['tables','fenced_code'])
soup=BeautifulSoup(html,'html.parser');story=[];template='A4L'
for node in soup.contents:
 if isinstance(node,Comment):
  m=re.search(r'page:(A4L|A3P|A3L)',str(node))
  if m:template=m.group(1);story.extend([NextPageTemplate(template),PageBreak()])
  continue
 if not getattr(node,'name',None):continue
 available=SIZES[template][0]-2*M
 if node.name in ('h1','h2','h3'):story.append(Paragraph(inline(node),styles[node.name]));continue
 if node.name=='p':
  img=node.find('img')
  if img:
   path=(SRC.parent/img['src']).resolve();drawing=svg2rlg(str(path));maxh=700 if template=='A3P' else 650
   scale=min(available/drawing.width,maxh/drawing.height);drawing.width*=scale;drawing.height*=scale;drawing.scale(scale,scale);story.extend([drawing,Spacer(1,10)])
  else:story.append(Paragraph(inline(node),styles['body']))
 elif node.name in ('ul','ol'):
  for i,li in enumerate(node.find_all('li',recursive=False),1):story.append(Paragraph(('• ' if node.name=='ul' else f'{i}. ')+inline(li),styles['body']))
 elif node.name=='table':
  rows=[]
  for tr in node.find_all('tr'):
   cells=tr.find_all(['th','td'],recursive=False);rows.append([Paragraph(('<b>'+inline(c)+'</b>') if c.name=='th' else inline(c),styles['cell']) for c in cells])
  t=Table(rows,colWidths=widths([x.get_text() for x in node.find_all('tr')[0].find_all(['th','td'])],available),repeatRows=1,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#edf6f3')),('GRID',(0,0),(-1,-1),.35,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,12)])
 else:raise ValueError('Élément Markdown non géré : '+node.name)
doc.build(story)
print(OUT)
