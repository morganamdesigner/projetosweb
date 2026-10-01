#!/usr/bin/env python3
"""Seção "Perguntas frequentes" (Home) redesenhada, com as perguntas e respostas novas.

Duas colunas: à esquerda (fixa ao rolar, no computador) o título e um cartão "Ainda com
dúvidas?" com botão para agendar visita; à direita o acordeão aninhado do Elementor em
cartões numerados, ícone +/- e o item aberto destacado. O FAQ Schema do próprio widget fica
ligado (perguntas podem aparecer direto no Google). CSS no widget HTML da seção.
Saída: ../secao-faq-elementor.json

Uso:  python3 build_secao_faq.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))

import build_elementor_json as base  # noqa: E402
from build_elementor_json import HANKEN, add, anim, button, container, dims, gap, heading, px, text, typo, widget  # noqa: E402

OUT = os.path.join(HERE, "..", "secao-faq-elementor.json")

NAVY = "#010658"
INK = "#3B3F6B"
RED = "#F10505"
BG = "#F5F6FA"
CONTATO = "https://colegiounicultura.com.br/contato/"  # CONFERIR o endereço da página de contato

DOCS = [
    "1 foto 3×4 recente;",
    "Cópia da certidão de nascimento do aluno;",
    "Cópias do RG e CPF do aluno;",
    "Cópias do RG e CPF do responsável financeiro;",
    "Cópia de um comprovante de residência atualizado;",
    "Cópia da carteirinha do convênio médico, caso possua;",
    "Declaração de escolaridade atual;",
    "Declaração de transferência original, para alunos que vêm de outra escola;",
    "Histórico escolar original, que poderá ser entregue posteriormente, substituindo a declaração de transferência;",
    "Laudo médico, quando houver, para subsidiar o planejamento do atendimento às necessidades educacionais do aluno.",
]

FAQ = [
    ("Como funcionam as aulas e como conhecer a escola?",
     "<p>Nossa proposta pedagógica reúne diferentes abordagens e estratégias de ensino para promover uma "
     "aprendizagem significativa, contemplando as diversas áreas do conhecimento e o desenvolvimento integral "
     "dos alunos.</p>"
     "<p>Para conhecer nossa estrutura e saber mais sobre a proposta pedagógica, entre em contato com o "
     "departamento de matrículas e agende uma visita. <strong>Será um prazer receber sua família!</strong></p>"),
    ("Quais documentos são necessários para efetivar a matrícula?",
     "<p>Para a matrícula, é necessário preencher o requerimento e apresentar os seguintes documentos:</p>"
     '<ul class="un-faq-list">' + "".join(f"<li>{d}</li>" for d in DOCS) + "</ul>"
     '<p class="un-faq-note">O departamento de matrículas orientará a família sobre os documentos aplicáveis à '
     "etapa escolar do aluno e os prazos de entrega.</p>"),
    ("O colégio oferece transporte escolar?",
     "<p>O colégio disponibiliza uma lista de indicações de prestadores de transporte escolar que atendem à "
     "unidade. A contratação, os valores, as rotas e os horários devem ser combinados diretamente entre a "
     "família e o prestador escolhido.</p>"),
    ("Existe período integral disponível?",
     "<p><strong>Sim!</strong> Oferecemos as modalidades integral e semi-integral, com uma rotina organizada "
     "para conciliar as atividades escolares com momentos de recreação, alimentação e cuidados.</p>"
     "<p>Para consultar horários, valores e disponibilidade para cada faixa etária, entre em contato com o "
     "departamento de matrículas.</p>"),
]


def answer(html):
    body = text(html, INK, typo("typography", HANKEN, 17, 400, lh=27, size_m=16, lh_m=25),
                extra={"_css_classes": "un-faq-answer"})
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "padding": dims(0, 28, 28, 74),
        "padding_mobile": dims(0, 18, 22, 18),
    }, [body])


def build():
    base._counter[0] = 35000  # faixa própria de IDs
    css = open(os.path.join(HERE, "un-faq.css"), encoding="utf-8").read().strip()

    # --- coluna da esquerda ---
    eyebrow = heading("Tire suas dúvidas", "p", RED,
                      typo("typography", HANKEN, 13, 700, lh=16, ls=1.4, transform="uppercase"))
    title = heading('Perguntas <span class="un-mark-red">frequentes</span>', "h2", NAVY,
                    typo("typography", HANKEN, 48, 700, lh=52, ls=-1.8, size_t=40, size_m=32, lh_t=44, lh_m=36,
                         ls_m=-1))
    intro = text("<p>Reunimos as respostas para as dúvidas mais comuns das famílias sobre aulas, matrícula, "
                 "transporte e período integral.</p>", INK,
                 typo("typography", HANKEN, 17, 400, lh=27, size_m=16, lh_m=25))
    help_title = heading("Ainda com dúvidas?", "h3", "#FFFFFF",
                         typo("typography", HANKEN, 24, 700, lh=30, ls=-0.5, size_m=21, lh_m=27))
    help_text = text("<p>Nossa equipe de matrículas está pronta para ajudar e receber sua família para uma "
                     "visita.</p>", "rgba(255, 255, 255, 0.8)",
                     typo("typography", HANKEN, 16, 400, lh=25, size_m=15, lh_m=23))
    help_btn = button("Agendar uma visita", RED, "#FFFFFF", typo("typography", HANKEN, 16, 700, lh=20),
                      dims(14, 24, 14, 24), icon=12,
                      extra={"link": {"url": CONTATO, "is_external": "", "nofollow": "", "custom_attributes": ""},
                             "button_background_hover_color": "#FFFFFF", "hover_color": NAVY})
    help_card = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(12),
        "padding": dims(30, 28, 30, 28),
        "padding_mobile": dims(24, 20, 24, 20),
        "margin": dims(12, 0, 0, 0),
        "border_radius": dims(24),
        "background_background": "gradient",
        "background_color": "rgba(241, 5, 5, 0.5)",
        "background_color_stop": px(0, "%"),
        "background_color_b": NAVY,
        "background_color_b_stop": px(55, "%"),
        "background_gradient_type": "radial",
        "background_gradient_position": "top right",
        "css_classes": "un-faq-help",
    }, [help_title, help_text, add(help_btn, {"_margin": dims(6, 0, 0, 0)})])
    style = widget("html", {"html": "<style>\n" + css + "\n</style>", "_css_classes": "un-faq-style"})
    side = container({
        "content_width": "full",
        "width": px(38, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(14),
        "css_classes": "un-faq-side",
    }, [style, add(eyebrow, anim("fadeInUp")), add(title, anim("fadeInUp", 100)), add(intro, anim("fadeInUp", 200)),
        add(help_card, anim("fadeInUp", 300))])

    # --- acordeão ---
    acc = widget("nested-accordion", {
        "items": [{"item_title": q, "_id": base.new_id()} for q, _ in FAQ],
        "title_tag": "h3",
        "default_state": "expanded",
        "max_items_expended": "one",
        "faq_schema": "yes",
        "accordion_item_title_position_horizontal": "stretch",
        "accordion_item_title_icon_position": "end",
        "accordion_item_title_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "accordion_item_title_icon_active": {"value": "fas fa-minus", "library": "fa-solid"},
        "accordion_item_title_space_between": px(14),
        "accordion_item_title_distance_from_content": px(0),
        "accordion_padding": dims(24, 24, 24, 24),
        "accordion_padding_mobile": dims(18, 18, 18, 18),
        "accordion_border_radius": dims(20),
        "accordion_border_normal_border": "none",
        "accordion_border_hover_border": "none",
        "accordion_border_active_border": "none",
        "content_border_border": "none",
        "title_typography_typography": "custom",
        "title_typography_font_family": HANKEN,
        "title_typography_font_size": px(19),
        "title_typography_font_size_mobile": px(17),
        "title_typography_font_weight": "600",
        "title_typography_line_height": px(26),
        "title_typography_line_height_mobile": px(23),
        "normal_title_color": NAVY,
        "hover_title_color": RED,
        "active_title_color": NAVY,
        "normal_icon_color": NAVY,
        "hover_icon_color": RED,
        "active_icon_color": "#FFFFFF",
        "icon_size": px(14),
        "icon_spacing": px(16),
        "_css_classes": "un-faq-acc",
    })
    acc["elements"] = [answer(a) for _, a in FAQ]
    for c in acc["elements"]:
        c["isInner"] = True
    main = container({
        "content_width": "full",
        "width": px(62, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
    }, [add(acc, anim("fadeInUp", 200))])

    return container({
        "content_width": "boxed",
        "boxed_width": px(1200),
        "html_tag": "section",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "flex-start",
        "flex_align_items_tablet": "stretch",
        "flex_gap": gap(64),
        "flex_gap_tablet": gap(36),
        "flex_wrap": "nowrap",
        "padding": dims(110, 24, 110, 24),
        "padding_tablet": dims(88, 24, 88, 24),
        "padding_mobile": dims(64, 16, 64, 16),
        "background_background": "classic",
        "background_color": BG,
        "css_classes": "gt-root un-faq",
    }, [side, main], inner=False)


def main():
    data = {"content": [build()], "page_settings": [], "version": "0.4",
            "title": "Unicultura - Seção FAQ", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
