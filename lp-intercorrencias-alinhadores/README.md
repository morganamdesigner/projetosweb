# LP · Guia Prático: Intercorrências com Alinhadores

O arquivo de importação é `lp-intercorrencias-alinhadores-elementor.json`. Ele traz a página inteira, do topo ao rodapé, com:

- containers Flexbox e Grid do Elementor;
- fonte Montserrat;
- todas as animações descritas nas notas 🎬 do Figma.

**Fonte do design:** arquivo Figma `BqhOLsRLn3SSVPxfFkAycj`, frame `5:6`, as notas de animação do frame `11:629` e o pacote `cena_scroll_pacote.zip`.

## Como importar

1. No WordPress, vá em *Templates → Saved Templates → Import Templates* e envie o JSON.
2. Crie uma página, clique em *Edit with Elementor*, abra a pasta de templates e insira **"LP · Guia Prático Intercorrências com Alinhadores"**.
3. Em *Configurações da página*, confira se o layout é **Elementor Canvas**, sem cabeçalho nem rodapé do tema. O JSON já vem assim.
4. Na importação, o Elementor copia as imagens para a Biblioteca de Mídia.

### Requisitos

- **Elementor 3.2x ou mais recente**, com Flexbox Container ativo. É o padrão nas instalações novas.
- **Elementor Pro.** Ele é usado em:
  - barra superior e coluna da agenda fixas (*Sticky*);
  - parallax da composição do hero (*Motion Effects*);
  - carrossel aninhado das páginas do guia;
  - CSS do elemento, que posiciona o brilho e as setas do carrossel.
- O **GSAP 3.12.5** e o **ScrollTrigger** carregam do cdnjs, dentro do widget de animações. Não há plugin para instalar.

## Estrutura

A estrutura toda é nativa: containers, títulos, textos, botões, imagens, lista de ícones, contador, carrossel e acordeão. Tudo pode ser editado pelo painel.

Há só **três widgets HTML**, onde não existe controle nativo equivalente:

| Widget HTML | Onde fica | Por quê |
|---|---|---|
| `LP · estilos e animações (não apagar)` | dentro da barra superior, invisível | CSS e JS das animações. Tudo se prende às classes `lp-*` dos containers e widgets. |
| `Cena 3D (150 quadros)` | seção 03 | O `<canvas>` que desenha a sequência de quadros conforme o scroll. |
| `Sublinhado (desenha no scroll)` | seção 03b | O traço em SVG sob "improviso:". O efeito de desenho usa `stroke-dashoffset`. |

O código-fonte do CSS e do JS está em `src/lp-motion.css` e `src/lp-motion.js`.

| # | Seção (nome no Navegador) | Como foi montada |
|---|---|---|
| 00 | Barra superior | Fixa no topo. Marquee ← de 30 s, que pausa no hover. |
| 01 | Hero | Logo, texto, botões e composição. Âncoras `#oferta` e `#por-dentro`. |
| 02 | Faixas em movimento | Duas faixas cruzadas em sentidos opostos, de 40 s. |
| 03 | Dor | Seção presa por cerca de 3 telas. O scroll avança os 150 quadros e acende 01 → 02 → 03, e por fim a pergunta. No celular, a cena fica em cima, o card embaixo, e não há pin. |
| 03b | Sem critério | Presa por cerca de 1,5 tela. A frase sobe, "improviso:" vai de 0,6 a 1 e o gradiente se preenche, o sublinhado se desenha e os pontos fazem parallax. |
| 03c | Consequências | Cards em cascata, números 00 → 0X (widget Contador), barra do "custo" e frase final com gradiente. |
| 04 | Apresentação | As 3 etapas entram em sequência, as setas se desenham e "Conduta" entra por último com escala. |
| 05 | Por dentro (`#por-dentro`) | Carrossel aninhado: autoplay de 4 s, arrastar e lightbox nativo com zoom. A página central fica em escala 1 e as laterais em 0,8 e 0,64, com tilt 3D no hover no desktop. |
| 06 | Agenda | Coluna da esquerda fixa (*Sticky → Stay in column*). A linha AGORA desce com o scroll, o card que ela alcança fica escuro ("na cadeira") e os anteriores ganham "✓ conduta definida". O contador "08 de 15" e a barra acompanham. |
| 07 | Para quem é | Os 6 interruptores ligam um a um (140 ms), o anel do medidor avança 60° por item até 6/6 e brilha. No desktop, dá para clicar e ligar ou desligar. Nos itens "Não é para você", o riscado se desenha. |
| 08 | Bônus e oferta (`#oferta`) | Play com anel pulsando, "De R$ 97,00" riscado se desenhando, preço com contagem 97 → 27, botão com reflexo e passos com linha de progresso. |
| 09 | Garantia, autora e FAQ | Anel do selo girando, órbita em volta da foto, etiqueta do nome entrando de baixo e acordeão nativo (um aberto por vez, + vira ×, FAQ Schema ligado). |
| 10 | Fechamento | Órbitas, brilho pulsando, título com gradiente e botão com reflexo. |
| 11 | Rodapé | Logo, aviso legal e links. |
| | Barra fixa no celular | Visível só no celular: "R$ 27 · Quero o guia". Aparece depois do hero e some na seção da oferta. |

### Regras gerais das animações

- **Entradas.** São as animações nativas do Elementor (*Motion Effects → Entrance Animation*), suavizadas no CSS: fade-up de 24 px, 600 ms, ease-out. A cascata usa atrasos de 80 a 150 ms.
- **Botões primários.** Sobem 2 px no hover e mostram um reflexo a cada 4 s.
- **Movimento reduzido.** Com `prefers-reduced-motion`, ficam desligados o marquee, o parallax, os giros, a flutuação e o pin. O conteúdo aparece no estado final.
- **No editor do Elementor.** Não há pin. As seções ficam editáveis normalmente.

## O que trocar antes de publicar

1. **Link do checkout.** Os botões "Quero o guia + as 2 aulas por R$ 27" (oferta) e o botão do fechamento apontam para `#checkout`. Os demais levam a `#oferta`.
2. **Páginas do carrossel (seção 05).** São 5 imagens provisórias. Troque pelas páginas reais do Canva: p.06, p.04, p.07, p.12 e p.22.
3. **Capa da aula bônus (seção 08).** No Figma, ela também é provisória. Para usar uma arte, coloque-a como fundo do container "Capa da aula".
4. **Bio da autora (seção 09).** O texto `CRO-[UF] [número]…` está igual ao Figma, que também pede dados reais.
5. **Logo.** Foi montado com ícone e títulos. Se houver o arquivo da marca, troque o container "Logo" por uma imagem (hero e rodapé).
6. **Textos não confirmados.** Os componentes abaixo não tinham o texto legível no material recebido, então foram escritos a partir do contexto. Confira cada um:
   - botões;
   - itens com check do hero;
   - texto da seção 04;
   - frases dos interruptores da seção 07;
   - perguntas e respostas do FAQ.
7. **Links do rodapé.** Termos de uso, Política de privacidade e Contato estão com `#`.

## Imagens e quadros da cena

Os arquivos estão em `assets/` e são servidos pelo jsDelivr a partir do commit `51f8984`:

- `hero-composicao.webp`
- `oferta-mockup.webp`
- `autora.webp` (seções 07 e 09)
- `expert-post-it.webp`
- os 150 quadros de `cena/`

**Recomendado em produção:** hospede os quadros no próprio site.

1. Envie a pasta `assets/cena/` para `wp-content/uploads/lp-alinhadores/cena/`, por FTP ou pelo gerenciador de arquivos.
2. No widget **Cena 3D**, troque o início do `data-frames` pelo novo endereço, mantendo `f{n}.webp` no final.

Os quadros só começam a baixar quando a seção 03 se aproxima da tela.

## Cenas presas no scroll (como funcionam)

As seções 03 (cena do paciente), 03b ("improviso:") e o notebook da 04 não usam travas por JavaScript. Cada uma está dentro de uma **trilha** alta (`lp-track`), e o conteúdo fica num **palco** (`lp-stage`) com `position: sticky`. Quem segura o palco na tela é o próprio navegador: não treme, não some e não precisa de recálculo. O script (`src/lp-boot.js`) só mede quanto da trilha já foi rolado e anima o conteúdo. No desktop, ele também liga a rolagem suave (Lenis).

| Trilha | Desktop | Celular |
|---|---|---|
| `lp-track--dor` | 400vh | sem palco preso (cena e card não cabem numa tela) |
| `lp-track--crit` | 330vh | 270vh |
| `lp-track--laptop` | 260vh | 220vh |

Para a cena durar mais ou menos, mude a altura em `src/lp-track.css`. No Navegador do Elementor, essas trilhas aparecem como "… · trilha do scroll" / "Palco (preso na tela)": **não remova esses containers**.

Para aplicar a versão atual dos widgets num export do site: `python3 src/patch_export.py <export.json> lp-intercorrencias-alinhadores-elementor.json <saída.json>`.

## Regerar o JSON

```bash
cd src
python3 build_lp.py
```

O script lê `lp-motion.css` e `lp-motion.js` e embute os dois no widget de animações. Os tokens de cor ficam no topo de `build_lp.py`.
