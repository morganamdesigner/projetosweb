# Colégio Unicultura: página Ensino Fundamental I (Elementor)

`fundamental1-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema).
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.
Outra opção é abrir a página no Elementor, apagar as seções antigas e importar pela pasta do ícone.

## O que mudou

| Seção | Antes | Agora |
|---|---|---|
| Menu + hero | Menu antigo, script de slide, título em H2 | Mesmo cabeçalho e cartão azul do hero v2 da Home, com **uma foto só** (`background-ensino-fundamental-1.webp`, sem slideshow). O título virou H1, "Desenvolver autonomia." aparece em laranja e o contador sobe até "+1.200 famílias". Os avatares vêm da página atual e "Fundamental I" fica destacado na faixa de segmentos. |
| Uma etapa de transição | Imagem vazia, frase de destaque em H2 | Foto com revelação de baixo para cima e parallax, selo flutuante "3º · 4º · 5º ano". A frase de destaque virou H3, com barra vermelha e efeito de marca-texto ao aparecer. |
| O que priorizamos | 3 listas de ícones | 12 cards em grade (3 colunas no desktop, 2 no tablet e no celular). O título fica fixo enquanto os cards passam (desktop), "nessa etapa:" aparece numa pílula que "carimba" ao entrar na tela e os cards sobem em cascata. No hover, o card sobe, o ícone gira de leve e uma linha vermelha cresce embaixo. |
| Galeria | Carrossel de imagens | A faixa de fotos verticais em movimento da Home, com as mesmas 6 fotos. Também desliza com o scroll e pausa no hover, com lightbox. |
| Sistema de ensino | Imagem + texto soltos | Cartão branco com o logo do Poliedro flutuando e um anel pulsando atrás. |
| Equipe | 10 slides, 6 vazios; nomes em H2 | Só os 4 slides com conteúdo, nomes em H3 e fonte Hanken Grotesk (antes Poppins). No hover, o card sobe e a foto dá zoom. |
| CTA com formulário | — | Entrada com zoom, brilho nos campos ao focar e botão que sobe no hover. |

Também há barra de progresso de leitura no topo e entradas suaves (32px) em todas as seções.
Quem ativa "reduzir movimento" no sistema vê tudo sem animação.

## Conferir antes de publicar

- **Nomes da equipe**: na página atual, o 2º card (foto `camila.webp`) repetia "Beatriz" e o 3º (foto `lucas.webp`) dizia "Nome do Professor". Deixei **Camila** e **Lucas** pelo nome das fotos. Confirme esses nomes.
- **Foto da seção "Uma etapa de transição"**: estava vazia. Usei `foto2-home.webp` da galeria; troque por uma foto do Fundamental I se tiver.
- **Textos novos** (curtos, só de apoio): "A etapa", "Prioridades", "Parceria pedagógica", "Doze frentes que caminham juntas, do 3º ao 5º ano.", o botão "Conhecer a etapa" (rola até a seção 2) e o selo "3º · 4º · 5º ano / Ensino Fundamental I". Os demais textos são os da página atual.
- **Foto do hero no celular**: fica no topo do cartão, com 230% de largura e ancorada a 88% na horizontal. Se o enquadramento não ficar bom, ajuste em Estilo > Fundo (modo celular) > Posição X.

## Arquivos

- `src/build_fund1.py` gera o JSON. Ele usa o cabeçalho de `colegio-unicultura-home/src/build_home_hero.py` e a galeria de `build_secao_galeria.py`, e lê o export atual da página.
- `src/un-fund1.css` / `src/un-fund1.js` têm os efeitos desta página. Eles vão embutidos no widget HTML do topo, junto com `un-home-v2.css/js` (cabeçalho flutuante, barra de progresso, contador).
- A galeria leva `un-galeria.css/js` da Home no próprio widget HTML.
