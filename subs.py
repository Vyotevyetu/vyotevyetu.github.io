import json,re
# order of subcategories per category; first matching rule wins
SUBS={
'cookware':[('Chapati pans, frying pans & sizzlers',lambda p:re.search('chapati|frying|sizzl',p['name'],re.I)),('Aluminium sufuria sets',lambda p:p['id'] in('kalu-12','kalu-1619','premium-5','suf-signature-belly5','suf-tornado7','suf-redberry','suf-signature8','suf-uken12','suf-oxford','suf-bellypot','suf-freedom8')),
            ('Big catering sufurias',lambda p:p['id'] in('kalu-55','freedom-big','uken-big')),
            ('Non-stick & granite sets',lambda p:p['id'] in('granite-set','srl-14','tc-14') or p['id'].startswith('bosch-')),
            ('Stainless steel cookware',lambda p:p['id'] in('stainless-set','marwa-30','marwa-72','srl-k104','freedom-belly4','marwa-yemetel-12')),
            ('Casseroles & stew pots',lambda p:p['id'].startswith(('pardini','pot-ceramic')))],
'hotpots':[('Chafing dishes & food warmers',lambda p:p['id'].startswith('chafing-')),('Stainless steel hotpots',lambda p:re.search(r'stainless|mirror|silver ?max|silverstar|steel',p['name'],re.I)),
           ('Marble & designer hotpots',lambda p:re.search(r'marble|turkish|leatherite|wood|wicker|flower|desire|taj|marilyn|regalia',p['name'],re.I)),
           ('Insulated hotpots',lambda p:True)],
'sets':[('58pc dinner sets',lambda p:'58pc' in p['name']),('Breakfast sets',lambda p:re.search('breakfast|tree mugs',p['name'],re.I)),('Dinner sets',lambda p:True)],
'pressure':[('Air fryers',lambda p:'fryer' in p['name'].lower()),('Electric pressure cookers',lambda p:True)],
'cookers':[('Gas cookers',lambda p:'cooker' in p['name'].lower()),('Charcoal grills & grill pans',lambda p:True)],
'flasks':[('Tumblers & travel cups',lambda p:p['id'].startswith(('tumbler-','cup-'))),('Tea urns',lambda p:re.search(r'\burn\b',p['name'],re.I)),('Water bottles',lambda p:p['id'].startswith('bottle')),('Tea flasks',lambda p:True)],
'dispensers':[('Bottle stands & taps',lambda p:p['id']=='rack-bucket-tap'),('Bottle water pumps',lambda p:p['id'].startswith('pump-')),('Bottom load dispensers',lambda p:'bottom' in p['name'].lower()),('Standing & table top dispensers',lambda p:True)],
'luggage':[('Suitcase sets',lambda p:re.search(r'\dpc|in-1|in1|set of',p['name'],re.I) and 'single' not in p['name'].lower()),('Duffle bags',lambda p:'duffle' in p['name'].lower()),('Single suitcases',lambda p:True)],
'umbrellas':[('Rain & sun umbrellas',lambda p:p['id'] in('umb-auto-uv','umb-16rib','umb-wine')),('Car sunshades & covers',lambda p:'car' in p['id']),('Shade & garden umbrellas',lambda p:True)],
'bedding':[('Blankets',lambda p:p['id'].startswith('blanket')),('Duvet sets',lambda p:'set' in p['id']),('Duvets',lambda p:'duvet' in p['id']),('Bedsheets',lambda p:True)],
'kettles':[('Toasters & sandwich makers',lambda p:p['id'].startswith(('toaster','sandwich-'))),('Electric kettles',lambda p:True)],
'microwaves':[('Microwaves with grill',lambda p:'grill' in p['name'].lower()),('Digital & manual microwaves',lambda p:True)],
'business':[('Shop scales',lambda p:p['id'].startswith('scale')),('Sugarcane juice machines',lambda p:'sugarcane' in p['id']),('Popcorn machines',lambda p:True)],
'bags':[('Kindergarten bags',lambda p:'kindergarten' in p['name'].lower()),('School & laptop backpacks',lambda p:True)],
'furniture':[('TV stands',lambda p:True)],
'irons':[('Steam irons',lambda p:'steam' in p['name'].lower()),('Dry irons',lambda p:True)],
'blenders':[('Blenders & grinders',lambda p:True)],
'mugs':[('Plastic & melamine mugs',lambda p:re.search(r'plastic|melamine',p['name'],re.I)),('Gift box mugs',lambda p:'gift' in p['name'].lower()),('Gold mugs',lambda p:'gold' in p['name'].lower()),('Black mugs',lambda p:re.search(r'black|dark',p['name'],re.I)),
        ('White & embossed mugs',lambda p:re.search(r'white|embossed|cream|macchiato',p['name'],re.I)),('Printed & coloured mugs',lambda p:True)],
'glass':[('Unbreakable acrylic glasses',lambda p:re.search('acrylic|unbreakable|kumi kumi|kenstar cold',p['name'],re.I)),('Water sets',lambda p:'set' in p['name'].lower()),('Wine, whisky & party glasses',lambda p:re.search('wine|whisky|champagne|martini|milkshake|horn',p['name'],re.I)),('Drinking glasses',lambda p:True)],
'plates':[('Soup plates & platters',lambda p:re.search('soup plates|platter',p['name'],re.I) and 'melamine' not in p['name'].lower()),('Plastic plates',lambda p:'plastic' in p['name'].lower()),('Bowls',lambda p:'bowl' in p['name'].lower()),('Melamine plates',lambda p:'melamine' in p['name'].lower()),('Stoneware plates',lambda p:'stoneware' in p['name'].lower()),('Ceramic & opal plates',lambda p:True)],
'trays':[('Tray sets',lambda p:p['id'].startswith(('tray-karuri','tray-house','tray-wood'))),('Steel trays & sinia plates',lambda p:re.search('steel',p['name'],re.I)),('Acrylic trays',lambda p:'acr' in p['id'] or 'clear' in p['id']),('Melamine & plastic trays',lambda p:True)],
'storage':[('Shoe racks',lambda p:p['id'].startswith('shoe-rack')),('Lunch boxes',lambda p:p['id'].startswith('lunchbox')),('Freezer & zip bags',lambda p:'freezer' in p['name'].lower() or 'zip' in p['name'].lower()),('Sugar dishes',lambda p:'sugar' in p['name'].lower() and 'jar' not in p['name'].lower() and 'shaker' not in p['name'].lower()),('Spice jars & shakers',lambda p:re.search('spice|shaker',p['name'],re.I)),('Storage jars & containers',lambda p:True)],
'kitchen':[('Kitchen tools & gadgets',lambda p:p['id'] in ('kit-jar-opener','bbq-gloves-800','garlic-tools','splash-shield')),('Cupboard organisers',lambda p:p['id'] in ('kit-shelf-raiser','kit-drawer-organizer')),('Baking & pastry tools',lambda p:p['id'] in ('kit-dumpling-4','kit-cake-turntable','kit-chapati-press')),('Oil bottles & sprayers',lambda p:p['id'].startswith('oil-')),('Kitchen tools & gadgets',lambda p:p['id'].startswith('utensils-')),('Kitchen tools & gadgets',lambda p:p['id'].startswith('kinu')),('Dish soap pumps & caddies',lambda p:p['id'].startswith(('caddy-','disp-','soap-'))),('Dish racks & kitchen racks',lambda p:'dish-rack' in p['id'] or p['id']=='rack-fold-5tier'),('Kitchen tools & gadgets',lambda p:p['id'].startswith('foil-sticker')),('Kitchen tools & gadgets',lambda p:re.search('scoop|opener|cutter|squeezer|peeler|grater|piping',p['name'],re.I)),('Measuring cups & jugs',lambda p:re.search('jug|measuring cups',p['name'],re.I)),('Kitchen towels & holders',lambda p:re.search('towel|hold|mug tree|roll|pair',p['name'],re.I) or p['id'].startswith('hold')),('Dish soap pumps & caddies',lambda p:True)],
'mats':[('Carpets & rugs',lambda p:p['id'].startswith('carpet')),('Table mats & placemats',lambda p:p['id'].startswith('tablemat')),('Door, floor & kitchen mats',lambda p:True)],
'cutlery':[('Cutlery sets',lambda p:p['id'].startswith('cutlery')),('Spoons & forks',lambda p:p['id'].startswith(('fork','spoon-kzh','spoon-gold','spoon-heavy'))),('Serving spoons & ladles',lambda p:p['id'].startswith(('ladle','spoon-melamine','spoon-serving'))),('Spoon & cutlery holders',lambda p:p['id'].startswith('spoonholder')),('Kitchen & butcher knives',lambda p:True)],
'home':[('Office & desk',lambda p:p['id'].startswith('desk-')),('Garden & outdoor',lambda p:p['id'].startswith(('solar-','trek-','garden-'))),('Cleaning supplies',lambda p:p['id'].startswith(('clean-','gloves-silicone','vac-','laundry-'))),('Pill organisers',lambda p:p['id'].startswith('pill-')),('Door curtains',lambda p:p['id'].startswith('curtain-')),('Health & personal care',lambda p:p['id'].startswith(('bp-','shaver-'))),('Appliance accessories',lambda p:p['id'].startswith('footpad')),('Garden & outdoor',lambda p:p['id'].startswith('hose')),('Cleaning',lambda p:p['id'].startswith('sweeper')),('Storage & organisers',lambda p:True)],
'jugs':[('Glass jugs',lambda p:'glass' in p['name'].lower()),('Plastic & acrylic jugs',lambda p:True)],
'decor':[('Christmas trees',lambda p:p['id'].startswith('tree-')),('Christmas pajamas',lambda p:p['id'].startswith('pj-')),('Garlands, wreaths & lights',lambda p:p['id'].startswith(('garland','wreath','lights-'))),('Table runners, banners & party',lambda p:p['id'].startswith(('runner','banner','balloon','cupcard','hat-','giftbox','bag-velvet'))),('Bows, stockings & ornaments',lambda p:p['id'].startswith(('bow-','ornament-','stocking','sign-','ribbon','pick-'))),('Christmas mats',lambda p:p['id'].startswith('mat-xmas')),('Christmas cushion covers',lambda p:True)],
'bathroom':[('Shower caddies & organisers',lambda p:p['id'].startswith('bath-')),('Toilet brushes',lambda p:'toilet brush' in p['name'].lower()),('Bathroom sets',lambda p:p['id'].startswith('bathset')),('Soap & lotion dispensers',lambda p:'dispenser' in p['name'].lower()),('Toilet mat sets',lambda p:'toilet' in p['name'].lower()),('Bathroom accessories',lambda p:True)],
}
def assign(P):
    for p in P:
        p.pop('sub',None)
        for lab,f in SUBS.get(p['cat'],[]):
            if f(p): p['sub']=lab; break
    return {c:[l for l,_ in v if any(p.get('sub')==l and p['cat']==c for p in P)] for c,v in SUBS.items()}
def apply():
    import sys
    P=json.load(open('products.json')); order=assign(P)
    json.dump(P,open('products.json','w'),ensure_ascii=False,indent=1)
    h=open('index.html').read()
    a=h.index('const PRODUCTS = ');b=h.index('];',a)+1
    h=h[:a]+'const PRODUCTS = '+json.dumps(P,ensure_ascii=False)+h[b:]
    if 'const SUBS = ' in h: h=re.sub(r'const SUBS = \{.*?\};','const SUBS = '+json.dumps(order,ensure_ascii=False)+';',h,count=1)
    else: h=h.replace('const CATNAME = ','const SUBS = '+json.dumps(order,ensure_ascii=False)+';\nconst CATNAME = ',1)
    open('index.html','w').write(h); print('subs applied')
if __name__=='__main__' and len(__import__('sys').argv)>1: apply()
elif __name__=='__main__':
    P=json.load(open('products.json')); order=assign(P)
    for c,ls in order.items():
        for l in ls: print(c,'|',l,'|',', '.join(re.sub(r'^[^\w(]+','',p['name'])[:30] for p in P if p.get('sub')==l and p['cat']==c))
