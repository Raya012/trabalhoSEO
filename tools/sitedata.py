# -*- coding: utf-8 -*-
"""Dados do site v1 - Casa do Chá Serrano (Grupo 1). Fonte única para site, planilha e relatório."""
import os
BASE = os.environ.get("BASE_URL", "https://casadochaserrano.netlify.app").rstrip("/")
BRAND = "Casa do Chá Serrano"
TODAY = "2026-11-13"
NAP = dict(street="Rua Exemplo, 123", district="Centro", city="Catanduva", region="SP",
           zip="15800-000", phone="(17) 99999-0000", phone_intl="+55-17-99999-0000",
           email="contato@casadochaserrano.example", lat=-21.1378, lng=-48.9728)

# chave da imagem -> (arquivo original no v0, nome novo, alt descritivo)
IMAGES = {
 "sencha":  ("IMG_0412.jpg", "cha-verde-sencha", "Xícara de chá verde sencha fumegante ao lado de uma tigela de folhas verdes"),
 "assam":   ("IMG_0413.jpg", "cha-preto-assam", "Xícara de chá preto Assam quente ao lado de uma tigela de folhas escuras e um cubo de açúcar"),
 "hibisco": ("IMG_0414.jpg", "cha-hibisco-laranja", "Copo de chá de hibisco gelado, com gelo, flores de hibisco e fatias de laranja"),
 "camomila":("IMG_0415.jpg", "cha-camomila-organica", "Xícara de chá de camomila quente ao lado de flores de camomila"),
 "capim":   ("DSC00982.jpg", "cha-capim-limao", "Xícara de chá de capim-limão com fatias de limão e folhas de capim-limão ao fundo"),
 "kit":     ("DSC00981.jpg", "kit-presente-cha-verde", "Caixa de presente vermelha com laço dourado e duas latas de chá"),
 "banner":  ("banner_final_v2.jpg", "bule-e-xicaras-de-cha", "Bule verde e duas xícaras de chá sobre a mesa, com folhas de chá espalhadas"),
 "loja":    ("foto1.jpg", "prateleiras-de-latas-de-cha", "Prateleiras com dezenas de latas coloridas de chá e duas xícaras no balcão"),
}

PRODUCTS = [
 dict(slug="cha-verde-sencha", cat="chas", img="sencha", sku="CCS-001", name="Chá verde sencha", price=34.90, peso="50 g",
  title="Chá verde sencha em folhas, 50 g | Casa do Chá Serrano",
  desc="Chá verde sencha de folha inteira, colhido na primavera, com sabor suave e vegetal. Pacote de 50 g por R$ 34,90 na Casa do Chá Serrano.",
  paras=["Chá verde de folha inteira, colhido na primavera. Sabor suave e vegetal, ideal para o início do dia. Pacote de 50 g.",
         "O sencha é um chá verde em folhas, apreciado pelo gosto fresco e levemente adocicado. Fica ótimo puro, sem açúcar, e acompanha bem o café da manhã."],
  prep="Use 1 colher de chá (cerca de 2 g) para cada 200 ml de água a 75–80 °C. Deixe em infusão por 2 a 3 minutos e coe. Água muito quente deixa o sabor amargo.",
  rel=["cha-preto-assam","cha-camomila-organica","kit-presente-cha-verde"],
  reviews=[(5,"Cliente de demonstração 1","Folhas inteiras e aroma fresco. Rende bem."),(4,"Cliente de demonstração 2","Sabor suave, bom para tomar de manhã.")]),
 dict(slug="cha-preto-assam", cat="chas", img="assam", sku="CCS-002", name="Chá preto Assam", price=29.90, peso="50 g",
  title="Chá preto Assam em folhas, 50 g | Casa do Chá Serrano",
  desc="Chá preto Assam encorpado, com notas maltadas, ótimo para tomar com leite. Pacote de 50 g por R$ 29,90 na Casa do Chá Serrano.",
  paras=["Chá preto encorpado, com notas maltadas, bom para ser tomado com leite. Pacote de 50 g.",
         "O Assam tem cor intensa e sabor marcante, por isso é uma boa escolha para quem gosta de chá forte no café da manhã ou na hora do lanche."],
  prep="Use 1 colher de chá para cada 200 ml de água a 95–100 °C. Deixe em infusão por 3 a 5 minutos. Combina com leite e com um pouco de açúcar.",
  rel=["cha-verde-sencha","cha-hibisco-laranja","cha-capim-limao"],
  reviews=[(5,"Cliente de demonstração 3","Encorpado, fica ótimo com leite."),(4,"Cliente de demonstração 4","Sabor forte, do jeito que eu gosto.")]),
 dict(slug="cha-hibisco-laranja", cat="chas", img="hibisco", sku="CCS-003", name="Chá de hibisco com laranja", price=27.50, peso="60 g",
  title="Chá de hibisco com laranja, 60 g | Casa do Chá Serrano",
  desc="Infusão de flores secas de hibisco com casca de laranja, servida quente ou gelada. Pacote de 60 g por R$ 27,50 na Casa do Chá Serrano.",
  paras=["Infusão de flores secas de hibisco com casca de laranja, servida quente ou gelada. Pacote de 60 g.",
         "A cor vermelha intensa e o toque cítrico da laranja fazem dela uma infusão refrescante, muito pedida para dias quentes."],
  prep="Use 1 colher de sopa para cada 300 ml de água a 90–95 °C e deixe em infusão por 5 a 7 minutos. Para tomar gelado, coe, deixe esfriar e sirva com gelo e fatias de laranja.",
  rel=["cha-capim-limao","cha-camomila-organica","cha-preto-assam"],
  reviews=[(5,"Cliente de demonstração 5","Gelada com laranja é a minha favorita."),(5,"Cliente de demonstração 6","Cor linda e sabor refrescante.")]),
 dict(slug="cha-camomila-organica", cat="chas", img="camomila", sku="CCS-004", name="Chá de camomila orgânica", price=24.90, peso="40 g",
  title="Chá de camomila orgânica, 40 g | Casa do Chá Serrano",
  desc="Flores inteiras de camomila orgânica para tomar à noite, em pacote de 40 g por R$ 24,90. Compre online na Casa do Chá Serrano.",
  paras=["Flores inteiras de camomila orgânica, para relaxar à noite. Pacote de 40 g.",
         "As flores são vendidas inteiras, sem misturas, o que deixa a infusão com aroma suave e sabor delicado."],
  prep="Use 1 colher de sopa de flores para cada 200 ml de água a 90–95 °C. Tampe a xícara e deixe em infusão por 5 minutos antes de coar.",
  rel=["cha-capim-limao","cha-hibisco-laranja","cha-verde-sencha"],
  reviews=[(5,"Cliente de demonstração 7","Flores inteiras e muito aromáticas."),(4,"Cliente de demonstração 8","Ótima para tomar antes de dormir.")]),
 dict(slug="cha-capim-limao", cat="chas", img="capim", sku="CCS-005", name="Chá de capim-limão", price=22.90, peso="40 g",
  title="Chá de capim-limão, 40 g | Casa do Chá Serrano",
  desc="Infusão cítrica e refrescante de capim-limão, em pacote de 40 g por R$ 22,90. Compre online na Casa do Chá Serrano.",
  paras=["Infusão cítrica e refrescante. Pacote de 40 g.",
         "O capim-limão dá à bebida um aroma de limão suave, sem acidez, e funciona bem quente ou gelado."],
  prep="Use 1 colher de sopa para cada 250 ml de água fervente e deixe em infusão por 5 a 8 minutos. Pode ser servido gelado com uma fatia de limão.",
  rel=["cha-hibisco-laranja","cha-camomila-organica","cha-verde-sencha"],
  reviews=[(4,"Cliente de demonstração 9","Aroma de limão bem agradável."),(5,"Cliente de demonstração 10","Refrescante, bom para o calor.")]),
 dict(slug="kit-presente-cha-verde", cat="acessorios", img="kit", sku="CCS-006", name="Kit presente de chá verde", price=79.90, peso="50 g de chá",
  title="Kit presente de chá verde sencha | Casa do Chá Serrano",
  desc="Kit presente com chá verde sencha de folha inteira (50 g) em caixa de presente. R$ 79,90 na Casa do Chá Serrano, com envio para todo o Brasil.",
  paras=["Kit presente com chá verde sencha de folha inteira, colhido na primavera, em pacote de 50 g. Acompanha caixa de presente.",
         "Uma opção prática para presentear quem gosta de chá ou quer conhecer o chá verde: o kit já vai embalado e pronto para entregar."],
  prep="O chá do kit é o mesmo chá verde sencha da loja: 1 colher de chá para cada 200 ml de água a 75–80 °C, por 2 a 3 minutos.",
  rel=["cha-verde-sencha","cha-preto-assam","cha-camomila-organica"],
  reviews=[(5,"Cliente de demonstração 11","Presente bonito e bem embalado."),(5,"Cliente de demonstração 12","Chegou rápido e a caixa é caprichada.")]),
]
for p in PRODUCTS:
    p["url"] = f"/{'chas' if p['cat']=='chas' else 'acessorios'}/{p['slug']}/"
    p["avg"] = round(sum(r[0] for r in p["reviews"]) / len(p["reviews"]), 1)
    p["price_str"] = "R$ " + f"{p['price']:.2f}".replace(".", ",")
PBY = {p["slug"]: p for p in PRODUCTS}

CATS = {
 "chas": dict(url="/chas/", name="Chás", h1="Chás em folhas e infusões",
   title="Comprar chá online: verde, preto e infusões | Casa do Chá",
   desc="Escolha entre chá verde, chá preto, hibisco, camomila e capim-limão. Chás em folhas e infusões com envio para todo o Brasil.", img="sencha"),
 "acessorios": dict(url="/acessorios/", name="Acessórios", h1="Kits presente e acessórios",
   title="Kits presente de chá | Casa do Chá Serrano",
   desc="Kit presente de chá verde em caixa de presente, pronto para dar de lembrança. Veja os kits e acessórios da Casa do Chá Serrano.", img="kit"),
}
# páginas fixas: chave -> (url, title, description, imagem og, indexável)
STATIC = {
 "home":    ("/", "Casa do Chá Serrano | Chás em folhas e infusões online",
             "Loja de chás de Catanduva-SP: chá verde, chá preto, hibisco, camomila e kits presente. Folhas selecionadas e envio para todo o Brasil.", "banner", True),
 "sobre":   ("/sobre/", "Quem somos: loja de chás de Catanduva-SP | Casa do Chá",
             "Conheça a Casa do Chá Serrano, loja familiar de Catanduva-SP que importa e embala chás em folhas e infusões desde 2019.", "loja", True),
 "contato": ("/contato/", "Contato e atendimento | Casa do Chá Serrano",
             "Fale com a Casa do Chá Serrano por WhatsApp ou e-mail. Endereço em Catanduva-SP, horário de atendimento e mapa de localização.", "loja", True),
 "carrinho":("/carrinho/", "Carrinho de compras | Casa do Chá Serrano", "Veja os itens do seu carrinho na Casa do Chá Serrano.", "banner", False),
 "checkout":("/checkout/", "Finalizar compra | Casa do Chá Serrano", "Etapa final da compra (simulação) na Casa do Chá Serrano.", "banner", False),
 "busca":   ("/busca/", "Buscar produtos | Casa do Chá Serrano", "Busque chás e kits presente no catálogo da Casa do Chá Serrano.", "banner", False),
}
HOURS = [("Mo-Fr","09:00","18:00"),("Sa","09:00","13:00")]

# mapa v0 -> v1 (redirecionamentos 301)
REDIRECTS = [
 ("/index.html","/"),("/home.html","/"),
 ("/Categoria_Chas.html","/chas/"),("/Categoria_Acessorios.html","/acessorios/"),
 ("/Prod_1.html","/chas/cha-verde-sencha/"),("/Prod_2.html","/chas/cha-preto-assam/"),
 ("/Prod_3.html","/chas/cha-hibisco-laranja/"),("/produto_camomila.HTML","/chas/cha-camomila-organica/"),
 ("/Prod_Orfao.html","/chas/cha-capim-limao/"),("/Prod_5.html","/acessorios/kit-presente-cha-verde/"),
 ("/sobre.html","/sobre/"),("/contato.html","/contato/"),("/carrinho.html","/carrinho/"),("/busca.html","/busca/"),
]
