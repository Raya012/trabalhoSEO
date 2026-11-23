# -*- coding: utf-8 -*-
"""Dados de planejamento (estratégia, SEM, palavras-chave, link building) - fonte única p/ planilha, relatório e slides."""
from sitedata import PBY
U = lambda s: PBY[s]["url"]
SEN, ASS, HIB, CAM, CAP, KIT = (U(s) for s in ("cha-verde-sencha", "cha-preto-assam", "cha-hibisco-laranja", "cha-camomila-organica", "cha-capim-limao", "kit-presente-cha-verde"))

OBJETIVO = ("Vender chás em folhas e infusões e kits presente pela internet para todo o Brasil, fazendo cada produto ser encontrado "
            "em buscas por compra e por modo de preparo, e reforçando o reconhecimento da marca em Catanduva e região.")
PERSONAS = [
 ("Marina, 34 anos – quer relaxar à noite", "Analista administrativa em Catanduva-SP. Toma chá à noite, compra pela internet e pelo celular. Busca camomila e capim-limão, prefere produto orgânico e quer saber como preparar.",
  "Pesquisa por modo de preparo e depois por \"comprar chá de camomila\". Precisa de descrição clara, peso do pacote e avaliações."),
 ("Roberto, 52 anos – procura um presente", "Gerente comercial em Ribeirão Preto-SP. Quer dar um presente prático a clientes e familiares, sem tempo para escolher muito. Valoriza embalagem bonita e envio rápido.",
  "Pesquisa \"kit de chá para presente\" e compara opções. Precisa de preço visível, foto da embalagem e informação de envio.")]
INDICADORES = [
 ("Páginas indexadas", "11 de 11 páginas indexáveis no relatório de cobertura do Search Console em até 30 dias", "Search Console > Páginas"),
 ("Cliques orgânicos por mês", "100 cliques/mês no 3º mês após a publicação (meta inicial, a ajustar com a linha de base)", "Search Console > Desempenho"),
 ("Posição média das consultas de compra", "Posição média ≤ 20 em 3 meses e ≤ 10 em 6 meses para as 8 consultas transacionais", "Search Console > Desempenho (filtro por consulta)"),
]

# (termo, intenção, página, prioridade, observação)
INFO, NAV, INV, TRA = "Informacional", "Navegacional", "Investigação comercial", "Transacional"
KEYWORDS = [
 ("como preparar chá verde sencha", INFO, SEN, "Média", "Seção \"Como preparar\" da página do produto"),
 ("temperatura da água para chá verde", INFO, SEN, "Média", "Atender dúvida frequente no mesmo texto de preparo"),
 ("tempo de infusão do chá preto", INFO, ASS, "Média", "Seção \"Como preparar\""),
 ("como fazer chá de hibisco gelado", INFO, HIB, "Alta", "Receita gelada descrita na página; boa para sazonalidade de calor"),
 ("como fazer chá de camomila com flores", INFO, CAM, "Média", "Seção \"Como preparar\""),
 ("diferença entre chá verde e chá preto", INFO, "/chas/", "Média", "Texto \"Como escolher seu chá\" com links para os produtos"),
 ("casa do chá serrano", NAV, "/", "Alta", "Termo de marca; home deve ser o 1º resultado"),
 ("casa do chá serrano catanduva", NAV, "/contato/", "Alta", "Página de contato com endereço, telefone, mapa e horário"),
 ("casa do chá serrano whatsapp", NAV, "/contato/", "Baixa", "Telefone/WhatsApp com link tel:"),
 ("loja de chá em catanduva", NAV, "/contato/", "Alta", "Termo local; apoia o perfil no Google Meu Negócio"),
 ("melhor chá verde em folhas", INV, SEN, "Média", "Avaliações e descrição do tipo de folha"),
 ("chá preto assam com leite", INV, ASS, "Baixa", "Descrição cita notas maltadas e combinação com leite"),
 ("chá em folhas ou saquinho", INV, "/chas/", "Baixa", "Texto de apoio na categoria"),
 ("melhor presente de chá", INV, "/acessorios/", "Média", "Categoria de kits para presente"),
 ("sabor do chá de capim-limão", INV, CAP, "Baixa", "Descrição do sabor cítrico e suave"),
 ("chá de camomila orgânica flores inteiras", INV, CAM, "Média", "Diferencial: flores inteiras e orgânicas"),
 ("comprar chá online", TRA, "/chas/", "Alta", "Categoria como página de entrada para compra"),
 ("comprar chá verde sencha", TRA, SEN, "Alta", "Product schema com preço e disponibilidade"),
 ("comprar chá preto assam", TRA, ASS, "Alta", "Product schema com preço e disponibilidade"),
 ("comprar chá de hibisco com laranja", TRA, HIB, "Alta", "Product schema com preço e disponibilidade"),
 ("comprar chá de camomila orgânica", TRA, CAM, "Alta", "Product schema com preço e disponibilidade"),
 ("comprar chá de capim-limão", TRA, CAP, "Alta", "Product schema com preço e disponibilidade"),
 ("kit de chá para presente", TRA, "/acessorios/", "Alta", "Categoria; termo mais genérico que o do produto"),
 ("comprar kit presente de chá verde", TRA, KIT, "Alta", "Página do produto; termo específico, evita canibalizar a categoria"),
]
SEM_KW = [("comprar chá verde sencha", "Exata", "[comprar chá verde sencha]"), ("comprar chá preto assam", "Exata", "[comprar chá preto assam]"),
          ("comprar chá online", "Frase", "\"comprar chá online\""), ("chá em folhas", "Frase", "\"chá em folhas\""),
          ("kit de chá para presente", "Frase", "\"kit de chá para presente\""), ("kit presente de chá verde", "Exata", "[kit presente de chá verde]"),
          ("chá de hibisco gelado", "Ampla", "chá de hibisco gelado"), ("loja de chá em catanduva", "Frase", "\"loja de chá em catanduva\""),
          ("casa do chá serrano", "Exata", "[casa do chá serrano]"), ("chá orgânico camomila", "Ampla", "chá orgânico camomila")]
NEGATIVAS = ["grátis", "receita", "o que é", "benefícios", "emagrecer", "saquinho", "pdf", "curso"]
ANUNCIOS = [
 dict(nome="Anúncio 1 – Kit presente", grupo="Kits presente", url="/acessorios/kit-presente-cha-verde/", caminho="kit-presente/cha-verde",
      titulos=["Kit Presente de Chá Verde", "Caixa de Presente Pronta", "Envio para todo o Brasil"],
      descricoes=["Chá verde sencha em caixa de presente. Embalagem artesanal da Casa do Chá Serrano.", "Presente prático e bonito. Veja o kit e peça pelo site."]),
 dict(nome="Anúncio 2 – Chá verde sencha", grupo="Chás em folhas", url="/chas/cha-verde-sencha/", caminho="cha/verde-sencha",
      titulos=["Chá Verde Sencha em Folhas", "Folhas Selecionadas 50 g", "Compre na Casa do Chá"],
      descricoes=["Sabor suave e vegetal, colhido na primavera. Pacote de 50 g por R$ 34,90.", "Loja de chás de Catanduva-SP com envio para todo o Brasil."]),
]
SEM_ARG = ("O orgânico fica com o que dura e custa menos para manter: termos de marca e de local (a loja deve ser o primeiro resultado), "
           "as dúvidas de preparo respondidas dentro das páginas de produto e as páginas de categoria. O pago vale onde há pressa ou disputa: "
           "lançamento de produto sem histórico, datas de presente (Dia das Mães, Natal, Dia dos Namorados) para o kit presente e as consultas de compra "
           "mais disputadas. A mídia paga dá resultado no mesmo dia e mede a demanda real; o SEO leva semanas, mas o tráfego não termina quando o orçamento acaba. "
           "A campanha é apenas simulada e não gasta dinheiro.")

LINKS = [
 ("Perfil no Google Meu Negócio e diretórios locais", "Cadastrar a loja no Google Meu Negócio e em diretórios de empresas de Catanduva e região, com os mesmos nome, endereço e telefone do site.", "Link comum (dofollow) para a home", "—"),
 ("Parceria com cafeterias e lojas de presentes da região", "Propor a lojas locais indicar o kit presente e a loja em suas páginas e redes, e fazer o mesmo por elas na página Quem somos.", "Link editorial, sem pagamento", "Se houver troca de produtos ou comissão: rel=\"sponsored\""),
 ("Conteúdo útil que merece link: guia de temperatura e tempo de infusão", "Publicar um guia ilustrado de preparo para chás e oferecê-lo a blogs de culinária e bem-estar.", "Link editorial (dofollow)", "—"),
 ("Amostras para resenhistas e microinfluenciadores", "Enviar produtos a quem faz resenhas de chá e pedir que declare o recebimento.", "Quando há produto grátis ou pagamento: rel=\"sponsored\"", "Perfis de rede social: normalmente nofollow"),
 ("Assessoria de imprensa local", "Divulgar a história da loja familiar de Catanduva (desde 2019) para portais e jornais regionais.", "Link editorial (dofollow)", "—"),
 ("Participação em comunidades e avaliações de clientes", "Responder dúvidas em fóruns e grupos sobre chá e incentivar clientes a avaliar os produtos, sem criar avaliações falsas.", "Links em comentários, fóruns e avaliações: rel=\"ugc\"", "Quando não se quer endossar o destino: rel=\"nofollow\""),
]
LINK_REGRAS = [("nofollow", "Link que o site não quer endossar ou que não controla (ex.: páginas pouco confiáveis)."),
               ("sponsored", "Links pagos, patrocinados, parcerias comerciais e links de afiliados."),
               ("ugc", "Links colocados por usuários: comentários, fóruns, avaliações e perfis.")]
PROIBIDO = "Compra de links, redes de blogs privados (PBN), troca excessiva de links, comentários em massa com link e avaliações falsas."

BLOQUEIOS = [  # (página/padrão, mecanismo, motivo)
 ("/carrinho/", "meta robots noindex,follow", "Página sem conteúdo próprio; muda para cada visitante."),
 ("/checkout/", "meta robots noindex,follow", "Etapa de compra simulada, sem valor de busca."),
 ("/busca/", "meta robots noindex,follow", "Busca interna; resultados não devem competir com as categorias."),
 ("/busca/?q=…", "robots.txt: Disallow: /*?q=", "Combinações infinitas de busca com parâmetro desperdiçam rastreamento."),
 ("/404.html", "meta robots noindex,follow", "Página de erro."),
]
IMPEDIMENTOS = [  # (o que poderia impedir, como foi evitado)
 ("robots.txt bloqueando o site, o CSS ou o JS", "robots.txt com Allow: / e sem bloqueio de /css/, /js/ e /imagens/; apenas /*?q= é bloqueado."),
 ("meta robots noindex esquecido em páginas importantes", "Noindex só em carrinho, checkout, busca e 404; auditoria local conferiu as 11 páginas indexáveis."),
 ("Páginas órfãs, sem nenhum link apontando para elas", "Todas as páginas recebem links do menu, de categorias ou de produtos relacionados; 0 órfãs (v0 tinha 3)."),
 ("Conteúdo duplicado (home.html = index.html; kit com texto igual ao do sencha)", "Redirecionamento 301 de home.html e index.html para / ; textos únicos por produto; canonical em todas as páginas."),
 ("URLs fora do sitemap, erro 404 ou redirecionamentos em cadeia", "sitemap.xml só com as 11 URLs canônicas, 301 diretos (um salto) e página 404 personalizada."),
]
GMN = [("Nome da empresa", "Casa do Chá Serrano"), ("Categoria principal", "Loja de chá"), ("Categorias secundárias", "Loja de presentes (a confirmar no cadastro)"),
       ("Endereço", "Rua Exemplo, 123, Centro, Catanduva - SP, 15800-000 (fictício; trocar pelo real)"), ("Área de atendimento", "Catanduva e região; envio para todo o Brasil"),
       ("Horário", "Seg a sex 9h–18h; sáb 9h–13h; dom fechado"), ("Telefone", "(17) 99999-0000"), ("Site", "URL pública da v1 (página inicial)"),
       ("Descrição", "Loja familiar de Catanduva-SP que importa e embala chás em folhas e infusões desde 2019. Chá verde, chá preto, hibisco, camomila, capim-limão e kits para presente, com envio para todo o Brasil."),
       ("Produtos", "6 produtos com foto, preço e link para a página do produto"), ("Fotos", "Fachada, balcão com latas de chá, produtos e embalagens"), ("Postagens", "Quinzenais: novidades, modos de preparo e kits para datas especiais")]
