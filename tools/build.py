# -*- coding: utf-8 -*-
"""Gerador estático da v1 (HTML/CSS/JS puros). Uso: BASE_URL=https://seu-site python3 tools/build.py"""
import os, json, shutil, html
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
from sitedata import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V0, V1 = os.path.join(ROOT, "v0"), os.path.join(ROOT, "v1")
P = urlparse(BASE).path.rstrip("/")          # prefixo se publicar em subpasta (ex.: GitHub Pages de projeto)
u = lambda path: P + path                    # link interno
abs_ = lambda path: BASE + path if path != "/" else BASE + "/"
esc = html.escape
W = [480, 800, 1200]

# ---------- imagens: WebP em 3 tamanhos, nomes claros, og:image 1200x630 ----------
def build_images():
    out = os.path.join(V1, "imagens"); os.makedirs(out, exist_ok=True)
    for k, (orig, name, alt) in IMAGES.items():
        im = Image.open(os.path.join(V0, "imagens", orig)).convert("RGB")
        for w in W:
            im.resize((w, round(w * im.height / im.width)), Image.LANCZOS).save(os.path.join(out, f"{name}-{w}.webp"), "WEBP", quality=74, method=6)
        top = (im.height - round(im.width * 630 / 1200)) // 2
        og = im.crop((0, top, im.width, top + round(im.width * 630 / 1200))).resize((1200, 630), Image.LANCZOS)
        og.save(os.path.join(out, f"og-{name}.jpg"), "JPEG", quality=76, optimize=True)
    # logo e ícones (gerados, sem direitos de terceiros)
    f = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", s)
    def icon(size):
        i = Image.new("RGB", (size, size), "#fbf8f1"); d = ImageDraw.Draw(i)
        d.rounded_rectangle((size*.06, size*.06, size*.94, size*.94), radius=size*.22, fill="#2e6b3f")
        d.text((size/2, size/2), "C", font=f(int(size*.62)), fill="white", anchor="mm"); return i
    icon(512).save(os.path.join(out, "logo-casa-do-cha-serrano.png"), optimize=True)
    icon(180).save(os.path.join(V1, "apple-touch-icon.png"), optimize=True)
    icon(48).save(os.path.join(V1, "favicon.ico"), sizes=[(32, 32), (48, 48)])
    open(os.path.join(V1, "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2e6b3f"/><text x="32" y="45" font-family="Georgia,serif" font-size="40" font-weight="bold" fill="#fff" text-anchor="middle">C</text></svg>')

def img(key, sizes, eager=False, width=1200, h=800, hi=False):
    _, name, alt = IMAGES[key]
    ss = ", ".join(f"{u('/imagens/'+name+'-'+str(w)+'.webp')} {w}w" for w in W)
    a = 'loading="eager" fetchpriority="high"' if hi else ('loading="eager"' if eager else 'loading="lazy"')
    return f'<img src="{u("/imagens/"+name+"-800.webp")}" srcset="{ss}" sizes="{sizes}" alt="{esc(alt)}" width="{width}" height="{h}" {a} decoding="async">'
def og(key): return abs_("/imagens/og-" + IMAGES[key][1] + ".jpg"), IMAGES[key][2]

# ---------- peças de layout ----------
def crumbs(items):  # items: [(nome, url|None)]
    li = "".join(f'<li><a href="{u(x)}">{esc(n)}</a></li>' if x else f'<li aria-current="page">{esc(n)}</li>' for n, x in items)
    return f'<nav class="migalhas" aria-label="Você está em"><ol>{li}</ol></nav>'
def crumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i+1, "name": n, **({"item": abs_(x)} if x else {})} for i, (n, x) in enumerate(items)]}
def card(p, lvl=2, eager=False):
    return (f'<article class="caixa card">{img(p["img"], "(max-width:780px) calc(100vw - 80px), 260px", eager)}'
            f'<h{lvl}>{esc(p["name"])}</h{lvl}><p class="preco">{p["price_str"]}</p><p class="peso">{p["peso"]}</p>'
            f'<a href="{u(p["url"])}">Ver detalhes: {esc(p["name"].lower())}</a></article>')

NAV = [("Início", "/"), ("Chás", "/chas/"), ("Acessórios", "/acessorios/"), ("Quem somos", "/sobre/"), ("Contato", "/contato/")]
def layout(path, title, desc, ogkey, body, ld, index=True, current=None):
    ogimg, ogalt = og(ogkey)
    nav = "".join(f'<a href="{u(x)}"{" aria-current=\"page\"" if x == path or (x != "/" and path.startswith(x)) else ""}>{n}</a>' for n, x in NAV)
    nav += f'<a href="{u("/carrinho/")}">Carrinho (<span data-cart-count>0</span>)</a>'
    ldj = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>\n' for b in ld)
    robots = "" if index else '<meta name="robots" content="noindex,follow">\n'
    n = NAP
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="uvLSXGaODWYup1hTf_RrvajP8Jx6eBySQoROAYKOhYo">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{abs_(path)}">
{robots}<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{abs_(path)}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(ogalt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2e6b3f">
<link rel="icon" href="{u('/favicon.ico')}" sizes="48x48">
<link rel="icon" href="{u('/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{u('/apple-touch-icon.png')}">
<link rel="stylesheet" href="{u('/css/estilo.css')}">
{ldj}</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="topo-in">
    <a class="logo" href="{u('/')}"><span class="logo-sel" aria-hidden="true">C</span>{BRAND}</a>
    <nav class="menu" aria-label="Principal">{nav}</nav>
    <form class="busca-form" role="search" action="{u('/busca/')}" method="get"><label class="sr-only" for="q">Buscar chás e kits</label><input id="q" name="q" type="search" placeholder="Buscar chás" required><button type="submit">Buscar</button></form>
  </div>
</header>
<main id="conteudo" class="conteudo">
{body}
</main>
<footer class="rodape">
  <nav class="rodape-menu" aria-label="Rodapé"><a href="{u('/chas/')}">Chás</a><a href="{u('/acessorios/')}">Acessórios</a><a href="{u('/sobre/')}">Quem somos</a><a href="{u('/contato/')}">Contato</a><a href="{u('/busca/')}">Buscar produtos</a></nav>
  <address>{BRAND} · {n["street"]}, {n["district"]}, {n["city"]}-{n["region"]} · CEP {n["zip"]} · <a href="tel:{n["phone_intl"]}">{n["phone"]}</a></address>
  <p>© 2026 {BRAND}. Todos os direitos reservados.</p>
</footer>
<script src="{u('/js/catalogo.js')}" defer></script>
<script src="{u('/js/loja.js')}" defer></script>
</body>
</html>
'''

def write(path, content):
    d = os.path.join(V1, path.strip("/")); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(content)

ORG = {"@type": "Organization", "@id": abs_("/#organizacao"), "name": BRAND, "url": abs_("/"),
       "logo": abs_("/imagens/logo-casa-do-cha-serrano.png"), "email": NAP["email"],
       "address": {"@type": "PostalAddress", "streetAddress": NAP["street"], "addressLocality": NAP["city"], "addressRegion": NAP["region"], "postalCode": NAP["zip"], "addressCountry": "BR"},
       "contactPoint": {"@type": "ContactPoint", "telephone": NAP["phone_intl"], "contactType": "customer service", "areaServed": "BR", "availableLanguage": "pt-BR"}}
CTX = "https://schema.org"
def ld(*blocks): return [{"@context": CTX, **b} for b in blocks]
pages_out = []   # (path, title, desc, indexable)

def build_pages():
    # HOME
    t, d, k, ix = STATIC["home"][1:]
    feat = [PBY[s] for s in ("cha-verde-sencha", "cha-hibisco-laranja", "kit-presente-cha-verde")]
    body = f'''<section class="hero">
  <div>
    <h1>Chás selecionados, direto de Catanduva para todo o Brasil</h1>
    <p>A {BRAND} vende chás em folhas e infusões de qualidade: chá verde, chá preto, hibisco, camomila e capim-limão, embalados de forma artesanal.</p>
    <div class="selos"><span class="selo">Folhas selecionadas</span><span class="selo">Embalagem artesanal</span><span class="selo">Envio para todo o Brasil</span></div>
  </div>
  {img("banner", "(max-width:780px) calc(100vw - 100px), 500px", hi=True)}
</section>
<section aria-labelledby="cats">
  <h2 id="cats">Escolha por categoria</h2>
  <div class="grade dois">
    <article class="caixa chamada"><h3>Chás em folhas e infusões</h3><p>Cinco opções para o dia a dia: do chá verde sencha ao chá de camomila para a noite.</p><p><a href="{u('/chas/')}">Ver todos os chás</a></p></article>
    <article class="caixa chamada"><h3>Kits presente e acessórios</h3><p>Caixa de presente com chá verde, pronta para entregar a quem você gosta.</p><p><a href="{u('/acessorios/')}">Ver kits e acessórios</a></p></article>
  </div>
</section>
<section aria-labelledby="dest">
  <h2 id="dest">Destaques da loja</h2>
  <div class="grade">{"".join(card(p, 3) for p in feat)}</div>
</section>
<section aria-labelledby="loja">
  <h2 id="loja">Uma loja de chás de família</h2>
  <p>Somos uma loja familiar de Catanduva-SP que importa e embala chás desde 2019. <a href="{u('/sobre/')}">Conheça nossa história</a> ou <a href="{u('/contato/')}">fale com a gente</a>.</p>
</section>'''
    write("/", layout("/", t, d, k, body, ld(ORG, {"@type": "WebSite", "name": BRAND, "url": abs_("/"), "inLanguage": "pt-BR", "publisher": {"@id": ORG["@id"]}})))
    pages_out.append(("/", t, d, True))

    # CATEGORIAS
    texts = {"chas": f'''<p>Aqui você encontra os chás em folhas e infusões da {BRAND}, todos em pacotes de 40 a 60 g. Cada produto tem página própria com descrição, modo de preparo e avaliações.</p>''',
             "acessorios": '<p>Kits prontos para presentear. Novos acessórios chegam em breve.</p>'}
    for ck, c in CATS.items():
        items = [p for p in PRODUCTS if p["cat"] == ck]
        cr = [("Início", "/"), (c["name"], None)]
        extra = ""
        if ck == "chas":
            extra = f'''<section aria-labelledby="esc"><h2 id="esc">Como escolher seu chá</h2>
<p>Para começar o dia, o <a href="{u(PBY['cha-verde-sencha']['url'])}">chá verde sencha</a> tem sabor suave, e o <a href="{u(PBY['cha-preto-assam']['url'])}">chá preto Assam</a> é encorpado e combina com leite. Para dias quentes, experimente o <a href="{u(PBY['cha-hibisco-laranja']['url'])}">chá de hibisco com laranja</a> gelado ou o <a href="{u(PBY['cha-capim-limao']['url'])}">chá de capim-limão</a>. À noite, o <a href="{u(PBY['cha-camomila-organica']['url'])}">chá de camomila orgânica</a> é uma boa pedida. Quer presentear? Veja o <a href="{u(PBY['kit-presente-cha-verde']['url'])}">kit presente de chá verde</a>.</p></section>'''
        else:
            extra = f'<p>Procurando chá em folhas? Veja a <a href="{u("/chas/")}">categoria de chás</a>.</p>'
        body = f'''{crumbs(cr)}
<h1>{c["h1"]}</h1>
{texts[ck]}
<div class="grade">{"".join(card(p, 2, i < 3) for i, p in enumerate(items))}</div>
{extra}'''
        il = {"@type": "ItemList", "name": c["h1"], "itemListElement": [{"@type": "ListItem", "position": i+1, "url": abs_(p["url"]), "name": p["name"]} for i, p in enumerate(items)]}
        write(c["url"], layout(c["url"], c["title"], c["desc"], c["img"], body, ld(il, crumb_ld(cr))))
        pages_out.append((c["url"], c["title"], c["desc"], True))

    # PRODUTOS
    for p in PRODUCTS:
        c = CATS[p["cat"]]; cr = [("Início", "/"), (c["name"], c["url"]), (p["name"], None)]
        rev = "".join(f'<blockquote class="caixa citacao" data-nota="{n}"><p class="nota"><span aria-hidden="true">{"★"*n}{"☆"*(5-n)}</span><span class="sr-only">Nota {n} de 5</span></p><p>{esc(tx)}</p><footer>{esc(au)}</footer></blockquote>' for n, au, tx in p["reviews"])
        rel = "".join(card(PBY[s], 3) for s in p["rel"])
        body = f'''{crumbs(cr)}
<article>
<div class="prod">
  {img(p["img"], "(max-width:780px) calc(100vw - 48px), 500px", hi=True)}
  <div>
    <h1>{esc(p["name"])}</h1>
    <p class="preco">{p["price_str"]}</p>
    <p><strong>Disponibilidade:</strong> em estoque · <strong>Peso:</strong> {p["peso"]} · <strong>Código:</strong> {p["sku"]}</p>
    <div class="caixa">{"".join(f"<p>{esc(x)}</p>" for x in p["paras"])}</div>
    <p><button type="button" class="botao" data-add="{p["slug"]}">Adicionar ao carrinho</button></p>
    <p class="aviso" data-added hidden>Produto adicionado. <a href="{u('/carrinho/')}">Ver carrinho</a></p>
  </div>
</div>
<section aria-labelledby="prep"><h2 id="prep">Como preparar</h2><p>{esc(p["prep"])}</p></section>
<section aria-labelledby="av"><h2 id="av">Avaliações de clientes</h2>
<p class="aviso-demo">Avaliações de demonstração: textos fictícios criados para o exercício acadêmico, a serem trocados por avaliações reais quando a loja for ao ar.</p>
<p><strong>Nota média: {str(p["avg"]).replace(".", ",")} de 5</strong> ({len(p["reviews"])} avaliações)</p>
{rev}</section>
</article>
<section aria-labelledby="rel"><h2 id="rel">Veja também</h2><div class="grade">{rel}</div></section>'''
        prod = {"@type": "Product", "@id": abs_(p["url"]) + "#produto", "name": p["name"], "description": " ".join(p["paras"]),
                "image": [abs_("/imagens/" + IMAGES[p["img"]][1] + f"-{w}.webp") for w in (1200, 800)], "sku": p["sku"],
                "brand": {"@type": "Brand", "name": BRAND}, "url": abs_(p["url"]),
                "offers": {"@type": "Offer", "url": abs_(p["url"]), "priceCurrency": "BRL", "price": f'{p["price"]:.2f}',
                           "priceValidUntil": "2027-12-31", "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                           "seller": {"@type": "Organization", "name": BRAND}},
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(p["avg"]), "reviewCount": str(len(p["reviews"])), "bestRating": "5", "worstRating": "1"},
                "review": [{"@type": "Review", "author": {"@type": "Person", "name": au}, "datePublished": TODAY,
                            "reviewRating": {"@type": "Rating", "ratingValue": str(n), "bestRating": "5", "worstRating": "1"}, "reviewBody": tx} for n, au, tx in p["reviews"]]}
        write(p["url"], layout(p["url"], p["title"], p["desc"], p["img"], body, ld(prod, crumb_ld(cr))))
        pages_out.append((p["url"], p["title"], p["desc"], True))

    # SOBRE
    t, d, k, ix = STATIC["sobre"][1:]; cr = [("Início", "/"), ("Quem somos", None)]
    body = f'''{crumbs(cr)}
<article>
<div class="duas">
  {img("loja", "(max-width:780px) calc(100vw - 48px), 500px", hi=True)}
  <div>
    <h1>Quem somos</h1>
    <p>Somos uma loja familiar de Catanduva-SP que importa e embala chás desde 2019.</p>
    <p>Selecionamos folhas e flores com cuidado e embalamos em pacotes de forma artesanal, para que o chá chegue fresco à sua casa, em qualquer lugar do Brasil.</p>
  </div>
</div>
<section aria-labelledby="como"><h2 id="como">Como trabalhamos</h2>
<ul><li>Folhas selecionadas, em pacotes de 40 a 60 g.</li><li>Embalagem artesanal, também em kits para presente.</li><li>Envio para todo o Brasil.</li></ul>
<p>Veja o que temos na <a href="{u('/chas/')}">categoria de chás</a> ou nos <a href="{u('/acessorios/')}">kits presente</a>. Dúvidas? Use nossa <a href="{u('/contato/')}">página de contato</a>.</p></section>
</article>'''
    write("/sobre/", layout("/sobre/", t, d, k, body, ld(crumb_ld(cr)))); pages_out.append(("/sobre/", t, d, True))

    # CONTATO (SEO local de 1 página)
    t, d, k, ix = STATIC["contato"][1:]; cr = [("Início", "/"), ("Contato", None)]; n = NAP
    bbox = f"{n['lng']-.012},{n['lat']-.008},{n['lng']+.012},{n['lat']+.008}"
    body = f'''{crumbs(cr)}
<article>
<h1>Fale com a {BRAND}</h1>
<p>Atendemos de Catanduva-SP, no interior de São Paulo, e enviamos chás para todo o Brasil. Escolha o canal mais prático.</p>
<div class="duas">
<section class="caixa" aria-labelledby="nap"><h2 id="nap">Onde estamos</h2>
<address><strong>{BRAND}</strong><br>{n["street"]}, {n["district"]}<br>{n["city"]}-{n["region"]}, CEP {n["zip"]}</address>
<p><strong>WhatsApp e telefone:</strong> <a href="tel:{n["phone_intl"]}">{n["phone"]}</a><br><strong>E-mail:</strong> <a href="mailto:{n["email"]}">{n["email"]}</a></p>
<h2 id="hor">Horário de atendimento</h2>
<p>Segunda a sexta: 9h às 18h<br>Sábado: 9h às 13h<br>Domingo: fechado</p></section>
<section aria-labelledby="mapa"><h2 id="mapa">Mapa</h2>
<iframe title="Mapa com a localização da {BRAND} em Catanduva-SP" loading="lazy" width="500" height="340" style="border:0;width:100%;border-radius:16px" src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={n["lat"]}%2C{n["lng"]}"></iframe></section>
</div>
<p>Prefere conhecer antes de falar? Veja os <a href="{u('/chas/')}">chás</a> e os <a href="{u('/acessorios/')}">kits presente</a>.</p>
</article>'''
    store = {"@type": "Store", "@id": abs_("/contato/") + "#loja", "name": BRAND, "url": abs_("/"), "image": abs_("/imagens/og-" + IMAGES["loja"][1] + ".jpg"),
             "telephone": n["phone_intl"], "email": n["email"],
             "address": ORG["address"], "geo": {"@type": "GeoCoordinates", "latitude": n["lat"], "longitude": n["lng"]},
             "areaServed": [{"@type": "City", "name": "Catanduva"}, {"@type": "Country", "name": "Brasil"}],
             "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"},
                                           {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"}]}
    write("/contato/", layout("/contato/", t, d, k, body, ld(store, crumb_ld(cr)))); pages_out.append(("/contato/", t, d, True))

    # NÃO INDEXÁVEIS: carrinho, checkout, busca
    t, d, k, ix = STATIC["carrinho"][1:]
    write("/carrinho/", layout("/carrinho/", t, d, k, f'''<h1>Seu carrinho</h1>
<div id="carrinho-itens" class="caixa vazio"><p>Nenhum item.</p></div>
<noscript><p>Ative o JavaScript para usar o carrinho simulado.</p></noscript>
<p><a href="{u('/chas/')}">Continuar comprando</a></p>
<p><a class="botao" href="{u('/checkout/')}">Finalizar compra (simulação)</a></p>''', [], index=False)); pages_out.append(("/carrinho/", t, d, False))
    t, d, k, ix = STATIC["checkout"][1:]
    write("/checkout/", layout("/checkout/", t, d, k, f'''<h1>Finalizar compra</h1>
<div class="caixa"><p>Esta é uma simulação para fins acadêmicos. Nenhum pedido é processado e nenhum dado é coletado.</p></div>
<p><a href="{u('/carrinho/')}">Voltar ao carrinho</a></p>''', [], index=False)); pages_out.append(("/checkout/", t, d, False))
    t, d, k, ix = STATIC["busca"][1:]
    write("/busca/", layout("/busca/", t, d, k, f'''<h1>Buscar produtos</h1>
<p id="busca-resumo">Digite o nome de um chá ou kit.</p>
<div id="busca-resultados" class="grade"></div>
<noscript><p>Ative o JavaScript para usar a busca ou navegue pelas <a href="{u('/chas/')}">categorias</a>.</p></noscript>''', [], index=False)); pages_out.append(("/busca/", t, d, False))

    # 404
    nf = f'''<h1>Página não encontrada</h1><p>O endereço pode ter mudado. Volte para a <a href="{u('/')}">página inicial</a>, veja os <a href="{u('/chas/')}">chás</a> ou os <a href="{u('/acessorios/')}">kits presente</a>.</p>'''
    open(os.path.join(V1, "404.html"), "w", encoding="utf-8").write(layout("/404.html", "Página não encontrada | Casa do Chá Serrano", "A página procurada não foi encontrada na Casa do Chá Serrano.", "banner", nf, [], index=False))

def build_assets():
    shutil.copytree(os.path.join(V0, "css"), os.path.join(V1, "css"), dirs_exist_ok=True)
    open(os.path.join(V1, "css", "estilo.css"), "a", encoding="utf-8").write('''
/* 7. ACRESCIMOS DA V1 (acessibilidade, migalhas, busca, avaliacoes) ------ */
a.logo{text-decoration:none}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.pular{position:absolute;left:-999px;top:0;background:#fff;padding:8px 14px;z-index:20}.pular:focus{left:8px}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #f4b400;outline-offset:2px}
.menu a[aria-current="page"]{background:var(--suave);color:var(--escuro)}
.busca-form{display:flex;gap:6px}.busca-form input{padding:8px 14px;border:1px solid var(--borda);border-radius:999px;font:inherit;font-size:15px;width:170px}
.busca-form button{padding:8px 16px;border:0;border-radius:999px;background:var(--cor);color:#fff;font-weight:700;cursor:pointer}
.conteudo h1.x,.hero h1{font-size:46px}.conteudo h2{font-size:28px}.conteudo h3{font-size:22px}
.card h2,.card h3{font-size:20px;margin:0 0 4px}.card .peso{margin:0 0 8px;color:#5b6772;font-size:15px}.card .preco{margin:2px 0 4px}
.migalhas ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;padding:0;margin:0 0 18px;font-size:15px;color:#5b6772}
.migalhas li+li:before{content:"\\203A";margin-right:6px}
.rodape-menu{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 20px;margin-bottom:12px}.rodape a{color:#e8f0e2}
.rodape address{font-style:normal;margin-bottom:6px}.rodape p{margin:0}
blockquote.citacao{margin:16px 0;padding-top:22px}.citacao:before{content:none}.citacao .nota{color:#f4b400;letter-spacing:3px;font-size:20px}.citacao footer{color:#5b6772;font-size:15px}.citacao .nota{margin:0}
.aviso-demo{background:var(--suave);border-radius:12px;padding:10px 16px;font-size:15px}.aviso{color:var(--escuro);font-weight:700}
@media(min-width:1100px){.topo-in{max-width:1280px;flex-wrap:nowrap;gap:12px}.logo{font-size:22px;white-space:nowrap}.menu{flex-wrap:nowrap}.menu a{padding:8px 11px;white-space:nowrap}.busca-form{flex-shrink:0}.busca-form input{width:130px}.busca-form button{padding:8px 14px}}
@media(max-width:780px){.hero h1{font-size:34px}.busca-form{width:100%}.busca-form input{flex:1}}
''')
    os.makedirs(os.path.join(V1, "js"), exist_ok=True)
    cat = [{"slug": p["slug"], "nome": p["name"], "preco": p["price"], "peso": p["peso"], "url": u(p["url"]),
            "img": u("/imagens/" + IMAGES[p["img"]][1] + "-480.webp"), "alt": IMAGES[p["img"]][2]} for p in PRODUCTS]
    open(os.path.join(V1, "js", "catalogo.js"), "w", encoding="utf-8").write("window.CATALOGO=" + json.dumps(cat, ensure_ascii=False) + ";\n")
    open(os.path.join(V1, "js", "loja.js"), "w", encoding="utf-8").write(LOJA_JS.replace("__P__", P))
    ind = [pg for pg in pages_out if pg[3]]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{abs_(pg[0])}</loc><lastmod>{TODAY}</lastmod></url>\n" for pg in ind) + "</urlset>\n"
    open(os.path.join(V1, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    open(os.path.join(V1, "robots.txt"), "w", encoding="utf-8").write(f"""# robots.txt - {BRAND}
User-agent: *
Allow: /
# Resultados de busca interna com parametro (infinitas combinacoes, sem valor para a busca)
Disallow: /*?q=
# /carrinho/, /checkout/ e /busca/ ficam rastreaveis de proposito: o Google precisa ler o
# meta robots noindex dessas paginas. CSS, JS e imagens NAO sao bloqueados.

Sitemap: {BASE}/sitemap.xml
""")
    open(os.path.join(V1, "_redirects"), "w", encoding="utf-8").write("# 301 (v0 -> v1). Funciona em Netlify e Cloudflare Pages.\n" + "".join(f"{a}  {P}{b}  301\n" for a, b in REDIRECTS))
    open(os.path.join(V1, ".nojekyll"), "w").close()

LOJA_JS = r'''(function(){
  var K="cds_carrinho", P="__P__";
  function ler(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(e){return {}}}
  function gravar(c){try{localStorage.setItem(K,JSON.stringify(c))}catch(e){}}
  function total(c){return Object.keys(c).reduce(function(s,k){return s+c[k]},0)}
  function brl(v){return "R$ "+v.toFixed(2).replace(".",",")}
  function contador(){var n=total(ler());document.querySelectorAll("[data-cart-count]").forEach(function(e){e.textContent=n})}
  function acha(s){return (window.CATALOGO||[]).filter(function(p){return p.slug===s})[0]}
  function esc(t){var d=document.createElement("div");d.textContent=t;return d.innerHTML}
  document.querySelectorAll("[data-add]").forEach(function(b){b.addEventListener("click",function(){
    var c=ler(),s=b.getAttribute("data-add");c[s]=(c[s]||0)+1;gravar(c);contador();
    var a=document.querySelector("[data-added]");if(a)a.hidden=false;});});
  var box=document.getElementById("carrinho-itens");
  if(box){(function draw(){var c=ler(),ks=Object.keys(c);if(!ks.length){box.className="caixa vazio";box.innerHTML="<p>Nenhum item.</p>";return}
    var t=0;box.className="caixa";box.innerHTML=ks.map(function(s){var p=acha(s);if(!p)return "";t+=p.preco*c[s];
      return "<p>"+esc(p.nome)+" × "+c[s]+" — "+brl(p.preco*c[s])+' <button type="button" data-rm="'+s+'">Remover</button></p>'}).join("")+"<p><strong>Total: "+brl(t)+"</strong></p>";
    box.querySelectorAll("[data-rm]").forEach(function(b){b.addEventListener("click",function(){var c=ler();delete c[b.getAttribute("data-rm")];gravar(c);contador();draw()})});})();}
  var res=document.getElementById("busca-resultados");
  if(res){var q=(new URLSearchParams(location.search).get("q")||"").trim().toLowerCase();var r=document.getElementById("busca-resumo");
    if(q){var f=(window.CATALOGO||[]).filter(function(p){return p.nome.toLowerCase().indexOf(q)>-1});
      r.textContent=f.length?f.length+" resultado(s) para “"+q+"”.":"Nenhum resultado para “"+q+"”.";
      res.innerHTML=f.map(function(p){return '<article class="caixa card"><img src="'+p.img+'" alt="'+esc(p.alt)+'" width="480" height="320" loading="lazy"><h2>'+esc(p.nome)+'</h2><p class="preco">'+brl(p.preco)+'</p><a href="'+p.url+'">Ver detalhes: '+esc(p.nome.toLowerCase())+'</a></article>'}).join("")}}
  contador();
})();
'''

if __name__ == "__main__":
    if os.path.isdir(V1): shutil.rmtree(V1)
    os.makedirs(V1); build_images(); build_pages(); build_assets()
    print("v1 gerada:", len(pages_out), "páginas | BASE =", BASE)
