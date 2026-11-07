import json, html, os, re, shutil, runpy, datetime
# SITE_SRC: kit data dir (build_pages.py, kit media, site-entry dirs). SITE_OUT: output dir (the site checkout by default).
ST=os.environ.get('SITE_SRC') or (os.path.dirname(os.path.abspath(__file__)) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'build_pages.py')) else '/workspace/deliver/kits/store')
OUT=os.path.abspath(os.environ.get('SITE_OUT','/workspace/site'))
os.chdir(ST); g=runpy.run_path('build_pages.py'); K=g['K']; LICL="Lite is free under the MIT License. Pro is sold under a commercial per-seat EULA: you can ship unlimited commercial and non-commercial games; you may not resell or redistribute the kit's source or assets as a template. Bundled art/audio is CC0."
BASE='https://openclawaimac.github.io'; TODAY=os.environ.get('SITE_DATE') or datetime.date.today().isoformat()
X={'factory-core':dict(genre='factory / automation',slug='factory-core',lastmod='2026-10-22',itch='https://huginhelm.itch.io/factory-core',repo='openclawaimac/godot-factory-core-lite',lite_tests=65,lite_short='Deterministic, headless belt + machine simulation: two-lane belts with side-loading and backpressure, Mk1 recipe machines, round-robin splitter, fair merger, JSON/.tres content, stats and save/load. 65 tests.'),
 'godot-survival-core':dict(genre='survival crafting',slug='godot-survival-core',lastmod='2026-10-22',itch='https://huginhelm.itch.io/godot-survival-core',repo='openclawaimac/godot-survival-core-lite',lite_tests=48,lite_short='Hunger/thirst needs, day/night clock, slot inventory, data-driven hand crafting and gatherables as pure-logic, headless-testable systems. 48 tests.'),
 'godot-tower-defense-core':dict(genre='tower defense',slug='godot-tower-defense-core',lastmod='2026-10-22',itch='https://huginhelm.itch.io/godot-tower-defense-core',repo='openclawaimac/godot-tower-defense-core-lite',lite_tests=54,lite_short='The full TD logic: JSON towers/enemies/waves/map, 4 targeting modes, splash, slow, flyers, armor, upgrades and a 3-wave demo. 54 tests.'),
 'godot-rts-advanced':dict(genre='3D real-time strategy (RTS)',slug='godot-rts-advanced',lastmod='2026-10-22',itch='https://huginhelm.itch.io/godot-rts-advanced',repo='openclawaimac/godot-rts-advanced-lite',lite_tests=114,lite_short='The RTS control layer: box selection, control groups, orders, formations, grid A*, production queue, capturable income points, camera, key rebinding and en/fr localization, with a primitive-shape demo. 114 tests.')}
# Kits with a prepared site entry (custom page, e.g. required media captions) instead of a generated page.
# The entry's PRICE_TBD token is replaced with the approved price.
# Optional entry keys: lite_tests/tests (counts are never required), card_kind (index card line, default 'kit / addon'),
# card_note (small print on the index card), repo_name/repo_note (llms.txt source-repo line), lastmod (sitemap date, default today).
E={'godot-destruction-core':dict(name='Godot Destruction Core',genre='2D destruction',slug='godot-destruction-core',price='16.00',lastmod='2026-10-22',
   card_note='Built with Godot Destruction Core — footage from Toonforce (in development)',itch='https://huginhelm.itch.io/godot-destruction-core',repo='openclawaimac/godot-destruction-core-lite',lite_tests=82,
   lite_short='Destructible cell terrain, damage shapes, single detonations and deterministic structural collapse with falling pieces, rubble and crush damage, plus a two-player demo. 82 tests.',
   short='Adds chain reactions, deterministic fire, load-based stress, image/mask import, debug overlays, command log/replay and the Fire Sale demo. 142 tests.'),
 'godot-vfx-core-2d':dict(name='VFX Core 2D for Godot 4',genre='2D particle effects / VFX',slug='godot-vfx-core-2d',price='13.00',lastmod='2026-11-07',
   itch='https://huginhelm.itch.io/vfx-core-2d-godot-4',repo='openclawaimac/godot-vfx-core-lite',card_kind='pack',repo_name='VFX Core 2D',repo_note='MIT source, README',
   lite_short='The full runtime (one-call API, pooling, particle budget, pixel mode, camera shake, hit-stop), the demo browser, the Destruction Core hook and 8 effects plus hit_flash (32 presets).',
   short='141 effects and 512 presets in nine themes, light-background and pixel presets, and hooks for Destruction Core, Tower Defense, Factory, Survival and RTS kits.')}
X.update(E)
e=html.escape; strip=lambda s:s.replace('`','')
# Optional test counts: render nothing (no '()' or 'None tests') when a kit has no count.
tc=lambda n,f:f.format(n) if n not in (None,'') else ''
CSS="body{font-family:system-ui,sans-serif;max-width:960px;margin:auto;padding:1rem;background:#14161c;color:#e6e6ea;line-height:1.5}a{color:#6cb6ff}img{max-width:100%;height:auto;border-radius:6px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.8rem}.p{background:#22252e;padding:1rem;border-radius:8px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #333;padding:.3rem .5rem;text-align:left}small{color:#999}"
def head(title,desc,url,img,ld):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="text/plain" title="llms.txt" href="{BASE}/llms.txt">
<script type="application/ld+json">
{json.dumps(ld,indent=1,ensure_ascii=False)}
</script><style>{CSS}</style></head><body>'''
os.makedirs(OUT,exist_ok=True); full=[]; cards=[]; llms=[]
for k,c in K.items():
    x=X[k]; d=f'{OUT}/{k}'; os.makedirs(d+'/screenshots',exist_ok=True)
    shutil.copy(f'{k}/{c["cover"]}',d); shutil.copy(f'{k}/preview.gif',d)
    for s in c['shots']: shutil.copy(f'{k}/screenshots/{s}.png',d+'/screenshots')
    url=f'{BASE}/{k}/'; gh=f'https://github.com/{x["repo"]}'; h1=f'{c["name"]} – Godot 4 {x["genre"]} starter kit / template'
    desc=f'{c["name"]}: a Godot 4 {x["genre"]} starter kit and project template in typed GDScript. Free MIT Lite on GitHub{tc(x.get("lite_tests")," ({} headless tests)")}, Pro €{c["price"]} on itch.io{tc(c.get("tests")," ({} headless tests)")}.'
    offers=[{"@type":"Offer","name":f"{c['name']} Lite","price":"0.00","priceCurrency":"EUR","availability":"https://schema.org/InStock","url":gh,"description":"Free edition, MIT License"},
            {"@type":"Offer","name":f"{c['name']} Pro","price":c['price'],"priceCurrency":"EUR","availability":"https://schema.org/InStock","url":x['itch'],"description":"Full kit, commercial per-seat EULA"}]
    ld=[{"@context":"https://schema.org","@type":["Product","SoftwareApplication"],"@id":url+"#product","name":c['name'],"alternateName":f"Godot 4 {x['genre']} starter kit","description":desc,"url":url,
        "image":[url+c['cover']]+[f'{url}screenshots/{s}.png' for s in c['shots']],"sku":f"{k}-{c['version']}","softwareVersion":c['version'],
        "applicationCategory":"DeveloperApplication","applicationSubCategory":"Game development template (Godot Engine 4)","operatingSystem":"Windows, macOS, Linux (Godot 4.7)",
        "programmingLanguage":"GDScript","softwareRequirements":"Godot Engine 4.7","keywords":', '.join(c['tags']+['starter kit','godot template']),
        "brand":{"@type":"Brand","name":"huginhelm"},"author":{"@type":"Organization","name":"huginhelm","url":BASE+"/"},"license":"https://opensource.org/licenses/MIT",
        "codeRepository":gh,"sameAs":[x['itch'],gh],"offers":offers},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"huginhelm Godot kits","item":BASE+"/"},{"@type":"ListItem","position":2,"name":c['name'],"item":url}]}]
    li=lambda xs:''.join(f'<li>{e(strip(i))}</li>' for i in xs)
    cmp=''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(p)}</td></tr>' for a,b,p in c['compare'])
    page=head(f'{h1} | huginhelm',desc,url,url+c['cover'],ld)+f'''
<nav><a href="../">← All huginhelm Godot kits</a></nav>
<header><h1>{e(h1)}</h1><p><strong>{e(c['tagline'])}</strong></p><p>{e(desc)}</p>
<img src="{c['cover']}" alt="{e(c['name'])} – Godot 4 {x['genre']} starter kit cover" width="630" height="500"></header>
<section class="p"><h2>Get it</h2><ul><li><strong>Lite (free, MIT):</strong> <a href="{gh}">{gh}</a> – {e(x['lite_short'])}</li>
<li><strong>Pro (€{c['price']} EUR, commercial EULA):</strong> <a href="{x['itch']}">{x['itch']}</a> – {tc(c.get('tests'),'{} passing headless tests, ')}playable demo</li></ul>
<p>Engine: Godot 4.7 (tested on 4.7.2) · Language: typed GDScript · Version {c['version']} · Run tests: <code>bash tools/run_tests.sh</code></p></section>
<h2>Lite vs Pro</h2><table><tr><th>Feature</th><th>Lite (free, MIT)</th><th>Pro (€{c['price']}, EULA)</th></tr>{cmp}</table>
<h2>Features (Pro)</h2><ul>{li(c['features'])}</ul>
<h2>Not included</h2><ul>{li(c['notdo'])}</ul>
<h2>Preview</h2><img src="preview.gif" alt="{e(c['name'])} gameplay preview" loading="lazy">
<h2>Screenshots</h2><div class="g">{''.join(f'<img src="screenshots/{s}.png" alt="{e(c["name"])} screenshot: {s[3:].replace("_"," ")}" loading="lazy" width="1280" height="720">' for s in c['shots'])}</div>
<h2>Assets &amp; licence</h2><p>{e(c['assets'])}.</p><p>{e(LICL)}</p><p><small>Code and docs written with AI coding agents. Machine-readable summary: <a href="../llms.txt">llms.txt</a>.</small></p>
</body></html>'''
    open(d+'/index.html','w').write(page)
    cards.append(f'<article class="p"><a href="{k}/"><img src="{k}/{c["cover"]}" alt="{e(c["name"])} cover" width="630" height="500" loading="lazy"></a><h2><a href="{k}/">{e(c["name"])}</a></h2><p>Godot 4 {x["genre"]} starter kit / template.</p><p><strong>Lite (free, MIT):</strong> {e(x["lite_short"])}</p><p><strong>Pro (€{c["price"]}):</strong> {e(c["short"])}</p><p><a href="{gh}">GitHub (Lite)</a> · <a href="{x["itch"]}">itch.io (Pro)</a></p></article>')
    llms.append(f'- [{c["name"]} – Godot 4 {x["genre"]} starter kit]({url}): Lite (free, MIT, {gh}): {x["lite_short"]} Pro (€{c["price"]}, {x["itch"]}): {c["short"]}')
    full.append(f'# {h1}\n\nURL: {url}\nLite (free, MIT{tc(x.get("lite_tests"),", {} tests")}): {gh}\nPro (€{c["price"]} EUR, commercial per-seat EULA{tc(c.get("tests"),", {} tests")}): {x["itch"]}\nEngine: Godot 4.7 (tested 4.7.2), typed GDScript, version {c["version"]}. Run tests: `bash tools/run_tests.sh`.\n\n{c["tagline"]}\n\n## Features (Pro)\n'+'\n'.join('- '+i for i in c['features'])+'\n\n## Not included\n'+'\n'.join('- '+i for i in c['notdo'])+'\n\n## Lite vs Pro\n| Feature | Lite (MIT) | Pro (EULA) |\n|---|---|---|\n'+'\n'.join(f'| {a} | {b} | {p} |' for a,b,p in c['compare'])+f'\n\nAssets: {c["assets"]}.\n')
for k,x in E.items():
    src=f'{k}/site-entry'; d=f'{OUT}/{k}'; shutil.rmtree(d,ignore_errors=True); shutil.copytree(f'{src}/{k}',d)
    pg=open(d+'/index.html').read().replace('PRICE_TBD',x['price']); assert 'PRICE_TBD' not in pg; open(d+'/index.html','w').write(pg)
    url=f'{BASE}/{k}/'; gh=f'https://github.com/{x["repo"]}'
    if os.path.exists(f'{k}/icon_256.png'): shutil.copy(f'{k}/icon_256.png',d+'/icon.png')
    cards.append(f'<article class="p"><a href="{k}/"><img src="{k}/cover_630x500.png" alt="{e(x["name"])} cover" width="630" height="500" loading="lazy"></a><h2><a href="{k}/">{e(x["name"])}</a></h2><p>Godot 4 {x["genre"]} {x.get("card_kind","kit / addon")}.</p><p><strong>Lite (free, MIT):</strong> {e(x["lite_short"])}</p><p><strong>Pro (€{x["price"]}):</strong> {e(x["short"])}</p><p><a href="{gh}">GitHub (Lite)</a> · <a href="{x["itch"]}">itch.io (Pro)</a></p>'+(f'<p><small>{e(x["card_note"])}</small></p>' if x.get('card_note') else '')+'</article>')
    llms.append(open(f'{src}/llms.txt.line').read().strip().replace('PRICE_TBD',x['price']))
    full.append(open(f'{src}/llms-full.section.md').read().replace('PRICE_TBD',x['price']))
    K[k]=dict(name=x['name'])
ld={"@context":"https://schema.org","@type":"ItemList","name":"huginhelm Godot 4 starter kits","url":BASE+"/","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/{k}/","name":K[k]['name']} for i,k in enumerate(K)]}
desc='Godot 4 starter kits and project templates by huginhelm: factory/automation, survival crafting, tower defense, 3D real-time strategy and 2D destruction, plus a 2D VFX pack. Typed GDScript, headless-tested, free MIT Lite editions plus Pro editions in EUR.'
open(f'{OUT}/index.html','w').write(head('huginhelm – Godot 4 starter kits & templates (factory, survival, tower defense, RTS, 2D destruction, 2D VFX)',desc,BASE+'/',f'{BASE}/factory-core/cover_630x500.png',[ld,{"@context":"https://schema.org","@type":"Organization","name":"huginhelm","url":BASE+"/","sameAs":["https://huginhelm.itch.io","https://github.com/openclawaimac"]}])+
 f'<h1>huginhelm – Godot 4 starter kits &amp; templates</h1><p>{e(desc)}</p><div class="g">{"".join(cards)}</div><p><small>For AI agents: <a href="llms.txt">llms.txt</a> · <a href="llms-full.txt">llms-full.txt</a> · <a href="sitemap.xml">sitemap</a></small></p></body></html>')
open(f'{OUT}/llms.txt','w').write(f'# huginhelm Godot 4 starter kits\n\n> Godot 4 (4.7) game starter kits / project templates in typed GDScript: factory & automation, survival crafting, tower defense, 3D real-time strategy (RTS), 2D destruction, plus a 2D VFX / particle effects pack. Each kit has a free MIT "Lite" edition on GitHub and a paid "Pro" edition (commercial per-seat EULA, prices in EUR) on itch.io. All kits run headless tests via `bash tools/run_tests.sh`.\n\nEach Lite repo contains AGENTS.md and llms.txt describing structure and extension points. Pro keeps the same API as Lite, so projects upgrade without code changes.\n\n## Kits\n\n'+'\n'.join(llms)+'\n\n## Source repositories\n\n'+'\n'.join(f'- [{X[k].get("repo_name",K[k]["name"])} Lite on GitHub](https://github.com/{X[k]["repo"]}): {X[k].get("repo_note","MIT source, README, AGENTS.md")}' for k in K)+f'\n\n## Optional\n\n- [Full details for all kits]({BASE}/llms-full.txt): features, limitations, Lite vs Pro tables\n- [huginhelm on itch.io](https://huginhelm.itch.io): store pages and web demos\n')
open(f'{OUT}/llms-full.txt','w').write('# huginhelm Godot 4 starter kits – full details\n\n> Godot 4.7 starter kits / templates. Lite = free MIT on GitHub, Pro = paid commercial EULA on itch.io (EUR).\n\n'+'\n\n'.join(full))
open(f'{OUT}/robots.txt','w').write(''.join(f'User-agent: {a}\nAllow: /\n\n' for a in ['*','GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','Claude-User','Claude-SearchBot','anthropic-ai','PerplexityBot','Perplexity-User','Google-Extended','Applebot-Extended','CCBot','Bytespider','Meta-ExternalAgent','Amazonbot','DuckAssistBot','cohere-ai','MistralAI-User','xAI-Bot','Grok'])+f'Sitemap: {BASE}/sitemap.xml\n')
open(f'{OUT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{m}</lastmod></url>\n' for u,m in [(BASE+'/',TODAY)]+[(f'{BASE}/{k}/',X[k].get('lastmod',TODAY)) for k in K]+[(BASE+'/llms.txt',TODAY),(BASE+'/llms-full.txt',TODAY)])+'</urlset>\n')
open(f'{OUT}/.nojekyll','w').write('')
open(f'{OUT}/README.md','w').write(f'# huginhelm Godot 4 starter kits\n\nSource of {BASE}/ – generated by build_site.py. Kits: '+', '.join(f'[{K[k]["name"]}]({BASE}/{k}/)' for k in K)+'.\n')
if os.path.abspath(__file__)!=os.path.join(OUT,'build_site.py'): shutil.copy(__file__,OUT+'/build_site.py')
