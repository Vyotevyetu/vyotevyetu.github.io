import json, html, os, re, datetime
ROOT='/home/claude/site'
P=json.load(open(f'{ROOT}/products.json'))
H=open(f'{ROOT}/index.html').read()
CATS=[c for c in json.loads(re.search(r'const CATS = (\[.*?\]);',H).group(1)) if c[0]!='all']
CN=dict(CATS)
SUBS=json.loads(re.search(r'const SUBS = (\{.*?\});',H).group(1))
slug=lambda x: re.sub(r'[^a-z0-9]+','-',x.lower()).strip('-')
SITE='https://vyotevyetu.github.io/'; PHONE='254114308114'; TODAY=datetime.date.today().isoformat()
INTRO={
'irons':'Iron boxes in Kenya: Ailyons steam iron boxes and heavy dry iron boxes with 1 year warranty, delivered in Nairobi.',
'kitchen':'Dish racks and kitchen accessories in Kenya: above-sink dish racks, measuring jugs, kitchen towels, towel holders, mug trees and scoops.',
'pressure':'Electric pressure cookers and air fryers in Kenya: 6L and 8L pressure cookers from Ramtons, Signature, Redberry and more, plus big air fryers. Delivered in Nairobi.',
'storage':'Kitchen storage jars, freezer bags and sugar dishes in Kenya: reusable aluminium foil zip freezer bags, airtight acrylic and glass jars, bamboo canisters, spice jars, cereal dispensers, salt shakers and sugar dishes.',
'sets':'Dinner sets, breakfast sets and tea sets in Kenya: 6-person sets, glass and ceramic, delivered across Nairobi.',
'cookware':'Sufurias and cookware sets in Kenya: aluminium sufuria sets with lids, big catering sufurias from 25L to 280L, chapati pans, granite and stainless sets.',
'hotpots':'Hotpot sets in Kenya: insulated food warmers and serving hotpots in 3, 4 and 6 piece sets for home, events and gifts.',
'cookers':'Gas cookers and grills in Kenya: glass top and infrared gas cookers, 3 burner cookers, charcoal grills and grill pans, delivered in Nairobi.',
'microwaves':'Microwaves in Kenya from trusted brands, delivered in Nairobi.',
'kettles':'Electric kettles in Kenya: stainless, glass and cordless kettles delivered in Nairobi.',
'flasks':'Flasks, tea urns and water bottles in Kenya: 9.5L tea urns for events, tea flasks, airpots and vacuum bottles that keep drinks hot or cold for hours.',
'blenders':'Blenders in Kenya: 2 in 1 blenders with grinder (mill) for smoothies, juice, soups and spices, delivered in Nairobi.',
'mugs':'Mugs in Kenya: ceramic, gold-rim and gift mugs, singles and sets of 6, delivered in Nairobi.',
'trays':'Serving trays in Kenya: steel, acrylic, melamine and oval sinia trays for serving tea, nyama choma and events.',
'plates':'Plates and bowls in Kenya: melamine plates, stoneware and ceramic dinner plates, Japanese side plates, bowls and serving bowls in sets of 6.',
'glass':'Glassware in Kenya: drinking glasses, tumblers and water sets in sets of 6.',
'jugs':'Water jugs in Kenya: ribbed glass jugs, glass juice jugs and unbreakable acrylic and plastic fridge jugs with lids, 1L to 4L, delivered in Nairobi.',
'decor':'Christmas trees, decor and family matching Christmas pajamas in Kenya: green artificial Christmas trees 3ft to 9ft, snow-flocked, pine-needle and pre-lit trees, mini trees with lights, pre-lit snowy garlands, red velvet and gold bows, ball and cypress garlands, wreaths with lights, stockings, star curtain lights, tree skirts, velvet baubles, glitter branches, star toppers, elf legs, Santa hats, star toppers, bells, candy ornaments, table runners, door banners, tree storage bags, and Christmas cushion covers and throw pillow covers in Kenya: 45 x 45cm printed covers in Santa, reindeer, plaid, snowflake and cream-gold designs. Any 4 for KES 1,990, delivered in Nairobi.',
'business':'Business machines in Kenya: commercial popcorn machines and sugarcane juice machines to start a small business. Delivered in Nairobi, delivery quoted per machine.',
'cutlery':'Cutlery, serving spoons and knives in Kenya: stainless table spoons and forks by the 6, soup ladles, rice serving spoons, egg turners, mandazi spoons, spaghetti spoons, melamine serving spoons, gold table spoons, gold spoon holders, 24 piece gold cutlery sets with stand, Feng kitchen knives, Tramontina knives, all-steel professional butcher knives, AIFEL butcher knives, bread knives, Kunsion marble knife sets with stand, wire web spoons and wooden mandazi skimmers, big soup ladles, steel spoon holders, mirror cutlery sets, egg-shaped executive cutlery sets, marble gold cutlery sets, cutlery holder cylinders, serviette holders, butcher knives and 24 piece cutlery sets, delivered in Nairobi.',
'bedding':'Bedding in Nairobi: duvets and cotton bedsheets.',
'dispensers':'Water dispensers in Kenya: hot and cold dispensers and dispenser stands.',
'bags':'School bags in Kenya for kids, delivered in Nairobi.',
'furniture':'TV stands in Kenya: modern laminated TV stands and cabinets with LED lights, delivered in Nairobi.',
'umbrellas':'Umbrellas in Kenya: automatic UV travel umbrellas, long 16-rib umbrellas, wine bottle gift umbrellas, car windscreen sunshades and big shade umbrellas for hawkers and gardens. Delivered in Nairobi.',
'luggage':'Suitcases and luggage in Kenya: 3 in 1 and 4 in 1 suitcase sets, carry-on and duffle bags.',
'bathroom':'Toilet mat sets and bathroom items in Kenya: 3 piece toilet mat sets, touchless soap dispensers, shower shelves and bath mats.',
'mats':'Heavy 3D living room carpets 5x8 ft, light 3D carpets 180x270cm, PVC floor carpet (mkeka) rolls, door mats, 2 piece printed kitchen mat sets with rubber grip, anti-fatigue kitchen mats, floor mats and woven table mats (placemats) in Nairobi.',
'home':'Home storage, organisers and garden in Kenya: magic expandable hose pipes 30m, 45m and 60m, storage bags, organisers and more, delivered in Nairobi.',
}
e=lambda s: html.escape(str(s), quote=True)
def clean(n): return re.sub(r'^[^\w(]+','',n).strip()
def prices(p):
    v=[x[1] for o in p.get('opts',[]) for x in o['v'] if len(x)>1]
    return (min(v+[p['price']]), max(v+[p['price']])) if v else (p['price'],p['price'])
def ptxt(p):
    lo,hi=prices(p); return f'KES {lo:,}' if lo==hi else f'from KES {lo:,}'
def wa(text): return f'https://wa.me/{PHONE}?text='+html.escape(__import__('urllib.parse').parse.quote(text),quote=True)
GC='<script data-goatcounter="https://vyotevyetu.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
CSS='''*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f6f5f0;color:#14231c}
a{color:#0f3d2e}header{background:#0f3d2e;color:#fff;padding:12px 18px;display:flex;align-items:center;gap:10px}header a{color:#fff;text-decoration:none;font-weight:800;font-size:19px}header img{width:34px;height:34px;border-radius:9px}
main{max-width:980px;margin:0 auto;padding:16px}.crumb{font-size:14px;color:#5f6e66;margin:4px 0 14px}.crumb a{color:#5f6e66}
.prod{display:grid;gap:22px;grid-template-columns:minmax(0,1fr)}.prod>div{min-width:0}@media(min-width:760px){.prod{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.prod img{width:100%;border-radius:18px;background:#fff}h1{font-size:26px;line-height:1.2;margin:0 0 8px}
.price{font-size:28px;font-weight:800;color:#0f3d2e;margin:6px 0 12px}.unit{font-size:15px;color:#5f6e66;font-weight:600}
.btn{display:block;text-align:center;padding:15px;border-radius:14px;font-weight:800;text-decoration:none;margin:10px 0}.wa{background:#1fa855;color:#fff}.shop{background:#efede5;color:#0f3d2e}
table{border-collapse:collapse;width:100%;margin:10px 0;background:#fff;border-radius:12px;overflow:hidden}td,th{padding:9px 12px;border-bottom:1px solid #e7e5dc;text-align:left}th{background:#efede5}
select{width:100%;padding:12px;font-size:16px;border-radius:12px;border:1px solid #d9d6ca;margin:6px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px}.card{background:#fff;border-radius:16px;overflow:hidden;text-decoration:none;color:#14231c;display:block}
.card img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}.card div{padding:9px 11px}.card b{display:block;font-size:14px;line-height:1.3}.card span{font-weight:800;color:#0f3d2e;font-size:15px}
h2{font-size:20px;margin:28px 0 12px}footer{background:#0f3d2e;color:#dfe7e2;padding:22px 18px;margin-top:30px;font-size:14px}footer a{color:#fff;margin-right:12px;display:inline-block;margin-bottom:6px}
.note{font-size:14px;color:#5f6e66}.gal{display:flex;gap:8px;overflow-x:auto;margin:10px 0 0}.gal img{width:84px;height:84px;object-fit:cover;border-radius:10px;border:1px solid #dfe7e2;flex:0 0 auto}'''
def head(title,desc,url,img,ld,typ='website'):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#0f3d2e">
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="Vyetu Vyote"><meta property="og:locale" content="en_KE">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{img}"><meta property="og:image:secure_url" content="{img}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="{e(title)}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:image" content="{img}">
<link rel="icon" href="{SITE}img/logo-mark.svg"><link rel="apple-touch-icon" href="{SITE}img/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<style>{CSS}</style>{GC}</head><body>
<header><a href="{SITE}"><img src="../img/apple-touch-icon.png" alt="Vyetu Vyote logo"></a><a href="{SITE}">Vyetu Vyote</a></header>'''
SALEJS=r'<script>(function(){var S=[["⚡ Black Friday","2026-11-27T00:00:00+03:00","2026-12-01T00:00:00+03:00","Mon 30 Nov"],["🎄 Festive Sale","2026-12-01T00:00:00+03:00","2027-01-01T00:00:00+03:00","31 Dec"]],n=Date.now(),s=null;S.forEach(function(x){if(n>=Date.parse(x[1])&&n<Date.parse(x[2]))s=x});if(!s)return;function sp(x){if(x<500)return x;var t=x<=1000?x-40:Math.floor(x*(x<=3000?.93:.92));t=Math.max(t,x-1000);var m=Math.floor(t/10)*10;while(m%100!==50&&m%100!==90)m-=10;return m}if(window.HERO){var pe=document.getElementById("pr");if(pe)pe.innerHTML=pe.innerHTML.replace("KES "+HERO[0].toLocaleString("en-US"),"KES\u00a0"+HERO[1].toLocaleString("en-US")+" <s style=\"opacity:.6;font-weight:400\">KES\u00a0"+HERO[0].toLocaleString("en-US")+"</s>")}var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),a=[],t;while(t=w.nextNode())a.push(t);a.forEach(function(t){t.nodeValue=t.nodeValue.replace(/KES ([\d,]+)/g,function(m,v){var x=+v.replace(/,/g,""),y=sp(x);return y<x?"KES "+y.toLocaleString("en-US"):m})});var pr=document.getElementById("pr");if(pr){var b=document.createElement("p");b.style.cssText="background:#d9412e;color:#fff;font-weight:800;padding:8px 12px;border-radius:10px;display:inline-block;margin:6px 0";b.textContent=s[0]+": up to 20% off, ends "+s[3];pr.parentNode.insertBefore(b,pr)}})();</script>'
FOOT='<footer><p><b>Vyetu Vyote</b> (also Vyote Vyetu): kitchenware and household items from Nairobi, Kenya. Order on WhatsApp <a href="https://wa.me/254114308114">0114 308 114</a>. Delivery in Nairobi and worldwide at the customer\'s cost. Pay by M-Pesa.</p><p>'+''.join(f'<a href="{SITE}c/{c}.html">{e(n)}</a>' for c,n in CATS)+f'</p><p><a href="{SITE}">Shop all products</a></p></footer>'+SALEJS+'</body></html>'
def gal(p):
    s=[]
    for x in list((p.get('vi') or {}).values())+list(p.get('imgs') or []):
        if x not in s and x!=p.get('dupmain'): s.append(x)
    return s
def galhtml(p,n):
    g=gal(p)
    vs=p.get('vids') or []
    vh=''.join(f'<video controls playsinline preload="none" poster="../vid/{v}.jpg" src="../vid/{v}.mp4" style="width:100%;max-width:420px;border-radius:12px;margin-top:10px;background:#000"></video>' for v in vs)
    if not g: return vh
    th=[f'../img/{p["id"]}.jpg']+[f'../img/v/{x}.jpg' for x in g]
    return '<div class="gal">'+''.join(f'<img loading="lazy" src="{u}" alt="{e(n)} photo {i+1}" onclick="document.getElementById(\'mainimg\').src=this.src">' for i,u in enumerate(th))+'</div>'+vh
def card(p): return f'<a class="card" href="{SITE}p/{p["id"]}.html"><img loading="lazy" src="../img/t/{p["id"]}.jpg" alt="{e(clean(p["name"]))}"><div><b>{e(clean(p["name"]))}</b><span>{ptxt(p)}</span></div></a>'

import re as _re
def _sents(d): return [x.strip().rstrip('.') for x in _re.split(r'(?<=[.!])\s+',d) if x.strip()]
def info(p):
    S=_sents(p['detail']); deals=[x for x in S if _re.match(r'^Any \d',x,_re.I)]; f=[x for x in S if x not in deals]
    h='<h2 style="margin-top:14px">Key features</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in f)+'</ul>'
    if deals: h+='<p style="background:#fff6df;border-radius:10px;padding:10px 12px"><b>🎁 Deals:</b> '+e('; '.join(deals))+'</p>'
    h+=f'<table><tr><th colspan="2">Specifications</th></tr><tr><td>Sold as</td><td>{e(p["unit"])}</td></tr><tr><td>Category</td><td>{e(CN.get(p["cat"],p["cat"]))}</td></tr>'+(f'<tr><td>Type</td><td>{e(p["sub"])}</td></tr>' if p.get('sub') else '')+'<tr><td>Condition</td><td>Brand new</td></tr>'+''.join(f'<tr><td>{e(o["n"])}</td><td>{len(o["v"])} options</td></tr>' for o in p.get('opts',[]))+f'<tr><td>Product code</td><td>{e(p["id"])}</td></tr></table>'
    return h
SELLER={"@type":"Organization","name":"Vyetu Vyote","url":SITE}
os.makedirs(f'{ROOT}/p',exist_ok=True); os.makedirs(f'{ROOT}/c',exist_ok=True)
for p in P:
    n=clean(p['name']); lo,hi=prices(p); url=f'{SITE}p/{p["id"]}.html'; img=f'{SITE}img/{p["id"]}.jpg'; cat=p['cat']
    title=f'{n} – {ptxt(p)} | Vyetu Vyote Kenya'
    d=p['detail']; oc=' · '.join(f'{len(o["v"])} {o["n"].lower()}s' for o in p.get('opts',[]) if len(o['v'])>1); desc=f'{ptxt(p)}'+(f' · {oc}' if oc else '')+'. '+(d if len(d)<=110 else d[:107].rsplit(' ',1)[0]+'…')+' Order on WhatsApp 0114 308 114, delivery in Nairobi.'
    offer={"@type":"Offer","price":lo,"priceCurrency":"KES","availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition","url":url,"seller":SELLER} if lo==hi else {"@type":"AggregateOffer","lowPrice":lo,"highPrice":hi,"priceCurrency":"KES","offerCount":sum(len(o['v']) for o in p['opts'] if any(len(x)>1 for x in o['v'])),"availability":"https://schema.org/InStock","url":url,"seller":SELLER}
    ld=[{"@context":"https://schema.org","@type":"Product","name":n,"description":d,"image":[img]+[f'{SITE}img/v/{x}.jpg' for x in gal(p)][:9],"sku":p['id'],"category":CN.get(cat,cat)+(' > '+p['sub'] if p.get('sub') else ''),"offers":offer},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Shop","item":SITE},{"@type":"ListItem","position":2,"name":CN.get(cat,cat),"item":f'{SITE}c/{cat}.html'},{"@type":"ListItem","position":3,"name":n,"item":url}]}]
    msg=f'Hi Vyetu Vyote, I would like to order: {n} ({ptxt(p)}). {url}'
    opts=''; js=''
    for o in p.get('opts',[]):
        priced=any(len(x)>1 for x in o['v'])
        if priced:
            opts+=f'<table><tr><th>{e(o["n"])}</th><th>Price</th></tr>'+''.join(f'<tr><td>{e(x[0])}</td><td>KES {x[1]:,}</td></tr>' for x in o['v'])+'</table>'
        else:
            opts+=f'<p><b>{e(o["n"])}:</b> {e(", ".join(x[0] for x in o["v"]))}</p>'
    if p.get('opts'):
        sels=''.join(f'<select data-n="{e(o["n"])}" aria-label="{e(o["n"])}">'+''.join(f'<option value="{e(x[0])}" data-p="{x[1] if len(x)>1 else ""}">{e(x[0])}{" · KES "+format(x[1],",") if len(x)>1 else ""}</option>' for x in o['v'])+'</select>' for o in p['opts'])
        opts=f'<p class="note">Pick your choice, then tap Order:</p>{sels}'+opts
        js='''<script>(function(){var S=document.querySelectorAll('select'),b=document.getElementById('order'),pr=document.getElementById('pr'),base=%s,name=%s,url=%s;
function u(){var ch=[],p=base;S.forEach(function(s){var o=s.options[s.selectedIndex];ch.push(o.value);if(o.dataset.p)p=+o.dataset.p;});
pr.firstChild.nodeValue='KES '+p.toLocaleString('en-US')+' ';b.href='https://wa.me/254114308114?text='+encodeURIComponent('Hi Vyetu Vyote, I would like to order: '+name+' ('+ch.join(', ')+') KES '+p.toLocaleString('en-US')+'. '+url);}
S.forEach(function(s){s.addEventListener('change',u)});u();})()</script>'''%(json.dumps(p['price']),json.dumps(n),json.dumps(url))
    rel=([q for q in P if q['cat']==cat and q.get('sub')==p.get('sub') and q['id']!=p['id']]+[q for q in P if q['cat']==cat and q.get('sub')!=p.get('sub')])[:8]
    body=f'''<main><div class="crumb"><a href="{SITE}">Shop</a> › <a href="{SITE}c/{cat}.html">{e(CN.get(cat,cat))}</a>{(' › <a href="'+SITE+'c/'+cat+'.html#'+slug(p['sub'])+'">'+e(p['sub'])+'</a>') if p.get('sub') else ''}</div>
<div class="prod"><div><img id="mainimg" src="../img/{p['id']}.jpg" alt="{e(n)}" width="1080">{galhtml(p,n)}</div><div><h1>{e(n)}</h1>
<div class="price" id="pr">{ptxt(p)} <span class="unit">· {e(p['unit'])}</span></div>{info(p)}{opts}
<a class="btn wa" id="order" href="{wa(msg)}" rel="nofollow">Order on WhatsApp</a>
<a class="btn shop" href="{SITE}#p={p['id']}">Open in the shop to add more items</a>
<p class="note">Delivery in Nairobi and worldwide (at customer's cost). Pay by M-Pesa to 0114 308 114. Questions? WhatsApp or call 0114 308 114.</p></div></div>
<h2>More {e(CN.get(cat,cat).lower())}</h2><div class="grid">{''.join(card(q) for q in rel)}</div>
<p><a href="{SITE}c/{cat}.html">See all {e(CN.get(cat,cat).lower())} →</a></p></main>{js}'''
    open(f'{ROOT}/p/{p["id"]}.html','w').write(head(title,desc,url,img,ld,'product')+body+(f'<script>var HERO=[{p["price"]},{p["hero"]}]</script>' if p.get('hero') else '')+FOOT)
def secs(c,items):
    L=SUBS.get(c) or []
    if len(L)<2: return '<div class="grid">'+''.join(card(p) for p in items)+'</div>'
    nav='<p class="note">'+' · '.join(f'<a href="#{slug(x)}">{e(x)}</a>' for x in L)+'</p>'
    return nav+''.join(f'<h2 id="{slug(x)}">{e(x)} <span class="note">({sum(1 for p in items if p.get("sub")==x)})</span></h2><p class="note"><a href="{SITE}#c={c}&s={slug(x)}">Open in the shop</a></p><div class="grid">'+''.join(card(p) for p in items if p.get('sub')==x)+'</div>' for x in L)
for c,name in CATS:
    items=[p for p in P if p['cat']==c]
    if not items: continue
    url=f'{SITE}c/{c}.html'; lo=min(prices(p)[0] for p in items)
    title=f'{name} in Kenya – {len(items)} items from KES {lo:,} | Vyetu Vyote'
    desc=INTRO.get(c,name)+(' Shop by type: '+', '.join(SUBS[c])+'.' if len(SUBS.get(c) or [])>1 else '')+f' From KES {lo:,}. Order on WhatsApp.'
    ld=[{"@context":"https://schema.org","@type":"CollectionPage","name":f'{name} in Kenya',"url":url,"description":desc,
         "mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":[{"@type":"ListItem","position":i+1,"url":f'{SITE}p/{p["id"]}.html',"name":clean(p['name'])} for i,p in enumerate(items)]}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Shop","item":SITE},{"@type":"ListItem","position":2,"name":name,"item":url}]}]
    body=f'''<main><div class="crumb"><a href="{SITE}">Shop</a> › {e(name)}</div><h1>{e(name)} in Kenya</h1><p>{e(INTRO.get(c,""))}</p>
<a class="btn shop" href="{SITE}#c={c}">Open {e(name.lower())} in the shop</a>{secs(c,items)}</main>'''
    open(f'{ROOT}/c/{c}.html','w').write(head(title,desc,url,f'{SITE}img/{items[0]["id"]}.jpg',ld)+body+FOOT)
urls=[(SITE,TODAY,'1.0')]+[(f'{SITE}c/{c}.html',TODAY,'0.8') for c,_ in CATS if any(p['cat']==c for p in P)]+[(f'{SITE}p/{p["id"]}.html',p.get('added',TODAY),'0.6') for p in P]
open(f'{ROOT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n' for u,m,pr in urls)+'</urlset>\n')
open(f'{ROOT}/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
print(len(P),'pages,',len(CATS),'cats,',len(urls),'urls')

# Meta / WhatsApp catalogue feed (public prices only, no supplier info)
import csv,re as _re
def _clean(t): return _re.sub(r'[^\w\s,.&()/%+\-:\'"]','',t.replace('–','-').replace('—','-').replace('×','x')).strip()
with open('catalog.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    _h=open('index.html').read(); _D=json.loads(_re.search(r'^const DEPTS = (.*?);$',_h,_re.M).group(1)); _DN={c:_re.sub(r'[^\w &]','',n).strip() for k,n,cs in _D for c in cs}
    import datetime as _dt; _lim=(_dt.date.today()-_dt.timedelta(days=14)).isoformat(); _cnt={}
    for _p in P:
        if _p.get('added','')>=_lim: _cnt[_p['added']]=_cnt.get(_p['added'],0)+1
    _new='9999'; _n=0
    for _d in sorted(_cnt,reverse=True):
        _new=_d; _n+=_cnt[_d]
        if _n>=40: break
    def _bud(x): return 'Under 500' if x<500 else '500 to 1000' if x<=1000 else '1000 to 3000' if x<=3000 else '3000 to 10000' if x<=10000 else 'Over 10000'
    w.writerow(['id','title','description','availability','condition','price','link','image_link','brand','google_product_category','product_type','additional_image_link','custom_label_0','custom_label_1','custom_label_2','custom_label_3','sale_price','sale_price_effective_date'])
    def _saleP(x):
        if not x or x<500: return x
        t=x-40 if x<=1000 else int(x*(0.93 if x<=3000 else 0.92)); t=max(t,x-1000); n=t//10*10
        while n%100 not in (50,90): n-=10
        return n
    _SR='2026-11-27T00:00+03:00/2027-01-01T00:00+03:00'
    for p in P:
        if p.get('soldout'): continue
        opts='; '.join(o['n']+': '+', '.join(v[0] for v in o['v']) for o in p.get('opts',[]))
        d0=_clean(p.get('detail',''));d0=d0 if d0.endswith('.') else d0+'.';desc=d0+(' Options: '+opts if opts else '')+f" Sold as {p.get('unit','')}. Delivery in Nairobi and worldwide at customer's cost."
        w.writerow([p['id'],_clean(p['name'])[:150],desc[:5000],'in stock','new',f"{p['price']} KES",f"{SITE}p/{p['id']}.html",f"{SITE}img/{p['id']}.jpg",'Vyetu Vyote','Home & Garden > Kitchen & Dining',CN.get(p['cat'],'')+(' > '+p['sub'] if p.get('sub') else ''),','.join(f"{SITE}img/v/{x}.jpg" for x in gal(p)[:10]),_DN.get(p['cat'],''),_bud(p['price']),'New' if p.get('added','')>=_new else '','Deal' if _re.search(r'\bAny \d',p.get('detail','')) else '']+([f"{p.get('hero') or _saleP(p['price'])} KES",_SR] if (p.get('hero') or _saleP(p['price']))<p['price'] else ['','']))
print('catalog.csv written')

# merged products: keep old links working
import os as _os
_R=json.load(open('redirects.json')) if _os.path.exists('redirects.json') else {}
for _o,_n in _R.items():
    open(f'p/{_o}.html','w').write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{SITE}p/{_n}.html"><meta http-equiv="refresh" content="0;url={SITE}p/{_n}.html"></head><body><a href="{SITE}p/{_n}.html">See this product</a></body></html>')
print('redirect pages',len(_R))
