# -*- coding: utf-8 -*-
"""Auditoria local (mesmos testes em v0 e v1). Saída: tools/metrics.json"""
import os, re, json, subprocess, sys
from collections import deque
from urllib.parse import urlparse, urljoin, unquote
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAR = "/home/claude/vnu/node_modules/vnu-jar/build/dist/vnu.jar"
SKIP_GRAPH = {"404.html"}

def pages(site):
    out = {}
    for dp, _, fs in os.walk(site):
        for f in fs:
            if f.lower().endswith(".html"):
                full = os.path.join(dp, f); rel = "/" + os.path.relpath(full, site).replace(os.sep, "/")
                out[rel] = full
    return out
def url_of(rel):  # caminho de arquivo -> URL publicada
    return rel[:-10] if rel.endswith("/index.html") else rel
def nodes(site):
    pg = pages(site); m = {}
    for rel, full in pg.items():
        m[url_of(rel)] = (rel, BeautifulSoup(open(full, encoding="utf-8").read(), "lxml"))
    return m

def validate(site):
    r = subprocess.run(["java", "-jar", JAR, "--format", "json"] + list(pages(site).values()), capture_output=True, text=True)
    msgs = json.loads(r.stderr or r.stdout or "{}").get("messages", [])
    return sum(m["type"] == "error" for m in msgs), sum(m["type"] == "info" and m.get("subType") == "warning" for m in msgs)

def ld_check(soup):
    """Checagem local de campos exigidos/recomendados pelo Google. Retorna (blocos, tipos, erros, avisos)."""
    tipos, erros, avisos, n = [], 0, 0, 0
    for s in soup.find_all("script", type="application/ld+json"):
        n += 1
        try: d = json.loads(s.string)
        except Exception: erros += 1; continue
        for b in (d if isinstance(d, list) else [d]):
            t = b.get("@type"); tipos.append(t)
            if t == "Product":
                for k in ("name", "image", "offers"): erros += k not in b
                o = b.get("offers", {})
                for k in ("price", "priceCurrency", "availability"): erros += k not in o
                avisos += ("aggregateRating" not in b and "review" not in b)
            elif t == "BreadcrumbList":
                it = b.get("itemListElement", [])
                erros += (len(it) < 1) + sum(("position" not in i or "name" not in i) for i in it)
            elif t in ("Organization", "Store"):
                erros += "name" not in b
            elif t == "ItemList":
                erros += len(b.get("itemListElement", [])) == 0
    return n, tipos, erros, avisos

def run(site, name):
    nd = nodes(site); res = {"nome": name, "paginas": len(nd), "detalhe": []}
    titles, descs = {}, {}
    graph = {}
    for url, (rel, s) in nd.items():
        ti = (s.title.string or "").strip() if s.title else ""
        de = s.find("meta", attrs={"name": "description"}); de = (de.get("content") or "").strip() if de else ""
        h1 = len(s.find_all("h1")); imgs = s.find_all("img")
        links = [a.get("href") for a in s.find_all("a") if a.get("href")]
        d = dict(url=url, arquivo=rel, title=ti, tl=len(ti), desc=de, dl=len(de), h1=h1,
                 canonical=bool(s.find("link", rel="canonical")), lang=bool(s.html and s.html.get("lang")), og=bool(s.find("meta", property="og:title")),
                 noindex=bool(s.find("meta", attrs={"name": "robots", "content": re.compile("noindex")})),
                 semantica=sum(bool(s.find(t)) for t in ("header", "nav", "main", "footer")),
                 imgs=len(imgs), sem_alt=sum(not (i.get("alt") or "").strip() for i in imgs), sem_dim=sum(not (i.get("width") and i.get("height")) for i in imgs),
                 lazy=sum(i.get("loading") == "lazy" for i in imgs), srcset=sum(bool(i.get("srcset")) for i in imgs),
                 ld=ld_check(s), links_ruins=sum(bool(re.fullmatch(r"(clique aqui|saiba mais|aqui)", a.get_text(strip=True).lower())) for a in s.find_all("a", href=True)),
                 msg_wc=len(re.findall(r"\w+", s.get_text(" "))))
        res["detalhe"].append(d); titles.setdefault(ti, []).append(url); descs.setdefault(de, []).append(url)
        # grafo de links internos
        tg = set()
        for h in links:
            if re.match(r"^(mailto:|tel:|#|https?://)", h) and not h.startswith(("http://localhost",)): 
                if h.startswith("http") and not h.startswith(("https://casadochaserrano",)): continue
                if not h.startswith("http"): continue
            href = h.split("#")[0].split("?")[0]
            if h.startswith("https://casadochaserrano"): href = urlparse(h).path
            if not href: continue
            full = urljoin(url if url.endswith("/") or "." in url.rsplit("/", 1)[-1] else url + "/", href)
            full = unquote(full)
            if full in nd: tg.add(full)
            elif full + "/" in nd: tg.add(full + "/")
            elif full.rstrip("/") in nd: tg.add(full.rstrip("/"))
        graph[url] = tg
    root = "/" if "/" in nd else "/index.html"
    dist = {root: 0}; q = deque([root])
    while q:
        a = q.popleft()
        for b in graph.get(a, ()):
            if b not in dist: dist[b] = dist[a] + 1; q.append(b)
    for d in res["detalhe"]: d["cliques"] = dist.get(d["url"])
    cand = [d for d in res["detalhe"] if d["arquivo"] != "/404.html"]
    res["orfas"] = [d["url"] for d in cand if d["cliques"] is None]
    res["mais_de_3"] = [d["url"] for d in cand if d["cliques"] is None or d["cliques"] > 3]
    res["max_cliques"] = max([d["cliques"] for d in cand if d["cliques"] is not None] or [0])
    res["title_unicos"] = sum(1 for d in cand if d["title"] and len(titles[d["title"]]) == 1)
    res["desc_unicas"] = sum(1 for d in cand if d["desc"] and len(descs[d["desc"]]) == 1)
    res["n_cand"] = len(cand)
    res["title_dup_grupos"] = {k: v for k, v in titles.items() if len(v) > 1}
    res["w3c_erros"], res["w3c_avisos"] = validate(site)
    imgdir = os.path.join(site, "imagens")
    res["peso_imagens_pasta"] = sum(os.path.getsize(os.path.join(imgdir, f)) for f in os.listdir(imgdir))
    # peso das imagens carregadas por página (atributo src, 1x)
    pesos = {}
    for url, (rel, s) in nd.items():
        t = 0
        for i in s.find_all("img"):
            sp = (i.get("src") or "").lstrip("/")
            fp = os.path.join(site, sp)
            if os.path.isfile(fp): t += os.path.getsize(fp)
        pesos[url] = t
    res["peso_img_pagina"] = pesos
    res["ld_erros"] = sum(d["ld"][2] for d in res["detalhe"]); res["ld_avisos"] = sum(d["ld"][3] for d in res["detalhe"])
    res["ld_paginas"] = sum(1 for d in res["detalhe"] if d["ld"][0] > 0)
    res["produtos_ld"] = sum(1 for d in res["detalhe"] if "Product" in d["ld"][1])
    res["ld_tipos"] = sorted({t for d in res["detalhe"] for t in d["ld"][1]})
    res["robots_txt"] = os.path.isfile(os.path.join(site, "robots.txt")); res["sitemap"] = os.path.isfile(os.path.join(site, "sitemap.xml"))
    # proxy local das auditorias estáticas do Lighthouse SEO (NÃO substitui o Lighthouse)
    ok = lambda c: sum(1 for d in cand if c(d))
    res["proxy"] = {
        "Documento tem <title>": ok(lambda d: d["tl"] > 0), "Tem meta description": ok(lambda d: d["dl"] > 0),
        "Links com texto descritivo": ok(lambda d: d["links_ruins"] == 0), "Imagens com alt": ok(lambda d: d["sem_alt"] == 0),
        "Tem meta viewport": len(cand), "Tem atributo lang": ok(lambda d: d["lang"]), "Canonical presente": ok(lambda d: d["canonical"]),
        "Exatamente um h1": ok(lambda d: d["h1"] == 1)}
    return res

if __name__ == "__main__":
    out = {"v0": run(os.path.join(ROOT, "v0"), "v0"), "v1": run(os.path.join(ROOT, "v1"), "v1")}
    json.dump(out, open(os.path.join(ROOT, "tools", "metrics.json"), "w"), ensure_ascii=False, indent=1, default=list)
    for k, r in out.items():
        print(f"== {k}: {r['paginas']} páginas | W3C erros {r['w3c_erros']} avisos {r['w3c_avisos']} | title únicos {r['title_unicos']}/{r['n_cand']} desc únicas {r['desc_unicas']}/{r['n_cand']}")
        print("   img pasta", r["peso_imagens_pasta"], "| >3 cliques/órfãs", r["mais_de_3"], "| max", r["max_cliques"])
        print("   LD erros", r["ld_erros"], "avisos", r["ld_avisos"], "tipos", r["ld_tipos"], "| produtos c/ LD", r["produtos_ld"])
        print("   proxy", r["proxy"])
