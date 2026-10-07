# Cicatrize 3X: Página de Vendas da Pós-graduação (Elementor)

`cicatrize-pos-elementor.json` é a página inteira (hero até rodapé), montada só com **containers** e widgets do **Elementor gratuito**: Heading, Text Editor, Button, Icon, Icon List, Image, Counter, Nested Accordion e HTML. Não depende do Elementor Pro.

**Como importar:** vá em **Templates > Modelos salvos > Importar**, crie a página e insira o modelo. O modelo já vem com **Elementor Canvas**, então a página sai sem o cabeçalho e o rodapé do tema, como deve ser numa página de vendas.

Requisitos: Elementor 3.16 ou mais recente (containers em grade) com **Containers** e **Nested Elements** ativos em Elementor > Configurações > Recursos.

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
