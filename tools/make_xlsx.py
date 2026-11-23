# -*- coding: utf-8 -*-
import json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from sitedata import *
from planning import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, "tools", "metrics.json")))
v0, v1 = M["v0"], M["v1"]
F = "Arial"; thin = Side(style="thin", color="BBBBBB"); B = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD = PatternFill("solid", fgColor="1F3D2A"); YEL = PatternFill("solid", fgColor="FFFF00"); OKF = PatternFill("solid", fgColor="E8F0E2")
wb = Workbook()

def sheet(name, headers, rows, widths, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = name
    for j, h in enumerate(headers, 1):
        c = ws.cell(1, j, h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = HEAD; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = B
    for i, r in enumerate(rows, 2):
        for j, v in enumerate(r, 1):
            c = ws.cell(i, j, v); c.font = Font(name=F, size=10); c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = B
    for j, w in enumerate(widths, 1): ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = "A2"; ws.row_dimensions[1].height = 32
    return ws

# 1. Palavras-chave
kw_rows = [(i + 1, k[0], k[1], k[2], k[3], None, k[4]) for i, k in enumerate(KEYWORDS)]
ws = sheet("Palavras-chave", ["#", "Termo de busca", "Intenção", "Página alvo (v1)", "Prioridade", "Volume mensal (preencher)", "Observação"], kw_rows, [5, 40, 22, 40, 11, 18, 55], first=True)
n = len(KEYWORDS)
for r in range(2, n + 2): ws.cell(r, 6).fill = YEL
ws.cell(n + 3, 2, "Termos duplicados (deve ser 0):").font = Font(name=F, bold=True)
ws.cell(n + 3, 4, f'=SUMPRODUCT(--(COUNTIF(B2:B{n+1},B2:B{n+1})>1))').font = Font(name=F, bold=True)
for k, t in enumerate([INFO, NAV, INV, TRA]):
    ws.cell(n + 4 + k, 2, f"Termos – {t}").font = Font(name=F); ws.cell(n + 4 + k, 4, f'=COUNTIF(C2:C{n+1},"{t}")').font = Font(name=F)
ws.cell(n + 9, 2, "Total de termos").font = Font(name=F, bold=True); ws.cell(n + 9, 4, f"=COUNTA(B2:B{n+1})").font = Font(name=F, bold=True)
ws.cell(n + 11, 2, "Legenda: células amarelas = a preencher. O volume vem do Planejador de Palavras-chave do Google Ads ou do Ubersuggest (não foi inventado). Cada termo aponta para uma única página.").font = Font(name=F, italic=True, size=9)

# 2. Mapa KW -> página
urls = ["/", "/chas/", "/acessorios/"] + [p["url"] for p in PRODUCTS] + ["/sobre/", "/contato/"]
rows = []
for i, ur in enumerate(urls, 2):
    rows.append((ur, f"=COUNTIF('Palavras-chave'!$D$2:$D${n+1},A{i})", '=IF(B%d>0,"Sim","Sem termo (ok se institucional)")' % i,
                 "; ".join(k[0] for k in KEYWORDS if k[2] == ur) or "—"))
sheet("Mapa termo-página", ["Página (URL)", "Nº de termos", "Tem termo?", "Termos mapeados"], rows, [42, 12, 28, 100])

# 3. Title e description
rows = []
cand = [p for p in v1["detalhe"] if p["arquivo"] != "/404.html"]
order = {u: i for i, u in enumerate(urls + ["/carrinho/", "/checkout/", "/busca/"])}
cand.sort(key=lambda d: order.get(d["url"], 99))
N = len(cand)
for i, d in enumerate(cand, 2):
    rows.append((d["url"], d["title"], f"=LEN(B{i})", f'=IF(AND(C{i}>0,C{i}<=60),"OK","Revisar")', f"=IF(COUNTIF($B$2:$B${N+1},B{i})=1,\"Único\",\"Duplicado\")",
                 d["desc"], f"=LEN(F{i})", f'=IF(AND(G{i}>0,G{i}<=160),"OK","Revisar")', f"=IF(COUNTIF($F$2:$F${N+1},F{i})=1,\"Única\",\"Duplicada\")", "Não" if d["noindex"] else "Sim"))
ws = sheet("Title e description", ["URL", "Title", "Caracteres", "Limite 60", "Título único?", "Description", "Caracteres", "Limite 160", "Description única?", "Indexável?"], rows, [38, 52, 11, 10, 13, 70, 11, 10, 15, 11])
ws.cell(N + 3, 1, "Páginas com title único").font = Font(name=F, bold=True); ws.cell(N + 3, 2, f'=COUNTIF(E2:E{N+1},"Único")&" de "&COUNTA(A2:A{N+1})').font = Font(name=F, bold=True)
ws.cell(N + 4, 1, "Páginas com description única").font = Font(name=F, bold=True); ws.cell(N + 4, 2, f'=COUNTIF(I2:I{N+1},"Única")&" de "&COUNTA(A2:A{N+1})').font = Font(name=F, bold=True)

# 4. URLs antes/depois
rows = []
for i, (a, b) in enumerate(REDIRECTS, 2):
    rows.append((a, P_ if (P_ := "") else b, f"=LEN(A{i})", f"=LEN(B{i})", 301, "Sim" if a != b else "—"))
ws = sheet("URLs antes-depois", ["URL v0 (antes)", "URL v1 (depois)", "Caracteres antes", "Caracteres depois", "Status", "Mudou?"], rows, [30, 42, 14, 14, 9, 9])
notes = ["Problemas da v0: maiúsculas (Categoria_Chas.html), sublinhado em vez de hífen, extensão .HTML em maiúsculas (produto_camomila.HTML), nomes sem significado (Prod_1, Prod_5), duas URLs para a mesma home (index.html e home.html), produto sem categoria na URL.",
         "v1: minúsculas, hífens, sem acentos, sem extensão, sem parâmetros; hierarquia /categoria/produto/; barra final padronizada; canonical igual à URL final."]
for k, t in enumerate(notes): ws.cell(len(REDIRECTS) + 3 + k, 1, t).font = Font(name=F, size=9, italic=True)

# 5. Redirecionamentos 301
rows = [(i, a, b, 301, f"{a}  {b}  301", "Netlify / Cloudflare Pages (_redirects)") for i, (a, b) in enumerate(REDIRECTS, 1)]
sheet("Redirects 301", ["#", "De (v0)", "Para (v1)", "Código", "Linha do arquivo _redirects", "Onde funciona"], rows, [5, 28, 42, 9, 62, 38])

# 6. Mídia paga
rows = [(i + 1, k[0], k[1], k[2], "Simulada: sem gasto") for i, k in enumerate(SEM_KW)]
ws = sheet("Mídia paga", ["#", "Palavra-chave", "Tipo de correspondência", "Como escrever na campanha", "Observação"], rows, [5, 34, 22, 36, 24])
r0 = len(rows) + 3
ws.cell(r0, 1, "Palavras-chave negativas: " + ", ".join(NEGATIVAS)).font = Font(name=F, size=10, bold=True)
r = r0 + 2
for a in ANUNCIOS:
    ws.cell(r, 1, a["nome"]).font = Font(name=F, bold=True); ws.cell(r, 4, f"Grupo: {a['grupo']} · URL final: {BASE}{a['url']}").font = Font(name=F, size=9); r += 1
    for t in a["titulos"]:
        ws.cell(r, 2, "Título").font = Font(name=F, size=10); ws.cell(r, 3, t).font = Font(name=F, size=10); ws.cell(r, 4, f"=LEN(C{r})&\" / 30 caracteres\"").font = Font(name=F, size=9); r += 1
    for t in a["descricoes"]:
        ws.cell(r, 2, "Descrição").font = Font(name=F, size=10); ws.cell(r, 3, t).font = Font(name=F, size=10); ws.cell(r, 4, f"=LEN(C{r})&\" / 90 caracteres\"").font = Font(name=F, size=9); r += 1
    r += 1
ws.column_dimensions["C"].width = 60

# 7. Link building
rows = [(i + 1, a, b, c, d) for i, (a, b, c, d) in enumerate(LINKS)]
ws = sheet("Link building", ["#", "Ação", "Como executar", "Tipo de link / atributo", "Quando usar outro atributo"], rows, [4, 38, 62, 38, 42])
r = len(rows) + 3
for rel, txt in LINK_REGRAS:
    ws.cell(r, 2, f'rel="{rel}"').font = Font(name=F, bold=True); ws.cell(r, 3, txt).font = Font(name=F, size=10); r += 1
ws.cell(r + 1, 2, "O que NÃO fazer").font = Font(name=F, bold=True, color="C00000"); ws.cell(r + 1, 3, PROIBIDO).font = Font(name=F, size=10)

# 8. Métricas antes/depois
def kb(x): return round(x / 1024, 1)
rows = [
 ("Nota de SEO no Lighthouse (home)", 73, 100, "Chrome > Lighthouse, modo celular, URLs públicas, 19/11/2026"),
 ("Nota de SEO no Lighthouse (página de produto)", 73, 100, "Idem (v0: Prod_1.html; v1: chá verde sencha)"),
 ("Desempenho no Lighthouse (home)", 84, 100, "Idem"), ("Desempenho no Lighthouse (produto)", 72, 100, "Idem"),
 ("Acessibilidade no Lighthouse (home e produto)", 76, 100, "Mesma nota nas duas páginas"), ("Boas práticas no Lighthouse (home e produto)", 96, 100, "Mesma nota nas duas páginas"),
 ("Erros do validador W3C (14 páginas HTML)", v0["w3c_erros"], v1["w3c_erros"], "Nu HTML Checker (vnu 24.x) rodado localmente em todas as páginas"),
 ("Erros de dados estruturados (JSON-LD, checagem local)", v0["ld_erros"], v1["ld_erros"], "v0 não tem nenhum bloco; conferir v1 também no Teste de Resultados Enriquecidos"),
 ("Páginas de produto com dados estruturados Product", v0["produtos_ld"], v1["produtos_ld"], "de 6 páginas de produto"),
 ("Páginas com title único", v0["title_unicos"], v1["title_unicos"], "de 14 páginas (404 excluída)"),
 ("Páginas com description única", v0["desc_unicas"], v1["desc_unicas"], "de 14 páginas"),
 ("Peso total da pasta de imagens (KB)", kb(v0["peso_imagens_pasta"]), kb(v1["peso_imagens_pasta"]), "v1 inclui 3 tamanhos WebP por foto e imagens de compartilhamento"),
 ("Páginas a mais de 3 cliques da home (inclui órfãs)", len(v0["mais_de_3"]), len(v1["mais_de_3"]), "v0: home.html, busca.html e Prod_Orfao.html sem link de entrada"),
 ("Páginas órfãs", len(v0["orfas"]), len(v1["orfas"]), "Rastreio do grafo de links internos a partir da home"),
 ("Imagens sem texto alternativo", sum(d["sem_alt"] for d in v0["detalhe"]), sum(d["sem_alt"] for d in v1["detalhe"]), "Total de tags <img>"),
 ("Páginas com exatamente um h1", sum(d["h1"] == 1 for d in v0["detalhe"] if d["arquivo"] != "/404.html"), sum(d["h1"] == 1 for d in v1["detalhe"] if d["arquivo"] != "/404.html"), "de 14 páginas; Categoria_Chas tinha 2 h1 e as demais usavam h2/h3"),
]
ws = sheet("Métricas antes-depois", ["Métrica", "v0 (antes)", "v1 (depois)", "Variação", "Como foi medido"], [(a, b, c, None, d) for a, b, c, d in rows], [52, 14, 14, 14, 70])
for i in range(2, len(rows) + 2):
    ws.cell(i, 4, f'=IF(AND(ISNUMBER(B{i}),ISNUMBER(C{i}),B{i}<>0),(C{i}-B{i})/B{i},"—")').number_format = "0%"; ws.cell(i, 4).font = Font(name=F, size=10)
ws.cell(len(rows) + 3, 1, "Lighthouse: execução real do grupo. Demais valores vieram do script tools/audit.py. W3C: validado por envio de arquivo, porque o Netlify injeta um script externo na página publicada.").font = Font(name=F, italic=True, size=9)

wb.move_sheet("Métricas antes-depois", offset=-(len(wb.sheetnames) - 1))
out = os.path.join(ROOT, "docs"); os.makedirs(out, exist_ok=True)
wb.save(os.path.join(out, "Planilha_SEO_Grupo1.xlsx")); print("ok")
