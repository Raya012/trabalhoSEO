# Casa do Chá Serrano – Trabalho de SEO (Grupo 1)

Tecnologia em Sistemas para Internet · IMES Catanduva · Prof. Esp. Thales Emanuel Figueiredo

- **Integrantes:** Vinicyus Raya, Braian Elizeu e Mariana Miguel
- **Site v1 (otimizado):** https://casadochaserrano-grupo1.netlify.app  ·  **Site v0 (inicial):** https://casadochaserrano-v0.netlify.app


## Estrutura
| Pasta | Conteúdo |
|---|---|
| `v0/` | Kit inicial, intacto (sem SEO) |
| `v1/` | Site otimizado, pronto para publicar (aponte o servidor para esta pasta) |
| `tools/` | `sitedata.py` (dados), `build.py` (gerador estático), `audit.py` (auditoria v0 x v1), scripts da planilha, do relatório e dos slides |
| `docs/` | Relatório (PDF), planilha de apoio (xlsx) e slides (pptx) |

## Publicar
1. Defina o endereço final e gere a v1: `BASE_URL=https://seu-site.netlify.app python3 tools/build.py`
   (requer Python 3 e Pillow). Isso reescreve canonical, Open Graph, JSON-LD, sitemap.xml e robots.txt.
2. Publique a pasta `v1/` no **Netlify** ou **Cloudflare Pages**. O arquivo `v1/_redirects` faz os 301 da v0 para a v1.
   O GitHub Pages não faz 301; funciona o site, mas os redirecionamentos não.
3. Publique a v0 em outro endereço para o comparativo.
4. Rode Lighthouse e o Teste de Resultados Enriquecidos nas duas URLs, envie o `sitemap.xml` ao Search Console e insira os prints no relatório.

## Dados fictícios a trocar antes de ir ao ar
Endereço, CEP, horário e coordenadas (`tools/sitedata.py`, campo `NAP` e `HOURS`) e as 12 avaliações de demonstração dos produtos.

## Declaração de uso de IA
Claude (Anthropic) foi usado para gerar o código do site, os textos, os scripts, a planilha, o relatório e os slides. Detalhes no relatório.
