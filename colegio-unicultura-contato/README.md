# Colégio Unicultura: página Contato (Elementor)

`contato-elementor.json` é a página inteira, sem o rodapé (ele é um modelo do tema). URL sugerida: `/contato`.
Para importar, vá em **Templates > Modelos salvos > Importar** e depois insira o modelo na página.
A copy é a enviada pela cliente.

## Estrutura

| # | Seção | Design e efeitos |
|---|---|---|
| — | Menu + hero | Mesmo cabeçalho da Home. Cartão azul com "Vamos **conversar?**", o texto da copy, um botão verde **"Chamar no WhatsApp"** (com pulso suave) e "Ver todos os canais" (↓). À direita, uma ilustração animada: celular com uma **conversa que aparece mensagem a mensagem** e "digitando…", envelope, pino de mapa e telefone tocando. |
| 01 | Fale com a gente | Cartão azul em destaque para o **WhatsApp** (número grande + botão), e 4 cartões: Telefone, E-mail, Endereço e Horário da secretaria. No hover o cartão sobe e o ícone fica vermelho. |
| 02 | Onde estamos | **Google Maps** (widget nativo, sem chave de API) em um quadro arredondado, em tons de cinza/azul até o mouse passar. Por cima, um cartão com o endereço, o horário e o botão **"Como chegar"** (abre a rota no Google Maps). No celular o cartão fica abaixo do mapa. |
| 03 | Redes sociais | Fundo azul com grade, o texto da copy e um cartão por rede (Instagram, Facebook, YouTube). No hover cada cartão ganha **a cor da rede** e a seta gira. |

Também tem o número gigante vazado (01 a 03), o índice lateral fixo (telas ≥ 1200px), entradas suaves e a barra de progresso de leitura.

## Dados para preencher

Todos os dados estão como `[inserir …]`. Dá para editar direto no Elementor, ou trocar no topo do
`src/build_contato.py` (bloco "DADOS DE CONTATO") e gerar de novo com `python3 build_contato.py`.

| Onde | O que colocar |
|---|---|
| Cartão WhatsApp (número) e **todos os botões "Chamar no WhatsApp"** (hero e cartão) | Número e link `https://wa.me/55DDDNUMERO` |
| Cartão Telefone | Número. Para ligar ao tocar, link `tel:+55DDDNUMERO` no título |
| Cartão E-mail | E-mail. Link `mailto:email@...` no título |
| Cartão Endereço + cartão do mapa | Endereço completo |
| Cartão Horário + cartão do mapa | Horário da secretaria |
| Widget Google Maps | Campo "Localização": trocar "Colégio Unicultura" pelo endereço completo |
| Botão "Como chegar" | Trocar o fim do link pelo endereço (`...destination=Rua+Tal,+123,+Cidade`) |
| Redes sociais | Perfil de cada rede (`[@perfil]`) e os links do ícone, do nome e da seta. **Apagar o cartão das redes que o colégio não usa** (a grade se ajusta; em 2 cartões, mude a grade para 2 colunas) |

Textos de apoio que não estavam na copy: "Contato", "Ver todos os canais", "Canais de atendimento",
"O jeito mais rápido de falar com a gente.", "Visite a escola", "Como chegar", "Redes sociais",
"Siga a Unicultura" e as falas da ilustração.

## Arquivos

- `src/build_contato.py` gera o JSON (reaproveita o cabeçalho e os capítulos das páginas Diferenciais/Parceiros).
- `src/un-contato.css` tem as animações desta página. Ele vai embutido no widget HTML do topo.
- `src/ilustracoes/conversa.svg` é a ilustração do hero (também pode ir para a Biblioteca de Mídia, mas como imagem fica parada).
