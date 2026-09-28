# Colégio Unicultura: página Diferenciais (Elementor)

`diferenciais-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema).
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.
A copy é a enviada pela cliente.

## Estrutura

| # | Seção | Design e efeitos |
|---|---|---|
| — | Menu + hero | Mesmo cabeçalho da Home. Cartão azul com brilho vermelho e grade de pontos, H1 "Aprendizagem que **ultrapassa a sala de aula**" e os botões "Agende uma visita" (→ /matriculas) e "Fale com a gente" (→ CTA final). À direita, uma **órbita com os 8 diferenciais**: ícones girando em 2 anéis em volta de "8 diferenciais". Cada ícone mostra o nome no hover e leva à seção. Embaixo, o índice "Navegue:" com links para as 8 seções. |
| 01 | Olimpíadas Científicas | "Desafiar também é uma forma de *ensinar*." (marca-texto ao aparecer), com pílulas das 6 habilidades. Cartão azul com uma **medalha balançando** (SVG) e a frase "Mais do que medalhas…". |
| 02 | Plantão de Monitoria | Foto (placeholder) com revelação de baixo para cima e selo flutuante "Anos Finais e Ensino Médio", texto e 3 checks. |
| 03 | Clube de Leitura | Texto + foto com parallax. À direita, as 5 palavras (Repertório, Interpretação, Argumentação, Imaginação, Pensamento crítico) começam **vazadas e se preenchem** ao passar pela tela. A última fica em vermelho. |
| 04 | Pensamento Computacional | Fundo azul com grade, um "terminal" que **digita** "criar, testar, resolver" com cursor piscando, e 3 cards (Tecnologia, Cultura Maker, Metodologia STEAM) que **inclinam em 3D** seguindo o mouse. |
| 05 | Socioemocional, Financeira e Empreendedora | 3 cards com ícone (Emoções · Relações · Escolhas / Planejamento · Recursos / Desafios · Projetos) e a faixa "Habilidades tão importantes *quanto o conteúdo acadêmico.*". |
| 06 | Sistema Bilíngue | Foto (placeholder) com os balões **"Hello!" e "Olá!" flutuando**, texto e 3 checks. |
| 07 | Projetos Pedagógicos | Fundo azul, 3 etapas (Investigação → Produção → Conhecimento aplicado) ligadas por uma **linha que se desenha** ao aparecer (vertical no celular), e o quadro "Diferentes áreas do saber, um mesmo desafio.". |
| 08 | Escola de Esportes | Foto grande (placeholder), texto, pílulas Físico/Emocional/Social e 4 cards de valores (Disciplina, Cooperação, Perseverança, Respeito). |
| — | CTA final | Cartão azul com anéis pulsando, "Agendar visita" (→ /matriculas) e "Falar pelo WhatsApp" (fica verde no hover). |

Em todas as seções: **número gigante vazado** (01 a 08) ao fundo com parallax, entradas suaves, títulos em "cortina" e barra de progresso de leitura. Em telas a partir de 1200px aparece um **índice lateral fixo** (um ponto por diferencial, o atual em vermelho, com o nome ao lado) que leva a cada seção.

## Para completar

- **Fotos**: 4 placeholders do Elementor (Monitoria, Leitura, Bilíngue, Esportes). O texto alternativo de cada um diz qual foto usar. Substitua no widget Imagem e troque também o texto alternativo.
- **Link do WhatsApp**: o botão "Falar pelo WhatsApp" está sem link. Use `https://wa.me/55DDDNUMERO`.
- **Textos de apoio que não estavam na copy**: rótulos das seções ("Leitura e repertório", "Tecnologia · Maker · STEAM"...), "Navegue:", "Para desenvolver", "Venha nos visitar", o terminal "criar, testar, resolver", as áreas do quadro de Projetos (Linguagens, Matemática, Ciências, Humanas, Artes) e os títulos dos cards, que saíram da própria copy. Ajuste à vontade.
- O índice lateral usa o atributo `data-chapter` das seções (Avançado > Atributos, recurso do Elementor Pro).

## Arquivos

- `src/build_diferenciais.py` gera o JSON (reaproveita o cabeçalho e os helpers das outras páginas).
- `src/un-dif.css` / `src/un-dif.js` têm os efeitos desta página. Eles vão embutidos no widget HTML do topo, junto com `un-home-v2.css/js` e `un-fund1.css/js`.
