import json,re,io
from docx import Document
from docx.shared import Inches,Pt
from PIL import Image
P=json.load(open('products.json'))
pool={}
for p in P: pool.setdefault(re.sub(r'^[^\w(]+','',p['name']).strip(),[]).append(p['id'])
d=Document(); st=d.styles['Normal']; st.font.name='Arial'; st.font.size=Pt(10)
lines=open('agent_kb.txt').read().split('\n')
tbl=None
for l in lines:
    nm=l[2:].split(': KES')[0] if l.startswith('- ') and ': KES' in l else None
    if nm and pool.get(nm):
        pid=pool[nm].pop(0)
        if tbl is None: tbl=d.add_table(rows=0,cols=2)
        r=tbl.add_row().cells
        im=Image.open(f'img/t/{pid}.jpg').convert('RGB'); im.thumbnail((180,240))
        b=io.BytesIO(); im.save(b,'JPEG',quality=48,optimize=True); b.seek(0)
        r[0].width=Inches(1.3); r[1].width=Inches(5.2)
        r[0].paragraphs[0].add_run().add_picture(b,width=Inches(1.2))
        r[1].paragraphs[0].add_run(l[2:])
        continue
    tbl=None
    if not l.strip(): continue
    if l.isupper() and len(l)<60: d.add_heading(l.title(),level=1 if l.startswith(('ABOUT','PRODUCTS')) else 2)
    else: d.add_paragraph(l)
d.save('agent_kb.docx')
