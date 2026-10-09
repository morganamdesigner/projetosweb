# Cicatrize 3X: Página de Vendas da Pós-graduação (Elementor)

`cicatrize-pos-elementor.json` é a página inteira (hero até rodapé), montada só com **containers** e widgets do **Elementor gratuito**: Heading, Text Editor, Button, Icon, Icon List, Image, Counter, Nested Accordion e HTML. Não depende do Elementor Pro.

**Como importar:** vá em **Templates > Modelos salvos > Importar**, crie a página e insira o modelo. O modelo já vem com **Elementor Canvas**, então a página sai sem o cabeçalho e o rodapé do tema, como deve ser numa página de vendas.

Requisitos: Elementor 3.16 ou mais recente (containers em grade) com **Containers** e **Nested Elements** ativos em Elementor > Configurações > Recursos.

## WhatsApp flutuante: `whatsapp-flutuante-elementor.json` (09/10)

Botão de WhatsApp só para dúvidas, sem roubar a atenção da conversão:
- **Quando aparece:** quando a pessoa já passou do hero **e** está há pelo menos 25 s na página. As duas condições valem juntas, então nunca aparece de cara.
- **Cor:** petróleo com o ícone branco e um anel rosé pulsando, porque o verde da página é só dos botões de ação.
- **Balão:** quando o botão aparece, mostra "Dúvidas? Fale com a nossa equipe no WhatsApp" por 7 s, uma vez por visita, com um × para fechar.
- **Celular:** fica acima da barra verde fixa "Quero minha vaga".
- **Mensagem pronta:** abre o WhatsApp com "Olá! Tenho uma dúvida sobre a Pós-graduação em Tratamento de Feridas e Podiatria."

**Como usar:** importe e coloque o container em qualquer lugar da página; o fim é o melhor. Depois troque `55SUBSTITUIR-NUMERO` no link `wa.me` pelo número com DDI e DDD, só dígitos (ex.: `5534999999999`). Para mudar o tempo, altere `data-delay="25"`. `whatsapp-flutuante-codigo.html` traz só o código do widget.

## Grade curricular com os 17 módulos novos: `secao-grade-elementor.json` (09/10)

Montada a partir do conteúdo programático atualizado e da seção exportada do site. Mantém o fundo, o título, os contadores e os mockups. Cole no lugar da seção 5.

- **5 blocos, com os módulos em ordem crescente:**
  - Base clínica: 01–06 (140 h);
  - Feridas complexas: 07–10 (80 h);
  - Podiatria: 11–14 (80 h);
  - Tecnologia: 15 (20 h);
  - Carreira: 16–17 (80 h).
  O Módulo 02 (Emergências na pessoa idosa) foi para Base clínica para manter a sequência.
- **Mockups menores:** até 240 px no computador e miniatura ao lado do nome do bloco no celular, sobre o quadro claro original. No computador, o mockup e o nome acompanham a rolagem.
- **Cada módulo fechado** mostra "Módulo 01 · 20 h" e o nome. Aberto, mostra os tópicos (em 2 colunas no computador) e quem ensina. Os módulos 03, 04, 06 e 07 têm duas disciplinas, cada uma com seu subtítulo.
- **Título e contador:** "17 módulos. 400 horas." e o contador "Disciplinas" virou "Módulos".
- **Ficou de fora:** CPFs, e-mails, coordenadoras da Anhanguera e bibliografia.

**Conferir:**
- **Carga horária:** o documento diz "Total 450 horas", mas a soma dos módulos dá 400 h (14 × 20 h + 3 × 40 h). A seção usa 400 h.
- **Resto da página:** ainda fala em "17 disciplinas" (selos do hero, Como funciona, FAQ, oferta). Se for mudar para "17 módulos" ou para outra carga horária, é preciso ajustar lá também.
- **Nome dos blocos:** se os mockups já trazem o nome do bloco escrito, dá para apagar o título "Base clínica" e os outros ao lado da imagem.

## Faixa do topo: `faixa-topo-elementor.json` (08/10)

Faixa verde-água escuro (#0E7C72) acima do hero com "Turma de Membros Fundadores · Vagas limitadas · Condição exclusiva da primeira turma":
- o texto em branco corre sem parar (122 s no computador, 24 s no celular) e pausa quando o mouse passa por cima;
- as frases são separadas por bolinhas feitas em CSS, sem símbolos;
- um ponto pulsa no início e um brilho atravessa a faixa;
- a faixa inteira é um link para a oferta (`#oferta`).

O CSS vai dentro do próprio widget. `faixa-topo-codigo.html` traz só o código do widget HTML, para colar direto no Elementor.

**Como usar:** importe o arquivo e coloque o container acima do hero, como primeiro item da página. Ou cole `faixa-topo-codigo.html` no widget que já está na página. A etiqueta "Turma de Membros Fundadores · Vagas limitadas" que está dentro do hero passa a repetir a faixa, então você pode tirá-la.

## Oferta mais conversiva: `secao-oferta-elementor.json` (08/10)

Parte da seção exportada do site, com as suas imagens (`src/entrada/secao-oferta-2026-10-08.json`). Cole no lugar da seção 9. O CSS vai dentro da própria seção.

**Bônus:**
- Faixa diagonal "BÔNUS 1", "BÔNUS 2"... no canto de cada cartão, com um brilho que passa de tempos em tempos.
- O valor voltou nos 4 cartões. Ele tinha sumido dos 3 primeiros quando os ícones foram trocados pelas imagens. Os 3 primeiros mostram "Valor R$ 677 · GRÁTIS PARA VOCÊ" e o Doppler mostra "Valor R$ 1.500 · SORTEIO".
- O ícone saiu, porque a imagem já mostra o bônus.
- No celular, cada cartão fica horizontal: imagem 40% e texto 60%.

**Preço:**
- "De ~~R$ 11.800~~ por" no lugar de "Valor da pós-graduação".
- Selo "Economize R$ 8.300 pagando no Pix" (11.800 − 3.500).
- Linha de confiança abaixo do botão: "Pagamento seguro · Pix ou cartão em até 12x".

**"O que recebe":**
- Novo item: "Chance de levar os bônus exclusivos da Aula Magna (veja abaixo)".
- No celular e no tablet, essa lista aparece **antes** do cartão de preço, para a pessoa ver o valor antes do preço.

## Página completa com ajustes de celular: `pagina-completa-elementor.json` (07/10)

Parte da página exportada do site (`src/entrada/pagina-completa-2026-10-07.json`) e muda só o que está listado abaixo. Textos, imagens e as outras edições continuam iguais.

**Celular:**
- **Grade curricular:** os cartões dos blocos ficam escuros (petróleo) e o ícone do bloco fica rosé, para "BLOCO 01" e "5 disciplinas" terem contraste. No computador nada muda.
- **Faixa "Turma de Membros Fundadores" (hero):** tinha largura fixa de 432 px, maior que a tela, e por isso a fonte estava em 8 px. Agora ela ocupa 100% da largura e a fonte vai para 10 px.
- **Botões verdes:** cabem em uma linha (13 px).
- **Paradoxo:** as 2 fotos ficam lado a lado em vez de empilhadas.
- **Como funciona:** os 8 cartões viram uma lista compacta, com o ícone à esquerda e o texto à direita.
- **Corpo docente:** os cartões das professoras ficam horizontais, com a foto à esquerda e o texto à direita.
- **Quem é o Dr. Cicatriz:** a moldura rosé não encosta mais na borda da tela.
- **Rodapé:** textos centralizados.

**Geral:**
- O parallax das fotos fica limitado a 40 px, para não sobrepor os textos em telas altas.

**Como usar:** importe o arquivo e substitua o conteúdo da página por ele. O CSS e o JS já vão dentro do hero.

**Correção do corpo docente no celular:** `secao-corpo-docente-elementor.json` traz só a seção 7, para colar no lugar da atual. No celular, o texto dos cartões das professoras sumia porque ficava com 100% de largura ao lado da foto e o cartão escondia o que passava da borda. Agora a foto ocupa 36% e o texto 64%. As regras de CSS desses cartões vão dentro da própria seção, então ela funciona mesmo sem atualizar o CSS do hero.

Para refazer a partir de um export novo: `python3 src/build_ajustes_pagina.py export.json`.

## Cards da seção 2 em 1 com imagens: `grid-2em1-imagens-elementor.json`

Os ícones dos 3 cards ("Raciocínio clínico", "Cicatrização mais rápida", "Atuação ampliada na podiatria") deram lugar a uma imagem grande no topo de cada card:
- a imagem ocupa a largura toda do card, com altura de 240 px no computador, 320 px no tablet e 210 px no celular, recortada para cobrir o espaço;
- no hover, a imagem dá um zoom suave (Animação ao passar o mouse: Crescer);
- o número (01, 02, 03) virou uma etiqueta sobre o canto da imagem;
- o título, a linha rosé e o texto continuam iguais, logo abaixo.

**Como usar:** importe o arquivo e troque o grid antigo da seção 2 em 1 por este. Depois clique em cada imagem e escolha a foto. No Navegador, cada uma diz o que mostrar:
- **Card 01:** avaliação clínica de uma ferida;
- **Card 02:** curativo ou ferida em cicatrização;
- **Card 03:** avaliação podológica do pé.

Tamanho ideal: horizontal, cerca de 1200 × 800 px, em WebP ou JPG. Mantenha o assunto no centro, porque a imagem é recortada pelas bordas.

## Hero completo num arquivo só: `hero-completo-elementor.json`

Traz o hero inteiro num arquivo:
- o container da foto de fundo, já com as classes `cz cz-hero`;
- o conteúdo com os selos do MEC e da Anhanguera;
- a barra de vagas;
- o CSS e o JS da página, num widget HTML invisível ("⚙ CSS + JS da página").

**Como usar:**
1. Suba `assets/selo-reconhecido-mec.webp` e `assets/logo-anhanguera.svg` na Biblioteca de Mídia, sem renomear.
2. Importe o arquivo e coloque-o no lugar do hero atual.
3. **Coloque a foto de fundo de novo:** Estilo > Fundo > Imagem, no computador e no celular. No celular, a posição já vem em "top center".
4. **Apague o container "⚙ Estilos e animações" do topo da página,** se ele ainda existir. O CSS e o JS agora vêm dentro do hero, e com os dois o script rodaria em dobro.

**Selos no celular:** flutuam sobre a foto do expert, no topo do hero. O selo do MEC fica embaixo à esquerda e a logo da Anhanguera em cima à direita, como no computador. As posições usam `vw` a partir do topo da coluna de texto, a mesma medida da margem de 74vw que deixa a foto aparecer. Para ajustar, use **Avançado > Posição** de cada imagem (no Navegador: "Selo MEC sobre a foto (só celular)" e "Logo Anhanguera sobre a foto (só celular)"). Valores mais negativos sobem a imagem. No tablet, os selos continuam lado a lado abaixo do texto.

**Camada escura:** vem desligada, porque a sua foto de fundo já tem o design pronto. Para ligar o degradê escuro e a textura de filme, acrescente `cz-camada` em Avançado > Classes CSS do hero.

## Atualização do hero: selos do MEC e da Anhanguera (07/10)

Arquivos novos:
- `hero-selos-elementor.json`: o container de conteúdo do hero, montado a partir do que está publicado no site (mantém suas edições).
- `estilos-animacoes-elementor.json`: o container "⚙ Estilos e animações" com o CSS e o JS atualizados.
- `assets/selo-reconhecido-mec.webp` e `assets/logo-anhanguera.svg`: as imagens dos selos.

**Por que as animações e o fundo dos ícones sumiram:** tudo isso dependia das classes `cz cz-hero` no container de fora do hero (onde fica a foto de fundo). Quando o fundo foi trocado, essas classes saíram. Agora:
- o container de conteúdo do hero tem a classe `cz` própria;
- o fundo "vidro" dos ícones é configuração nativa (Estilo > Fundo e Borda);
- o CSS do hero não depende mais de `.cz-hero`.

**Selos separados:**
- **No computador:** o selo do MEC (redondo) e a logo da Anhanguera (num cartão branco) flutuam sobre a foto de fundo. Para mudar a posição, use **Avançado > Posição** de cada imagem.
- **No tablet e no celular:** os dois ficam lado a lado, logo abaixo do texto de apoio.
- O brilho rosé dessa coluna saiu, porque ficaria por cima do rosto do expert.

**Passo a passo:**
1. Envie as 2 imagens de `assets/` para a **Biblioteca de Mídia**, sem renomear. O JSON aponta para `.../uploads/2026/10/selo-reconhecido-mec.webp` e `.../uploads/2026/10/logo-anhanguera.svg`. Se o WordPress mudar o nome (ex.: `-1`), é só clicar na imagem e escolher de novo.
2. Importe `hero-selos-elementor.json` e coloque o container no lugar do conteúdo atual do hero, dentro do container que tem a foto de fundo.
3. Importe `estilos-animacoes-elementor.json` e coloque-o no topo da página, no lugar do "⚙ Estilos e animações" antigo. Se ele tiver sido apagado, é por isso que as animações pararam na página toda.
4. (Opcional) Volte as classes `cz cz-hero` em **Avançado > Classes CSS** do container com a foto de fundo. Elas trazem de volta a camada escura de leitura sobre a foto e a textura de filme.

O script `src/build_hero_selos.py` refaz esse hero a partir de um export novo: `python3 src/build_hero_selos.py export.json`.

## Estrutura (nomes no Navegador do Elementor)

| # | Seção | O que tem |
|---|---|---|
| ⚙ | Estilos e animações | Widget HTML com o CSS e o JS da página e o botão fixo do celular. **Não apagar.** |
| 1 | Hero | Logo, selo "Membros Fundadores" com ponto pulsando, H1 que sobe palavra por palavra (o trecho "certificado pelo MEC" ganha um marca-texto), 4 selos com ícones, CTA, a foto do expert com dois chips flutuando e a barra "30% das vagas preenchidas", que enche e conta até 30% |
| 2 | O paradoxo | Texto, a faixa inclinada "Agora troque de lugar." que se revela, colagem com 2 fotos do expert com parallax e, no fim, a frase de fechamento, que acende palavra por palavra conforme a rolagem |
| — | Faixa de palavras | Faixa rosé inclinada, em movimento contínuo |
| 3 | A pós 2 em 1 | Diagrama animado com dois círculos ("Feridas" + "Podiatria") que se unem em "1 diploma MEC", 3 cards com efeito 3D e brilho que segue o mouse, e a frase de destaque acendendo com a rolagem |
| 4 | Para quem é | Título fixo à esquerda (no computador), 5 itens com ícones e números vazados, nota de elegibilidade |
| 5 | O que você vai dominar | Contadores animados (17 · 400 · 5 · 100%) e um acordeão por bloco: nome da disciplina visível, descrição ao clicar |
| 6 | Como funciona | 8 cards em grade (4 > 2 > 1 colunas) e o CTA |
| 7 | Corpo docente | Card de destaque do Dr. Cicatriz com as 6 disciplinas dele em chips, mais 6 cards de professores |
| 8 | Quem é o Dr. Cicatriz | Foto com moldura rosé, credenciais, citação e assinatura que "se escreve" |
| 9 | Oferta (`#oferta`) | Cartão de preço com borda girando e preço riscado que se desenha, lista do que o Membro Fundador recebe, contagem regressiva até 27/10 às 23h59 e 4 cards de bônus |
| 10 | Perguntas frequentes | Acordeão com FAQ Schema (as perguntas podem aparecer no Google) e cartão de WhatsApp |
| 11 | CTA final | Pergunta de fechamento com anéis pulsando ao fundo |

## O que mudou em relação ao Figma

- **Cores:** só #0F4F5C, #3B5C66, #CF8A86 e #FFFFFF (mais tons claros e transparentes delas). O fundo azul-marinho da dobra 3 e o laranja dos ícones viraram petróleo e rosé. O petróleo mais fechado (#0B3C46) só aparece no degradê dos fundos escuros, para dar profundidade.
- **Botões padronizados:** um único estilo, em verde, com brilho que atravessa, anel pulsando e seta. Só os botões de ação são verdes. O botão do WhatsApp é contornado.
- **Textos do botão:** "GARANTIR INGRESSO - LOTE 01" e "Quero participar" foram trocados pelos da copy ("QUERO MINHA VAGA DE MEMBRO FUNDADOR" e "QUERO SER MEMBRO FUNDADOR").
- **Ícones trocados para combinar com o texto:** MEC → capelo, 100% online → notebook, 400 horas → livro, ao vivo → câmera, raciocínio clínico → cérebro, cicatrização → curativo, podiatria → pegadas, e assim por diante.
- **Dobra 3:** o parágrafo do Figma repetia a subheadline do hero. Usei o texto certo da copy. Também removi os rótulos "RJ PASS 1" dos cards.
- **No celular:** um botão "Quero minha vaga" fica fixo embaixo depois do hero e some na oferta e no CTA final.
- **Acessibilidade:** quem ativa "reduzir movimento" no sistema vê tudo sem animação. No editor do Elementor, tudo aparece sem esperar o scroll.

## Antes de publicar

### Fotos (no editor, aparece uma etiqueta "📷 SUBSTITUIR FOTO")
- **Hero, fundo:** está vazio, como você pediu. Vá em **1 · HERO > Estilo > Fundo > Imagem**. Já existe uma camada escura sobre a foto para o texto ficar legível.
- **Hero, foto do expert:** PNG recortado, com o selo do MEC e da Anhanguera. Se a foto do expert entrar no próprio fundo, apague esse widget.
- **Logo:** não consegui baixar o SVG do Figma daqui. Exporte o "Traced Image" e suba no widget de logo (246 px).
- **Paradoxo:** 2 fotos verticais do expert em atendimento.
- **Corpo docente:** 1 foto do Dr. Cicatriz e 6 dos professores (quadradas ou 4:5).
- **Quem é o Dr. Cicatriz:** 1 retrato vertical (4:5).

### Links
- **Checkout:** os 2 botões da oferta apontam para `https://SUBSTITUIR-LINK-DO-CHECKOUT`. Os outros levam à seção `#oferta`.
- **WhatsApp:** `https://wa.me/55SUBSTITUIR-NUMERO`, no botão e na última pergunta do FAQ.

### Itens da copy marcados com [confirmar] (deixei visíveis de propósito)
- **Como funciona > Avaliação:** "[confirmar: sem TCC, avaliação por disciplina]"
- **Oferta:** o valor da parcela ("12x de R$ [valor]"), as condições de boleto/cartão sem limite, a isenção de matrícula e o acesso vitalício.
- **FAQ:** cursos aceitos, TCC, formas de pagamento e o link do atendimento.

### Ajustes no widget "⚙ Estilos e animações"
- **Barra de vagas:** mude `data-percent="30"` no widget HTML da barra (dentro do hero).
- **Contagem regressiva:** `data-end="2026-10-27T23:59:00-03:00"`. Depois do prazo, ela mostra "Os bônus da Aula Magna foram encerrados".

### Outros
- **Textos novos (curtos, de apoio) que não estão na copy:** as legendas dos selos do hero ("Estude de onde estiver", "Encontro com o tutor"), as etiquetas das seções, a frase de apoio em "Para quem é", o cartão "Ainda com dúvidas?", o texto do CTA final e o rodapé.
- **Professoras Danielle e Thais:** a copy não traz a titulação detalhada delas, então o card mostra só o que elas ensinam.

## Arquivos

- `src/build_cicatrize.py` gera o JSON (`python3 src/build_cicatrize.py`). A copy, os links e as cores ficam no começo do arquivo.
- `src/cz-page.css` e `src/cz-page.js` vão embutidos no widget HTML do topo. Todas as classes usam o prefixo `cz-`.
