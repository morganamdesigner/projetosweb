# Garatuja | Colégio Unicultura: página Elementor

Página completa gerada a partir do Figma
[Colégio Unicultura / frame "Garatuja" (145:5)](https://www.figma.com/design/lJJPm2MeiSx9EiGFABkx29/Col%C3%A9gio-Unicultura?node-id=145-5),
com 1920 × 7027 px no desktop.

| Arquivo | Conteúdo |
|---|---|
| `garatuja-elementor.json` | Template pronto para importar no Elementor: 60 containers e 72 widgets. |
| `src/gt-page.css` | CSS complementar. O JSON já traz esse CSS embutido. |
| `src/gt-page.js` | JS de 15 linhas que marca a página como "rolada" (menu fixo). O JSON também já traz esse JS embutido. |
| `secao-bilingue-elementor.json` | Seção extra "Escola bilíngue", que não está no Figma. É um template de container separado, com o próprio CSS embutido (seção 11). |
| `secao-galeria-polaroids-elementor.json` | Seção extra "Galeria de polaroids": carrossel com 10 fotos, fora do Figma (seção 12). |
| `src/build_elementor_json.py` | Script que gera o JSON. Rode `python3 src/build_elementor_json.py` para regenerar. |

---

## 1. Como importar

1. No WordPress, vá em **Templates → Saved Templates → Import Templates** e envie `garatuja-elementor.json`.
2. Crie uma página (ou abra uma existente), clique em **Edit with Elementor**, abra a pasta **Templates**, vá na aba **My Templates** e clique em **Insert** em "Garatuja - Colégio Unicultura".
3. Em **Page Settings**, defina **Page Layout: Elementor Canvas**. A página tem navbar e rodapé próprios, então o cabeçalho e o rodapé do tema não devem aparecer. Ative também **Hide Title**.
4. Troque as imagens-placeholder pelos assets reais (seção 3).
5. Preencha os links dos botões, do menu e das redes sociais (seção 6).

Requisitos:

- **Elementor 3.16 ou superior**, com Flexbox Container e Grid Container ativos. O formato das chaves foi conferido no código-fonte do Elementor 4.4.
- **Elementor Pro** é necessário **apenas para o formulário** do CTA (widget *Form*). Sem o Pro, o widget não aparece. Nesse caso, substitua-o por um shortcode do seu plugin de formulários e aplique a classe `gt-form` ao widget.

---

## 2. Estrutura criada

```
Página (Elementor Canvas)
├─ [gt-top]  Container boxed 1480 · fundo #EEEFF4
│  ├─ <header> HERO [gt-hero]  1480×768 · imagem de fundo + overlay gradiente · raio 40
│  │  ├─ Recorte sup. esq. [gt-notch--tl] → 2 × Image (logos)
│  │  ├─ [gt-navbar-wrap] (reserva o espaço do menu)
│  │  │  └─ <nav> Navbar de vidro [gt-navbar] → [gt-navbar-logos] 2 × Image · Icon List (menu) · Social Icons · Button "Matricule-se"
│  │  ├─ Conteúdo (570px) → Heading <p> (selo) · Heading H1 · Text Editor · Button
│  │  └─ Recorte inf. dir. [gt-notch--br] (decorativo, oculto no mobile)
│  └─ <section> "Duas etapas" (boxed 1048, 2 colunas) → Heading H2 · Text Editor · Button
├─ [gt-etapas] Container boxed 1488 · fundo #F2CA50
│  ├─ <section> Card "Educação Infantil" (#020659, raio 40) → Image · Coluna (eyebrow, H2, texto, Grid 2×5)
│  ├─ <section> Card "1º e 2º anos" (#1B1F76, borda sup. amarela, sobreposto -121px) → Coluna (… Grid 2×6) · Image
│  └─ Button "Agendar visita"
├─ [gt-galeria] Linha full width → 4 × Image (25% × 652px)
├─ <section> [gt-experiencias] fundo #010658 → H2 · Grid 3×2 (6 containers → Icon Box H3) · Button
├─ <section> [gt-depois] fundo branco + shape divider "curve" azul → Image (leão) · H2 · Text Editor
├─ <section> [gt-cta] fundo #F2CA50 → Card 960 (Foto + depoimento de vidro | H2 · texto · Form)
├─ <footer> [gt-footer] fundo #010658 → 3 colunas (logo/redes/links · Contato · Navegação) + barra ©
└─ [gt-css] HTML widget com o <style> da página (sem altura visível)
```

Decisões de estrutura:

- **100% containers flex/grid nativos.** Não há Sections ou Columns legadas.
- **Grid Container** nativo nos checklists (2 colunas) e nos cards de experiências (3 colunas). Com linhas em `1fr`, todos os cards de uma grade ficam com a mesma altura.
- **Hierarquia de títulos:** um único **H1** no hero. Cada seção tem um **H2**, os cards de experiências usam **H3**, e os títulos do rodapé ("Contato", "Navegação") também são H2. Selos e eyebrows ("EDUCAÇÃO INFANTIL", etc.) usam Heading com tag `<p>`, porque não são títulos.
- O título do CTA aparece no Figma como "Heading 3", mas foi feito como **H2** porque abre uma seção nova. Os títulos do rodapé aparecem como "Heading 5" e viraram **H2** para não pular níveis.
- **Landmarks semânticos** via *HTML Tag* do container: `header`, `nav`, `section` e `footer`.
- **Sobreposições do Figma** feitas com margem negativa, sem `position:absolute`:
  - o card do Fundamental sobe 121 px sobre o card do Infantil;
  - a curva azul abaixo das experiências é um **Shape Divider "Curve"** nativo no topo da seção branca.

---

## 3. Assets que precisam ser substituídos

O proxy de rede deste ambiente bloqueou o download dos arquivos do Figma, então **nenhuma imagem pôde ser incorporada**. Cada widget ou fundo de imagem aponta para uma URL-placeholder (`https://example.com/substituir-asset-figma/<nome>`). Durante a importação, o Elementor tenta baixar essa URL, não consegue e usa o placeholder cinza padrão dele. A estrutura, as dimensões e o `object-fit` já estão configurados.

No Figma, selecione o nó indicado, use **Export** no formato sugerido, envie para a Biblioteca de Mídia e troque a imagem no widget. Preencha o **texto alternativo** na Biblioteca de Mídia; a sugestão está na última coluna.

| # | Onde | Nó Figma | Export | Tamanho no layout | Alt sugerido |
|---|---|---|---|---|---|
| 1 | Hero → fundo do container `gt-hero` | `145:98` "Firefly (6) 1" | JPG 2x | 1480×768, cover (zoom 123%) | *(fundo decorativo)* |
| 2 | Hero → logo Colégio Unicultura | `145:144` "Traced Image" | **SVG** | 123×64 | Colégio Unicultura |
| 3 | Hero → logo Garatuja | `145:146` "WhatsApp Image…" | PNG 2x | 99×49 | Garatuja - Educação Infantil e Fundamental I |
| 4 | Card Educação Infantil → foto | `145:335` "IMG_1142 1" | JPG 2x | 541×812, raio 20 | Menino brincando com massinha… |
| 5 | Card 1º e 2º anos → foto | `145:560` "IMG_1142 1" | JPG 2x | 541×812, raio 20 | Crianças do 1º e 2º anos… |
| 6 | Galeria → foto 1 | `145:570` | JPG | 480×652 | Corredor da Garatuja com árvore decorativa |
| 7 | Galeria → foto 2 | `145:575` | JPG | 480×652 | Crianças em atividade de movimento |
| 8 | Galeria → foto 3 | `145:580` | JPG | 480×652 | Duas alunas sorrindo durante atividade |
| 9 | Galeria → foto 4 | `145:585` | JPG | 480×652 | Espaço de brincar temático com bombeiros |
| 10 | "E depois da Garatuja?" → leão | `145:591` "Vector" | **SVG** | 462×617 | Leão, símbolo do Colégio Unicultura |
| 11 | CTA → fundo do painel da foto | `145:608` "Container" (imagem) | JPG 2x | 516×463, cover, pos. 50% 35% | *(fundo)* |
| 12 | Rodapé → logo Garatuja (branco) | `145:649` "Gemini_Generated_Image…" | PNG 2x | 222×112 | Garatuja |

**Ícones:** o Figma usa SVGs próprios. Foram colocados ícones Font Awesome equivalentes, que são nativos do Elementor. Para fidelidade total, exporte os SVGs e use **Icon → Upload SVG** em cada widget:

| Onde | Nó Figma | Ícone usado agora |
|---|---|---|
| Educação Criativa | `145:10` | `fa-brain` |
| Sistema Bilíngue | `145:19` | `fa-language` |
| Robótica Educacional | `145:28` | `fa-robot` |
| Educação Abrangente | `145:37` | `fa-heart` (regular) |
| Projetos Pedagógicos | `145:47` | `fa-cubes` |
| Escola de Esportes | `145:56` | `fa-volleyball-ball` |
| Marcador dos checklists | `145:158` | `fa-dot-circle` (regular), amarelo |

O quadrado de 64 px dos ícones de experiências tem, no Figma, um fundo em gradiente amarelo que faz parte do próprio SVG (`imgSvg`). Na versão atual ele é amarelo sólido `#F2CA50` (Icon Box "Stacked"). Se você exportar o frame inteiro de 64×64 como SVG, use a vista **Default** do Icon Box com tamanho 64.

---

## 4. Fontes

Todas são **Google Fonts** e ficam disponíveis direto no Elementor, sem configuração extra. Nenhuma substituição foi necessária.

| Fonte | Uso | Pesos |
|---|---|---|
| **Hanken Grotesk** | Títulos, textos, botões em gradiente | 300 (normal e *itálico*), 400, 500, 600, 700 |
| **DM Sans** | Menu, selo do hero, botões navy/brancos, depoimento, formulário, rodapé | 400, 600, 700 |
| **Inter** | Eyebrows e itens dos checklists | 400, 700 |

Tamanhos principais no desktop, com tablet e mobile entre parênteses:

- H1 55/51.7 (48 · 36)
- H2 das seções 60–62 (48–52 · 36–38)
- H2 das experiências 40 (· 32)

Os valores de letter-spacing negativos do Figma foram mantidos em px, por exemplo −2.75 no H1 e −3.1 no "Duas etapas".

---

## 5. Cores (extraídas do Figma)

| Token | Hex | Uso |
|---|---|---|
| Navy | `#010658` | Textos, seção de experiências, CTA, rodapé |
| Navy 2 | `#020659` | Hero (base), card Infantil, botões navy |
| Navy 3 | `#1B1F76` | Card 1º e 2º anos |
| Navy título | `#010558` | "Duas etapas, uma" |
| Amarelo | `#F2CA50` | Destaques, fundos das seções amarelas, ícones sociais |
| Gradiente botão | `#FFE900 → #FBBC04` | Botões "Agendar uma visita" (sombra `rgba(253,211,3,.3)`) |
| Overlay hero | `#060720 → rgba(1,6,88,0)` a 52% | Gradiente sobre a foto do hero |
| Fundo do topo | `#EEEFF4` | **Amostrado do render.** O nó do Figma declara branco, mas o render mostra uma textura cinza-clara. Ajuste se tiver o valor oficial. |

---

## 6. Links e interações

Nenhuma URL foi inventada. Todos os pontos clicáveis ficam com o campo **Link** vazio e prontos para receber o endereço:

- **Menu da navbar** (Icon List): Home, Unicultura, Garatuja, Diferenciais, Parceiros, Contato
- **Botão "Matricule-se"**
- **Botões de agendamento:**
  - "Agendar uma visita" (hero e experiências)
  - "Agendar visita" ("Duas etapas" e seção das etapas)
- **Redes sociais** (Social Icons, no topo e no rodapé): Facebook, Instagram, LinkedIn
- **Rodapé:** Política de privacidade, Termos de uso e os links de "Navegação"
- **Contatos do rodapé:** os telefones usam `tel:+551112345678` e o e-mail usa `mailto:`, montados a partir dos textos do próprio Figma. Atualize-os quando os dados reais forem definidos.

**Formulário do CTA:** tem os campos *Nome* e *Telefone/WhatsApp*, ambos obrigatórios. Configure a ação de envio em **Form → Actions After Submit**.

---

## 7. CSS personalizado

O CSS vai embutido em um widget **HTML** no fim da página (container `gt-css`, sem altura), então a importação funciona mesmo no Elementor gratuito. Se preferir, mova o conteúdo de `src/gt-page.css` para **Aparência → Personalizar → CSS adicional**, ou para o Custom CSS do Pro, e apague o container `gt-css`.

Todas as regras usam classes com prefixo `gt-`, aplicadas apenas nesta página. Não há estilos globais nem `!important`.

O CSS foi usado só onde o Elementor não tem controle nativo:

| Classe | Por quê |
|---|---|
| `gt-notch`, `gt-notch--tl`, `gt-notch--br` | Reproduzem a máscara "Subtract" do hero: recortes com cantos côncavos em que os logos ficam "encaixados". Não existe controle nativo para cantos côncavos. |
| `gt-navbar`, `gt-glass` | `backdrop-filter: blur()` da navbar (51.5px) e do cartão de depoimento (9px). |
| `gt-highlight` | Faixa amarela arredondada atrás de "transição cuidada", que acompanha a quebra de linha (`box-decoration-break`). |
| `gt-btn-arrow`, `gt-btn-arrow--light` | Círculo amarelo ou branco atrás da seta ↗ dos botões. A seta é o ícone nativo `arrow-right` girado −45°. |
| `gt-form` | Cor do placeholder e padding/altura dos campos (inexistentes nos controles do Form). |
| `gt-root` | Zera a margem do último `<p>` dos Text Editors, porque alguns temas adicionam margem. Também suaviza as animações de entrada. |
| `gt-btn-shine`, `gt-card-hover`, `gt-zoom`, `gt-lion` | Efeitos de hover e loop (seção 9). |

---

## 8. Responsividade

O Figma só tem a versão desktop. O comportamento em tablet (≤1024 px) e mobile (≤767 px) foi definido para seguir a lógica do layout:

| Seção | Tablet | Mobile |
|---|---|---|
| Hero | A navbar desce para baixo do recorte dos logos e ocupa 100% da largura. A foto passa a `cover`. | A navbar vira coluna, com links quebrando linha e centralizados. H1 com 36 px. O recorte inferior direito some e o raio cai para 24. O overlay escurece mais a foto para manter o contraste. |
| Duas etapas | Colunas empilhadas. | Título com 38 px. |
| Cards das etapas | Foto em cima, com 100% × 560. O texto fica embaixo. Checklist em 2 colunas. | Foto com 380 px. Checklist em 1 coluna. Padding e raio menores. |
| Galeria | 2 × 2 com 480 px de altura. | 2 × 2 com 240 px de altura. |
| Experiências | 2 colunas. | 1 coluna, com os cards em altura automática. |
| E depois da Garatuja? | Leão em cima (320 px), texto centralizado. | Leão com 200 px e título com 36 px. A curva do divider cai para 28 px. |
| CTA | Foto e formulário a 50% / 50%. | Empilhado, com a foto em 420 px de altura. |
| Rodapé | 3 colunas de 30%. | 1 coluna. |

---

## 9. Animações e efeitos de scroll

Os efeitos combinam recursos nativos do Elementor e do Elementor Pro com CSS em `gt-page.css`. São 53 elementos com animação de entrada, todas na duração **Fast** (0,75 s). No CSS, o deslocamento dessas entradas foi reduzido para 32 px. A animação nativa desloca 100% da altura do elemento, o que numa foto de 812 px ficaria exagerado.

| Onde | Efeito | Como foi feito |
|---|---|---|
| Hero | Selo, H1, texto e botão entram em cascata (0 / 120 / 240 / 360 ms). | Entrance Animation *Fade In Up* (nativa) |
| Hero | A foto de fundo faz um zoom lento de 135% para 123% ao carregar (só desktop). | CSS (`.gt-hero`) |
| Navbar | Depois de 40 px de scroll, fica **fixa no topo** (16 px de distância), vai para o **centro da tela** e **se expande** de 803 px para até 1240 px. O vidro escurece, ganha sombra e os **dois logos aparecem à esquerda**. Os links ficam no centro e as redes sociais e o botão à direita. Desktop e tablet. | CSS (`.gt-scrolled`, `.gt-navbar-logos`) + `gt-page.js` |
| "Duas etapas" | O título aparece e a faixa amarela se desenha da esquerda para a direita. A coluna da direita sobe logo depois. | *Fade In* + CSS (`.gt-highlight`) · *Fade In Up* |
| Cards das etapas | Eyebrow, H2 e texto em cascata. Os itens do checklist entram em ziguezague (40–80 ms entre eles). | *Fade In Up* |
| Cards das etapas | As fotos fazem parallax leve ao rolar (velocidade 1, só desktop). | **Pro**: *Motion Effects → Vertical Scroll* |
| Galeria | As fotos aparecem em sequência. No hover, dão um zoom de 6%. | *Fade In* + CSS (`.gt-zoom`) |
| Experiências | Os cards entram em cascata por coluna. No hover, o card sobe 6 px, ganha sombra e o ícone gira levemente. | *Fade In Up* + CSS (`.gt-card-hover`) |
| E depois da Garatuja? | O leão entra com zoom suave e depois "respira" em loop lento (6 s). | *Zoom In* + CSS (`.gt-lion`) |
| CTA | O card sobe. O depoimento de vidro desliza da esquerda (450 ms). | *Fade In Up* · *Fade In Left* |
| Botões amarelos | No hover, sobem 2 px e um brilho atravessa o botão. | CSS (`.gt-btn-shine`) |
| Botões com seta | No hover, o círculo cresce e a seta ↗ anda na diagonal. | CSS (`.gt-btn-arrow`) |

**Acessibilidade:** quando o sistema do usuário pede "reduzir movimento", o Elementor já desliga as animações de entrada. O CSS desliga o restante: zoom do hero, faixa, leão, brilho e hovers com deslocamento.

**Para ajustar no editor:**
- **Entradas:** *Advanced → Motion Effects → Entrance Animation* do widget ou container.
- **Navbar fixa:** controlada pelo CSS e pelo JS da página, não pelo *Sticky* do Pro. **Não ative o Sticky** nesse container, porque os dois brigariam pela posição do menu.
- **Parallax:** widget de imagem → *Advanced → Motion Effects → Scrolling Effects*.

**Logos do menu fixo:** ficam no container `gt-navbar-logos`, o primeiro item da navbar, com as imagens `logo-colegio-unicultura-menu.svg` (77 px) e `logo-garatuja-menu.png` (81 px). Como o menu fixo tem fundo azul-escuro, use as **versões brancas (negativas)** dos logos. No topo da página esse espaço fica oculto. No editor ele aparece com contorno tracejado, para você poder trocar as imagens.

**Por que o menu fixo não usa o Sticky do Pro:** o Sticky grava posição e largura direto no elemento. Isso impedia centralizar e alargar o menu de forma confiável. Agora o `gt-page.js` só adiciona a classe `gt-scrolled` ao topo da página depois de 40 px de scroll, e o CSS faz o resto. O container `gt-navbar-wrap` guarda a altura do menu no hero, então o conteúdo não "pula" quando o menu fica fixo. No celular o menu continua sem ficar fixo.

**Não incluída:** a faixa rolante "MATRÍCULAS ABERTAS 2026 ✦ VAGAS LIMITADAS" (camadas `DiagonalTape`) está **oculta** no Figma, então não foi adicionada. Se o designer confirmar, ela pode ser criada com CSS.

---

## 10. Decisões e diferenças conhecidas

- **Formulário:** usa o widget *Form* do Elementor Pro, porque o Elementor gratuito não tem formulário. As chaves desse widget não puderam ser conferidas no código-fonte, que é fechado.
- **Emojis dos contatos no rodapé** (📞 ✉️ 📍) foram trocados por ícones Font Awesome no Icon List. Emojis mudam de aparência entre sistemas e não aceitam cor. Se quiser os emojis de volta, remova os ícones e cole o emoji no início do texto de cada item.
- **Letras das redes sociais** ("f", "◎", "in", em texto no Figma) viraram os ícones de marca equivalentes (Facebook, Instagram, LinkedIn) do widget Social Icons.
- **Textura de ruído** dos cards azuis e do fundo do topo foi ignorada; foram usadas cores sólidas. Se quiser a textura, aplique a imagem exportada do Figma como fundo do container.
- **Asterisco decorativo** do CTA (`145:606`) fica totalmente coberto pela foto no Figma, então não foi recriado.
- **Elementos ocultos no Figma** não foram recriados, porque não aparecem no design. Isso inclui:
  - faixas "MATRÍCULAS ABERTAS";
  - asteriscos do hero;
  - o 2º botão "Conhecer proposta";
  - legendas da galeria.
- **Largura do texto dos checklists:** algumas quebras de linha podem diferir levemente do Figma, onde cada caixa de texto tinha uma largura manual (174–209 px). No Elementor, o texto ocupa a largura do card.

---

## 11. Seção extra: "Escola bilíngue"

Seção criada à parte, fora do Figma, para reforçar que a Garatuja é bilíngue e tem aulas de inglês desde a Educação Infantil. Ela é gerada por `src/build_secao_bilingue.py` e o CSS dela fica em `src/gt-bilingue.css`, embutido num widget HTML dentro da própria seção. Visual: card amarelo com raio de 40 px, no mesmo padrão da página.

| Bloco | O que faz |
|---|---|
| Texto | Selo "Escola bilíngue · Bilingual school", H2 "Aqui, a infância fala **dois idiomas**" (faixa azul que se desenha ao aparecer), parágrafo, 3 destaques e o botão "Agendar uma visita". |
| Foto | Foto de aula de inglês (placeholder `bilingue-aula-de-ingles.jpg`, 520 px de altura, raio 32) com dois balões de fala flutuando: **"Hello!"** (branco) e **"Olá!"** (azul). |
| Cards que viram | Quatro cards com a palavra em português na frente. Ao passar o mouse ou tocar, o card gira e mostra a palavra em inglês: Brincar → Play, Cores → Colors, Amigos → Friends, Histórias → Stories. Ficam em 4 colunas no desktop e 2 × 2 no celular. |
| Bandeira ao rolar | Conforme o card sobe na tela, uma imagem da bandeira EUA/Reino Unido aparece suavemente sobre o amarelo, de 0% até **28%** de opacidade. É o *Background Overlay* nativo do card, com a opacidade controlada por `src/gt-bilingue.js`. |
| Faixa rolante | Faixa azul inclinada (−2°) com pares de palavras (HELLO · OLÁ ✦ PLAY · BRINCAR ✦ …). Pausa no hover e fica oculta para leitores de tela (atributo `aria-hidden`, do Pro). |

**Como inserir logo abaixo do hero:**
1. Importe `secao-bilingue-elementor.json` em *Templates → Import*.
2. Na página, insira o template "Garatuja - Seção Escola bilíngue".
3. No *Navigator*, arraste-o para **dentro do container `gt-top`**, entre o hero e a seção "Duas etapas".

A seção também funciona se ficar solta entre dois containers da página.

**Textos:** foram escritos a partir do que a escola informou (bilíngue, com aulas de inglês desde a Educação Infantil) e do que já está na página. Não há números nem cargas horárias inventados. Revise e ajuste à vontade.

**Bandeira:** no editor, selecione o container do card (`gt-bi-card`) → *Estilo → Background Overlay* e troque a imagem (placeholder `bandeira-eua-reino-unido.webp`). A **opacidade** definida ali é o **máximo** que a bandeira atinge; o script vai de 0 até esse valor durante o scroll. Para uma versão monocromática dourada, mude *Blend Mode* para **Luminosity** (0.35 funciona bem). No editor a bandeira aparece sempre na opacidade máxima, porque o script não roda dentro dele. Para quem ativou "reduzir movimento" no sistema, ela aparece direto no máximo.

**Imagem a substituir:** `bilingue-aula-de-ingles.jpg`, com o alt sugerido "Crianças da Garatuja em aula de inglês". Não existe no Figma, então é preciso uma foto nova.

---

## 12. Seção extra: "Galeria de polaroids"

Carrossel de fotos das crianças em estilo polaroid. Foi feito com o widget nativo **Image Carousel** (gratuito) e o CSS de `src/gt-galeria.css`, embutido num widget HTML da própria seção. O gerador é `src/build_secao_galeria.py`.

| Parte | Detalhe |
|---|---|
| Cabeçalho | "NOSSO DIA A DIA" · H2 "Momentos que viram **memória**" · texto curto. |
| Polaroids | Moldura branca, fita adesiva amarela no topo, inclinações alternadas (−3°, 2°, −1,5°, 3°) e fotos cortadas em 4:5. No hover, a foto endireita e cresce. |
| Carrossel | 4 fotos visíveis no desktop, 3 no tablet e 1 no celular. Passa sozinho a cada 3,5 s, pausa no hover e no toque, e é infinito. Tem setas amarelas e pontos. |
| Lightbox | Clicando, a foto abre em tela cheia, com navegação entre todas. |
| Legendas | Ficam abaixo de cada foto em fonte manuscrita (**Caveat**, Google Fonts). O texto vem do campo **Legenda** de cada imagem na Biblioteca de Mídia. |

**Onde colocar:** entre "Experiências que enriquecem a aprendizagem" e "E depois da Garatuja?". O fundo é o mesmo azul das Experiências (#010658), então a curva azul do topo de "E depois" continua encaixando.

**Trocar as fotos:**
1. Selecione o carrossel e, em *Content → Images*, clique na galeria.
2. Remova o placeholder e adicione as 10 fotos.
3. Na mesma janela, preencha em cada foto a **Legenda** (aparece na polaroid) e o **Texto alternativo**, para acessibilidade.
4. Depois apague da Biblioteca de Mídia o placeholder amarelo (`010658.png`), que a importação baixou.

A importação baixa **uma** imagem-placeholder real (placehold.co) e a repete nos 10 slides, para o carrossel já aparecer montado. Se o seu servidor não conseguir baixá-la, o carrossel vem vazio; é só adicionar as fotos como acima.

**Fotos:**
- **Autorização:** como são crianças, garanta a autorização por escrito dos responsáveis para uso de imagem (LGPD e ECA).
- **Formato:** use 4:5, com uns 1200 px no lado maior, em WebP.

