# -*- coding: utf-8 -*-
import json, os, re, subprocess, collections, urllib.robotparser, xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Preformatted, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from sitedata import *
from planning import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, "tools", "metrics.json"))); v0, v1 = M["v0"], M["v1"]
FD = "/usr/share/fonts/truetype/dejavu/"
for n, f in (("DV", "DejaVuSans.ttf"), ("DVB", "DejaVuSans-Bold.ttf"), ("DVI", "DejaVuSans-Oblique.ttf"), ("DVM", "DejaVuSansMono.ttf")): pdfmetrics.registerFont(TTFont(n, FD + f))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")
GREEN, DARK, SOFT = colors.HexColor("#2e6b3f"), colors.HexColor("#1f3d2a"), colors.HexColor("#e8f0e2")
st = dict(
 body=ParagraphStyle("b", fontName="DV", fontSize=9.6, leading=14.2, alignment=TA_JUSTIFY, spaceAfter=6, textColor=colors.HexColor("#26303a")),
 h1=ParagraphStyle("h1", fontName="DVB", fontSize=17, leading=21, textColor=DARK, spaceBefore=4, spaceAfter=8),
 h2=ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, textColor=GREEN, spaceBefore=8, spaceAfter=4),
 cell=ParagraphStyle("c", fontName="DV", fontSize=7.8, leading=10),
 cellb=ParagraphStyle("cb", fontName="DVB", fontSize=7.8, leading=10, textColor=colors.white),
 note=ParagraphStyle("n", fontName="DVI", fontSize=8.2, leading=11.5, textColor=colors.HexColor("#5b6772"), spaceAfter=6),
 bul=ParagraphStyle("bu", fontName="DV", fontSize=9.6, leading=14, leftIndent=14, bulletIndent=3, spaceAfter=2),
 code=ParagraphStyle("code", fontName="DVM", fontSize=7.4, leading=9.4, backColor=colors.HexColor("#f3f5f4"), borderPadding=5, spaceAfter=8),
 cap=ParagraphStyle("cap", fontName="DVI", fontSize=8, leading=10, textColor=colors.HexColor("#5b6772"), alignment=1, spaceAfter=8))
def esc(t): return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
P_ = lambda t, s="body": Paragraph(t, st[s])
def B(items): return [Paragraph(i, st["bul"], bulletText="•") for i in items]
def T(rows, widths, header=True, zebra=True):
    data = [[Paragraph(esc(c) if not str(c).startswith("<") else c, st["cellb"] if (header and i == 0) else st["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1 if header else 0)
    sty = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#c9d3cc")), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header: sty.append(("BACKGROUND", (0, 0), (-1, 0), DARK))
    if zebra: sty += [("BACKGROUND", (0, i), (-1, i), SOFT) for i in range(2 if header else 1, len(rows), 2)]
    t.setStyle(TableStyle(sty)); return t
def PRINT(txt):  # espaço reservado para evidência que só o grupo consegue capturar
    t = Table([[Paragraph(f"<b>[Inserir print]</b> {esc(txt)}", st["cell"])]], colWidths=[17 * cm], rowHeights=[1.5 * cm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#b8860b")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff8dc")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])); return t
def FIG(name, w=16.5):
    from PIL import Image as PI
    f = os.path.join(ROOT, "docs", "fig", name); iw, ih = PI.open(f).size; return Image(f, width=w * cm, height=w * cm * ih / iw)

UP = "/mnt/user-data/uploads/"
F301, FW1, FW0, FRICH, FLH0, FLH0P, FLH1, FLH1P, FROB, FSM = ("a6ed52d8-963e-4228-a024-394e62936676.jpg", "b41d141a-262c-4987-a9cd-fcb575e0781c.jpg", "02b78843-2a57-41c9-85a4-af9630668a1a.jpg", "81b9a3b2-8087-4836-ba46-8c5c50c4d035.jpg",
    "e4e6d5a8-8021-4944-8c2c-c1940b21baf6.jpg", "bd0b8692-ad83-4f3d-9da5-46217a96cb14.jpg", "d7d5cf67-64f0-435f-b79c-729e47139a81.jpg", "b294b247-1e68-43d6-bbe3-94e9ea8bb8ab.jpg", "1795090664385_image.png", "WhatsApp_Image_2026-11-19_at_09_14_50.jpeg")
def _img(f, w):
    from PIL import Image as PI
    iw, ih = PI.open(UP + f).size; return Image(UP + f, width=w * cm, height=w * cm * ih / iw)
FCON = "1795091124475_image.png"
def PIC(f, w, cap): return KeepTogether([_img(f, w), Paragraph(cap, st["cap"])])
def PICS(items, w, ncols=2):
    rows = []
    for i in range(0, len(items), ncols):
        ch = items[i:i + ncols]; rows.append([_img(f, w) for f, _ in ch]); rows.append([Paragraph(c, st["cap"]) for _, c in ch])
    t = Table(rows, colWidths=[(w + .3) * cm] * ncols); t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOX", (0, 0), (-1, -1), 0, colors.white)])); return t
KB = lambda b: f"{b/1024:,.0f}".replace(",", ".")
cand1 = sorted([d for d in v1["detalhe"] if d["arquivo"] != "/404.html"], key=lambda d: d["url"])

class Doc(BaseDocTemplate):
    def __init__(s, fn):
        super().__init__(fn, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2.2 * cm, bottomMargin=2 * cm, title="Relatório de Auditoria e Otimização de SEO – Grupo 1", author="Grupo 1 – Casa do Chá Serrano")
        s.addPageTemplates([PageTemplate("capa", [Frame(2 * cm, 2 * cm, 17 * cm, 25.7 * cm)], onPage=lambda c, d: None),
                            PageTemplate("n", [Frame(2 * cm, 2 * cm, 17 * cm, 25.5 * cm)], onPage=s.deco)])
    def deco(s, c, d):
        c.saveState(); c.setFont("DV", 7.5); c.setFillColor(colors.HexColor("#5b6772"))
        c.drawString(2 * cm, 28.1 * cm, "Auditoria e Otimização de SEO · Grupo 1 · Casa do Chá Serrano"); c.drawRightString(19 * cm, 1.2 * cm, f"Página {d.page}")
        c.setStrokeColor(GREEN); c.line(2 * cm, 27.9 * cm, 19 * cm, 27.9 * cm); c.restoreState()
    def afterFlowable(s, f):
        if isinstance(f, Paragraph) and f.style.name in ("h1",): s.notify("TOCEntry", (0, f.getPlainText(), s.page))

# ---------- dados extras medidos agora ----------
vm = json.loads(subprocess.run(["java", "-jar", "/home/claude/vnu/node_modules/vnu-jar/build/dist/vnu.jar", "--format", "json"] + [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(ROOT, "v0")) for f in fs if f.lower().endswith(".html")], capture_output=True, text=True).stderr)["messages"]
top = collections.Counter(re.sub(r"“[^”]*”", "“…”", m["message"]) for m in vm if m["type"] == "error").most_common(5)
rp = urllib.robotparser.RobotFileParser(); rp.parse(open(os.path.join(ROOT, "v1", "robots.txt")).read().splitlines())
rtests = [(BASE + p, rp.can_fetch("Googlebot", BASE + p)) for p in ("/", "/chas/", "/chas/cha-verde-sencha/", "/css/estilo.css", "/js/loja.js", "/imagens/cha-verde-sencha-800.webp", "/carrinho/", "/busca/")]
sm = ET.parse(os.path.join(ROOT, "v1", "sitemap.xml")).getroot(); ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [e.find("s:loc", ns).text for e in sm.findall("s:url", ns)]
canon = {BASE + d["url"] if d["url"] != "/" else BASE + "/" for d in v1["detalhe"] if d["arquivo"] != "/404.html" and not d["noindex"]}
sm_ok = set(locs) == canon

S = []
# ---------- CAPA ----------
S += [Spacer(1, 3 * cm), P_("TECNOLOGIA EM SISTEMAS PARA INTERNET · IMES CATANDUVA", "note"), P_("Relatório de Auditoria e Otimização de SEO", ParagraphStyle("t", fontName="DVB", fontSize=26, leading=31, textColor=DARK, spaceAfter=10)) if False else Paragraph("Relatório de Auditoria e Otimização de SEO", ParagraphStyle("t", fontName="DVB", fontSize=26, leading=31, textColor=DARK, spaceAfter=10)),
      Paragraph("Casa do Chá Serrano · loja virtual de nicho (Grupo 1)", ParagraphStyle("t2", fontName="DV", fontSize=14, leading=18, textColor=GREEN, spaceAfter=30)),
      T([["Grupo", "1 – Loja virtual de nicho (kit v0: Casa do Chá Serrano)"], ["Integrantes", "Vinicyus Raya, Braian Elizeu e Mariana Miguel"], ["Disciplina / professor", "Otimização para Motores de Busca · Prof. Esp. Thales Emanuel Figueiredo"],
         ["Site v1 (otimizado)", BASE], ["Site v0 (inicial)", "https://casadochaserrano-v0.netlify.app"], ["Repositório Git", "[preencher] · pastas v0/ e v1/, professor como leitor"], ["Data do relatório", "19 de novembro de 2026"]], [4.2, 12.8], header=False),
      Spacer(1, 1.2 * cm), P_("<b>Aviso de transparência.</b> Os números de W3C, imagens, títulos, descrições, cliques e dados estruturados foram medidos com scripts incluídos no repositório (pasta tools/) sobre os dois sites. Os prints (Lighthouse, W3C, Teste de Resultados Enriquecidos, 301 e Search Console) foram feitos pelo grupo nas URLs públicas em 19/11/2026. Não há prints pendentes.", "note"), PageBreak()]
from reportlab.platypus import NextPageTemplate
S.insert(0, NextPageTemplate("capa")); S.insert(S.index(S[-1]), NextPageTemplate("n")) if False else None
S = [S[0]] + S[1:-1] + [NextPageTemplate("n"), S[-1]]
toc = TableOfContents(); toc.levelStyles = [ParagraphStyle("toc", fontName="DV", fontSize=10, leading=17, leftIndent=0)]
S += [P_("Sumário", "h1"), toc, PageBreak()]

# ---------- 0. RESUMO ----------
S += [P_("Resumo executivo e resultados em números", "h1"),
 P_("A v0 recebida era uma loja de chás sem nenhum cuidado de SEO: títulos repetidos (“Home”, “Produto”), nenhuma descrição, nomes de arquivo como Prod_1.html, duas páginas iniciais idênticas, três páginas órfãs, fotos de 700 KB sem texto alternativo e nenhum dado estruturado. A v1 reconstrói o site como um gerador estático (tools/build.py, HTML, CSS e JavaScript puros, sem plugin de SEO) com 11 páginas indexáveis e 4 de apoio (carrinho, checkout, busca e 404)."),
 T([["Métrica (mesmos testes nos dois sites)", "v0 (antes)", "v1 (depois)"],
    ["Nota de SEO no Lighthouse (celular)", "73", "100"],
    ["Erros do validador W3C (14 páginas HTML)", v0["w3c_erros"], v1["w3c_erros"]],
    ["Erros de dados estruturados (checagem local)", "0 (não há dados estruturados)", v1["ld_erros"]],
    ["Páginas de produto com dados estruturados Product", "0 de 6", f"{v1['produtos_ld']} de 6"],
    ["Páginas com title único", f"{v0['title_unicos']} de 14", f"{v1['title_unicos']} de 14"],
    ["Páginas com description única", f"{v0['desc_unicas']} de 14", f"{v1['desc_unicas']} de 14"],
    ["Peso total da pasta de imagens", f"{KB(v0['peso_imagens_pasta'])} KB", f"{KB(v1['peso_imagens_pasta'])} KB"],
    ["Páginas a mais de 3 cliques da home (inclui órfãs)", f"{len(v0['mais_de_3'])}", f"{len(v1['mais_de_3'])}"],
    ["Imagens sem texto alternativo", sum(d['sem_alt'] for d in v0['detalhe']), sum(d['sem_alt'] for d in v1['detalhe'])]], [9, 4, 4]),
 Spacer(1, 6), FIG("antes-depois.png"), P_("Figura 1 – Principais comparativos medidos por tools/audit.py.", "cap"),
 P_("A pasta de imagens da v1 pesa menos porque cada foto de 1800 px (cerca de 700 KB em JPG) virou WebP em três larguras. A pasta inclui os três tamanhos e as imagens de compartilhamento, e uma página carrega só um deles (seção 7).", "note"), PageBreak()]

# ---------- 1. ESTRATÉGIA ----------
S += [P_("1. Estratégia: objetivo, público e indicadores", "h1"), P_("Objetivo do site", "h2"), P_(OBJETIVO), P_("Personas", "h2"),
      T([["Persona", "Perfil", "Como busca e o que precisa"]] + [list(p) for p in PERSONAS], [3.3, 7, 6.7]),
      P_("As personas são fictícias, criadas para orientar decisões do exercício; devem ser confirmadas com dados reais de clientes quando a loja for ao ar.", "note"),
      P_("Indicadores de sucesso mensuráveis", "h2"), T([["Indicador", "Meta", "Onde medir"]] + [list(i) for i in INDICADORES], [4, 8.5, 4.5]),
      P_("As metas são hipóteses de partida. Como o site é novo, a linha de base real vem do Search Console nas primeiras semanas; depois disso as metas são revisadas.", "note"),
      P_("Como a estratégia aparece no site", "h2")] + B(["Uma página própria para cada produto, com preço, peso, modo de preparo e avaliações (Persona 1).",
      "Categoria “Kits presente e acessórios” e kit presente em destaque na home (Persona 2).", "Atendimento em Catanduva-SP e envio para todo o Brasil escritos na home, em Quem somos e em Contato."]) + [PageBreak()]

# ---------- 2. SEM ----------
S += [P_("2. SEO x SEM: plano de mídia paga simulado", "h1"), P_("Nenhum valor foi gasto. A campanha existe apenas como plano e fica na planilha de apoio (aba “Mídia paga”).", "note"),
      P_("Dez palavras-chave e tipo de correspondência", "h2"), T([["#", "Palavra-chave", "Correspondência", "Escrita na campanha"]] + [[i + 1, k[0], k[1], k[2]] for i, k in enumerate(SEM_KW)], [1, 6, 3.5, 6.5]),
      P_("Palavras-chave negativas: " + ", ".join(NEGATIVAS) + ". Servem para não pagar por cliques de quem procura receita, benefício de saúde ou chá em saquinho.", "note"), P_("Dois anúncios de texto", "h2")]
for a in ANUNCIOS:
    S.append(T([[a["nome"], f"Grupo de anúncios: {a['grupo']} · URL final: {BASE}{a['url']}"]] + [["Título %d" % (i + 1), f"{t}  ({len(t)}/30)"] for i, t in enumerate(a["titulos"])] + [["Descrição %d" % (i + 1), f"{t}  ({len(t)}/90)"] for i, t in enumerate(a["descricoes"])], [3.2, 13.8])); S.append(Spacer(1, 6))
S += [P_("O que fica no orgânico e o que vale pagar", "h2"), P_(SEM_ARG), PageBreak()]

# ---------- 3. INDEXAÇÃO ----------
S += [P_("3. Indexação: rastrear, indexar e ranquear", "h1"), FIG("fluxo-indexacao.png"), P_("Figura 2 – Caminho de uma página da loja até aparecer em uma busca.", "cap"),
      P_("No <b>rastreamento</b>, o Googlebot descobre URLs por links internos e pelo sitemap.xml e respeita o robots.txt. Na <b>indexação</b>, lê o HTML, o título, os textos, as imagens e o JSON-LD e decide se guarda a página. No <b>ranqueamento</b>, compara as páginas indexadas com a intenção de quem pesquisa. Em uma loja, o risco mais comum é uma página de produto não ser descoberta ou ser vista como cópia de outra."),
      P_("Cinco coisas que poderiam impedir a indexação e como foram evitadas", "h2"), T([["#", "Risco", "Como foi evitado na v1"]] + [[i + 1, a, b] for i, (a, b) in enumerate(IMPEDIMENTOS)], [1, 6.5, 9.5]),
      P_("Checklist de verificação (todos conferidos pelo script de auditoria)", "h2")] + B(["Todas as 11 páginas indexáveis respondem com link de entrada (0 órfãs) e têm canonical apontando para si mesmas.", "Nenhuma página indexável tem meta robots noindex.", "O sitemap.xml lista exatamente as URLs canônicas indexáveis: " + ("sim" if sm_ok else "NÃO, revisar") + ".", "CSS, JavaScript e imagens estão liberados no robots.txt.", "Páginas v0 antigas respondem com redirecionamento 301 (seção 10)."]) + [PageBreak()]

# ---------- 4. ROBOTS ----------
S += [P_("4. Crawlers e robots.txt", "h1"), P_("Arquivo publicado na raiz do site (v1/robots.txt)", "h2"), Preformatted(open(os.path.join(ROOT, "v1", "robots.txt"), encoding="utf-8").read(), st["code"]),
      P_("Decisão importante: as páginas de carrinho, checkout e busca <b>não</b> foram bloqueadas no robots.txt. Se o rastreador não pode abrir uma página, ele não lê o noindex dela, e a URL ainda pode aparecer no Google. Por isso elas ficam rastreáveis com meta robots noindex,follow. O robots.txt só bloqueia as URLs de busca com parâmetro (/busca/?q=…), que não têm página própria."),
      P_("Páginas fora do índice e motivo", "h2"), T([["Página ou padrão", "Mecanismo", "Motivo"]] + [list(b) for b in BLOQUEIOS], [3.6, 5, 8.4]),
      P_("Teste do robots.txt", "h2"), P_("Teste local com o interpretador padrão de robots.txt do Python (urllib.robotparser) como Googlebot, sobre a URL " + BASE + ":"),
      T([["URL testada", "Rastreamento permitido?"]] + [[u_.replace(BASE, "") or "/", "Sim" if ok else "Não"] for u_, ok in rtests], [11, 6]),
      P_("O robotparser do Python não interpreta o curinga “*?q=”; por isso o arquivo também foi conferido no Search Console (print abaixo).", "note"), PIC(FROB, 13.5, "Search Console, Configurações > robots.txt (19/11/2026): arquivo buscado, 399 bytes, sem problemas; a regra Disallow: /*?q= e a linha Sitemap foram lidas pelo Google."), PageBreak()]

# ---------- 5. HTML ----------
S += [P_("5. HTML semântico", "h1"), P_("A v0 usava div para tudo: cabeçalho, menu e rodapé eram <b>div</b>, não havia <b>main</b>, <b>article</b> ou <b>section</b>, nenhum h1 (a página de chás tinha dois), nem atributo lang. Na v1, todas as páginas seguem a mesma estrutura:"),
      Preformatted('<html lang="pt-BR">\n<body>\n  <a class="pular" href="#conteudo">Pular para o conteúdo</a>\n  <header> <a class="logo">…</a> <nav aria-label="Principal">…</nav> <form role="search">…</form> </header>\n  <main id="conteudo">\n    <nav aria-label="Você está em"><ol>… migalhas …</ol></nav>\n    <article> <h1>Chá verde sencha</h1> … <section><h2>Como preparar</h2></section> <section><h2>Avaliações</h2></section> </article>\n    <section><h2>Veja também</h2> <h3>… cards …</h3></section>\n  </main>\n  <footer> <nav aria-label="Rodapé">…</nav> <address>…</address> </footer>\n</body>', st["code"]),
      P_("Regras aplicadas: um único h1 por página; hierarquia sem pular nível (h1 > h2 > h3, e nas categorias h1 > h2 nos cards); links com texto descritivo (“Ver detalhes: chá verde sencha” no lugar de “clique aqui”); lang=\"pt-BR\"; nav com aria-label; foco visível e link “pular para o conteúdo”."),
      P_("Resultado no validador W3C (Nu HTML Checker, rodado nas 14 páginas HTML de cada versão)", "h2"),
      T([["", "v0", "v1"], ["Erros", v0["w3c_erros"], v1["w3c_erros"]], ["Avisos", v0["w3c_avisos"], v1["w3c_avisos"]], ["Páginas sem h1 ou com mais de um", sum(d["h1"] != 1 for d in v0["detalhe"]), sum(d["h1"] != 1 for d in v1["detalhe"] if d["arquivo"] != "/404.html")],
         ["Links “clique aqui” / “saiba mais”", sum(d["links_ruins"] for d in v0["detalhe"]), sum(d["links_ruins"] for d in v1["detalhe"])]], [9, 4, 4]),
      Spacer(1, 4), P_("<b>Observação sobre a validação.</b> Na URL publicada, o validador W3C aponta um erro causado por um script que o Netlify injeta depois do &lt;/html&gt; nos planos gratuitos, e não por um arquivo do site. Por isso a validação foi feita enviando os arquivos HTML (aba “Validate by File Upload”), com v0 e v1 testadas do mesmo jeito.", "note"), P_("Erros mais frequentes da v0", "h2"), T([["Ocorrências", "Mensagem do validador"]] + [[n_, m_] for m_, n_ in top], [2.5, 14.5]), Spacer(1, 4),
      PICS([(FW1, "v1: arquivo index.html enviado ao validador W3C (Validate by File Upload): “No errors or warnings to show”. As páginas de produto foram enviadas do mesmo jeito."), (FW0, "v0: o mesmo teste no index.html da v0 aponta, entre outros, falta de doctype, de lang e de alt na imagem e ausência de h1.")], 8.2), PageBreak()]

# ---------- 6. META TAGS ----------
S += [P_("6. Meta tags", "h1"), P_("Todas as páginas da v1 têm: <b>title</b> único com até 60 caracteres; <b>description</b> única com até 160; <b>canonical</b> absoluto; <b>viewport</b> e <b>charset</b>; Open Graph completo (locale, type, site_name, title, description, url, image 1200×630 com texto alternativo) e <b>twitter:card</b>. O formato do título é “assunto principal | Casa do Chá Serrano”, com o termo mais importante no começo. Descrições citam o benefício e o preço quando há produto."),
      T([["URL", "Title", "Car.", "Desc.", "Index?"]] + [[d["url"], d["title"], d["tl"], d["dl"], "não" if d["noindex"] else "sim"] for d in sorted(cand1, key=lambda d: (not d["url"] == "/", d["url"]))], [4.8, 8.4, 1, 1.2, 1.6]),
      P_("A planilha de apoio (aba “Title e description”) traz as descrições completas, a contagem de caracteres por fórmula e a conferência de duplicados. A v0 tinha apenas 3 títulos únicos (Contato, Carrinho, Busca) e nenhuma description: “Home” aparecia em três páginas, “Produto” em cinco.", "note"),
      P_("Exemplo do cabeçalho de uma página de produto (v1/chas/cha-verde-sencha/index.html)", "h2"),
      Preformatted(re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', open(os.path.join(ROOT, "v1", "chas", "cha-verde-sencha", "index.html"), encoding="utf-8").read().split("</head>")[0], flags=re.S).replace(BASE, "…")[:2300], st["code"]), PageBreak()]

# ---------- 7. IMAGENS ----------
rows = [["Arquivo na v0", "Arquivo na v1 (800 px)", "JPG v0", "WebP 480", "WebP 800", "WebP 1200"]]
tot = [0, 0, 0, 0]
for k, (orig, name, alt) in IMAGES.items():
    s0 = os.path.getsize(os.path.join(ROOT, "v0", "imagens", orig)); w = [os.path.getsize(os.path.join(ROOT, "v1", "imagens", f"{name}-{x}.webp")) for x in (480, 800, 1200)]
    rows.append([orig, f"{name}-800.webp", KB(s0) + " KB", KB(w[0]) + " KB", KB(w[1]) + " KB", KB(w[2]) + " KB"]); tot = [tot[0] + s0, tot[1] + w[0], tot[2] + w[1], tot[3] + w[2]]
rows.append(["Total (8 fotos)", "", KB(tot[0]) + " KB", KB(tot[1]) + " KB", KB(tot[2]) + " KB", KB(tot[3]) + " KB"])
pw = lambda url0, url1: (v0["peso_img_pagina"].get(url0, 0), v1["peso_img_pagina"].get(url1, 0))
pp = [("Início", "/", "/"), ("Chás (categoria)", "/Categoria_Chas.html", "/chas/"), ("Chá verde sencha", "/Prod_1.html", "/chas/cha-verde-sencha/"), ("Quem somos", "/sobre.html", "/sobre/")]
S += [P_("7. Otimização de imagens", "h1"), P_("As oito fotos da v0 tinham nomes sem significado (IMG_0412.jpg, foto1.jpg, banner_final_v2.jpg), 1800×1200 px, cerca de 700 KB cada e nenhum texto alternativo. Na v1:"),
      ] + B(["Nomes descritivos em minúsculas com hífen (cha-verde-sencha-800.webp).", "Formato WebP, em três larguras (480, 800 e 1200 px), com qualidade 74; atributo srcset e sizes em todas as imagens de conteúdo.", "width e height em todas as imagens, o que evita deslocamento do layout.", "Texto alternativo descritivo e único (“Xícara de chá verde sencha fumegante ao lado de uma tigela de folhas verdes”).", "Imagem principal de cada página (banner da home e foto do produto) com loading=\"eager\" e fetchpriority=\"high\"; as demais com loading=\"lazy\".", "Imagens de compartilhamento 1200×630 em JPG (og-*.jpg), usadas só nas meta tags."]) + [
      Spacer(1, 4), T(rows, [3.6, 5.2, 2, 2, 2, 2.2]), P_("Peso das imagens carregadas por página (atributo src, tela 1x)", "h2"),
      T([["Página", "v0", "v1 (src de 800 px)", "Redução"]] + [[n_, KB(pw(a, b)[0]) + " KB", KB(pw(a, b)[1]) + " KB", f"{(1 - pw(a, b)[1] / pw(a, b)[0]) * 100:.0f}%"] for n_, a, b in pp], [5.5, 3.5, 4.5, 3.5]),
      P_("A v1 só baixa a largura que o aparelho precisa; em celular, o navegador escolhe a de 480 px (cerca de 20 KB). A foto de produto tinha 700 KB e agora tem entre 20 e 60 KB. As fotos ilustradas do kit têm poucos detalhes e comprimem bem; fotografias reais comprimem menos.", "note"), PageBreak()]

# ---------- 8. ARQUITETURA ----------
dist = {d["url"]: d["cliques"] for d in v1["detalhe"]}
S += [P_("8. Arquitetura do site", "h1"), FIG("arquitetura.png"), P_("Figura 3 – Hierarquia da v1.", "cap"),
      P_("O menu principal (Início, Chás, Acessórios, Quem somos, Contato e Carrinho) e o rodapé aparecem em todas as páginas, então nenhuma página fica a mais de 2 cliques da home. As categorias ligam para seus produtos, os produtos ligam para a categoria (migalhas) e para três produtos relacionados (“Veja também”), e o texto “Como escolher seu chá” da categoria de chás cria links com texto descritivo para cada produto."),
      T([["Página", "Cliques da home (v1)"]] + [[d["url"], dist[d["url"]]] for d in sorted(cand1, key=lambda d: (dist[d["url"]], d["url"]))], [11, 6]),
      Spacer(1, 4), P_("Na v0, três páginas não tinham nenhum link de entrada: <b>" + "</b>, <b>".join(v0["orfas"]) + "</b>. A página Prod_Orfao.html (chá de capim-limão) era um produto à venda que nenhum visitante ou robô conseguia achar; agora ela é /chas/cha-capim-limao/, listada na categoria e no sitemap. Contagem por rastreamento do grafo de links internos (tools/audit.py)."), PageBreak()]

# ---------- 9/10. PALAVRAS-CHAVE E LINKS ----------
S += [P_("9. Palavras-chave e SEO off-page", "h1"), P_("Foram pesquisados 24 termos, classificados por intenção, cada um ligado a uma única página. Os volumes mensais não foram inventados: a coluna fica para o grupo preencher com o Planejador de Palavras-chave ou o Ubersuggest (planilha, aba “Palavras-chave”). Os termos de compra ficam em páginas de produto e de categoria; os de preparo ficam na seção “Como preparar” de cada produto, para não criar páginas finas."),
      T([["#", "Termo", "Intenção", "Página alvo"]] + [[i + 1, k[0], k[1], k[2]] for i, k in enumerate(KEYWORDS)], [0.8, 6.3, 3.6, 6.3]),
      Spacer(1, 4), P_("Para evitar canibalização, o termo genérico (“kit de chá para presente”) fica na categoria e o específico (“comprar kit presente de chá verde”) fica no produto. A planilha confere por fórmula que nenhum termo aparece duas vezes.", "note"),
      P_("Plano de link building ético (6 ações)", "h2"), T([["Ação", "Como executar", "Tipo / atributo do link"]] + [[a, b, c + (" · " + d if d != "—" else "")] for a, b, c, d in LINKS], [4.2, 8, 4.8]),
      P_("Quando usar cada atributo", "h2")] + B([f"<b>rel=\"{r_}\"</b>: {t_}" for r_, t_ in LINK_REGRAS]) + [P_("<b>Evitar:</b> " + PROIBIDO), PageBreak()]

# ---------- 11. URLs ----------
S += [P_("10. URLs e redirecionamentos 301", "h1"), P_("Regras da v1: minúsculas, hífens, sem acentos, sem extensão, sem parâmetros, hierarquia /categoria/produto/ e barra final padronizada. O canonical de cada página é igual à URL final, o que evita duas URLs para o mesmo conteúdo."),
      T([["URL v0 (antes)", "URL v1 (depois)", "Status"]] + [[a, b, "301"] for a, b in REDIRECTS], [5.2, 9.3, 2.5]),
      P_("Os 14 redirecionamentos estão no arquivo v1/_redirects (formato Netlify e Cloudflare Pages). Para que eles valham, a v1 deve ser publicada no mesmo endereço em que a v0 estava ou os endereços da v0 devem ser apontados para a v1; a v0 de comparação pode ficar em outro endereço. <b>O GitHub Pages não faz redirecionamento 301</b> (só meta refresh, que não transmite o mesmo sinal); por isso o repositório recomenda Netlify ou Cloudflare Pages.", "body"),
      P_("Teste feito após a publicação: Prod_1.html responde 301 e leva a /chas/cha-verde-sencha/ (print abaixo).", "note"), PIC(F301, 12.5, "Chrome, aba Rede (19/11/2026): Prod_1.html responde 301 e a página /chas/cha-verde-sencha/ é carregada em seguida (coluna Initiator: /Prod_1.html)."), Spacer(1, 6),
      P_("Pontos de atenção encontrados na v0", "h2")] + B(["home.html e index.html eram a mesma página em duas URLs (conteúdo duplicado).", "Prod_5.html repetia o texto do chá sencha com “kit presente” no título: conteúdo quase duplicado. Na v1 tem texto próprio.", "A extensão .HTML em maiúsculas (produto_camomila.HTML) e os sublinhados e maiúsculas de Categoria_Chas.html são fáceis de errar ao compartilhar.", "A categoria de chás tinha um bloco de palavras repetidas (“chá barato, comprar chá, chá para emagrecer…”), que é técnica de spam e foi removido. As palavras agora aparecem em frases normais."]) + [PageBreak()]

# ---------- 12. DADOS ESTRUTURADOS ----------
prod_ld = re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@type":"Product".*?)</script>', open(os.path.join(ROOT, "v1", "chas", "cha-verde-sencha", "index.html"), encoding="utf-8").read()).group(1)
pj = json.dumps(json.loads(prod_ld), ensure_ascii=False, indent=1).replace(BASE, "…")
pj = re.sub(r'"review": \[.*?\n \]\n?\}$', '"review": [ … 2 avaliações … ]\n}', pj, flags=re.S)
S += [P_("11. Dados estruturados (JSON-LD)", "h1"),
      T([["Tipo de página", "Tipos JSON-LD", "Páginas"], ["Início", "Organization + WebSite", "1"], ["Categorias", "ItemList + BreadcrumbList", "2"], ["Produto", "Product (Offer com preço, moeda e disponibilidade; AggregateRating; Review) + BreadcrumbList", "6"],
         ["Quem somos", "BreadcrumbList", "1"], ["Contato", "Store (endereço, telefone, geo, horário) + BreadcrumbList", "1"], ["Carrinho, checkout, busca, 404", "nenhum (páginas noindex)", "4"]], [4, 10.5, 2.5]),
      Spacer(1, 4), P_("Trecho do JSON-LD da página do chá verde sencha", "h2"), Preformatted(pj[:2300], st["code"]),
      P_(f"<b>Verificação local:</b> o script tools/audit.py conferiu os campos exigidos pelo Google (name, image e offers com price, priceCurrency e availability; BreadcrumbList com position e name) em {sum(d['ld'][0] for d in v1['detalhe'])} blocos JSON-LD, com {v1['ld_erros']} erros. Essa checagem é local e <b>não substitui</b> o Teste de Resultados Enriquecidos do Google."),
      P_("<b>Atenção sobre avaliações.</b> O trabalho pede avaliação em dados estruturados Product, mas proíbe avaliações falsas. Como a loja é fictícia, as 12 avaliações (2 por produto) são <b>de demonstração</b>: aparecem com essa identificação na própria página (“Avaliações de demonstração: textos fictícios criados para o exercício acadêmico”), o que mantém o dado estruturado igual ao conteúdo visível. Se a loja for ao ar, devem ser substituídas por avaliações reais de clientes; o Google não aceita avaliações inventadas."),
      PIC(FRICH, 13.5, "Teste de Resultados Enriquecidos (Google), página do chá verde sencha: 6 itens válidos (Snippets do produto 1, Listagens do comerciante 1, Indicadores de localização atual 1, Snippets de avaliação 3). A listagem do comerciante mostra apenas problemas não críticos, relativos a campos opcionais como frete e política de devolução."), PageBreak()]

# ---------- 13. SEO LOCAL ----------
S += [P_("12. SEO local", "h1"), P_("Mesmo sendo uma loja virtual, a Casa do Chá Serrano é de Catanduva-SP. A estratégia local de uma página usa /contato/ como página de entrada para buscas como “loja de chá em Catanduva”:"),
      ] + B(["<b>NAP igual em todo o site:</b> nome, endereço e telefone aparecem no rodapé de todas as páginas, na página de contato e no JSON-LD com o mesmo formato.", "Mapa incorporado (OpenStreetMap), horário de atendimento e telefone com link tel:.", "JSON-LD do tipo Store com endereço, coordenadas, horário e área de atendimento (Catanduva e Brasil).", "Texto de localização coerente: “Catanduva-SP, no interior de São Paulo” e “envio para todo o Brasil”, sem listar dezenas de cidades.", "Título e descrição da página com a cidade: “Contato e atendimento” e “Endereço em Catanduva-SP, horário e mapa”."]) + [
      P_("Dados fictícios.", "h2"), P_("O kit v0 não informava endereço, então foram usados dados <b>fictícios</b>: “Rua Exemplo, 123, Centro, Catanduva-SP, CEP 15800-000”, horário de segunda a sexta 9h–18h e sábado 9h–13h, e o telefone do kit, (17) 99999-0000. Antes da publicação real, o grupo deve trocar por dados verdadeiros e ajustar tools/sitedata.py (campo NAP) e o mapa."),
      P_("Simulação do perfil no Google Meu Negócio", "h2"), T([["Campo", "Preenchimento"]] + [list(g) for g in GMN], [4, 13]), PIC(FCON, 13.5, "Página /contato/ da v1 publicada (19/11/2026): nome, endereço e telefone, horário de atendimento e mapa incorporado. Endereço e horário são fictícios no exercício."), PageBreak()]

# ---------- 14. SITEMAP ----------
S += [P_("13. Sitemap XML", "h1"), P_("O sitemap.xml lista só as URLs canônicas e indexáveis (11), cada uma com lastmod, e é indicado no robots.txt. Carrinho, checkout, busca e 404 ficam de fora. Conferido por script: o conjunto de URLs do arquivo é " + ("idêntico" if sm_ok else "DIFERENTE do") + " ao conjunto de canonicals das páginas indexáveis."),
      Preformatted(open(os.path.join(ROOT, "v1", "sitemap.xml"), encoding="utf-8").read().replace(BASE, "…")[:1900], st["code"]),
      P_("Envio ao Google Search Console", "h2")] + B(["Adicionar a propriedade com a URL da v1 e verificar a propriedade (arquivo HTML ou meta tag).", "Em Sitemaps, enviar “sitemap.xml” e conferir o status “Êxito” e as 11 páginas descobertas.", "Em Inspeção de URL, testar a home e uma página de produto e pedir a indexação.", "Sem acesso ao Search Console, validar o arquivo em um validador de sitemap e explicar o resultado na apresentação."]) + [PIC(FSM, 13.5, "Search Console, Sitemaps (19/11/2026): /sitemap.xml enviado e lido, status Processado, 11 páginas encontradas. A propriedade foi verificada por tag HTML (meta google-site-verification, na home)."), PageBreak()]

# ---------- 15. ANTES/DEPOIS ----------
S += [P_("14. Comparativo antes e depois", "h1"), P_("Os mesmos testes foram aplicados à v0 e à v1 no mesmo dia (19/11/2026), com os mesmos scripts, sobre as pastas dos repositórios. O Lighthouse foi rodado no Chrome, em modo celular, nas duas URLs públicas, no mesmo dia."),
      T([["Métrica", "v0", "v1", "Observação"], ["SEO no Lighthouse – início", "73", "100", "Chrome, modo celular, 19/11/2026"], ["SEO no Lighthouse – produto", "73", "100", "Idem (v0: Prod_1.html; v1: chá verde sencha)"],
         ["Desempenho – início / produto", "84 / 72", "100 / 100", "Idem"], ["Acessibilidade – início / produto", "76 / 76", "100 / 100", "Idem"], ["Boas práticas – início / produto", "96 / 96", "100 / 100", "Idem"],
         ["Erros W3C", v0["w3c_erros"], v1["w3c_erros"], "Nu HTML Checker, 14 páginas"], ["Erros de dados estruturados", "sem dados", v1["ld_erros"], "Checagem local; conferir no Google"],
         ["Title únicos", f"{v0['title_unicos']}/14", f"{v1['title_unicos']}/14", ""], ["Description únicas", f"{v0['desc_unicas']}/14", f"{v1['desc_unicas']}/14", ""],
         ["Peso da pasta de imagens", f"{KB(v0['peso_imagens_pasta'])} KB", f"{KB(v1['peso_imagens_pasta'])} KB", f"−{(1 - v1['peso_imagens_pasta'] / v0['peso_imagens_pasta']) * 100:.0f}%"],
         ["Páginas a mais de 3 cliques", len(v0["mais_de_3"]), len(v1["mais_de_3"]), "Inclui páginas órfãs"], ["Páginas com um único h1", f"{sum(d['h1'] == 1 for d in v0['detalhe'])}/14", f"{sum(d['h1'] == 1 for d in v1['detalhe'] if d['arquivo'] != '/404.html')}/14", ""],
         ["Imagens sem alt", sum(d["sem_alt"] for d in v0["detalhe"]), sum(d["sem_alt"] for d in v1["detalhe"]), "Total de <img>"]], [6, 2.6, 2.6, 5.8]),
      Spacer(1, 6), P_("Auditorias estáticas parecidas com as do Lighthouse (verificação local, não é a nota do Lighthouse)", "h2"),
      T([["Auditoria", "v0 (de 14 páginas)", "v1 (de 14 páginas)"]] + [[k, v0["proxy"][k], v1["proxy"][k]] for k in v0["proxy"]], [8, 4.5, 4.5]),
      Spacer(1, 4), PICS([(FLH0, "v0 início: Desempenho 84 · Acessibilidade 76 · Boas práticas 96 · SEO 73"), (FLH0P, "v0 produto (Prod_1.html): 72 · 76 · 96 · 73"), (FLH1, "v1 início: 100 · 100 · 100 · 100"), (FLH1P, "v1 produto (chá verde sencha): 100 · 100 · 100 · 100")], 8.2), P_("Limitações. As notas de desempenho do Lighthouse e a posição real no Google dependem de publicação, tempo e indexação, e não são prometidas aqui. A v1 melhora as bases técnicas (rastreamento, semântica, imagens, dados), mas a posição final depende também da concorrência e de conteúdo novo.", "note"), PageBreak()]

# ---------- 16. CONCLUSÕES ----------
S += [P_("15. Conclusões e próximos passos", "h1"), P_("A v1 elimina os problemas técnicos que a v0 tinha de propósito: páginas órfãs, duplicadas e sem título, URLs ruins, imagens pesadas e sem alt, sem dados estruturados e sem controle de indexação. A medida mais importante para uma loja foi dar a cada produto uma URL limpa, um título e uma descrição próprios e dados estruturados de Product, porque é isso que torna o produto encontrável e elegível a resultados enriquecidos."),
      P_("O que falta fazer (depende do grupo)", "h2")] + B(["Subir o repositório no Git com o professor como leitor e fazer commits de cada integrante.", "Acompanhar os três indicadores no Search Console.", "Trocar os dados fictícios (endereço, horário) e as avaliações de demonstração por dados reais.", "Ajustar nomes dos integrantes na capa, na apresentação e no README."]) + [
      P_("Declaração de uso de IA", "h1"),
      P_("Ferramenta usada: <b>Claude (Anthropic)</b>, em conversa com o grupo, em 19/11/2026. O uso é declarado abaixo, como o enunciado exige."),
      T([["Parte do trabalho", "Uso da IA"],
         ["Código do site v1", "Gerado pela IA: gerador estático em Python, HTML, CSS e JavaScript."],
         ["Textos do site, títulos e descrições", "Redigidos pela IA a partir do kit v0."],
         ["Scripts de auditoria, planilha, relatório, slides e diagramas", "Gerados pela IA; os números vêm dos scripts, nada foi estimado."],
         ["Análise do kit v0 e do enunciado", "Feita pela IA, com orientação passo a passo ao grupo."]], [6.5, 10.5]),
      Spacer(1, 6), P_("O que o grupo fez", "h2"),
      T([["Atividade", "Feita pelo grupo"],
         ["Publicação", "Publicação da v0 e da v1 no Netlify, com os nomes dos endereços."],
         ["Testes com ferramentas reais", "Lighthouse (4 páginas), validador W3C, Teste de Resultados Enriquecidos e teste do 301 no navegador."],
         ["Search Console", "Criação da propriedade, verificação por tag HTML, envio do sitemap e conferência do robots.txt."],
         ["Evidências", "Todos os prints deste relatório foram tirados pelo grupo nas URLs públicas."],
         ["Decisões e correções", "Pedido de ajuste do cabeçalho do site; definição do repositório e dos integrantes."]], [6.5, 10.5]),
      P_("Todos os integrantes são responsáveis por conhecer e saber explicar cada parte entregue, já que qualquer um pode ser chamado na apresentação.", "note"),
      P_("Como reproduzir", "h2"), Preformatted("python3 tools/build.py          # gera v1/ (BASE_URL=https://seu-site python3 tools/build.py)\npython3 tools/audit.py          # mede v0 e v1 e grava tools/metrics.json\njava -jar vnu.jar v1/**/*.html  # validador W3C (Nu HTML Checker)", st["code"])]

doc = Doc(os.path.join(ROOT, "docs", "Relatorio_SEO_Grupo1.pdf")); doc.multiBuild(S)
from pypdf import PdfReader; print("páginas:", len(PdfReader(os.path.join(ROOT, "docs", "Relatorio_SEO_Grupo1.pdf")).pages), "sitemap ok:", sm_ok, "robots:", rtests)
