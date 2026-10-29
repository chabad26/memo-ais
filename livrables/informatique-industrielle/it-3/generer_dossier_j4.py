"""Dossier C4 autonome depuis la fiche Markdown et les preuves conservées."""
from pathlib import Path
from urllib.parse import unquote
from html import escape
import re
import textwrap
import markdown
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Preformatted
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'docs/informatique-industrielle/it-3/documenter-protections-limites.md'
OUT=ROOT/'docs/assets/files/informatique-industrielle/it-3/J4-configuration-tests-securite-IT-OT-Olivier-HIMBLOT.pdf'
for name,f in [('Lato','Lato-Regular.ttf'),('LatoBold','Lato-Bold.ttf'),('LatoItalic','Lato-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/lato/'+f))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold',italic='LatoItalic',boldItalic='LatoBold')
W,H=landscape(A4);M=34;AW=W-2*M;INK=HexColor('#18354c');TEAL=HexColor('#00695c');LINE=HexColor('#c7d4df')
styles={
 'body':ParagraphStyle('body',fontName='Lato',fontSize=9.5,leading=12.5,textColor=INK,spaceAfter=8),
 'h1':ParagraphStyle('h1',fontName='LatoBold',fontSize=21,leading=26,textColor=INK,spaceAfter=16),
 'h2':ParagraphStyle('h2',fontName='LatoBold',fontSize=17,leading=22,textColor=TEAL,spaceAfter=12),
 'h3':ParagraphStyle('h3',fontName='LatoBold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=8,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Lato',fontSize=8,leading=10.5,textColor=INK),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=7.4,leading=10,textColor=INK,spaceAfter=10),
}
def chrome(c,doc):
    c.saveState();c.setFillColor(INK);c.rect(0,H-42,W,42,fill=1,stroke=0)
    c.setFillColor(HexColor('#ffffff'));c.setFont('LatoBold',10);c.drawString(M,H-25,'AIS · INFORMATIQUE INDUSTRIELLE · J4 · DOSSIER C4')
    c.setStrokeColor(LINE);c.line(M,31,W-M,31);c.setFillColor(INK);c.setFont('Lato',8)
    c.drawString(M,18,'Olivier HIMBLOT · 29 octobre 2026 · Montval proposé / laboratoire testé');c.drawRightString(W-M,18,f'Page {doc.page}');c.restoreState()
def inline(n):
    s=n.decode_contents();return re.sub(r'<code>(.*?)</code>',r'<font name="Courier">\1</font>',s,flags=re.S)
def image_flow(img):
    path=(SRC.parent/unquote(img['src'])).resolve()
    if path.suffix=='.svg':
        d=svg2rlg(str(path));scale=min(AW/d.width,350/d.height);d.scale(scale,scale);d.width*=scale;d.height*=scale;return d
    with PILImage.open(path) as p:w,h=p.size
    scale=min(AW/w,350/h);return Image(str(path),width=w*scale,height=h*scale,hAlign='LEFT')
story=[]
soup=BeautifulSoup(markdown.markdown(SRC.read_text(),extensions=['tables','fenced_code']),'html.parser')
for n in soup.contents:
    if not getattr(n,'name',None):continue
    if n.name in ('h1','h2','h3'):
        if n.name=='h2' and not n.get_text().startswith('Compétence C4'):story.append(PageBreak())
        story.append(Paragraph(inline(n),styles[n.name]));continue
    if n.name=='p':
        im=n.find('img')
        if im:story.extend([image_flow(im),Spacer(1,12)])
        else:story.append(Paragraph(inline(n),styles['body']))
    elif n.name in ('ul','ol'):
        for i,li in enumerate(n.find_all('li',recursive=False),1):story.append(Paragraph(('• ' if n.name=='ul' else f'{i}. ')+inline(li),styles['body']))
    elif n.name=='table':
        rows=[]
        for tr in n.find_all('tr'):
            cells=tr.find_all(['th','td'],recursive=False)
            rows.append([Paragraph(('<b>'+inline(c)+'</b>') if c.name=='th' else inline(c),styles['cell']) for c in cells])
        count=len(rows[0]);weights={2:[.25,.75],3:[.25,.35,.40],4:[.20,.27,.28,.25],7:[.045,.14,.14,.14,.10,.185,.25]}.get(count,[1/count]*count)
        t=Table(rows,colWidths=[AW*x/sum(weights) for x in weights],repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#edf6f3')),('GRID',(0,0),(-1,-1),.35,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5)]));story.extend([t,Spacer(1,12)])
    elif n.name=='pre':
        lines=[]
        for line in n.get_text().splitlines():lines.extend(textwrap.wrap(line,160,replace_whitespace=False,drop_whitespace=False,subsequent_indent='    ') or [''])
        story.append(Preformatted('\n'.join(lines),styles['code']))
    else:raise ValueError(n.name)
doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=58,bottomMargin=43,title='J4-configuration-tests-securite-IT-OT',author='Olivier HIMBLOT',subject='C4 — Sécuriser les communications entre les environnements IT et OT')
doc.build(story,onFirstPage=chrome,onLaterPages=chrome)
print(OUT)
