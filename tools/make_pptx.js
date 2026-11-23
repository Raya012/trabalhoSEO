const pptxgen = require("pptxgenjs");
const m = require("./metrics.json"); const v0 = m.v0, v1 = m.v1;
const kb = b => Math.round(b / 1024);
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SEO – Casa do Chá Serrano (Grupo 1)";
const G = "2E6B3F", D = "1F3D2A", S = "E8F0E2", BG = "FBF8F1", R = "B85042", T = "26303A";
const F = "Calibri", FH = "Georgia";
function base(title, notes) {
  const s = pres.addSlide(); s.background = { color: BG };
  s.addText(title, { x: 0.6, y: 0.35, w: 12.1, h: 0.8, fontFace: FH, fontSize: 30, bold: true, color: D, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.ellipse, { x: 0.6, y: 1.15, w: 0.14, h: 0.14, fill: { color: G }, line: { color: G } });
  s.addText("Casa do Chá Serrano · SEO · Grupo 1", { x: 0.6, y: 7.05, w: 6, h: 0.3, fontFace: F, fontSize: 10, color: "6B7780", margin: 0, isTextBox: true });
  if (notes) s.addNotes(notes); return s;
}
function card(s, x, y, w, h, head, body, hc) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: "D5DDD8", width: 1 }, rectRadius: 0.12 });
  s.addText(head, { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: 0.45, fontFace: FH, fontSize: 16, bold: true, color: hc || G, margin: 0, isTextBox: true });
  s.addText(body, { x: x + 0.2, y: y + 0.6, w: w - 0.4, h: h - 0.7, fontFace: F, fontSize: 18, color: T, valign: "top", paraSpaceAfter: 6, margin: 0, isTextBox: true });
}
function big(s, x, y, w, num, lab, col) {
  s.addText(num, { x, y, w, h: 0.9, fontFace: FH, fontSize: 40, bold: true, color: col || G, margin: 0, isTextBox: true });
  s.addText(lab, { x, y: y + 0.9, w, h: 0.6, fontFace: F, fontSize: 13, color: T, margin: 0, valign: "top", isTextBox: true });
}
// 1 capa
let s = pres.addSlide(); s.background = { color: D };
s.addText("Auditoria e otimização de SEO", { x: 0.8, y: 2.1, w: 11.5, h: 1.2, fontFace: FH, fontSize: 46, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
s.addText("Casa do Chá Serrano · loja virtual de nicho", { x: 0.8, y: 3.4, w: 11.5, h: 0.6, fontFace: F, fontSize: 24, color: "BFD9B8", margin: 0, isTextBox: true });
s.addText("Grupo 1 · Vinicyus Raya, Braian Elizeu e Mariana Miguel · Tecnologia em Sistemas para Internet · IMES Catanduva", { x: 0.8, y: 5.6, w: 11.5, h: 0.5, fontFace: F, fontSize: 16, color: "FFFFFF", margin: 0, isTextBox: true });
s.addNotes("Vinicyus (1 min): apresentar o grupo, o cenário (loja de chás de Catanduva) e o roteiro: diagnóstico, otimização, provas ao vivo.");
// 2 diagnóstico
s = base("Ponto de partida: a v0 não era encontrável", "Vinicyus (1 min). Mostrar que cada número vem do script tools/audit.py, rodado nas duas versões.");
big(s, 0.6, 1.7, 2.9, String(v0.w3c_erros), "erros no validador W3C");
big(s, 3.7, 1.7, 2.9, v0.title_unicos + " de 14", "páginas com title único (“Home”, “Produto”)", R);
big(s, 6.8, 1.7, 2.9, "0 de 14", "páginas com meta description", R);
big(s, 9.9, 1.7, 2.9, kb(v0.peso_imagens_pasta).toLocaleString("pt-BR") + " KB", "de imagens, sem nenhum alt", R);
card(s, 0.6, 3.9, 6.0, 2.8, "Estrutura", "3 páginas órfãs (uma delas é um produto à venda)\nhome.html = index.html (duplicada)\nURLs como Prod_1.html e produto_camomila.HTML\nNenhum h1; a categoria tinha dois");
card(s, 6.8, 3.9, 6.0, 2.8, "Conteúdo", "Links “clique aqui” em todo o site\nBloco de palavras repetidas (spam)\nKit presente com texto copiado do sencha\nSem dados estruturados, sem robots.txt, sem sitemap");
// 3 estratégia
s = base("Estratégia: quem compra e como medimos", "Vinicyus (1 min). Personas fictícias; metas são hipóteses até termos a linha de base do Search Console.");
card(s, 0.6, 1.6, 6.0, 2.4, "Marina, 34 – relaxar à noite", "Busca preparo e depois “comprar chá de camomila”. Precisa de peso, descrição clara e avaliações.");
card(s, 6.8, 1.6, 6.0, 2.4, "Roberto, 52 – procura presente", "Busca “kit de chá para presente”. Precisa de preço, foto da embalagem e envio.");
big(s, 0.6, 4.4, 3.9, "11 de 11", "páginas indexadas em 30 dias");
big(s, 4.7, 4.4, 3.9, "100/mês", "cliques orgânicos no 3º mês");
big(s, 8.8, 4.4, 4.0, "≤ 20", "posição média das 8 consultas de compra em 3 meses");
// 4 SEM
s = base("SEO x SEM: o que pagar e o que não", "Vinicyus (1 min). Campanha apenas simulada, sem gasto: 10 palavras-chave e 2 anúncios na planilha.");
card(s, 0.6, 1.6, 6.0, 4.0, "Orgânico", "Marca e local: “casa do chá serrano”, “loja de chá em Catanduva”\nDúvidas de preparo, dentro de cada produto\nPáginas de categoria\nDura e custa menos para manter", G);
card(s, 6.8, 1.6, 6.0, 4.0, "Pago (simulado)", "Kit presente em datas de presente\nLançamento de produto sem histórico\nConsultas de compra mais disputadas\nResultado no mesmo dia e mede a demanda", R);
s.addText("10 palavras-chave · exata, frase e ampla · 8 negativas · 2 anúncios (kit presente e chá verde sencha)", { x: 0.6, y: 5.95, w: 12.2, h: 0.5, fontFace: F, fontSize: 16, color: D, margin: 0, isTextBox: true });
// 5 indexação
s = base("Indexação e robots.txt: uma decisão que importa", "Braian (1,5 min). Explicar por que não bloqueamos carrinho e busca no robots.txt: o Google precisa abrir a página para ler o noindex.");
card(s, 0.6, 1.6, 4.0, 3.3, "1. Rastrear", "Links internos, robots.txt e sitemap.xml levam o Googlebot às 11 páginas.");
card(s, 4.7, 1.6, 4.0, 3.3, "2. Indexar", "HTML semântico, title, texto, alt e JSON-LD dizem o que cada página é.");
card(s, 8.8, 1.6, 4.0, 3.3, "3. Ranquear", "Intenção de busca, qualidade e relevância decidem a posição.");
s.addText([{ text: "noindex,follow", options: { bold: true, color: G } }, { text: " em carrinho, checkout, busca e 404 (rastreáveis, para o noindex ser lido).  ", options: {} }, { text: "Disallow: /*?q=", options: { bold: true, color: R } }, { text: " só nas buscas com parâmetro. CSS, JS e imagens liberados.", options: {} }],
  { x: 0.6, y: 5.3, w: 12.2, h: 1.2, fontFace: F, fontSize: 18, color: T, margin: 0, isTextBox: true, valign: "top" });
// 6 semântica e meta
s = base("HTML semântico e meta tags", "Braian (1,5 min). Demonstração ao vivo 1: validador W3C na home e em um produto.");
card(s, 0.6, 1.6, 6.0, 4.6, "Semântica", "header, nav, main, article, section, footer\nUm h1 por página, sem pular nível\nlang=\"pt-BR\", links descritivos\nMigalhas, link “pular para o conteúdo”\nW3C: " + v0.w3c_erros + " erros → " + v1.w3c_erros);
card(s, 6.8, 1.6, 6.0, 4.6, "Meta tags (14 páginas)", "Title único até 60 caracteres\nDescription única até 160\nCanonical, viewport, charset\nOpen Graph com imagem 1200×630 e twitter:card\nTitle único: " + v0.title_unicos + " → " + v1.title_unicos + " de 14");
// 7 imagens
s = base("Imagens: de 700 KB para ~30 KB por foto", "Mariana (1 min). WebP em 480, 800 e 1200 px com srcset; width e height; lazy fora da primeira dobra; alt descritivo.");
s.addChart(pres.charts.BAR, [{ name: "Peso da pasta de imagens (KB)", labels: ["v0 (JPG)", "v1 (WebP, 3 tamanhos)"], values: [kb(v0.peso_imagens_pasta), kb(v1.peso_imagens_pasta)] }],
  { x: 0.6, y: 1.5, w: 6.4, h: 5.1, barDir: "col", chartColors: [R, G], showValue: true, dataLabelFontSize: 14, dataLabelFontFace: "Arial", showLegend: false, catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, valGridLine: { color: "DDDDDD", size: 0.5 }, catGridLine: { style: "none" }, showTitle: true, title: "Peso da pasta de imagens (KB)", titleFontSize: 14 });
card(s, 7.3, 1.6, 5.5, 4.8, "O que mudou", "IMG_0412.jpg → cha-verde-sencha-800.webp\nsrcset e sizes em todas as fotos\nAlt único e descritivo (14 → 0 sem alt)\nA página de produto baixa ~30 KB");
// 8 arquitetura
s = base("Arquitetura e URLs", "Mariana (1 min). Demonstração ao vivo 2: Screaming Frog ou o script audit.py mostrando 0 órfãs e profundidade máxima 2.");
big(s, 0.6, 1.7, 3.0, "2", "cliques no máximo (v0: 3 órfãs)");
big(s, 3.8, 1.7, 3.0, "0", "páginas órfãs");
big(s, 7.0, 1.7, 3.0, "14", "redirecionamentos 301 v0 → v1");
card(s, 0.6, 3.6, 6.0, 3.0, "Hierarquia", "/ → /chas/ → /chas/cha-verde-sencha/\n/ → /acessorios/ → kit presente\nMenu, rodapé e “Veja também” em todas as páginas");
card(s, 6.8, 3.6, 6.0, 3.0, "URLs", "/Prod_1.html → /chas/cha-verde-sencha/\nMinúsculas, hífens, sem extensão\nCanonical igual à URL final\n301 em Netlify ou Cloudflare Pages");
// 9 keywords
s = base("Palavras-chave e SEO off-page", "Mariana (1 min). Volumes mensais ficam para o grupo preencher no Planejador de Palavras-chave; não foram inventados.");
big(s, 0.6, 1.7, 2.8, "24", "termos, cada um em uma única página");
big(s, 3.6, 1.7, 2.8, "4", "intenções: info, navegação, investigação, compra");
card(s, 6.6, 1.6, 6.2, 2.4, "Sem canibalização", "“kit de chá para presente” → categoria\n“comprar kit presente de chá verde” → produto");
card(s, 0.6, 4.2, 12.2, 2.5, "6 ações éticas de links", "Google Meu Negócio e diretórios locais · parcerias com cafeterias e lojas de presentes · guia de preparo linkável · amostras (rel=sponsored) · imprensa local · comunidades e avaliações (rel=ugc). Sem compra de links.");
// 10 dados estruturados e local
s = base("Dados estruturados e SEO local", "Mariana (1 min). Demonstração ao vivo 3: Teste de Resultados Enriquecidos em uma página de produto. Explicar que as avaliações são de demonstração e identificadas como tal.");
card(s, 0.6, 1.6, 6.0, 4.7, "JSON-LD", "Product: preço, moeda, disponibilidade, nota e avaliações\nBreadcrumbList nas páginas internas\nItemList nas categorias\nOrganization e WebSite na home\nErros na checagem local: " + v1.ld_erros);
card(s, 6.8, 1.6, 6.0, 4.7, "SEO local em /contato/", "Nome, endereço e telefone iguais em todo o site\nStore com endereço, geo e horário\nMapa, horário e telefone com link\nPerfil simulado no Google Meu Negócio\nDados de endereço fictícios no exercício");
// 11 antes/depois
s = base("Antes e depois, com os mesmos testes", "Mariana (1,5 min). Lighthouse em modo celular, nas duas URLs públicas, no mesmo dia.");
const hd = o => ({ text: o, options: { bold: true, color: "FFFFFF", fill: { color: D } } });
const rows = [[hd("Métrica"), hd("v0"), hd("v1")],
  ["Nota de SEO no Lighthouse", "73", "100"], ["Desempenho (início / produto)", "84 / 72", "100 / 100"], ["Acessibilidade", "76", "100"], ["Erros W3C", String(v0.w3c_erros), String(v1.w3c_erros)],
  ["Produtos com dados estruturados", "0 de 6", "6 de 6"], ["Title / description únicos", v0.title_unicos + " / 0 de 14", "14 / 14 de 14"],
  ["Peso da pasta de imagens", kb(v0.peso_imagens_pasta) + " KB", kb(v1.peso_imagens_pasta) + " KB"], ["Páginas a mais de 3 cliques", String(v0.mais_de_3.length), String(v1.mais_de_3.length)]];
s.addTable(rows, { x: 0.6, y: 1.6, w: 12.2, colW: [6.2, 3.0, 3.0], fontFace: F, fontSize: 16, color: T, border: { type: "solid", color: "D5DDD8", pt: 1 }, rowH: 0.5, valign: "middle" });
// 12 demo
s = base("Demonstração ao vivo: três verificações", "Vinicyus, Braian e Mariana (3 min), uma verificação para cada. Ensaiar antes; ter os links abertos em abas.");
card(s, 0.6, 1.6, 3.9, 4.5, "1. Validador W3C", "validator.w3.org na home e em um produto: sem erros. Mostrar a v0 com erros.");
card(s, 4.7, 1.6, 3.9, 4.5, "2. Dados estruturados", "Teste de Resultados Enriquecidos em /chas/cha-verde-sencha/: Product e Breadcrumb válidos.");
card(s, 8.8, 1.6, 4.0, 4.5, "3. Lighthouse", "Chrome > Lighthouse > SEO nas duas URLs. Comparar as notas e abrir o robots.txt e o sitemap.xml.");
// 13 conclusão
s = pres.addSlide(); s.background = { color: D };
s.addText("Conclusões", { x: 0.8, y: 0.8, w: 11, h: 0.8, fontFace: FH, fontSize: 38, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
s.addText([{ text: "Cada produto agora tem URL limpa, título, descrição e dados estruturados próprios", options: { bullet: true, breakLine: true } }, { text: "Nenhuma página órfã, duplicada ou sem controle de indexação", options: { bullet: true, breakLine: true } },
  { text: "Melhorias medidas com números, não só descritas", options: { bullet: true, breakLine: true } }, { text: "Próximos passos: Search Console, avaliações reais, dados reais de endereço e linha de base de cliques", options: { bullet: true } }],
  { x: 0.8, y: 2.0, w: 11.5, h: 3.6, fontFace: F, fontSize: 22, color: "FFFFFF", paraSpaceAfter: 14, valign: "top", margin: 0, isTextBox: true });
s.addText("Obrigado! Perguntas?", { x: 0.8, y: 6.2, w: 11, h: 0.6, fontFace: FH, fontSize: 26, color: "BFD9B8", margin: 0, isTextBox: true });
s.addNotes("Mariana (1 min) conclui; depois, perguntas individuais. Declarar o uso de IA (Claude) como no relatório.");
pres.writeFile({ fileName: "../docs/Apresentacao_SEO_Grupo1.pptx" }).then(() => console.log("pptx ok"));
