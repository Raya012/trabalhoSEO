# -*- coding: utf-8 -*-
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sitedata import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "fig"); os.makedirs(OUT, exist_ok=True)
G, D, S = "#2e6b3f", "#1f3d2a", "#e8f0e2"
plt.rcParams["font.family"] = "DejaVu Sans"
M = json.load(open(os.path.join(ROOT, "tools", "metrics.json")))

def box(ax, x, y, w, h, t, fc=S, ec=G, fs=9, bold=False, tc=D):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal", wrap=True)

# 1. rastrear -> indexar -> ranquear
fig, ax = plt.subplots(figsize=(9, 2.6)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 3.2)
steps = [("1. Rastrear", "O Googlebot segue links,\nlê robots.txt e sitemap.xml"), ("2. Indexar", "Lê HTML, títulos, texto,\nimagens e JSON-LD; guarda a página"), ("3. Ranquear", "Compara com a busca\n(intenção, qualidade, relevância)")]
for i, (a, b) in enumerate(steps):
    x = 0.2 + i * 4
    box(ax, x, 1.7, 3.4, 1.1, a, fc=G, tc="white", bold=True, fs=11); box(ax, x, 0.2, 3.4, 1.3, b, fs=8.5)
    if i < 2: ax.annotate("", xy=(x + 3.95, 2.25), xytext=(x + 3.45, 2.25), arrowprops=dict(arrowstyle="->", color=D, lw=2))
fig.savefig(f"{OUT}/fluxo-indexacao.png", dpi=170, bbox_inches="tight"); plt.close(fig)

# 2. arquitetura do site
fig, ax = plt.subplots(figsize=(9, 4.6)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 6.4)
box(ax, 4.6, 5.4, 2.8, .8, "Início  /", fc=G, tc="white", bold=True, fs=10)
box(ax, 0.3, 3.7, 2.4, .8, "Chás  /chas/", fs=9); box(ax, 3.2, 3.7, 2.6, .8, "Acessórios  /acessorios/", fs=9)
box(ax, 6.3, 3.7, 2.4, .8, "Quem somos  /sobre/", fs=9); box(ax, 9.2, 3.7, 2.5, .8, "Contato  /contato/", fs=9)
for x in (1.5, 4.5, 7.5, 10.45): ax.plot([6, x], [5.4, 4.5], color=D, lw=1.2)
prods = ["Sencha", "Assam", "Hibisco", "Camomila", "Capim-limão"]
for i, p in enumerate(prods):
    x = 0.1 + i * 1.18; box(ax, x, 1.6, 1.08, .7, p, fs=7.5, fc="white"); ax.plot([1.5, x + .54], [3.7, 2.3], color=G, lw=.9)
box(ax, 6.4, 1.6, 1.9, .7, "Kit presente", fs=8, fc="white"); ax.plot([4.5, 7.35], [3.7, 2.3], color=G, lw=.9)
box(ax, 8.8, 1.45, 3.0, 1.0, "Fora do índice (noindex):\n/carrinho/ · /checkout/ · /busca/", fs=8, fc="#f6e3d9", ec="#b85042")
ax.text(0.3, 0.8, "Nível 0 = home · Nível 1 = categorias e institucionais (1 clique) · Nível 2 = produtos (2 cliques)\nOs produtos também se ligam entre si por \"Veja também\"; o menu e o rodapé aparecem em todas as páginas.", fontsize=8, color=D, va="center")
fig.savefig(f"{OUT}/arquitetura.png", dpi=170, bbox_inches="tight"); plt.close(fig)

# 3. antes/depois (peso e pontos)
v0, v1 = M["v0"], M["v1"]
fig, axs = plt.subplots(1, 3, figsize=(9, 2.9))
def bars(ax, a, b, title, fmt):
    r = ax.bar(["v0", "v1"], [a, b], color=["#b85042", G], width=.55); ax.set_title(title, fontsize=9, color=D)
    for rect, v in zip(r, [a, b]): ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height(), fmt(v), ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False); ax.set_ylim(0, max(a, b) * 1.22); ax.tick_params(labelsize=8)
bars(axs[0], v0["peso_imagens_pasta"] / 1024, v1["peso_imagens_pasta"] / 1024, "Peso da pasta de imagens (KB)", lambda v: f"{v:,.0f}".replace(",", "."))
bars(axs[1], v0["w3c_erros"], v1["w3c_erros"], "Erros no validador W3C", lambda v: f"{v:.0f}")
bars(axs[2], v0["title_unicos"], v1["title_unicos"], "Páginas com title único (de 14)", lambda v: f"{v:.0f}")
fig.tight_layout(); fig.savefig(f"{OUT}/antes-depois.png", dpi=170); plt.close(fig)
print("figuras ok")
