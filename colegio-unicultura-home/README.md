# Colégio Unicultura | Home: hero, menu e melhorias

Arquivo: `home-elementor.json`. É a **página inteira**, montada a partir do export `elementor-831-2026-09-25.json` enviado pelo cliente. O rodapé é um template à parte e não faz parte do arquivo.

Para regenerar, rode `python3 src/build_home.py [export-da-home.json]`.

## 1. Hero e menu (padrão Garatuja, identidade da Home)

O 1º bloco (`hero-slider`) foi substituído pela mesma estrutura do hero da Garatuja, partindo da última versão ajustada pelo cliente (menu do WordPress, hambúrguer no celular, foto no topo com fade). No Figma, o hero da Home (`57:1640`) tem exatamente o mesmo formato: cartão recortado de 1480×768 com os dois logos no recorte.

| Parte | Como ficou |
|---|---|
| Cartão com recortes | Recortes com cantos côncavos em **#FDFDFF** (fundo da Home). Logos Unicultura e Garatuja no recorte superior. |
| Fotos | As **duas fotos** que alternavam por CSS agora usam o **Slideshow de fundo nativo** (fade de 1,5 s a cada 6 s, com Ken Burns). O overlay é o mesmo gradiente da Garatuja. |
| Menu | Barra de vidro com o menu do WordPress, pointer vermelho **#F10505** e dropdown com hover #F0F2FA / #010658. Os ícones sociais e o botão "Agendar visita" são os **widgets originais da Home**, com os mesmos estilos. |
| Menu ao rolar | Depois de 40 px, fica fixo, centralizado, se alarga até 1240 px, escurece e mostra os logos brancos (desktop e tablet). |
| Celular | Hambúrguer na linha dos logos. Ícones sociais e botão ocultos. A foto fica no topo, dissolvendo no azul, com o texto embaixo. |
| Conteúdo | Os **widgets originais** da Home: selo vermelho, título, texto, botões "Agendar visita" / "Conhecer Proposta" e a prova social "+1.200 famílias", com a animação própria dela. Entram em cascata. |

**Removidos do hero antigo:**
- o CSS das duas imagens com `::before`/`::after`;
- o script `show-second`, que não era usado pelo CSS.

### Fotos do slideshow

Estão com as mesmas URLs usadas antes: `foto2-home-2.webp` e `group_6.webp`. **Atenção:** se algum desses arquivos for a arte já recortada, exportada do Figma com o recorte, os logos e o gradiente, troque pela **foto pura**. O recorte agora é feito pelo container, e a foto pura evita recorte duplo e logos repetidos.

Para trocar:
1. Selecione o container `gt-hero` e abra *Estilo → Background → Slideshow → Galeria*.
2. Troque as fotos.
3. Se as fotos novas já tiverem um gradiente escuro, reduza a opacidade do *Background Overlay*.

## 2. Melhorias no resto da página

**SEO e hierarquia de títulos.** A página não tinha **H1**.

| Título | Antes | Depois |
|---|---|---|
| Título do hero | H2 | **H1** |
| Selo "EDUCAÇÃO INFANTIL AO ENSINO MÉDIO" | H2 | `<p>` |
| "TIRE SUAS DÚVIDAS" | H2 | `<p>` |
| Títulos dos cards do carrossel de etapas | H2 | H3 |

Todos têm tipografia própria, então o visual não muda.

**Correção:** a cor das bolinhas ativas do carrossel de etapas estava escrita `##FF0B0B`, que é inválida, e virou `#FF0B0B`.

**Animações de entrada**, na duração *Fast* e suavizadas para 32 px de deslocamento:

| Seção | Animação |
|---|---|
| Duas escolas | Título, texto e as duas linhas. As fotos dão um zoom suave no hover (classe `un-zoom`). |
| Carrossel de fotos | Fade. |
| Nossa Proposta | Títulos, imagem, texto e botão em cascata. |
| Etapas Unicultura | Ícone, título, botões e o carrossel. |
| Diferenciais | Os cards entram em cascata, linha a linha, e o hover existente foi mantido. |
| Depoimentos | Título, texto e os cards. |
| CTA com formulário | O card sobe. |
| FAQ | Títulos e o acordeão. |

Quem ativou "reduzir movimento" no sistema vê a página sem as animações de entrada; o Elementor já as desliga, e o CSS desliga o restante.

## 3. Ajustes (2ª rodada)

- **Celular:** a foto do slideshow não se repete mais para baixo. O slideshow do Elementor não define `no-repeat`; o CSS agora define, com o azul #020659 atrás.
- **Menu fixo:**
  - fundo **azul** (rgba(1, 6, 88, 0.94)) ao rolar, com seletor reforçado para vencer a cor do container;
  - **20 px** do topo;
  - logada no WordPress, fica 20 px abaixo da barra de administração.
- **Editor:** o espaço tracejado dos logos do menu fixo só aparece no desktop e no tablet, não mais no celular.

### Animações e scroll novos

| Efeito | Onde | Como |
|---|---|---|
| Barra de progresso de leitura | Topo da tela, vermelha, avançando com o scroll | `un-home.js` + `.un-progress` |
| Contador | "+1.200 famílias" conta de 0 a 1.200 quando a prova social aparece (espera os 3,5 s da animação dela) | Classe `un-count` + atributo `data-delay` (Pro → *Custom Attributes*) |
| Títulos com cortina | "Duas escolas", "Nossa Proposta"/"Pedagógica", "Etapas", "O que os pais…", "Perguntas frequentes" se revelam da esquerda para a direita | Classe `un-reveal` + entrada *Fade In* |
| Parallax | Fotos de "Duas escolas" e de "Nossa Proposta" (só desktop) | **Pro**: *Motion Effects → Vertical Scroll*, velocidade 1 |

Com "reduzir movimento" ativado no sistema:
- **Desligados:** o contador (mostra direto 1.200) e a cortina dos títulos.
- **Mantida:** a barra de progresso, que só acompanha a leitura.

## 4. CSS e JS

Ficam num widget HTML sem altura, no fim do bloco do topo. O código fonte está em `src/un-home.css` e `src/un-home.js`.

As classes são as mesmas da Garatuja (`gt-top`, `gt-hero`, `gt-notch`, `gt-navbar`, `gt-navbar-logos`, `gt-scrolled`...), mais `un-zoom`. O CSS da página (`p { margin: 0 }`) foi mantido.

## 5. Como aplicar

1. Faça um backup da Home atual (*Templates → Salvar como template*).
2. Importe `home-elementor.json` em *Templates → Import*.
3. Na Home, apague o conteúdo e insira o template importado.
4. Salve e confira no desktop, no tablet e no celular.

---

## Seção extra: Depoimentos (`secao-depoimentos-elementor.json`)

Substitui a seção atual "O que os pais dizem sobre nós?". Gerador: `src/build_secao_depoimentos.py`. O CSS e o JS (`src/un-depoimentos.css` e `src/un-depoimentos.js`) vão embutidos num widget HTML da própria seção.

| Parte | Como é |
|---|---|
| Esquerda | Selo "★★★★★ Famílias Unicultura", título com "dizem sobre nós?" em itálico laranja #FFB867 (entra com efeito de cortina), texto, 2 números com barra vermelha e o botão "Agendar visita" com seta em círculo vermelho. |
| Números | **+1.200** famílias (o mesmo dado do hero, conta de 0 a 1.200) e **2** escolas, uma trajetória. |
| Direita (desktop/tablet) | **Duas colunas de cards rolando sem fim**, uma subindo e outra descendo. Os cards ficam em zigue-zague, com fade no topo e embaixo, e a rolagem pausa com o mouse em cima. |
| Celular | Carrossel horizontal de arrastar, um card por vez, com o próximo aparecendo na borda. |
| Card | Aspas vermelhas, **etiqueta do segmento** (Garatuja em amarelo, Fundamental em azul, Ensino Médio em vermelho), 5 estrelas, depoimento, iniciais e "Mãe do Theo · Garatuja". Sobe 4 px no hover. |
| Fundo | Azul #0D1261 (o mesmo da seção atual), aspas gigantes translúcidas e um brilho vermelho suave. |

**⚠️ Os 8 depoimentos são EXEMPLOS.** No editor, cada card mostra a etiqueta vermelha "EXEMPLO - substituir"; ela não aparece no site publicado.

**Como substituir um depoimento:**
- Edite o card e troque o texto, o nome, a relação, as iniciais e a etiqueta do segmento.
- Cada coluna tem o **conjunto original** e uma **cópia** logo abaixo (`un-depo-dup`), que só serve para a rolagem não ter emenda. Ao editar um card, **faça a mesma alteração na cópia**. Outra opção: edite o conjunto original, apague a cópia e duplique o original de novo, adicionando a classe `un-depo-dup` e o atributo `aria-hidden|true`.

Tenha a autorização das famílias para publicar nomes e depoimentos.

**Como aplicar:**
1. Importe o JSON em *Templates → Import*.
2. Na Home, apague a seção antiga de depoimentos.
3. Insira o template "Unicultura - Seção Depoimentos" no mesmo lugar.

