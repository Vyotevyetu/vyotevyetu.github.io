import json,re
P=json.load(open('products.json'))
pool={}
for p in P: pool.setdefault(re.sub(r'^[^\w(]+','',p['name']).strip(),[]).append(p['id'])
out=[];n=0
for l in open('agent_kb.txt').read().split('\n'):
    l=re.sub(r' Photo and order: https://vyotevyetu\.github\.io/p/\S+$','',l)
    nm=l[2:].split(': KES')[0] if l.startswith('- ') and ': KES' in l else None
    if nm and pool.get(nm):
        l=l.rstrip()+(' ' if l.rstrip().endswith('.') else '. ')+f'Photo and order: https://vyotevyetu.github.io/p/{pool[nm].pop(0)}.html'; n+=1
    out.append(l)
t='\n'.join(out)
rule="- When a customer asks about a product, send its 'Photo and order' link so they can see the photo. To browse a whole category, send the catalogue link or https://vyotevyetu.github.io\n"
if "'Photo and order' link" not in t: t=t.replace("- Do not offer discounts other than the deals below.\n","- Do not offer discounts other than the deals below.\n"+rule,1)
open('agent_kb.txt','w').write(t); print(n)
