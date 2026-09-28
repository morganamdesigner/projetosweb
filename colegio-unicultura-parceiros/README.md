# Colégio Unicultura: página Parceiros (Elementor)

`parceiros-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema). URL sugerida: `/parceiros`.
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.
A copy é a enviada pela cliente.

## Estrutura

| # | Seção | Design e efeitos |
|---|---|---|
| — | Menu + hero | Mesmo cabeçalho da Home. Cartão azul com H1 "Parceiros que **fortalecem nossa proposta**", "Agende uma visita" (→ /matriculas) e "Fale com a gente" (→ CTA final). À direita, uma **rede animada**: a Unicultura no centro, ligada aos 4 parceiros por linhas com pontinhos laranja correndo. Cada parceiro é clicável e leva à sua seção. Embaixo, "Nossos parceiros:" com links. |
| 01 | Sistema de Ensino Poliedro | Ilustração: tablet com gráfico de desempenho (as **barras crescem**), livro e um **poliedro girando**. Logo do Poliedro (já na biblioteca), selo "3º ano do Fundamental → 3ª série do Médio" e pílulas (Material didático, Tecnologia, Avaliações, Acompanhamento da aprendizagem). |
| 02 | Programa Lidere | Ilustração: degraus com coração, moeda e **foguete subindo**, e um caminho tracejado em movimento. Selo "Toda a trajetória no Unicultura". |
| 03 | Sim Inova | Fundo azul com grade. Ilustração: **robô que pisca e acena**, antena piscando, **engrenagens girando** e "</>". Selo "Tecnologia · Maker · STEAM". |
| 04 | Simple Education | Ilustração: balões **"Hello!" e "Olá!" flutuando**, globo, órbita girando e blocos A-B-C. Selo "Ensino Fundamental — Anos Iniciais". |
| — | CTA final | "Quer conhecer de perto **como cada parceria funciona na prática?**", "Agendar visita" (→ /matriculas) e "Falar pelo WhatsApp". |

Como nos Diferenciais: número gigante vazado (01 a 04) com parallax, índice lateral fixo (telas ≥ 1200px), entradas suaves e barra de progresso de leitura.
O logo de cada parceiro fica num **selo branco flutuando** no canto da ilustração.

## Para completar

- **Logos**: Lidere, Sim Inova e Simple Education estão com o placeholder do Elementor (widget Imagem dentro do selo branco). Troque pela imagem do logo. O Poliedro já usa `poliedro.webp` da biblioteca.
- **WhatsApp**: o botão "Falar pelo WhatsApp" está sem link (`https://wa.me/55DDDNUMERO`).
- **Textos de apoio que não estavam na copy**: "Parceiros educacionais", "Nossos parceiros:", "Parceiro 01…04", os selos de etapa ("Toda a trajetória no Unicultura", "Tecnologia · Maker · STEAM") e as pílulas (tiradas da própria copy).

## Ilustrações

As 5 ilustrações são SVG próprios, desenhados para esta página, e estão em `src/ilustracoes/`
(`rede-parceiros.svg`, `poliedro.svg`, `lidere.svg`, `sim-inova.svg`, `simple-education.svg`).
Elas vão embutidas em widgets HTML (por isso animam). Também podem ser enviadas à Biblioteca de Mídia e usadas
em outros lugares, mas como imagem ficam paradas.

## Arquivos

- `src/build_parceiros.py` gera o JSON (reaproveita o cabeçalho, os capítulos e o CTA da página Diferenciais).
- `src/un-par.css` tem as animações desta página. Ele vai embutido no widget HTML do topo, junto com `un-home-v2`, `un-fund1` e `un-dif`.
