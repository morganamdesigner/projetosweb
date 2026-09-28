# Colégio Unicultura: página Sobre (Elementor)

`sobre-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema).
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.
Os textos e imagens são os do export atual da página.

## O que mudou

| Seção | Antes | Agora |
|---|---|---|
| Menu + hero | Menu antigo, script de slide, slideshow antigo configurado junto com a foto | Cabeçalho da Home e cartão azul com a foto `colegio-unicultura-bg-sobre.webp`. H1 "Conhecimento para ir **cada vez mais longe.**" com marca-texto vermelho suave (sem amarelo, como no hero novo da Home). Tem também o contador "+1.200 famílias" e os botões "Agendar visita" (→ /matriculas) e "Conhecer a proposta" (↓). |
| Faixa de palavras (nova) | — | Excelência acadêmica ✦ Acolhimento ✦ Autonomia ✦ Protagonismo ✦ Formação integral (os valores do texto da proposta), em movimento. |
| Uma trajetória construída com propósito | Texto, link e 2 fotos soltos | **Colagem**: foto grande com revelação de baixo para cima e parallax, foto menor sobreposta com borda branca (parallax no sentido oposto) e selo azul "3º ano do Fundamental → 3ª série do Médio". A frase "Não queremos apenas…" virou destaque com barra vermelha e marca-texto em "prepará-los". A chamada da **Garatuja** virou um cartão com o logo. |
| Galeria | Carrossel de imagens | Faixa de fotos verticais em movimento (as mesmas 6 fotos). |
| Nossa proposta pedagógica | Fundo preto com imagem de moldura; os 3 parágrafos dentro de um título | Fundo azul com grade. À esquerda, fixo ao rolar: etiqueta vermelha "Qualidade que faz a diferença", título, pílulas com os 5 valores e o botão. À direita, os 3 parágrafos viram **cartões numerados que acendem** ao chegar na tela. |
| O que buscamos formar | 10 listas separadas, todas com ícone de coração; destaque em degradê amarelo | Grade de **10 cartões, cada um com um ícone próprio**, em cascata. "formar" aparece numa pílula azul que "carimba". No hover o cartão sobe e o ícone fica vermelho. |
| Sistema de ensino | Imagem + texto soltos | Cartão do Poliedro com o logo flutuando (como nas outras páginas). |
| CTA final (novo) | — | "Quer conhecer o Unicultura **de perto?**", com "Agendar visita" e "Falar pelo WhatsApp". |

Animações removidas: o script de slide do hero e as classes antigas `scroll-bottom` nos textos da proposta.

## Conferir antes de publicar

- **Imagem de fundo da proposta** (`frame_1171276326.webp`): saiu, porque a seção agora usa o azul da identidade. Se quiser a imagem de volta, dá para colocar como foto num dos lados.
- **Textos novos** (curtos): "Nossa história", "Nosso método de ensino" (era o subtítulo em minúsculas da seção), o selo "3º ano do Fundamental → 3ª série do Médio", os títulos dos 3 cartões da proposta ("Cada etapa respeitada", "Uma trajetória contínua", "Base sólida e parceiros") e o CTA final.
- **WhatsApp** do CTA final: botão sem link (`https://wa.me/55DDDNUMERO`).

## Arquivos

- `src/build_sobre.py` gera o JSON (reaproveita hero, faixa, galeria, Poliedro e CTA das outras páginas).
- `src/un-sobre.css` tem os efeitos desta página. Ele vai embutido no widget HTML do topo.
