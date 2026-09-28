# Colégio Unicultura: página Ensino Médio (Elementor)

`ensino-medio-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema).
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.

## Estrutura nova

| # | Seção | O que tem |
|---|---|---|
| 1 | Menu + hero | Mesmo cabeçalho e cartão azul da Home e do Fundamental, com uma foto só. O título "Excelência acadêmica. Preparação para o futuro." virou H1, com a 2ª frase em laranja. Também tem o contador "+1.200 famílias", "Ensino Médio" em destaque e o botão "Conhecer a proposta". |
| 2 | Faixa de palavras (nova) | ENEM ✦ Vestibulares ✦ Pensamento crítico ✦ Projeto de vida ✦ Autonomia intelectual ✦ Vida universitária, em movimento contínuo. |
| 3 | Uma trajetória que consolida | Título + texto lado a lado, e os 14 itens em cards com ícone (3 colunas, 2 no tablet, 1 no celular) que entram em cascata. "Preparação para ENEM e vestibulares" fica em destaque (azul, com brilho passando). "consolida:" aparece numa pílula que "carimba" ao entrar na tela. |
| 4 | Diferenciais que fazem parte dessa fase | Layout em blocos: à esquerda, cartão azul com título, texto e botão (brilho laranja em movimento lento e grade de pontos). À direita, 3 cards numerados com ícone: Plantão de Monitoria, Clube de Leitura, Simulados e análise de desempenho. Os cards entram em sequência e, no hover, deslizam, o ícone fica azul e gira, e uma barra vermelha aparece. A foto `foto-estudante-uni-bg.webp` saiu desta seção: é uma composição pronta e ficava estranha cortada atrás do texto. |
| 5 | Estrutura para os principais processos seletivos | Cartão do Poliedro com o logo flutuando. |
| 6 | Galeria | A faixa de fotos verticais em movimento da Home. |
| 7 | Manifesto: "Mais do que uma universidade, um caminho próprio" | Seção azul com um caminho laranja que se desenha conforme o scroll, com um ponto vermelho percorrendo a linha. "caminho próprio" ganha um sublinhado que cresce, e a frase "Não queremos apenas…" acende palavra por palavra. |
| 8 | Equipe | Só os 4 slides com conteúdo (6 estavam vazios), nomes em H3 e fonte Hanken Grotesk. |
| 9 | CTA com formulário | Mesmas animações das outras páginas. |

## Conferir antes de publicar

- **Foto do hero**: a página não tinha foto de fundo (só o slideshow antigo). Usei `foto2-home-2.webp`. Troque por uma foto do Ensino Médio em Estilo > Fundo do cartão azul.
- **"Ensino Médio · 1ª à 3ª série"** no selo do hero: acrescentei as séries. Confirme.
- **Botão "Ver todos os diferenciais"**: estava sem link na página atual.
- **Nomes da equipe**: "Camila" (foto `camila.webp`) e "Lucas" (foto `lucas.webp`), como no Fundamental. Confirme.
- **Textos novos** (curtos, de apoio): "Nossa proposta", "No dia a dia", "Nosso propósito", as frases de apoio dos 3 cards de diferenciais ("Revisão de conteúdos e esclarecimento de dúvidas.", "Leitura, conversa e repertório cultural.", "Preparação intensiva para o ENEM e os vestibulares."), a faixa de palavras e o botão "Conhecer a proposta". Os dois títulos "Mais do que uma universidade, um" + "caminho próprio" viraram um só H2 (antes eram dois títulos separados).

## Arquivos

- `src/build_medio.py` gera o JSON. Ele reaproveita as funções de `build_fund1.py` e `build_fund2.py`.
- `src/un-medio.css` / `src/un-medio.js` têm o card em destaque, os chips, o caminho desenhado com o scroll e a frase que acende. Eles vão embutidos no widget HTML do topo, junto com o CSS/JS da Home e dos Fundamentais.
