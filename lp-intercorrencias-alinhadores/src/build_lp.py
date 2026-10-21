#!/usr/bin/env python3
"""LP "Guia Prático: Intercorrências com Alinhadores" para Elementor (containers Flexbox/Grid).

Fonte: Figma BqhOLsRLn3SSVPxfFkAycj, frame 5:6 ("LP · Intercorrências com Alinhadores · Desktop 1920"),
as notas de animação do frame 11:629 e o pacote cena_scroll_pacote.zip (150 quadros da seção 03).

Tudo é container/widget nativo. Há só três widgets HTML: o de estilos e scripts das animações (no topo),
o canvas da cena 3D (seção 03) e o traço SVG que se desenha sob "improviso:" (seção 03b).

Saída: ../lp-intercorrencias-alinhadores-elementor.json
Uso:   python3 build_lp.py
"""
import json
import os

from el import (MONT, border, button, cls, col, container, counter, dims, gap, grad, heading, html, icon,
                icon_list, image, link, new_id, px, row, setv, shadow, solid, text, typo, widget, anim)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "lp-intercorrencias-alinhadores-elementor.json")

# Imagens servidas pelo jsDelivr a partir do commit com os assets. Na importação, o Elementor
# copia as imagens dos widgets para a Biblioteca de Mídia.
ASSETS_COMMIT = "51f898463bb3dbb93ae46643a172b2e4d80e09d8"
ASSET = f"https://cdn.jsdelivr.net/gh/morganamdesigner/projetosweb@{ASSETS_COMMIT}/lp-intercorrencias-alinhadores/assets/"
CHECKOUT = "#checkout"  # TROCAR pelo link do checkout (Hotmart, Kiwify etc.)

# ---------------------------------------------------------------------------
# Tokens (paleta do pacote da cena + amostras do print do Figma)
# ---------------------------------------------------------------------------
NOITE = "#011324"
PROF = "#0B2D4A"
MED = "#0E3C5E"
TURQ = "#00C2C7"
AZUL = "#0A92C4"
AZC = "#7ED3E6"
TXT = "#C3D6E3"
WHITE = "#FFFFFF"
INK = "#4A5F73"
MUTED = "#8A9BAA"
LIGHT = "#F4F8FB"
LINE = "rgba(126, 211, 230, 0.18)"
GLASS = "rgba(255, 255, 255, 0.05)"
CYAN_GRAD = ("#07E3F3", "#0A92C4")
GREEN_GRAD = ("#22E36E", "#00A99D")


def section(settings, children, title, classes, boxed=True):
    s = {
        "content_width": "boxed" if boxed else "full",
        "html_tag": "section",
        "flex_direction": "column",
        "padding": dims(120, 24),
        "padding_tablet": dims(96, 24),
        "padding_mobile": dims(72, 16),
        "css_classes": "lp " + classes,
    }
    if boxed:
        s["boxed_width"] = px(1140)
    s.update(settings)
    return container(s, children, title, inner=False)


def r(desktop, tablet=None, mobile=None, key="flex_direction"):
    s = {key: desktop}
    if tablet is not None:
        s[f"{key}_tablet"] = tablet
    if mobile is not None:
        s[f"{key}_mobile"] = mobile
    return s


def w(pct, tablet=100, mobile=None):
    s = {"width": px(pct, "%")}
    if tablet is not None:
        s["width_tablet"] = px(tablet, "%")
    if mobile is not None:
        s["width_mobile"] = px(mobile, "%")
    return s


def eyebrow(label, color=TURQ, center=False, extra_cls=""):
    el = heading(label, color, typo("typography", 12, 700, lh=1.3, ls=3, transform="uppercase"),
                 align="center" if center else "left")
    return cls(el, ("lp-eyebrow " + ("lp-eyebrow--center " if center else "") + extra_cls).strip())


def h2(title, color, size=42, align="left", tag="h2", t=None, m=None, lh=1.15):
    return heading(title, color, typo("typography", size, 800, lh=lh, ls=-0.5, size_t=t or round(size * .86),
                                      size_m=m or round(size * .7)), tag=tag, align=align)


def body(html_, color, size=17, align="left", weight=400, lh=1.6, m=None):
    return text(html_, color, typo("typography", size, weight, lh=lh, size_m=m or max(14, size - 1)), align=align)


def btn_primary(label, url, green=False, full=False, small=False):
    pad = dims(14, 22) if small else dims(22, 34)
    b = button(label, url, (NOITE, None, NOITE, None),
               typo("typography", 13 if small else 15, 800, lh=1.2, ls=0.6, transform="uppercase", size_m=13),
               pad, icon=not small, gradient=GREEN_GRAD if green else CYAN_GRAD,
               button_box_shadow_box_shadow_type="yes",
               button_box_shadow_box_shadow=shadow(0, 14, 34, -12, "rgba(0, 194, 199, 0.55)"),
               text_padding_mobile=dims(14, 20) if small else dims(18, 22))
    if full:
        setv(b, align="justify")
    return cls(b, "lp-btn" + (" lp-btn--full" if full else ""))


def btn_ghost(label, url):
    b = button(label, url, (WHITE, "rgba(255, 255, 255, 0.04)", WHITE, "rgba(255, 255, 255, 0.10)"),
               typo("typography", 15, 700, lh=1.2, ls=0.3, size_m=13), dims(21, 30), border_color="rgba(255, 255, 255, 0.22)",
               text_padding_mobile=dims(17, 22),
               selected_icon={"value": "fas fa-arrow-down", "library": "fa-solid"})
    return cls(b, "lp-btn--ghost")


def orbits_glow(gx="50%", gy="50%", size=520):
    """Brilho turquesa que pulsa (container vazio posicionado pelo CSS)."""
    return setv(container({"css_classes": "lp-glow"}, [], "Brilho (decorativo)"),
                custom_css=f"selector{{--gx:{gx};--gy:{gy};--gs:{size}px}}")


def logo():
    """Assinatura horizontal (troque por uma imagem do logo, se houver)."""
    mark = icon("fas fa-tooth", NOITE, 20, view="stacked", secondary=None, padding=12)
    setv(mark, primary_color=TURQ, secondary_color=NOITE, _flex_size="none")
    names = col([
        heading("Guia prático", AZC, typo("typography", 9, 700, lh=1.2, ls=2.4, transform="uppercase")),
        heading("Intercorrências com", WHITE, typo("typography", 12, 600, lh=1.2)),
        heading("Alinhadores", TURQ, typo("typography", 19, 800, lh=1.05, ls=-0.3)),
    ], 1)
    return row([mark, names], 12, "Logo", flex_align_items="center", width=px(260), width_mobile=px(220))


# ---------------------------------------------------------------------------
# 00 · Barra superior (marquee) + widget de estilos/scripts
# ---------------------------------------------------------------------------

def motion_widget():
    css = open(os.path.join(HERE, "lp-motion.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "lp-motion.js"), encoding="utf-8").read().strip()
    code = (
        "<style>\n" + css + "\n</style>\n"
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>\n'
        "<script>\nwindow.addEventListener('DOMContentLoaded',function(){if(window.gsap&&window.ScrollTrigger)gsap.registerPlugin(ScrollTrigger);});\n</script>\n"
        "<script defer>\n" + js + "\n</script>"
    )
    return setv(html(code), _title="LP · estilos e animações (não apagar)", _position="absolute",
                _element_width="initial", _element_custom_width=px(0), _css_classes="lp-motion")


def s00_topbar():
    item = lambda t: heading(t, WHITE, typo("typography", 12, 700, lh=1.2, ls=2.4, transform="uppercase", size_m=11))
    track = row([item("Guia clínico de consulta rápida"), item("Acesso imediato")], 28, "Itens (o script repete)",
                css_classes="lp-marquee__track", flex_align_items="center", width=px(100, "%"))
    return container({
        "html_tag": "div",
        "flex_direction": "row",
        "flex_align_items": "center",
        "min_height": px(44),
        "overflow": "hidden",
        "css_classes": "lp lp-marquee lp-topbar",
        **grad("#00863F", "#137C5D", 90),
        "sticky": "top",
        "sticky_on": ["desktop", "tablet", "mobile"],
        "z_index": 100,
    }, [motion_widget(), track], "00 · Barra superior (marquee)", inner=False)


# ---------------------------------------------------------------------------
# 01 · Hero
# ---------------------------------------------------------------------------

def s01_hero():
    tag = heading("O alinhador não encaixou. E agora?", TXT, typo("typography", 26, 500, lh=1.3, size_t=24, size_m=19))
    h1 = heading('O guia prático de consulta rápida com a conduta para as '
                 '<span class="lp-shine">15 intercorrências mais comuns</span> com alinhadores.', WHITE,
                 typo("typography", 42, 800, lh=1.12, ls=-0.6, size_t=38, size_m=29), tag="h1")
    sub = body("<p>Para ortodontistas e dentistas que já tratam com alinhadores. Cada situação organizada em sinais, "
               "avaliação e conduta, para você decidir na cadeira entre manter a etapa, recuar um alinhador, recolar, "
               "fazer IPR ou replanejar.</p>", TXT, 18, m=16)
    method = heading("Sinais<span>→</span>Avaliação<span>→</span>Conduta", WHITE,
                     typo("typography", 12, 700, lh=1.3, ls=2.2, transform="uppercase", size_m=11),
                     _element_width="auto", _flex_align_self="flex-start", _padding=dims(13, 21), **solid(GLASS, "_background"),
                     **border(1, LINE, 999, on_widget=True))
    cls(method, "lp-method")
    checks = icon_list([
        "15 intercorrências organizadas em sinais, avaliação e conduta",
        "Critérios claros para manter, recuar, recolar, fazer IPR ou replanejar",
        "Para consultar na cadeira: no celular, no tablet ou no computador",
    ], TXT, typo("icon_typography", 16, 500, lh=1.5, size_m=15), icon_color=TURQ, icon_size=18, space=14)
    ctas = row([btn_primary("Quero o guia por R$ 27", "#oferta", green=True), btn_ghost("Ver o guia por dentro", "#por-dentro")],
               16, "Botões", flex_align_items="center", flex_wrap="wrap", **r("row", None, "column", "flex_direction"),
               flex_align_items_mobile="stretch")
    note = heading("PDF + Bônus · Acesso imediato · Garantia de 7 dias", "rgba(126, 211, 230, 0.75)",
                   typo("typography", 13, 500, lh=1.4, ls=0.3))
    texts = [tag, h1, sub, method, checks, ctas, note]
    for i, el in enumerate(texts):
        anim(el, "fadeInUp", i * 80)
    text_col = col(texts, 24, "Texto", **w(54), flex_justify_content="center", css_classes="lp-hero-text")

    visual = image(ASSET + "hero-composicao.webp",
                   "Dra. Joyce Duarte com páginas do guia Intercorrências com Alinhadores, o ebook e um tablet",
                   width=(100, "%"),
                   motion_fx_motion_fx_scrolling="yes", motion_fx_translateY_effect="yes",
                   motion_fx_translateY_direction="", motion_fx_translateY_speed=px(1.5),
                   motion_fx_translateY_affectedRange={"unit": "%", "size": "", "sizes": {"start": 0, "end": 100}},
                   motion_fx_devices=["desktop"])
    cls(visual, "lp-float")
    visual_col = anim(col([visual], 0, "Composição (expert + ebook)", width=px(42, "%"),
                          flex_justify_content="center", css_classes="lp-hero-visual",
                          _flex_align_self_tablet="center",
                          width_tablet=px(80, "%"), width_mobile=px(100, "%")), "fadeInUp", 200)

    content = row([text_col, visual_col], 40, "Conteúdo", **r("row", "column"), flex_align_items="center",
                  flex_gap_tablet=gap(56), margin=dims(72, 0, 0, 0), margin_mobile=dims(40, 0, 0, 0))
    return section({
        "padding": dims(32, 24, 140, 24),
        "padding_tablet": dims(28, 24, 110, 24),
        "padding_mobile": dims(20, 16, 90, 16),
        "min_height": px(1000),
        "min_height_tablet": px(0),
        **grad(MED, NOITE, 125, 0, 72),
    }, [orbits_glow("74%", "44%", 560), logo(), content], "01 · Hero", "lp-hero lp-orbits")


# ---------------------------------------------------------------------------
# 02 · Faixas cruzadas em movimento
# ---------------------------------------------------------------------------

def s02_ribbons():
    words = ["Para ortodontistas", "Guia prático", "15 intercorrências", "Alinhadores"]

    def band(title, color, bg, extra_cls):
        items = [heading(t, color, typo("typography", 18, 800, lh=1.2, ls=0.6, transform="uppercase", size_m=14))
                 for t in words]
        track = row(items, 30, "Itens (o script repete)", css_classes="lp-marquee__track", flex_align_items="center")
        return container({"flex_direction": "row", "flex_align_items": "center", "min_height": px(56),
                          "min_height_mobile": px(44), "overflow": "hidden",
                          "css_classes": "lp-marquee lp-ribbon " + extra_cls, **bg}, [track], title)

    back = band("Faixa de trás (→)", AZC, solid("#0A4A63"), "lp-ribbon--back lp-marquee--rev")
    front = band("Faixa da frente (←)", NOITE, grad(CYAN_GRAD[0], CYAN_GRAD[1], 90), "lp-ribbon--front")
    return container({
        "html_tag": "div",
        "min_height": px(104),
        "min_height_mobile": px(84),
        "margin": dims(-52, 0, -52, 0),
        "z_index": 5,
        "css_classes": "lp lp-ribbons",
        "flex_direction": "column",
    }, [back, front], "02 · Faixas em movimento", inner=False)


# ---------------------------------------------------------------------------
# 03 · Dor: cena do paciente (scroll)
# ---------------------------------------------------------------------------

SCENE_STOPS = [
    {"from": 0.24, "to": 0.40, "n": "01", "t": "alinhador folgado"},
    {"from": 0.52, "to": 0.68, "n": "02", "t": "gap no lateral"},
    {"from": 0.82, "to": 1.01, "n": "03", "t": "attachment do canino ausente", "ring": False},
]


def s03_dor():
    stops = json.dumps(SCENE_STOPS, ensure_ascii=False).replace("'", "&#39;")
    scene = html(
        f'<div class="lp-scene" data-frames="{ASSET}cena/f{{n}}.webp" data-count="150" data-stops=\'{stops}\'>'
        '<canvas width="1120" height="760" role="img" aria-label="Paciente em 3D sentado na cadeira do dentista, '
        'olhando preocupado para o alinhador"></canvas>'
        '<div class="lp-scene__ring"></div>'
        '<div class="lp-scene__label" aria-hidden="true"><b>01</b><span>alinhador folgado</span></div>'
        '<div class="lp-scene__prog" aria-hidden="true"><span></span><span></span><span></span></div></div>',
        _title="Cena 3D (150 quadros)")
    scene_col = col([scene], 0, "Cena", width=px(620), width_tablet=px(100, "%"), _flex_size="shrink")

    chip = heading("Consulta de retorno · alinhador 14", AZC,
                   typo("typography", 10, 600, lh=1.3, ls=2.5, transform="uppercase"),
                   _element_width="auto", _flex_align_self="flex-start", _padding=dims(8, 14), **solid(GLASS, "_background"),
                   _border_radius=dims(999))
    cls(chip, "lp-dor-chip")
    title = h2("O paciente senta na cadeira.", WHITE, 26, t=24, m=20, lh=1.3)

    def case_row(n, label):
        num = cls(heading(n, "rgba(126, 211, 230, 0.4)", typo("typography", 11, 700, lh=1, ls=2.2)), "lp-dor-num")
        txt = heading(label, "rgba(255, 255, 255, 0.45)", typo("typography", 15, 600, lh=1.45, size_m=14),
                      _flex_size="shrink")
        return row([setv(num, _flex_size="none"), txt], 14, f"Linha {n}", flex_align_items="center",
                   padding=dims(16, 18), padding_mobile=dims(12, 14), **solid(GLASS), **border(1, LINE, 14),
                   css_classes="lp-dor-row")

    rows = col([case_row("01", "O alinhador está folgado."), case_row("02", "Tem gap no lateral."),
                case_row("03", "O attachment do canino não está mais lá.")], 10, "Sinais")
    sep = container({"min_height": px(1), "height": px(1), **solid(LINE)}, [], "Divisória")
    ask = heading("E a pergunta aparece:", AZC, typo("typography", 14, 500, lh=1.4))
    q = cls(heading("É falta de uso, é attachment, é IPR ou é o planejamento?", WHITE,
                    typo("typography", 22, 800, lh=1.3, size_m=18)), "lp-dor-q")
    card = col([chip, title, rows, sep, ask, q], 20, "Card do caso", width=px(500), width_tablet=px(100, "%"),
               padding=dims(40), padding_mobile=dims(22),
               **grad("rgba(14, 60, 94, 0.92)", "rgba(1, 19, 36, 0.95)", 160), **border(1, LINE, 28),
               box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 30, 60, -20, "rgba(0, 0, 0, 0.5)"),
               _flex_size="none", z_index=2)
    return section({
        "min_height": px(100, "vh"),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
        "flex_gap": gap(40),
        "flex_gap_mobile": gap(18),
        "padding": dims(80, 24),
        "padding_mobile": dims(88, 16, 40, 16),
        "overflow": "hidden",
        **grad(MED, NOITE, 135, 0, 80),
    }, [scene_col, card], "03 · Dor (cena presa no scroll)", "lp-dor", boxed=False)


# ---------------------------------------------------------------------------
# 03b · Sem critério: frase de impacto
# ---------------------------------------------------------------------------

def s03b_impact():
    dots = container({"css_classes": "lp-dots"}, [], "Grade de pontos (decorativa)")
    over = eyebrow("Sem critério", "#5B7083", center=True, extra_cls="lp-eyebrow--both lp-impact-over")
    l1 = cls(h2("Sem critério, a consulta vira", PROF, 56, "center", t=44, m=28, lh=1.15), "lp-impact-l1")
    word = cls(heading("improviso:", PROF, typo("typography", 190, 900, lh=1.0, ls=-5, size_t=128, size_m=72),
                       align="center"), "lp-impact-word")
    line = setv(html('<div class="lp-impact-line" aria-hidden="true"><svg viewBox="0 0 960 22">'
                     '<path d="M6 15 C 220 7, 560 3, 954 10" pathLength="1" fill="none" stroke="#0B2D4A" '
                     'stroke-width="5" stroke-linecap="round"/></svg></div>'),
                _title="Sublinhado (desenha no scroll)", _element_width="initial", _element_custom_width=px(860),
                _element_custom_width_tablet=px(80, "%"), _element_custom_width_mobile=px(86, "%"),
                _margin=dims(-6, 0, 0, 0))
    hint = cls(icon_list([{"text": "role para ver o que acontece", "icon": "fas fa-mouse"}], "#5B7083",
                         typo("icon_typography", 13, 500, lh=1.4), icon_color="#5B7083", icon_size=16,
                         _margin=dims(28, 0, 0, 0)), "lp-impact-hint")
    return section({
        "content_width": "full",
        "min_height": px(100, "vh"),
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "flex_gap": gap(10),
        **solid("#E8EDF1"),
    }, [dots, over, l1, word, line, hint], "03b · Sem critério (frase presa no scroll)", "lp-impact lp-orbits",
        boxed=False)


# ---------------------------------------------------------------------------
# 03c · Consequências
# ---------------------------------------------------------------------------

def s03c_conseq():
    photo = anim(image(ASSET + "expert-post-it.webp",
                       'Dra. Joyce Duarte segurando um post-it azul escrito "Esse guia vai te salvar"',
                       width=(100, "%")), "fadeInLeft")
    photo_col = col([photo], 0, "Foto (post-it)", **w(46, None), width_tablet=px(70, "%"), width_mobile=px(100, "%"), _flex_align_self_tablet="center")
    items = [
        "Você prolonga a etapa “para ver se encaixa”",
        "Pede refinamento sem corrigir a causa, e o refinamento herda o erro",
        "Culpa a colaboração quando o gap localizado aponta para attachment, espaço ou staging",
        "Não sabe o que dizer ao paciente quando o tratamento atrasa",
    ]
    cards = []
    for i, t in enumerate(items, 1):
        num = counter(0, i, "0", TURQ, typo("typography_number", 30, 800, lh=1, size_m=24), duration=900,
                      _flex_size="none", _element_width="initial", _element_custom_width=px(52))
        cards.append(anim(row([num, body(f"<p>{t}</p>", WHITE, 17, weight=500, lh=1.5, m=15)], 18,
                              f"Consequência {i}", flex_align_items="flex-start", padding=dims(30, 32),
                              padding_mobile=dims(22, 20), **solid(GLASS), **border(1, LINE, 18),
                              css_classes="lp-conseq-card"), "fadeInUp", (i - 1) * 100))
    cost = col([body("<p><strong>O custo aparece depois:</strong> mais consultas, mais refinamentos e um paciente "
                     "que começa a duvidar do tratamento.</p>", TXT, 17, lh=1.6, m=15)], 0, "O custo",
               padding=dims(24, 32), padding_mobile=dims(20), **solid("rgba(0, 194, 199, 0.08)"),
               **border(1, "rgba(0, 194, 199, 0.3)", 18), css_classes="lp-cost lp-io", margin=dims(10, 0, 0, 0))
    final = cls(h2('O planejamento você já tem. <span class="lp-grad">Este guia é para quando o caso sai dele.</span>',
                   WHITE, 30, t=28, m=23, lh=1.3, tag="p"), "lp-sweep lp-io")
    right = col(cards + [cost, setv(final, _margin=dims(18, 0, 0, 0))], 16, "Consequências", **w(49, 100))
    return section({
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(48),
        **grad("#0A6B95", "#081B2F", 0, 0, 58, kind="radial", position="top right"),
        "overflow": "hidden",
    }, [photo_col, right], "03c · Sem critério (consequências)", "lp-conseq")


# ---------------------------------------------------------------------------
# 04 · Apresentação
# ---------------------------------------------------------------------------

def s04_apresentacao():
    left = [
        eyebrow("Apresentação", AZUL),
        h2('Guia Prático: Intercorrências com Alinhadores. <span class="lp-hl">Do diagnóstico à conduta.</span>',
           PROF, 40, t=36, m=28),
        body("<p>Um material de consulta rápida, escrito para ser aberto na cadeira. Cada intercorrência segue a "
             "mesma estrutura, do primeiro sinal à decisão clínica, com referências para aprofundar quando precisar."
             "</p>", INK, 17),
        col([icon("fas fa-quote-left", TURQ, 20),
             body('<p>Cada capítulo começa com uma pergunta direta <span style="color:#00C2C7">e termina numa '
                  'decisão clínica que você aplica na mesma consulta.</span></p>', WHITE, 18, weight=600, lh=1.5)],
            12, "Destaque", padding=dims(28, 32), padding_mobile=dims(24), **grad(PROF, NOITE, 135),
            border_radius=dims(20), margin=dims(8, 0, 0, 0)),
    ]
    for i, el in enumerate(left):
        anim(el, "fadeInUp", i * 80)

    def step(n, label, desc, dark=False):
        num = heading(n, NOITE, typo("typography", 15, 800, lh=1.46), align="center",
                      _element_width="initial", _element_custom_width=px(48), _padding=dims(13, 0),
                      _border_radius=dims(999), _flex_size="none", **grad(CYAN_GRAD[0], CYAN_GRAD[1], 135, prefix="_background"))
        info = col([heading(label, TURQ if dark else AZUL, typo("typography", 11, 800, lh=1.3, ls=2.2, transform="uppercase")),
                    body(f"<p>{desc}</p>", WHITE if dark else PROF, 15, weight=500, lh=1.5, m=14)], 4, "Texto")
        s = row([num, info], 18, f"Etapa {n}", flex_align_items="center", padding=dims(20, 24),
                padding_mobile=dims(18), border_radius=dims(18),
                box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 18, 40, -24, "rgba(11, 45, 74, 0.35)"),
                **(grad(PROF, NOITE, 135) if dark else {**solid(WHITE), **border(1, "#E3EBF1")}))
        return s

    def arrow():
        return container({"min_height": px(34), "width": px(48), "margin": dims(0, 0, 0, 24),
                          "css_classes": "lp-arrow lp-io", "_flex_size": "none"}, [], "Seta (desenha)")

    s1 = anim(step("01", "Sinais", "O que você observa na consulta de retorno."), "fadeInUp", 0)
    s2 = anim(step("02", "Avaliação", "O que checar, e em que ordem, para chegar à causa provável."), "fadeInUp", 150)
    s3 = anim(step("03", "Conduta", "Manter, recuar, recolar, fazer IPR ou replanejar, com os critérios de cada escolha.",
                   dark=True), "zoomIn", 450)
    right = col([body("<p>Cada intercorrência segue o mesmo raciocínio:</p>", INK, 14, weight=500), s1, arrow(), s2,
                 arrow(), s3], 6, "Método", **w(47, 100))
    top = row([col(left, 20, "Texto", **w(46)), right], 72, "Texto e método", **r("row", "column"),
              flex_align_items="center", flex_gap_tablet=gap(48))
    return section({
        "flex_gap": gap(80),
        "flex_gap_tablet": gap(64),
        **grad("#FBFAFC", "#EEF3F7", 180),
    }, [top, laptop()], "04 · Apresentação", "lp-apres")


PAGE_IMG = "https://placehold.co/1046x1482/F4F8FB/0B2D4A.png?text=Troque+pela+p%C3%A1gina+do+guia"


def laptop():
    """Notebook que abre com o scroll, com uma página do guia na tela (seção 04)."""
    css = open(os.path.join(HERE, "lp-laptop.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "lp-laptop.js"), encoding="utf-8").read().strip()
    code = setv(html("<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"),
                _title="Notebook · estilos e animação (não apagar)", _position="absolute",
                _element_width="initial", _element_custom_width=px(0))

    bar = row([
        row([container({"width": px(8), "min_height": px(8), "border_radius": dims(8), **solid(c), "_flex_size": "none"},
                       [], "Ponto") for c in ("#FF6B6B", "#FFC94D", "#3DDC84")], 5, "Botões da janela",
            flex_align_items="center", width=px(44), _flex_size="none"),
        heading("Guia Prático · Intercorrências com Alinhadores.pdf", "rgba(255, 255, 255, 0.85)",
                typo("typography", 11, 600, lh=1.3, size_m=8), align="center", _flex_size="shrink"),
        heading("p. 05", AZC, typo("typography", 11, 700, lh=1.3, size_m=8)),
    ], 12, "Barra do leitor de PDF", flex_align_items="center", flex_justify_content="space-between",
        padding=dims(9, 14), padding_mobile=dims(6, 10), **solid(PROF), _flex_size="none")
    page = cls(image(PAGE_IMG, "Página do guia: Intercorrência 01, Alinhador não encaixa de forma generalizada",
                     width=(100, "%"), image_box_shadow_box_shadow_type="yes",
                     image_box_shadow_box_shadow=shadow(0, 20, 40, -16, "rgba(11, 45, 74, 0.35)")),
               "lp-screen-page")
    setv(page, _element_width="initial", _element_custom_width=px(60, "%"),
         _element_custom_width_mobile=px(70, "%"), _flex_align_self="center", _margin=dims(18, 0, 0, 0),
         _margin_mobile=dims(10, 0, 0, 0), _title="Página do guia (tela)")
    content = col([page], 0, "Conteúdo da tela", flex_align_items="center", css_classes="lp-screen-content",
                  _flex_size="shrink")
    screen = col([bar, content], 0, "Tela", overflow="hidden", border_radius=dims(6),
                 **grad("#EEF3F7", "#DCE5EC", 180), css_classes="lp-screen")
    front = col([screen], 0, "Tampa · frente (tela)", padding=dims(14), padding_mobile=dims(7),
                border_radius=dims(18, 18, 0, 0), **grad("#1C2733", "#0B121A", 180),
                box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 0, 0, 1, "rgba(255, 255, 255, 0.08)"),
                css_classes="lp-lid-front")
    back = col([icon("fas fa-tooth", "rgba(255, 255, 255, 0.55)", 30, align="center")], 0, "Tampa · costas",
               flex_justify_content="center", flex_align_items="center", border_radius=dims(18, 18, 0, 0),
               **grad("#C9D2DB", "#8E9BA8", 180), css_classes="lp-lid-back")
    lid = container({"flex_direction": "column", "css_classes": "lp-lid"}, [front, back], "Tampa (abre no scroll)")
    notch = container({"width": px(16, "%"), "min_height": px(7), "border_radius": dims(0, 0, 8, 8),
                       **solid("#8E9BA8")}, [], "Entalhe")
    base = col([notch], 0, "Base", flex_align_items="center", min_height=px(20), min_height_mobile=px(12),
               border_radius=dims(2, 2, 16, 16), **grad("#E3E9EF", "#9AA7B4", 180), css_classes="lp-base",
               box_shadow_box_shadow_type="yes",
               box_shadow_box_shadow=shadow(0, 30, 50, -18, "rgba(11, 45, 74, 0.45)"))
    caption = body("<p>O guia abre como no seu computador, pronto para consultar na cadeira.</p>",
                   INK, 14, "center", weight=500)
    return col([code, lid, base, setv(caption, _margin=dims(18, 0, 0, 0))], 0, "Notebook (abre no scroll)",
               flex_align_items="center", content_width="boxed", boxed_width=px(920), css_classes="lp-laptop")


# ---------------------------------------------------------------------------
# 05 · Veja o guia por dentro (carrossel)
# ---------------------------------------------------------------------------

PAGES = [
    ("p.06", "Sinais, avaliação e conduta em uma página"),
    ("p.04", "A rotina de checagem para toda consulta de retorno"),
    ("p.07", "Sinais, avaliação e conduta em uma página"),
    ("p.12", "Sinais, avaliação e conduta em uma página"),
    ("p.22", "Referências em Vancouver, com DOI"),
]


def s05_por_dentro():
    head = col([
        eyebrow("Veja o guia por dentro", TURQ, center=True),
        h2('Veja como <span class="lp-hl">cada intercorrência</span> está organizada.', WHITE, 42, "center", t=36, m=28),
    ], 16, "Título", flex_align_items="center", content_width="boxed", boxed_width=px(720))
    anim(head, "fadeInUp")

    slides = []
    for code, cap in PAGES:
        img = image(f"https://placehold.co/696x984/F4F8FB/0B2D4A.png?text=Guia+{code}", f"Página {code} do guia: {cap}",
                    width=(100, "%"), link_to="file", open_lightbox="yes",
                    image_box_shadow_box_shadow_type="yes",
                    image_box_shadow_box_shadow=shadow(0, 30, 60, -20, "rgba(0, 0, 0, 0.6)"))
        cls(img, "lp-page-img")
        capt = cls(heading(cap, TXT, typo("typography", 14, 500, lh=1.45), align="center"), "lp-page-cap")
        slides.append(col([img, capt], 16, f"Página {code}", flex_align_items="center"))
    carousel = widget("nested-carousel", {
        "carousel_name": "Páginas do guia",
        "carousel_items": [{"slide_title": f"Página {c}", "_id": new_id()} for c, _ in PAGES],
        "slides_to_show": "5",
        "slides_to_show_tablet": "3",
        "slides_to_show_mobile": "1",
        "slides_to_scroll": "1",
        "autoplay": "yes",
        "autoplay_speed": 4000,
        "pause_on_hover": "yes",
        "pause_on_interaction": "yes",
        "infinite": "yes",
        "speed": 600,
        "arrows": "yes",
        "pagination": "bullets",
        "image_spacing_custom": px(20),
        "image_spacing_custom_mobile": px(12),
        "arrows_size": px(18),
        "arrows_color": WHITE,
        "arrows_hover_color": TURQ,
        "dots_color_inactive": "rgba(126, 211, 230, 0.3)",
        "dots_color": TURQ,
        "_css_classes": "lp-pages",
        "_element_width": "initial",
        "_element_custom_width": px(100, "%"),
        "_padding": dims(30, 60, 60, 60),
        "_padding_mobile": dims(20, 30, 50, 30),
    })
    carousel["elements"] = slides
    for s in slides:
        s["isInner"] = True
    hint = icon_list([{"text": "Toque em uma página para ampliar", "icon": "fas fa-search-plus"}],
                     "rgba(126, 211, 230, 0.8)", typo("icon_typography", 13, 500, lh=1.4), icon_color=TURQ,
                     icon_size=14, icon_align="center")
    return section({
        "content_width": "full",
        "_element_id": "por-dentro",
        "flex_align_items": "center",
        "flex_gap": gap(48),
        "padding": dims(110, 24),
        **grad(MED, NOITE, 0, 0, 70, kind="radial", position="center center"),
        "custom_css": "selector .lp-pages .swiper-pagination-bullet-active{width:28px;border-radius:4px}",
    }, [head, container({"content_width": "boxed", "boxed_width": px(1480), "flex_direction": "column"}, [carousel], "Carrossel"),
        hint], "05 · Veja o guia por dentro (#por-dentro)", "lp-inside lp-orbits", boxed=False)


# ---------------------------------------------------------------------------
# 06 · Agenda (o que tem dentro)
# ---------------------------------------------------------------------------

CATEGORIES = [("Encaixe e tracking", 1), ("Attachment e IPR", 2), ("Paciente e uso", 3), ("Movimento e mecânica", 4)]
AGENDA = [
    ("08:00", "Alinhador que não encaixa de forma generalizada", "Manter a etapa, recuar ou reescanear?", 1),
    ("08:30", "Dente que não acompanha a sequência", "Attachment, contato, espaço ou staging?", 1),
    ("09:00", "Attachment descolado", "Como recolar, e o que investigar quando descola de novo", 2),
    ("09:30", "Attachment desgastado ou mal formado", "Como inspecionar e quando refazer", 2),
    ("10:00", "Tempo de uso insuficiente", "Como avaliar a adesão sem culpar o paciente", 3),
    ("10:30", "Alinhador perdido ou quebrado", "Voltar ao anterior ou avançar?", 3),
    ("11:00", "Dor excessiva ou lesão de mucosa", "Resposta esperada ou sinal de alerta?", 3),
    ("11:30", "Rotação não expressa", "Retenção, espaço, staging ou recurso auxiliar?", 4),
    ("12:00", "Extrusão não expressa", "É posição ou é forma?", 4),
    ("12:30", "Mordida aberta posterior", "Monitorar ou replanejar?", 4),
    ("13:00", "Espaços indesejados", "O espaço é o problema ou o sintoma?", 1),
    ("13:30", "Contatos apertados ou IPR inadequado", "Quanto, onde e quando desgastar, e quando não", 2),
    ("14:00", "Elásticos sem a resposta esperada", "É uso, mecânica ou diagnóstico?", 4),
    ("14:30", "Efeito montanha-russa em extrações", "Quais sinais olhar e por que não usar elástico anterior por reflexo", 4),
    ("15:00", "Fim da sequência sem o resultado planejado", "Como listar o que não expressou e refinar com objetivos claros", 1),
]


def s06_agenda():
    count = cls(heading("01", TURQ, typo("typography", 44, 800, lh=1, size_m=36)), "lp-agenda-count")
    bar = container({"min_height": px(6), "height": px(6), "width": px(100, "%"), "border_radius": dims(6),
                     **solid("rgba(255, 255, 255, 0.12)"), "css_classes": "lp-agenda-bar"}, [], "Barra de progresso")
    counter_box = row([setv(count, _flex_size="none"),
                       col([heading("de 15 retornos", WHITE, typo("typography", 15, 600, lh=1.4)), bar], 10, "Progresso",
                           _flex_size="shrink")], 18, "Contador", flex_align_items="center", padding=dims(20, 22),
                      **grad(PROF, NOITE, 135), border_radius=dims(18))
    legend = cls(icon_list([{"text": n} for n, _ in CATEGORIES], INK, typo("icon_typography", 13, 500, lh=1.4),
                           icon_value="fas fa-circle", icon_size=9, space=8, icon_vertical_offset=px(0),
                           icon_self_vertical_align="center"), "lp-legend")
    side_items = [
        eyebrow("O que tem dentro", AZUL),
        h2('As <span class="lp-hl">15 situações</span> que mais travam a consulta de retorno.', PROF, 38, t=34, m=28),
        body("<p>Imagine a sua agenda de amanhã. Cada horário é uma intercorrência do guia, com a pergunta que você "
             "vai precisar responder na cadeira.</p>", INK, 16),
        counter_box, legend, btn_primary("Quero o guia por R$ 27", "#oferta"),
    ]
    for i, el in enumerate(side_items):
        anim(el, "fadeInUp", i * 80)
    side = col(side_items, 22, "Coluna fixa (sticky)", width=px(34, "%"), width_tablet=px(100, "%"),
               sticky="top", sticky_on=["desktop"], sticky_offset=96, sticky_parent="yes")

    # topo da agenda
    tab = lambda t, on: heading(t, NOITE if on else AZC, typo("typography", 12, 700, lh=1.3), _padding=dims(7, 16),
                                _border_radius=dims(999), **solid(TURQ if on else GLASS, "_background"))
    top = row([
        row([icon("far fa-calendar-alt", TURQ, 18, view="framed", secondary="transparent", padding=11, library="fa-regular",
                  border_width=dims(1), _flex_size="none"),
             col([heading("Agenda · Consultório", WHITE, typo("typography", 17, 700, lh=1.3, size_m=15)),
                  heading("Terça-feira · dia de retornos", AZC, typo("typography", 13, 500, lh=1.4))], 2, "Títulos")],
            14, "Título", flex_align_items="center", _flex_size="shrink"),
        row([tab("Hoje", True), tab("Semana", False)], 6, "Abas", flex_align_items="center", _flex_size="none",
            width=px(170), flex_justify_content="flex-end",
            hide_mobile="hidden-mobile"),
    ], 16, "Topo da agenda", flex_align_items="center", flex_justify_content="space-between",
        padding=dims(22, 28), padding_mobile=dims(18, 18), **grad(PROF, NOITE, 135))

    now = row([heading("agora", NOITE, typo("typography", 10, 800, lh=1.2, ls=2, transform="uppercase"),
                        _padding=dims(4, 10), _border_radius=dims(999), **solid(TURQ, "_background"),
                        _flex_size="none")], 0, "Linha AGORA (desce com o scroll)", flex_align_items="center",
              css_classes="lp-now", min_height=px(32))
    slots = [now]
    for i, (hour, title, question, cat) in enumerate(AGENDA, 1):
        n = f"{i:02d}"
        meta = row([cls(heading(f"Paciente {n} · retorno", MUTED, typo("typography", 10, 600, lh=1.3, ls=1.4,
                                                                        transform="uppercase")), "lp-slot-meta"),
                    cls(heading("na cadeira", TURQ, typo("typography", 9, 800, lh=1.3, ls=1.2, transform="uppercase"),
                                _padding=dims(3, 8), _border_radius=dims(999),
                                **solid("rgba(0, 194, 199, 0.15)", "_background")), "lp-slot-chip")],
                   8, "Paciente", flex_align_items="center")
        info = col([meta,
                    cls(heading(title, PROF, typo("typography", 16, 700, lh=1.35, size_m=15), tag="h3"), "lp-slot-title"),
                    cls(body(f"<p>{question}</p>", INK, 14, lh=1.5, m=13), "lp-slot-q")], 4, "Consulta", _flex_size="shrink")
        done = cls(heading("✓ conduta definida", AZUL, typo("typography", 11, 700, lh=1.3), _padding=dims(6, 12),
                           _border_radius=dims(999), **solid("#E6F8F9", "_background"), _flex_size="none"),
                   "lp-slot-done")
        num = cls(heading(n, "#C7D3DD", typo("typography", 26, 800, lh=1, size_m=22), _flex_size="none"), "lp-slot-num")
        card = row([info, done, num], 16, "Card", flex_align_items="center", _flex_size="shrink",
                   padding=dims(18, 22, 18, 40), padding_mobile=dims(16, 14, 16, 32), **solid(WHITE),
                   **border(1, "#E6EEF4", 16), css_classes=f"lp-slot-card lp-cat-{cat}")
        state = " is-done" if i < 3 else (" is-active" if i == 3 else "")
        slots.append(row([cls(heading(hour, MUTED, typo("typography", 13, 700, lh=1.3, size_m=11)), "lp-slot-time"), card], 18, f"{hour} · Paciente {n}", flex_align_items="flex-start",
                         flex_gap_mobile=gap(10), padding=dims(6, 0), css_classes="lp-slot" + state))
        setv(slots[-1]["elements"][0], _element_width="initial", _element_custom_width=px(52),
             _element_custom_width_mobile=px(38), _flex_size="none", _margin=dims(20, 0, 0, 0))
    board_slots = col(slots, 2, "Horários", padding=dims(16, 28, 28, 24), padding_mobile=dims(12, 12, 20, 10),
                      css_classes="lp-slots")
    board = col([top, board_slots], 0, "Agenda", width=px(61, "%"), **solid(WHITE), **border(1, "#E3EBF1", 24),
                overflow="hidden", box_shadow_box_shadow_type="yes",
                box_shadow_box_shadow=shadow(0, 40, 80, -40, "rgba(11, 45, 74, 0.35)"), width_tablet=px(100, "%"))
    return section({
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(56),
        **solid(LIGHT),
    }, [side, anim(board, "fadeInUp", 150)], "06 · O que tem dentro (agenda)", "lp-agenda lp-orbits")


# ---------------------------------------------------------------------------
# 07 · Para quem é: teste de compatibilidade
# ---------------------------------------------------------------------------

YES = [
    "Já trata com alinhadores e quer mais segurança nas consultas de retorno.",
    "Já ficou em dúvida entre manter a etapa, recuar um alinhador ou pedir refinamento.",
    "Quer um material de consulta rápida para abrir na cadeira, no celular ou no tablet.",
    "Prefere decidir com critério clínico em vez de depender só do relatório do laboratório.",
    "Quer explicar ao paciente, com segurança, por que o tratamento atrasou e o que vai mudar.",
    "Quer reduzir refinamentos e consultas extras causados por condutas no improviso.",
]
NO = [
    "Procura um curso completo de planejamento digital, do zero.",
    "Quer um protocolo pronto que dispense o exame clínico.",
    "Espera que um material substitua o diagnóstico individual e o seu julgamento profissional.",
]


def s07_para_quem():
    head = anim(col([
        eyebrow("Para quem é", TURQ, center=True),
        h2("Este guia é para você se:", WHITE, 40, "center", t=34, m=27),
        body("<p>Veja quantos interruptores combinam com a sua rotina.</p>", TXT, 16, "center"),
    ], 14, "Título", flex_align_items="center"), "fadeInUp")

    photo = col([btn_primary("Quero o guia por R$ 27", "#oferta")], 0, "Foto da autora", **w(34, 100),
                min_height=px(640), min_height_tablet=px(460), min_height_mobile=px(420),
                flex_justify_content="flex-end", flex_align_items="center", padding=dims(28),
                background_background="classic",
                background_image={"url": ASSET + "autora.webp", "id": "", "size": "", "alt": "Dra. Joyce Duarte",
                                  "source": "library"},
                background_position="top center", background_size="cover", background_repeat="no-repeat",
                **grad("rgba(1, 19, 36, 0)", "rgba(1, 19, 36, 0.85)", 180, 55, 100, prefix="background_overlay"),
                border_radius=dims(24), overflow="hidden")
    anim(photo, "fadeInLeft")

    def switch(t, i):
        return anim(row([body(f"<p>{t}</p>", WHITE, 15, weight=500, lh=1.5, m=14)], 0, f"Interruptor {i}",
                        flex_align_items="center", min_height=px(64), padding=dims(14, 24),
                        padding_mobile=dims(14, 16), **solid("rgba(0, 194, 199, 0.07)"),
                        **border(1, "rgba(126, 211, 230, 0.16)", 16), css_classes="lp-switch lp-switch--yes"),
                    "fadeInUp", i * 60)

    meter = row([
        container({"width": px(64), "min_height": px(64), "_flex_size": "none", "css_classes": "lp-meter-ring"}, [],
                  "Anel do medidor"),
        col([cls(heading("0/6", WHITE, typo("typography", 24, 800, lh=1.1)), "lp-meter-num"),
             cls(heading("✓ Compatibilidade total", TURQ, typo("typography", 12, 800, lh=1.3, ls=1.5, transform="uppercase")),
                 "lp-meter-full")], 4, "Resultado"),
    ], 18, "Medidor", flex_align_items="center", padding=dims(16, 24), border_radius=dims(16),
        **solid("rgba(255, 255, 255, 0.04)"), css_classes="lp-meter", margin=dims(4, 0, 0, 0))

    def no_row(t, i):
        return anim(row([cls(body(f"<p>{t}</p>", INK, 15, weight=500, lh=1.5, m=14), "lp-strike lp-io")], 0,
                        f"Não é {i}", flex_align_items="center", min_height=px(64), padding=dims(14, 24),
                        padding_mobile=dims(14, 16), **solid("#F7F9FB"), border_radius=dims(16),
                        css_classes="lp-switch lp-switch--no"), "fadeInUp", i * 60)

    switches = col([switch(t, i) for i, t in enumerate(YES, 1)] + [meter], 10, "Para você", css_classes="lp-switches")
    nots = col([heading("Não é para você se:", WHITE, typo("typography", 22, 700, lh=1.3, size_m=19), tag="h3")]
               + [no_row(t, i) for i, t in enumerate(NO, 1)], 10, "Não é para você", margin=dims(26, 0, 0, 0))
    right = col([switches, nots], 0, "Teste", **w(62, 100))
    grid = row([photo, right], 32, "Conteúdo", **r("row", "column"), flex_align_items="stretch")
    return section({
        "flex_gap": gap(56),
        **grad("#2F7680", "#04162A", 0, 0, 62, kind="radial", position="top right"),
        "overflow": "hidden",
    }, [head, grid], "07 · Para quem é (teste de compatibilidade)", "lp-fit")


# ---------------------------------------------------------------------------
# 08 · Bônus e oferta
# ---------------------------------------------------------------------------

def s08_oferta():
    chip = heading("Bônus exclusivo", NOITE, typo("typography", 10, 800, lh=1.3, ls=1.5, transform="uppercase"),
                   _element_width="auto", _flex_align_self="flex-start", _padding=dims(6, 14), _border_radius=dims(999), **solid(TURQ, "_background"))
    play = cls(icon("fas fa-play", TURQ, 24, view="stacked", secondary=NOITE, padding=26, align="center"), "lp-play")
    setv(play, primary_color=TURQ, secondary_color=NOITE)
    cover = col([chip, play, heading("Capa da aula (bônus) · troque pela arte final", "rgba(195, 214, 227, 0.6)",
                                     typo("typography", 11, 500, lh=1.3))], 0, "Capa da aula",
                width=px(500), width_tablet=px(100, "%"), _flex_size="none", min_height=px(300),
                min_height_mobile=px(220), flex_justify_content="space-between", padding=dims(20),
                **grad(MED, NOITE, 135), border_radius=dims(18), overflow="hidden")
    info_items = [
        eyebrow("Bônus exclusivo", TURQ),
        h2("2 aulas gravadas: como aplicar o guia na sua rotina clínica", WHITE, 28, t=26, m=22, lh=1.3, tag="h3"),
        body("<p>Da avaliação na cadeira à decisão de conduta. Assista quando quiser e reveja sempre que precisar.</p>",
             TXT, 16),
        heading("O guia diz o quê. As aulas mostram como.", TURQ, typo("typography", 20, 700, lh=1.4, size_m=17)),
    ]
    for i, el in enumerate(info_items):
        anim(el, "fadeInUp", i * 80)
    bonus = row([cover, col(info_items, 14, "Texto", _flex_size="shrink")], 40, "Card do bônus", **r("row", "column"),
                flex_align_items="center", flex_align_items_tablet="stretch", padding=dims(32),
                padding_mobile=dims(18), **solid("rgba(255, 255, 255, 0.04)"), **border(1, LINE, 24))
    anim(bonus, "fadeInUp")

    price = row([
        heading("por", PROF, typo("typography", 22, 600, lh=1.2), _margin=dims(0, 0, 14, 0)),
        counter(97, 27, "R$\u00a0", AZUL, typo("typography_number", 88, 800, lh=1, size_m=64), duration=1400),
        heading("· pagamento único", MUTED, typo("typography", 15, 500, lh=1.3), _margin=dims(0, 0, 14, 0)),
    ], 12, "Preço", flex_align_items="flex-end", flex_wrap="wrap")
    buy = [
        eyebrow("Tudo o que você leva hoje", AZUL),
        icon_list(["Guia Prático em PDF: as 15 intercorrências em sinais, avaliação e conduta",
                   "Bônus: 2 aulas gravadas de aplicação clínica"], PROF,
                  typo("icon_typography", 16, 600, lh=1.5, size_m=15), icon_value="fas fa-check-square",
                  icon_color=TURQ, icon_size=18, space=14),
        cls(heading("De R$ 97,00", MUTED, typo("typography", 20, 500, lh=1.3), _margin=dims(10, 0, 0, 0)), "lp-old lp-io"),
        price,
        body("<p>Menos do que você cobra por uma única consulta de retorno.</p>", INK, 16),
        btn_primary("Quero o guia + as 2 aulas por R$ 27", CHECKOUT, full=True),
        icon_list([{"text": "Compra segura · Material 100% digital · Pagamento único · Garantia de 7 dias",
                    "icon": "fas fa-lock"}], MUTED, typo("icon_typography", 12, 500, lh=1.5), icon_color=MUTED,
                  icon_size=12),
    ]
    offer = row([
        col([anim(image(ASSET + "oferta-mockup.webp", "Guia Intercorrências com Alinhadores no tablet, o ebook "
                        "impresso, páginas soltas e o selo de +2 aulas bônus", width=(100, "%")), "zoomIn")],
            0, "Mockup guia + aula", **w(44, 100), flex_justify_content="center", flex_align_items="center",
            padding=dims(40, 24), **grad("#F4F8FB", "#E1E9F0", 160)),
        col(buy, 16, "Compra", **w(56, 100), padding=dims(52, 56), padding_mobile=dims(32, 22),
            flex_justify_content="center"),
    ], 0, "Caixa da oferta", **r("row", "column"), flex_align_items="stretch", **solid(WHITE), border_radius=dims(28),
        overflow="hidden", box_shadow_box_shadow_type="yes",
        box_shadow_box_shadow=shadow(0, 50, 100, -40, "rgba(0, 194, 199, 0.35)"))
    anim(offer, "fadeInUp")

    recv = []
    for i, t in enumerate([
        "Finalize o pagamento com Pix ou cartão",
        "Receba o acesso no e-mail à plataforma assim que o pagamento for confirmado",
        "Assista às aulas e faça download do guia completo",
        "Abra o guia na próxima consulta, no celular, no tablet ou no computador",
    ], 1):
        recv.append(anim(col([heading(f"{i:02d}", TURQ, typo("typography", 26, 800, lh=1.2)),
                              body(f"<p>{t}</p>", TXT, 15, lh=1.55)], 14, f"Passo {i}", padding=dims(26, 25),
                             **solid("rgba(255, 255, 255, 0.04)"), **border(1, LINE, 18)), "fadeInUp", (i - 1) * 120))
    steps = container({
        "container_type": "grid",
        "grid_columns_grid": px(4, "fr"),
        "grid_columns_grid_tablet": px(2, "fr"),
        "grid_columns_grid_mobile": px(1, "fr"),
        "grid_rows_grid": px(1, "fr"),
        "grid_rows_grid_tablet": px(2, "fr"),
        "grid_rows_grid_mobile": px(4, "fr"),
        "grid_gaps": gap(20),
        "grid_auto_flow": "row",
        "css_classes": "lp-steps lp-io",
        "margin": dims(14, 0, 0, 0),
    }, recv, "Passos")
    how = col([heading("Como você recebe:", WHITE, typo("typography", 24, 700, lh=1.3, size_m=20), tag="h3"), steps],
              18, "Como você recebe")
    return section({
        "_element_id": "oferta",
        "flex_gap": gap(72),
        "flex_gap_mobile": gap(48),
        **grad(NOITE, "#0A3756", 180),
        "overflow": "hidden",
    }, [bonus, offer, how], "08 · Bônus e oferta (#oferta)", "lp-offer lp-orbits")


# ---------------------------------------------------------------------------
# 09 · Garantia, autora e FAQ
# ---------------------------------------------------------------------------

FAQ = [
    ("Já tenho o planejamento do laboratório. Por que preciso do guia?",
     "O planejamento mostra o caminho ideal. O guia é para quando o caso sai dele: ajuda você a identificar a "
     "causa provável da intercorrência e a decidir a conduta na própria consulta."),
    ("Serve para qualquer marca de alinhador?",
     "Sim. As condutas partem de sinais clínicos e de princípios de biomecânica, não de um sistema específico. "
     "Você aplica com o alinhador que já usa no consultório."),
    ("Serve para quem está começando com alinhadores?",
     "Serve para quem já trata ou está começando a tratar com alinhadores. O guia não ensina planejamento do zero: "
     "ele organiza a tomada de decisão nas consultas de retorno."),
    ("Em que formato recebo o guia?",
     "Em PDF, otimizado para consulta rápida no celular, no tablet ou no computador. As aulas bônus ficam na "
     "plataforma de acesso."),
    ("Como funcionam as 2 aulas bônus?",
     "São aulas gravadas que mostram como aplicar o guia na rotina clínica, da avaliação na cadeira à decisão de "
     "conduta. Assista quando quiser e reveja sempre que precisar."),
    ("O pagamento é único ou é assinatura?",
     "É um pagamento único de R$ 27, no Pix ou no cartão. Não há mensalidade."),
    ("Como funciona a garantia?",
     "Você tem 7 dias para usar o guia e assistir às aulas. Se não fizer sentido para a sua prática, peça o "
     "reembolso e recebe 100% do valor de volta, sem perguntas."),
    ("Como recebo o acesso?",
     "Assim que o pagamento é confirmado, você recebe no e-mail o acesso à plataforma, com o download do guia e as "
     "aulas."),
]


def s09_confianca():
    seal = col([heading("7", TURQ, typo("typography", 64, 800, lh=1), align="center"),
                heading("dias de garantia", AZC, typo("typography", 9, 700, lh=1.3, ls=2, transform="uppercase"),
                        align="center")], 4, "Selo 7 dias", width=px(180), min_height=px(180), _flex_size="none",
               flex_justify_content="center", flex_align_items="center", **grad(PROF, NOITE, 135),
               border_radius=dims(999), css_classes="lp-seal", width_mobile=px(140), min_height_mobile=px(140))
    guarantee = row([anim(seal, "zoomIn"),
                     col([h2("Garantia de 7 dias.", PROF, 32, t=30, m=25, lh=1.2, tag="h3"),
                          body("<p>Baixe o guia, assista às aulas e use na sua próxima consulta de retorno. Se não fizer "
                               "sentido para a sua prática, peça o reembolso em até 7 dias e você recebe 100% do valor "
                               "de volta. Sem perguntas.</p>", INK, 16)], 12, "Texto", _flex_size="shrink")],
                    48, "Garantia", **r("row", None, "column"), flex_align_items="center", padding=dims(44, 48),
                    padding_mobile=dims(32, 22), flex_gap_mobile=gap(24), **solid(WHITE), border_radius=dims(24),
                    box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 30, 60, -30, "rgba(11, 45, 74, 0.25)"))
    anim(guarantee, "fadeInUp")

    tag = anim(col([heading("Dra. Joyce Duarte", WHITE, typo("typography", 17, 700, lh=1.3)),
                    heading("Ortodontista · Especialista em alinhadores", AZC, typo("typography", 12, 500, lh=1.4))], 4,
                   "Etiqueta do nome", padding=dims(15, 19), **solid(PROF), border_radius=dims(14),
                   box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 20, 40, -16, "rgba(1, 19, 36, 0.6)"),
                   margin=dims(-70, 0, 0, 0), margin_mobile=dims(-60, 0, 0, 0), _flex_align_self="flex-end",
                   z_index=2), "fadeInUp", 300)
    photo = col([image(ASSET + "autora.webp", "Dra. Joyce Duarte, autora do guia", width=(100, "%"), height=480,
                       radius=24, position="top center", height_mobile=px(400)), tag], 0, "Foto da autora",
                width=px(400), width_mobile=px(100, "%"), _flex_size="none", css_classes="lp-author-photo",
                margin=dims(20))
    author = row([anim(photo, "fadeInUp"),
                  col([eyebrow("Quem escreveu", AZUL),
                       h2("Dra. Joyce Duarte", PROF, 40, t=36, m=30),
                       body("<p>Ortodontista, CRO-[UF] [número]. [Formação e especialização.] "
                            "[Tempo de atuação com alinhadores.]</p>", INK, 17)], 14, "Texto", _flex_size="shrink")],
                 72, "Quem escreveu", **r("row", "column"), flex_align_items="center", flex_gap_tablet=gap(40))

    acc = widget("nested-accordion", {
        "items": [{"item_title": q, "_id": new_id()} for q, _ in FAQ],
        "title_tag": "h3",
        "default_state": "expanded",
        "max_items_expended": "one",
        "faq_schema": "yes",
        "n_accordion_animation_duration": {"unit": "ms", "size": 250, "sizes": []},
        "accordion_item_title_position_horizontal": "stretch",
        "accordion_item_title_icon_position": "end",
        "accordion_item_title_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "accordion_item_title_icon_active": {"value": "fas fa-plus", "library": "fa-solid"},
        "accordion_item_title_space_between": px(12),
        "accordion_item_title_distance_from_content": px(0),
        "accordion_background_normal_background": "classic",
        "accordion_background_normal_color": WHITE,
        "accordion_background_hover_background": "classic",
        "accordion_background_hover_color": WHITE,
        "accordion_background_active_background": "classic",
        "accordion_background_active_color": WHITE,
        "accordion_padding": dims(22, 26),
        "accordion_padding_mobile": dims(18, 18),
        "accordion_border_radius": dims(18),
        "accordion_border_normal_border": "solid",
        "accordion_border_normal_width": dims(1),
        "accordion_border_normal_color": "#E3EBF1",
        "accordion_border_hover_border": "solid",
        "accordion_border_hover_width": dims(1),
        "accordion_border_hover_color": "#BFEFF0",
        "accordion_border_active_border": "solid",
        "accordion_border_active_width": dims(1),
        "accordion_border_active_color": TURQ,
        "content_border_border": "none",
        **typo("title_typography", 16, 700, lh=1.45, size_m=15),
        "normal_title_color": PROF,
        "hover_title_color": AZUL,
        "active_title_color": PROF,
        "normal_icon_color": PROF,
        "hover_icon_color": AZUL,
        "active_icon_color": WHITE,
        "icon_size": px(12),
        "icon_spacing": px(16),
        "_css_classes": "lp-faq",
    })
    acc["elements"] = [col([body(f"<p>{a}</p>", INK, 15, lh=1.6, m=14)], 0, f"Resposta {i}",
                           padding=dims(0, 26, 24, 26), padding_mobile=dims(0, 18, 18, 18))
                       for i, (_, a) in enumerate(FAQ, 1)]
    faq = row([anim(col([eyebrow("FAQ", AZUL), h2("Perguntas frequentes", PROF, 40, t=34, m=28)], 14, "Título",
                        width=px(300), width_tablet=px(100, "%"), _flex_size="none"), "fadeInUp"),
               anim(col([acc], 0, "Perguntas", _flex_size="shrink"), "fadeInUp", 150)],
              80, "FAQ", **r("row", "column"), flex_align_items="flex-start", flex_gap_tablet=gap(32))
    return section({"flex_gap": gap(96), "flex_gap_mobile": gap(72), **solid(LIGHT)},
                   [guarantee, author, faq], "09 · Garantia, autora e FAQ", "lp-trust")


# ---------------------------------------------------------------------------
# 10 · Fechamento
# ---------------------------------------------------------------------------

def s10_fechamento():
    items = [
        cls(h2('A próxima intercorrência já está <span class="lp-grad">na sua agenda</span>.', WHITE, 48, "center",
               t=40, m=30), "lp-sweep lp-io"),
        body("<p>A diferença é como você chega nessa consulta: com critério ou com improviso. Por R$ 27, você leva o "
             "guia com as 15 situações e as 2 aulas de aplicação.</p>", TXT, 17, "center"),
        setv(btn_primary("Quero chegar com critério na próxima consulta", CHECKOUT), align="center",
             _margin=dims(18, 0, 0, 0)),
        icon_list([{"text": "R$ 27 · Pagamento único · Acesso imediato · Garantia de 7 dias", "icon": "fas fa-lock"}],
                  "rgba(126, 211, 230, 0.75)", typo("icon_typography", 13, 500, lh=1.4), icon_color=AZC, icon_size=12,
                  icon_align="center"),
    ]
    for i, el in enumerate(items):
        anim(el, "fadeInUp", i * 100)
    content = col(items, 18, "Conteúdo", content_width="boxed", boxed_width=px(820), flex_align_items="center")
    return section({
        "padding": dims(140, 24),
        "flex_align_items": "center",
        **grad("#0C3555", NOITE, 180),
    }, [orbits_glow("50%", "62%", 620), content], "10 · Fechamento", "lp-close lp-orbits")


# ---------------------------------------------------------------------------
# 11 · Rodapé + barra fixa do celular
# ---------------------------------------------------------------------------

def s11_rodape():
    info = col([
        heading("Guia Prático: Intercorrências com Alinhadores", WHITE, typo("typography", 17, 700, lh=1.4)),
        body("<p>Produto 100% digital. Acesso individual e intransferível.</p>", TXT, 14),
        body("<p>Material de apoio à decisão clínica, destinado a cirurgiões-dentistas habilitados. Não substitui o "
             "julgamento profissional individualizado. As condutas dependem do diagnóstico de cada caso.</p>",
             "rgba(195, 214, 227, 0.6)", 12, lh=1.65, m=12),
    ], 8, "Texto legal", width=px(640), width_tablet=px(60, "%"), width_mobile=px(100, "%"))
    top = row([logo(), info], 48, "Topo", **r("row", None, "column"), flex_justify_content="space-between",
              flex_align_items="flex-start")
    sep = container({"min_height": px(1), "height": px(1), **solid(LINE)}, [], "Divisória")
    links = icon_list([{"text": "Termos de uso", "url": "#", "icon": ""},
                       {"text": "Política de privacidade", "url": "#", "icon": ""},
                       {"text": "Contato", "url": "#", "icon": ""}], "rgba(195, 214, 227, 0.75)",
                      typo("icon_typography", 13, 500, lh=1.4), inline=True, space=28, indent=0)
    bottom = row([links, heading("© 2026", "rgba(195, 214, 227, 0.75)", typo("typography", 13, 500, lh=1.4))], 24,
                 "Links", flex_justify_content="space-between", flex_align_items="center", flex_wrap="wrap")
    return section({"padding": dims(64, 24, 40, 24), "padding_mobile": dims(48, 16, 110, 16), "flex_gap": gap(32),
                    **solid("#021325"), "html_tag": "footer"}, [top, sep, bottom], "11 · Rodapé", "lp-footer")


def mobile_bar():
    return container({
        "flex_direction": "row",
        "flex_justify_content": "space-between",
        "flex_align_items": "center",
        "flex_gap": gap(12),
        "padding": dims(8, 8, 8, 20),
        **solid("rgba(1, 19, 36, 0.94)"),
        **border(1, "rgba(0, 194, 199, 0.4)", 999),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": shadow(0, 16, 40, -10, "rgba(0, 0, 0, 0.6)"),
        "css_classes": "lp lp-mbar",
        "hide_desktop": "hidden-desktop",
        "hide_tablet": "hidden-tablet",
    }, [heading("R$ 27", WHITE, typo("typography", 20, 800, lh=1.1)),
        setv(btn_primary("Quero o guia", "#oferta", small=True), _flex_size="none")],
        "Barra fixa no celular (aparece depois do hero)", inner=False)


HUG = ("heading", "button", "icon", "counter")


def fix_rows(el):
    """No Elementor, filhos de uma linha têm largura base de 100%. Widgets curtos ficam com
    largura automática e sem encolher; textos longos encolhem para caber no espaço que sobra."""
    s = el["settings"]
    if el["elType"] == "container" and s.get("flex_direction") == "row" and len(el["elements"]) > 1:
        for ch in el["elements"]:
            cs = ch["settings"]
            if ch["elType"] != "widget":
                continue
            if "_element_width" in cs:
                cs.setdefault("_flex_size", "none")
            elif ch["widgetType"] in HUG and cs.get("_flex_size") in (None, "none"):
                cs["_element_width"] = "auto"
                cs["_flex_size"] = "none"
            elif "_flex_size" not in cs:
                cs["_flex_size"] = "shrink"
    # O controle de largura do container tem padrão 100% no celular: sem width_mobile, uma largura fixa
    # (bolinhas da janela, anel do medidor, setas, selos) vira 100% no celular.
    if el["elType"] == "container" and s.get("width") and "width_mobile" not in s:
        s["width_mobile"] = dict(s.get("width_tablet") or s["width"])
    for ch in el["elements"]:
        fix_rows(ch)
    return el


def build():
    content = [
        s00_topbar(),
        s01_hero(),
        s02_ribbons(),
        s03_dor(),
        s03b_impact(),
        s03c_conseq(),
        s04_apresentacao(),
        s05_por_dentro(),
        s06_agenda(),
        s07_para_quem(),
        s08_oferta(),
        s09_confianca(),
        s10_fechamento(),
        s11_rodape(),
        mobile_bar(),
    ]
    content = [fix_rows(c) for c in content]
    return {
        "content": content,
        "page_settings": {
            "template": "elementor_canvas",
            "hide_title": "yes",
            "background_background": "classic",
            "background_color": NOITE,
        },
        "version": "0.4",
        "title": "LP · Guia Prático Intercorrências com Alinhadores",
        "type": "page",
    }


def main():
    data = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
