import json, html, os
P=json.load(open('/home/claude/site/products.json'))
SITE='https://vyotevyetu.github.io/'
os.makedirs('/home/claude/site/p',exist_ok=True)
for p in P:
    e=lambda s: html.escape(s, quote=True)
    title=f"{p['name']} · KES {p['price']:,}"
    desc=f"{p['detail']} ({p['unit']}). Order on WhatsApp from Vyetu Vyote, delivery in Nairobi & worldwide."
    img=f"{SITE}img/{p['id']}.jpg"; url=f"{SITE}p/{p['id']}.html"; dest=f"../#p={p['id']}"
    open(f"/home/claude/site/p/{p['id']}.html",'w').write(f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Vyetu Vyote</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="product"><meta property="og:site_name" content="Vyetu Vyote">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{img}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={dest}">
<style>body{{margin:0;font:16px system-ui,sans-serif;background:#f6f5f0;color:#14231c;display:grid;place-items:center;min-height:100vh;text-align:center;padding:20px}}img{{max-width:280px;border-radius:16px}}a{{color:#0f3d2e;font-weight:700}}</style>
</head><body><div><img src="../img/t/{p['id']}.jpg" alt=""><p><b>{e(p['name'])}</b><br>KES {p['price']:,}</p><a href="{dest}">Open in the shop</a></div>
<script>location.replace({json.dumps(dest)})</script></body></html>''')
print(len(P),'pages')
