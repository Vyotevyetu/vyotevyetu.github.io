# Rebuild the PRODUCTS AND PRICES part of agent_kb.txt from products.json: keep existing lines, add missing products, group by category and subcategory
import json,re
def run(root='/home/claude/site'):
    P=json.load(open(f'{root}/products.json')); byid={p['id']:p for p in P}
    h=open(f'{root}/index.html').read()
    SUBS=json.loads(re.search(r'const SUBS = (\{.*?\});',h).group(1)); CATS=json.loads(re.search(r'const CATS = (\[.*?\]);',h).group(1))
    kb=open(f'{root}/agent_kb.txt').read()
    a=kb.index('PRODUCTS AND PRICES\n')+len('PRODUCTS AND PRICES\n'); b=kb.index('Last updated:')
    lines={}; orphans={}; heads={n.upper():c for c,n in CATS}; cur=None
    for l in kb[a:b].split('\n'):
        t=l.strip()
        if not t or (t.startswith('(') and t.endswith(')')): continue
        if t in heads: cur=heads[t]; continue
        m=re.search(r'/p/([\w-]+)\.html',l)
        if m and m.group(1) in byid: lines[m.group(1)]=l
        elif not m and not (t.isupper() and not t.startswith('-')): orphans.setdefault(cur,[]).append(l)
    def gen(p):
        n=re.sub(r'^[^\w(]+','',p['name']); v=[x[1] for o in p.get('opts',[]) for x in o['v'] if len(x)>1]
        pr=f"from KES {min(v+[p['price']]):,}" if v and min(v)!=max(v) else f"KES {p['price']:,}"
        s=f"- {n}: {pr} ({p['unit']}). {p['detail']}."
        if p.get('opts'): s+=" Options: "+"; ".join(o['n']+": "+", ".join(x[0]+(f" (KES {x[1]:,})" if len(x)>1 else "") for x in o['v']) for o in p['opts'])+"."
        return s+f" Photo and order: https://vyotevyetu.github.io/p/{p['id']}.html"
    out=''
    for c,n in CATS[1:]:
        items=[p for p in P if p['cat']==c]
        if not items and not orphans.get(c): continue
        out+=n.upper()+'\n'; L=SUBS.get(c) or []
        groups=[(x,[p for p in items if p.get('sub')==x]) for x in L]+[(None,[p for p in items if p.get('sub') not in L])] if len(L)>1 else [(None,items)]
        for x,ps in groups:
            if not ps: continue
            if x: out+=f'({x})\n'
            out+='\n'.join(lines.get(p['id']) or gen(p) for p in ps)+'\n'
        if orphans.get(c): out+='\n'.join(orphans[c])+'\n'
        out+='\n'
    open(f'{root}/agent_kb.txt','w').write(kb[:a]+'\n'+out+kb[b:]); print('kb regrouped',len(P))
if __name__=='__main__': run()
