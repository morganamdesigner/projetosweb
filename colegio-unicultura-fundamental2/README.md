# Colégio Unicultura: página Ensino Fundamental II (Elementor)

`fundamental2-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema).
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.

## O que mudou

| Seção | Antes | Agora |
|---|---|---|
| Menu + hero | Menu antigo, script de slide, **sem foto de fundo definida** (só o slideshow antigo), título em H2 | Mesmo cabeçalho e cartão azul da Home e do Fundamental I, com uma foto só. O título virou H1, com "novos desafios." em laranja. Também tem o contador "+1.200 famílias", "Fundamental II" em destaque e o botão "Conhecer os eixos". |
| Faixa de palavras (nova) | — | Faixa azul inclinada com "Autonomia ✦ Cultura Digital ✦ Cultura Olímpica ✦ Plantão de Monitoria ✦ Sistema Poliedro ✦ Novos desafios", em movimento contínuo. Pausa no hover. |
| Três eixos | Lista de ícones com CSS inline e foto `group_11.webp` | A foto fica fixa enquanto os 3 cards (01, 02, 03) passam (desktop). Uma linha vermelha se preenche com o scroll, e cada card acende ao chegar na tela. |
| Aprofundar, argumentar e investigar | Texto branco sobre imagem em "contain", com espaçamentos enormes no tablet/celular (1700px, 800px) | Cartão com a foto `foto-estudante-uni-bg.webp` e degradê azul (no celular, a foto fica no topo). As três palavras entram uma a uma, saindo do desfoque. |
| Apoio que acompanha de perto | Logo + texto soltos | Logo flutuando com anéis pulsando, "de perto" em laranja, 3 checks (revisão, dúvidas, aprendizagens) e botão com seta. |
| Galeria, Poliedro, Equipe, CTA | Iguais às do Fundamental I antigo | Mesmas melhorias do Fundamental I: faixa de fotos em movimento, cartão do Poliedro, 6 slides vazios removidos, nomes em H3, fonte Hanken Grotesk e animações. |

## Conferir antes de publicar

- **Foto do hero**: a página não tinha foto de fundo. Usei `group_6.webp` (1ª foto do slideshow antigo desta página). Troque por uma foto do Fundamental II em Estilo > Fundo do cartão azul.
- **"5º ao 9º ano"**: mantive o texto da página, mas o Fundamental II costuma ser do 6º ao 9º ano (e a página do Fundamental I diz "3º ao 5º ano"). Confirme.
- **Botão "Ver todos os diferenciais"**: estava sem link na página atual. Coloque o link da página de diferenciais.
- **Nomes da equipe**: mesmos ajustes do Fundamental I ("Camila" na foto `camila.webp`, "Lucas" na foto `lucas.webp`). Confirme.
- **Textos novos** (curtos, de apoio): "Anos Finais", "Rumo ao Ensino Médio", "Plantão de Monitoria", "Parceria pedagógica", os 3 checks do apoio, a faixa de palavras e o botão "Conhecer os eixos". O título "Aprofundar, Argumentar, e Investigar." virou "Aprofundar, argumentar e investigar." (sem a vírgula antes do "e").

## Arquivos

- `src/build_fund2.py` gera o JSON. Ele reaproveita as funções de `colegio-unicultura-fundamental1/src/build_fund1.py` (hero, galeria, Poliedro, equipe, CTA).
- `src/un-fund2.css` / `src/un-fund2.js` têm a faixa de palavras, a linha do tempo dos eixos, as palavras que entram uma a uma e o bloco de apoio. Eles vão embutidos no widget HTML do topo, junto com `un-home-v2.css/js` e `un-fund1.css/js`.
