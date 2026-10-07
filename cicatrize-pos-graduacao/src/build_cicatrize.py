#!/usr/bin/env python3
"""Gera o JSON do Elementor da página de vendas "Pós-graduação em Tratamento de Feridas e Podiatria
- Método Cicatrize 3X" (página inteira, só com containers e widgets gratuitos do Elementor).

Fonte do design: Figma eNqgf5G4SY4L10nUBIprMO, frame 1:2 ("landing page cicatrize": hero, paradoxo e
"2 em 1"). As demais dobras seguem a copy do arquivo "Página de Vendas.docx".
Paleta: #0F4F5C #3B5C66 #CF8A86 #FFFFFF. Verde só nos botões de ação. Fonte: Lato.
CSS e JS (cz-page.css / cz-page.js) vão embutidos no widget HTML do topo da página.
Saída: ../cicatrize-pos-elementor.json

Uso:  python3 build_cicatrize.py
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "cicatrize-pos-elementor.json")
OUT_ASSETS = os.path.join(HERE, "..", "estilos-animacoes-elementor.json")
CSS_FILE = os.path.join(HERE, "cz-page.css")
JS_FILE = os.path.join(HERE, "cz-page.js")

# ---------------------------------------------------------------------------
# Identidade visual
# ---------------------------------------------------------------------------
TEAL = "#0F4F5C"
TEAL_DEEP = "#0B3C46"   # mesmo verde-petróleo, mais fechado (só para profundidade dos fundos escuros)
SLATE = "#3B5C66"
ROSE = "#CF8A86"
WHITE = "#FFFFFF"
MIST = "#F3F7F7"        # #0F4F5C a 5% sobre branco (fundos claros alternados)
GREEN = "#1FBF5C"       # só botões de ação
WHITE_80 = "rgba(255, 255, 255, 0.82)"
WHITE_60 = "rgba(255, 255, 255, 0.62)"

LATO = "Lato"
SCRIPT = "Caveat"       # só na assinatura

# ---------------------------------------------------------------------------
# Links (CONFERIR antes de publicar)
# ---------------------------------------------------------------------------
OFERTA = "#oferta"                                           # CTAs do meio da página levam à oferta
CHECKOUT = "https://SUBSTITUIR-LINK-DO-CHECKOUT"             # botões da oferta
WHATSAPP = "https://wa.me/55SUBSTITUIR-NUMERO"               # atendimento
BONUS_END = "2026-10-27T23:59:00-03:00"                      # fim dos bônus da Aula Magna (27/10, 23h59)
VAGAS_PERCENT = 30                                            # barra "vagas preenchidas"

CTA_MAIN = "QUERO MINHA VAGA DE MEMBRO FUNDADOR"
CTA_OFFER = "QUERO SER MEMBRO FUNDADOR"

# ---------------------------------------------------------------------------
# Helpers (mesmo padrão dos outros projetos do repositório)
# ---------------------------------------------------------------------------
_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"cicatrize-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
            "isLinked": top == right == bottom == left}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def typo(prefix, size, weight, lh=None, ls=None, transform=None, style=None, family=LATO,
         size_t=None, size_m=None, lh_t=None, lh_m=None, ls_m=None, lh_unit="px"):
    s = {
        f"{prefix}_typography": "custom",
        f"{prefix}_font_family": family,
        f"{prefix}_font_size": px(size),
        f"{prefix}_font_weight": str(weight),
    }
    if lh is not None:
        s[f"{prefix}_line_height"] = px(lh, lh_unit)
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = px(ls)
    if transform:
        s[f"{prefix}_text_transform"] = transform
    if style:
        s[f"{prefix}_font_style"] = style
    if size_t is not None:
        s[f"{prefix}_font_size_tablet"] = px(size_t)
    if size_m is not None:
        s[f"{prefix}_font_size_mobile"] = px(size_m)
    if lh_t is not None:
        s[f"{prefix}_line_height_tablet"] = px(lh_t, lh_unit)
    if lh_m is not None:
        s[f"{prefix}_line_height_mobile"] = px(lh_m, lh_unit)
    if ls_m is not None:
        s[f"{prefix}_letter_spacing_mobile"] = px(ls_m)
    return s


def _globals(settings):
    """Anula os valores globais do kit nos controles de cor/tipografia definidos (como no export do Elementor)."""
    g = {}
    for k in settings:
        if (k.endswith("_typography") or k.endswith("color") or k.endswith("_color_b")) \
                and not k.endswith("_tablet") and not k.endswith("_mobile"):
            g[k] = ""
    if g:
        settings["__globals__"] = g
    return settings


def container(settings, children, inner=True, title=None):
    s = {"flex_gap": gap(0), "padding": dims(0)}
    s.update(settings)
    if title:
        s["_title"] = title  # nome no Navegador do Elementor
    return {"id": new_id(), "elType": "container", "isInner": inner, "settings": _globals(s), "elements": children}


def col(children, **kw):
    """Container coluna (largura total) - atalho para os blocos internos."""
    s = {"content_width": "full", "flex_direction": "column"}
    s.update(kw)
    return container(s, children)


def row(children, **kw):
    s = {"content_width": "full", "flex_direction": "row", "flex_wrap": "nowrap"}
    s.update(kw)
    return container(s, children)


def widget(widget_type, settings, title=None):
    if title:
        settings["_title"] = title
    return {"id": new_id(), "elType": "widget", "isInner": False, "widgetType": widget_type,
            "settings": _globals(settings), "elements": []}


def link(url=""):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def anim(name="fadeInUp", delay=0):
    return {"__anim__": (name, delay)}


def add(el, *parts, classes=""):
    """Acrescenta animação de entrada nativa, configurações extras e classes a um elemento."""
    is_widget = el["elType"] == "widget"
    for part in parts:
        part = dict(part)
        if "__anim__" in part:
            name, delay = part.pop("__anim__")
            prefix = "_" if is_widget else ""
            el["settings"][f"{prefix}animation"] = name
            el["settings"]["animation_duration"] = ""
            if delay:
                el["settings"][f"{prefix}animation_delay"] = delay
        el["settings"].update(part)
    if classes:
        key = "_css_classes" if is_widget else "css_classes"
        el["settings"][key] = (el["settings"].get(key, "") + " " + classes).strip()
    return el


def fa(name, lib="fa-solid"):
    prefix = "fab" if lib == "fa-brands" else ("far" if lib == "fa-regular" else "fas")
    return {"value": f"{prefix} {name}", "library": lib}


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------

def heading(title, tag, color, typography, align="left", extra=None, classes="", title_nav=None):
    s = {"title": title, "header_size": tag, "align": align, "title_color": color}
    s.update(typography)
    if extra:
        s.update(extra)
    if classes:
        s["_css_classes"] = classes
    return widget("heading", s, title=title_nav)


def text(html, color, typography, align="left", extra=None, classes=""):
    s = {"editor": html, "align": align, "text_color": color}
    s.update(typography)
    if extra:
        s.update(extra)
    if classes:
        s["_css_classes"] = classes
    return widget("text-editor", s)


def html_widget(code, classes="", title=None):
    s = {"html": code}
    if classes:
        s["_css_classes"] = classes
    return widget("html", s, title=title)


def icon(name, color, bg=None, size=20, pad=14, radius=14, lib="fa-solid", align="left", extra=None):
    # tamanho fixo quando fica ao lado de um texto numa linha (Avançado > Layout > Tamanho: Nenhum)
    s = {"selected_icon": fa(name, lib), "align": align, "size": px(size), "_flex_size": "none"}
    if bg:
        s.update({"view": "stacked", "shape": "square", "primary_color": bg, "secondary_color": color,
                  "icon_padding": px(pad), "border_radius": dims(radius)})
    else:
        s.update({"view": "default", "primary_color": color})
    if extra:
        s.update(extra)
    return widget("icon", s)


def icon_list(items, color, typography, icon_color=ROSE, inline=False, space=12, icon_size=16, indent=12,
              extra=None, classes=""):
    lst = []
    for it in items:
        if isinstance(it, str):
            it = {"text": it}
        lst.append({"_id": new_id(), "text": it["text"], "selected_icon": it.get("icon", fa("fa-check")),
                    "link": link(it.get("url", ""))})
    s = {
        "view": "inline" if inline else "traditional",
        "icon_list": lst,
        "space_between": px(space),
        "text_color": color,
        "text_color_hover": color,
        "icon_color": icon_color,
        "icon_color_hover": icon_color,
        "icon_size": px(icon_size),
        "text_indent": px(indent),
        "icon_self_vertical_align": "center",
    }
    s.update(typography)
    if extra:
        s.update(extra)
    if classes:
        s["_css_classes"] = classes
    return widget("icon-list", s)


def photo(alt, kind="expert", radius=24, extra=None, title=None, classes=""):
    """Imagem SEM arquivo: o Elementor mostra o placeholder padrão. No editor aparece uma etiqueta
    "SUBSTITUIR FOTO" (CSS .cz-ph) e o nome no Navegador indica o que colocar."""
    s = {"image_size": "full", "align": "center", "link_to": "none", "width": px(100, "%"),
         "image_border_radius": dims(radius),
         "_css_classes": f"cz-ph cz-ph-{kind} {classes}".strip()}
    if extra:
        s.update(extra)
    w = widget("image", s, title=title or f"📷 {alt}")
    # alt do placeholder fica no próprio controle de imagem quando a foto for escolhida;
    # aqui só documentamos no título do Navegador
    return w


def cta(label=CTA_MAIN, url=OFERTA, align="left", align_m="stretch", full=False):
    """Botão de ação padrão (verde). Único lugar da página onde o verde aparece."""
    s = {
        "text": label,
        "link": link(url),
        "align": "justify" if full else align,
        "align_mobile": "justify",
        "size": "lg",
        "selected_icon": fa("fa-arrow-right"),
        "icon_align": "right",
        "icon_indent": px(12),
        "button_text_color": WHITE,
        "hover_color": WHITE,
        "background_background": "classic",
        "background_color": GREEN,
        "button_background_hover_background": "classic",
        "button_background_hover_color": GREEN,
        "text_padding": dims(22, 34, 22, 34),
        "text_padding_mobile": dims(20, 20, 20, 20),
        "border_radius": dims(12),
        "_css_classes": "cz-btn",
    }
    s.update(typo("typography", 16, 900, lh=20, ls=0.6, transform="uppercase", size_m=14, lh_m=18, ls_m=0.3))
    return widget("button", s, title="Botão de ação (verde)")


def ghost_button(label, url, icon_name, lib="fa-brands", dark=False):
    color = WHITE if dark else TEAL
    s = {
        "text": label,
        "link": link(url),
        "align": "left",
        "align_mobile": "justify",
        "size": "md",
        "selected_icon": fa(icon_name, lib),
        "icon_align": "left",
        "icon_indent": px(10),
        "button_text_color": color,
        "hover_color": TEAL if dark else WHITE,
        "background_background": "classic",
        "background_color": "rgba(0,0,0,0)",
        "button_background_hover_background": "classic",
        "button_background_hover_color": WHITE if dark else TEAL,
        "border_border": "solid",
        "border_width": dims(1.5),
        "border_color": color,
        "button_hover_border_color": WHITE if dark else TEAL,
        "text_padding": dims(16, 26, 16, 26),
        "border_radius": dims(12),
        "_css_classes": "cz-btn-ghost",
    }
    s.update(typo("typography", 15, 700, lh=20, ls=0.3))
    return widget("button", s)


def micro(textline, icon_name="fa-hourglass-half", color=WHITE_80, align="left"):
    w = icon_list([{"text": textline, "icon": fa(icon_name)}], color,
                  typo("icon_typography", 14, 400, lh=20, size_m=13), icon_color=ROSE, icon_size=13, indent=10,
                  classes="cz-micro")
    w["settings"]["icon_align"] = align
    w["settings"]["icon_align_mobile"] = "center"
    return w


def eyebrow(label, dark=True, align="left"):
    return heading(label, "p", ROSE, typo("typography", 12, 800, lh=14, ls=1.8, transform="uppercase",
                                          size_m=11, ls_m=1.4),
                   align=align, classes="cz-eyebrow")


def h2(title, color, align="left", size=46, classes="cz-split"):
    return heading(title, "h2", color,
                   typo("typography", size, 800, lh=size + 6, ls=-1.2, size_t=38, lh_t=44, size_m=30, lh_m=36,
                        ls_m=-0.6),
                   align=align, classes=classes)


def body(html, color=SLATE, align="left", size=18):
    return text(html, color, typo("typography", size, 400, lh=size + 11, size_m=16, lh_m=26), align=align)


def section(settings, children, title, classes=""):
    """Seção de primeiro nível: fundo de ponta a ponta e conteúdo boxed em 1200px."""
    s = {
        "content_width": "boxed",
        "boxed_width": px(1200),
        "html_tag": "section",
        "flex_direction": "column",
        "padding": dims(120, 24, 120, 24),
        "padding_tablet": dims(96, 24, 96, 24),
        "padding_mobile": dims(72, 16, 72, 16),
        "css_classes": f"cz {classes}".strip(),
    }
    s.update(settings)
    return container(s, children, inner=False, title=title)


def bg(color):
    return {"background_background": "classic", "background_color": color}


def dark_bg():
    return {
        "background_background": "gradient",
        "background_color": TEAL,
        "background_color_stop": px(0, "%"),
        "background_color_b": TEAL_DEEP,
        "background_color_b_stop": px(100, "%"),
        "background_gradient_type": "linear",
        "background_gradient_angle": px(160, "deg"),
    }


def card(children, dark=False, pad=(32, 30, 32, 30), radius=22, classes="", **kw):
    s = {
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(14),
        "padding": dims(*pad),
        "padding_mobile": dims(26, 22, 26, 22),
        "border_radius": dims(radius),
        "css_classes": classes,
    }
    if dark:
        s.update({"background_background": "classic", "background_color": "rgba(255, 255, 255, 0.05)",
                  "border_border": "solid", "border_width": dims(1), "border_color": "rgba(255, 255, 255, 0.12)"})
    else:
        s.update({"background_background": "classic", "background_color": WHITE,
                  "border_border": "solid", "border_width": dims(1), "border_color": "rgba(15, 79, 92, 0.1)"})
    s.update(kw)
    return container(s, children)


def grid(children, cols, cols_t, cols_m, gap_px=20, **kw):
    n = len(children)
    s = {
        "content_width": "full",
        "container_type": "grid",
        "grid_columns_grid": {"unit": "fr", "size": cols, "sizes": []},
        "grid_columns_grid_tablet": {"unit": "fr", "size": cols_t, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": cols_m, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": -(-n // cols), "sizes": []},
        "grid_rows_grid_tablet": {"unit": "fr", "size": -(-n // cols_t), "sizes": []},
        "grid_rows_grid_mobile": {"unit": "fr", "size": -(-n // cols_m), "sizes": []},
        "grid_gaps": {"column": str(gap_px), "row": str(gap_px), "isLinked": True, "unit": "px"},
        "grid_auto_flow": "row",
    }
    s.update(kw)
    return container(s, children)


def stagger(items, start=0, step=100, name="fadeInUp"):
    return [add(it, anim(name, start + i * step)) for i, it in enumerate(items)]


def reveal(items, start=0):
    """Revelação própria (.cz-rv) para elementos que já usam transform (cartões 3D, hover que desloca,
    fotos inclinadas): a animação nativa do Elementor sobrescreveria esse transform."""
    return [add(it, classes=f"cz-rv cz-d{min(start + i, 8)}") for i, it in enumerate(items)]


# ---------------------------------------------------------------------------
# 0. CSS + JS + CTA fixo do celular
# ---------------------------------------------------------------------------

def build_assets():
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    js = open(JS_FILE, encoding="utf-8").read().strip()
    sticky = (f'<a class="cz-sticky" href="{OFERTA}" aria-label="Quero minha vaga de Membro Fundador">'
              'Quero minha vaga'
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/>'
              '</svg></a>')
    code = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            "<style>\n" + css + "\n</style>\n" + sticky + "\n<script>\n" + js + "\n</script>")
    return container({
        "content_width": "full",
        "min_height": px(0),
        "css_classes": "cz cz-css",
    }, [html_widget(code, title="CSS + JS da página (não apagar)")], inner=False, title="⚙ Estilos e animações")


# ---------------------------------------------------------------------------
# 1. HERO
# ---------------------------------------------------------------------------

SEALS = [
    ("fa-graduation-cap", "Reconhecida pelo MEC", "Faculdade Anhanguera"),
    ("fa-laptop", "100% online", "Estude de onde estiver"),
    ("fa-book-open", "400 horas", "17 disciplinas"),
    ("fa-video", "Ao vivo todo mês", "Encontro com o tutor"),
]


def seal(icon_name, title, sub):
    return row([
        icon(icon_name, WHITE, bg="rgba(207, 138, 134, 0.22)", size=16, pad=11, radius=10),
        col([
            heading(title, "p", WHITE, typo("typography", 15, 800, lh=19, size_m=14, lh_m=18)),
            heading(sub, "p", WHITE_60, typo("typography", 13, 400, lh=17, size_m=12, lh_m=16)),
        ], flex_gap=gap(2), flex_justify_content="center"),
    ], flex_gap=gap(12), flex_align_items="center", css_classes="cz-seal")


def build_hero():
    logo = photo("Logo Método Cicatrize 3X · Pós-graduação", kind="logo", radius=0,
                 extra={"align": "left", "width": px(246), "width_mobile": px(190)},
                 title="📷 LOGO (subir o SVG do Figma)")

    pill = eyebrow("Turma de Membros Fundadores · Vagas limitadas")
    h1 = heading(
        '<span class="cz-pre">Você já trata feridas.</span>'
        'Torne-se o <em>Especialista</em> na área <span class="cz-rose cz-mark">certificado pelo MEC</span> '
        "que os pacientes procuram quando o caso é grave.",
        "h1", WHITE,
        typo("typography", 44, 800, lh=52, ls=-1, size_t=40, lh_t=48, size_m=30, lh_m=37, ls_m=-0.5),
        classes="cz-h1 cz-split")
    sub = body("<p>Pós-graduação em <strong>Tratamento de Feridas e Podiatria</strong>. Duas especialidades em uma "
               "única formação, com raciocínio clínico estruturado que acelera a cicatrização e diploma "
               "reconhecido pelo MEC.</p>", color=WHITE_80, size=18)

    seals = grid(stagger([seal(*s) for s in SEALS], 300, 90, "fadeIn"), 2, 2, 1, gap_px=18,
                 padding=dims(20, 22, 20, 22), padding_mobile=dims(18, 16, 18, 16),
                 border_radius=dims(18), css_classes="cz-seals")

    left = col([
        add(logo, anim("fadeIn")),
        add(pill, anim("fadeInUp", 100), {"_margin": dims(36, 0, 0, 0), "_margin_mobile": dims(26, 0, 0, 0)}),
        h1,
        add(sub, anim("fadeInUp", 250)),
        seals,
        add(cta(), anim("fadeInUp", 450), {"_margin": dims(8, 0, 0, 0)}),
        add(micro("Condição exclusiva da primeira turma. Não vai se repetir."), anim("fadeIn", 600)),
    ], width=px(54, "%"), width_tablet=px(100, "%"), flex_gap=gap(22), flex_gap_mobile=gap(18))

    chip_a = row([
        icon("fa-award", WHITE, bg=TEAL, size=14, pad=9, radius=8),
        col([heading("Reconhecida pelo MEC", "p", TEAL, typo("typography", 13, 800, lh=16)),
             heading("Faculdade Anhanguera", "p", SLATE, typo("typography", 12, 400, lh=15))], flex_gap=gap(1)),
    ], flex_gap=gap(10), flex_align_items="center", padding=dims(10, 16, 10, 10), border_radius=dims(14),
        **bg(WHITE), css_classes="cz-float-chip cz-chip-a")
    chip_b = row([
        icon("fa-user-md", WHITE, bg=ROSE, size=14, pad=9, radius=8),
        heading("Dr. Cicatriz · Coordenador", "p", TEAL, typo("typography", 13, 800, lh=16)),
    ], flex_gap=gap(10), flex_align_items="center", padding=dims(10, 16, 10, 10), border_radius=dims(14),
        **bg(WHITE), css_classes="cz-float-chip cz-chip-b")

    right = col([
        html_widget('<div class="cz-orb" aria-hidden="true"></div>'),
        add(photo("FOTO DO EXPERT com selo MEC + Anhanguera (PNG recortado)", radius=0),
            anim("fadeIn", 200)),
        chip_a,
        chip_b,
    ], width=px(46, "%"), width_tablet=px(70, "%"), width_mobile=px(100, "%"),
        flex_justify_content="flex-end", css_classes="cz-hero-photo cz-par-2")

    content = row([left, right], content_width="boxed", boxed_width=px(1200),
                  flex_direction_tablet="column", flex_align_items="center", flex_align_items_tablet="flex-start",
                  flex_gap=gap(40), flex_gap_tablet=gap(48),
                  padding=dims(48, 24, 72, 24), padding_tablet=dims(40, 24, 56, 24),
                  padding_mobile=dims(28, 16, 48, 16))

    vagas = container({
        "content_width": "full",
        "flex_direction": "column",
        "padding": dims(22, 16, 22, 16),
        "background_background": "classic",
        "background_color": "rgba(11, 60, 70, 0.78)",
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "rgba(255, 255, 255, 0.1)",
    }, [html_widget(f'<div class="cz-vagas cz-io" data-percent="{VAGAS_PERCENT}">'
                    f'<span class="cz-vagas-label"><b class="cz-vagas-n">0%</b> das vagas preenchidas</span>'
                    '<span class="cz-vagas-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" '
                    f'aria-valuenow="{VAGAS_PERCENT}" aria-label="Vagas preenchidas">'
                    '<span class="cz-vagas-fill"></span></span></div>',
                    title=f"Barra de vagas (mudar data-percent=\"{VAGAS_PERCENT}\")")])

    return container({
        "content_width": "full",
        "html_tag": "header",
        "flex_direction": "column",
        "flex_justify_content": "space-between",
        "min_height": px(100, "vh"),
        "min_height_tablet": px(0, "px"),
        # Foto de fundo: deixar vazia por enquanto (Estilo > Fundo > Imagem)
        "background_background": "classic",
        "background_color": TEAL_DEEP,
        "background_position": "center right",
        "background_size": "cover",
        "css_classes": "cz cz-hero",
    }, [content, vagas], inner=False, title="1 · HERO (inserir foto de fundo em Estilo > Fundo)")


# ---------------------------------------------------------------------------
# 2. O PARADOXO
# ---------------------------------------------------------------------------

def build_paradoxo():
    title = h2('Responda com <span class="cz-rose">sinceridade.</span>', TEAL, size=56)
    p1 = body("<p>Se fosse a vida de alguém que você ama — um pé diabético a um passo da amputação, uma ferida "
              "que não fecha há meses — <strong class=\"cz-rose\">você entregaria esse caso a um "
              "generalista?</strong></p>")
    p2 = body("<p><strong>Ou procuraria o Especialista:</strong> o profissional com nome, diploma e "
              "responsabilidade formal pelo resultado?</p>")
    swap = heading("Agora troque de lugar.", "p", WHITE,
                   typo("typography", 30, 800, lh=36, ls=-0.4, size_m=24, lh_m=30), classes="cz-swap")
    p3 = body("<p><strong>O problema não é o seu conhecimento.</strong> É que a sua competência ainda não tem o "
              "reconhecimento formal que ela merece.</p>")
    p4 = body("<p>E, na saúde, quem não é reconhecido como especialista perde a autoridade e se torna "
              "<span class=\"cz-mark\">mais um no mercado</span>.</p>")

    left = col([
        add(eyebrow("O paradoxo"), anim("fadeInUp")),
        title,
        add(p1, anim("fadeInUp", 100)),
        add(p2, anim("fadeInUp", 200)),
        add(swap, {"_margin": dims(18, 0, 18, 0)}),
        add(p3, anim("fadeInUp")),
        add(p4, anim("fadeInUp", 100)),
    ], width=px(50, "%"), width_tablet=px(100, "%"), flex_gap=gap(18))

    shot_a = col([photo("FOTO DO EXPERT em atendimento (vertical)")],
                 width=px(62, "%"), _flex_align_self="flex-end", border_radius=dims(24),
                 css_classes="cz-shot cz-shot-a cz-rv cz-d0")
    shot_b = col([photo("FOTO DO EXPERT tratando um paciente (vertical)")],
                 width=px(60, "%"), border_radius=dims(24), css_classes="cz-shot cz-shot-b cz-rv cz-d2")
    name = row([
        icon("fa-user-md", ROSE, size=14),
        heading("Abdeel Oliveira Martins Junior", "p", TEAL, typo("typography", 13, 700, lh=16)),
    ], flex_gap=gap(8), flex_align_items="center", padding=dims(12, 18, 12, 18), border_radius=dims(999),
        **bg(WHITE), css_classes="cz-name-chip")
    collage = col([
        shot_a,
        shot_b,
        name,
    ], width=px(46, "%"), width_tablet=px(100, "%"), width_mobile=px(100, "%"),
        flex_gap_mobile=gap(16), css_classes="cz-collage cz-par-2")

    cols = row([left, collage], flex_direction_tablet="column", flex_gap=gap(64), flex_gap_tablet=gap(56),
               flex_align_items="center")

    statement = heading(
        "Ninguém discute se o especialista é melhor que o generalista. "
        '<span class="cz-rose">A única pergunta é: quando VOCÊ vai assumir esse lugar?</span>',
        "p", TEAL, typo("typography", 40, 800, lh=50, ls=-0.8, size_t=34, lh_t=42, size_m=26, lh_m=34, ls_m=-0.4),
        align="center", classes="cz-scrub cz-statement")
    stmt_wrap = col([statement], padding=dims(110, 0, 0, 0), padding_mobile=dims(72, 0, 0, 0),
                    content_width="boxed", boxed_width=px(980), css_classes="cz-stmt")
    stmt_wrap["settings"]["width"] = px(100, "%")

    return section({**bg(WHITE), "flex_gap": gap(0), "flex_align_items": "center"},
                   [cols, stmt_wrap], "2 · O PARADOXO", "cz-paradoxo")


# ---------------------------------------------------------------------------
# Faixa de palavras
# ---------------------------------------------------------------------------

MARQUEE = ["Tratamento de Feridas", "Podiatria Clínica", "Reconhecida pelo MEC", "400 horas",
           "17 disciplinas", "100% online", "Método Cicatrize 3X"]


def build_marquee():
    line = "".join(f'<span>{w}</span><span class="cz-star">✦</span>' for w in MARQUEE)
    code = (f'<div class="cz-marquee" aria-hidden="true"><div class="cz-marquee-track">{line}{line}</div></div>')
    return container({
        "content_width": "full",
        "padding": dims(30, 0, 30, 0),
        "padding_mobile": dims(20, 0, 20, 0),
        "overflow": "hidden",
        "z_index": 2,
        **bg(WHITE),
        "css_classes": "cz cz-marquee-wrap",
    }, [html_widget(code)], inner=False, title="Faixa de palavras em movimento")


# ---------------------------------------------------------------------------
# 3. A PÓS 2 EM 1
# ---------------------------------------------------------------------------

VENN = (
    '<div class="cz-venn cz-io" role="img" aria-label="Tratamento de Feridas mais Podiatria Clínica: '
    'um único diploma reconhecido pelo MEC">'
    '<div class="cz-venn-c cz-venn-a"><span>Tratamento<br>de Feridas</span></div>'
    '<div class="cz-venn-c cz-venn-b"><span>Podiatria<br>Clínica</span></div>'
    '<div class="cz-venn-mid">'
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true"><path d="M22 10 12 5 2 10l10 5 10-5Z"/>'
    '<path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
    "<b>1 diploma</b><small>MEC</small></div></div>"
)

CHANGES = [
    ("fa-brain", "Raciocínio clínico estruturado.",
     "Você avalia qualquer ferida com um método simples e objetivo — e sabe exatamente por que a conduta "
     "funcionou."),
    ("fa-band-aid", "Cicatrização mais rápida.",
     "Conduta certa desde a primeira avaliação: o paciente se recupera antes e o seu resultado aparece."),
    ("fa-shoe-prints", "Atuação ampliada na podiatria.",
     "Você identifica alterações estruturais e biomecânicas e conduz essa parte do cuidado sem depender de "
     "outro profissional."),
]


def change_card(i, icon_name, title, desc):
    top = row([
        icon(icon_name, ROSE, bg="rgba(207, 138, 134, 0.14)", size=20, pad=14, radius=14),
        heading(f"0{i}", "p", "rgba(255, 255, 255, 0.28)", typo("typography", 40, 900, lh=40, ls=-1),
                align="right", classes="cz-num", extra={"_flex_size": "grow"}),
    ], flex_justify_content="space-between", flex_align_items="center")
    return card([
        top,
        heading(title, "h3", WHITE, typo("typography", 22, 800, lh=28, ls=-0.3, size_m=20, lh_m=26),
                extra={"_margin": dims(10, 0, 0, 0)}),
        container({"content_width": "full", "css_classes": "cz-card-line"}, []),
        body(f"<p>{desc}</p>", color=WHITE_80, size=16),
    ], dark=True, classes="cz-tilt")


def build_dois_em_um():
    title = h2("Duas especialidades. Um único diploma. "
               '<span class="cz-rose">Nenhum caso pela metade.</span>', WHITE)
    intro = body("<p>A Pós-graduação em Tratamento de Feridas e Podiatria – <strong>Método Cicatrize 3X</strong> "
                 "une, em uma só formação, o tratamento de feridas amplo e completo e a podiatria clínica. "
                 "Você resolve o caso inteiro, do início ao fim, <strong>sem precisar encaminhar</strong>.</p>",
                 color=WHITE_80)
    head = row([
        col([add(eyebrow("A pós 2 em 1"), anim("fadeInUp")), title, add(intro, anim("fadeInUp", 200))],
            width=px(56, "%"), width_tablet=px(100, "%"), flex_gap=gap(20)),
        col([html_widget(VENN, title="Diagrama 2 em 1 (animado)")],
            width=px(44, "%"), width_tablet=px(100, "%"), flex_justify_content="center"),
    ], flex_direction_tablet="column", flex_gap=gap(56), flex_gap_tablet=gap(40), flex_align_items="center")

    line = container({"content_width": "full", "css_classes": "cz-line cz-io",
                      "margin": dims(72, 0, 56, 0), "margin_mobile": dims(48, 0, 40, 0)}, [])

    sub = heading("O que muda na sua prática", "h3", ROSE,
                  typo("typography", 14, 800, lh=18, ls=1.8, transform="uppercase"), align="center")
    cards = grid(reveal([change_card(i + 1, *c) for i, c in enumerate(CHANGES)]), 3, 1, 1, gap_px=22,
                 margin=dims(28, 0, 0, 0))

    quote = heading(
        "Você deixa de ser quem troca curativo e passa a ser "
        '<span class="cz-rose">o Especialista certificado pelo MEC que resolve o caso que ninguém mais '
        "resolve.</span>",
        "p", WHITE, typo("typography", 34, 800, lh=44, ls=-0.6, size_t=30, lh_t=40, size_m=24, lh_m=32),
        align="center", classes="cz-scrub")
    quote_wrap = col([quote], content_width="boxed", boxed_width=px(900), padding=dims(96, 0, 40, 0), padding_mobile=dims(64, 0, 32, 0))
    quote_wrap["settings"]["width"] = px(100, "%")

    return section({**dark_bg(), "flex_align_items": "center"},
                   [head, line, add(sub, anim("fadeInUp")), cards, quote_wrap,
                    add(cta(align="center"), anim("zoomIn"))],
                   "3 · A PÓS 2 EM 1", "cz-dark cz-2em1")


# ---------------------------------------------------------------------------
# 4. PARA QUEM É
# ---------------------------------------------------------------------------

FOR_WHO = [
    ("fa-shield-alt", "Já atende feridas e quer <strong>segurança total em cada conduta</strong>, dos casos "
                      "simples aos complexos."),
    ("fa-graduation-cap", "Quer o <strong>título de Especialista</strong> e o diploma reconhecido pelo MEC no "
                          "seu currículo."),
    ("fa-shoe-prints", "Quer <strong>ampliar a atuação para a podiatria</strong> e parar de encaminhar (e "
                       "perder) pacientes."),
    ("fa-map-marker-alt", "Quer ser <strong>a referência em feridas na sua cidade</strong> e cobrar honorários "
                          "de especialista."),
    ("fa-laptop-medical", "Precisa de uma formação <strong>100% online</strong>, que caiba na rotina de plantão "
                          "e consultório."),
]


def for_item(i, icon_name, html):
    return row([
        icon(icon_name, WHITE, bg=TEAL, size=18, pad=14, radius=14),
        col([body(f"<p>{html}</p>", size=18)], flex_justify_content="center"),
        heading(f"0{i}", "p", TEAL, typo("typography", 44, 900, lh=44, ls=-1, size_m=32), align="right",
                classes="cz-for-n", extra={"_flex_size": "none"}),
    ], flex_gap=gap(20), flex_gap_mobile=gap(14), flex_align_items="center",
        padding=dims(22, 26, 22, 22), padding_mobile=dims(18, 16, 18, 16), border_radius=dims(18),
        border_border="solid", border_width=dims(1), border_color="rgba(15, 79, 92, 0.1)", **bg(WHITE),
        css_classes="cz-for")


def build_para_quem():
    note = row([
        icon("fa-user-nurse", WHITE, bg=ROSE, size=18, pad=13, radius=12),
        body("<p><strong>Exclusiva para Enfermeiros e Profissionais de Saúde</strong> com formação "
             "superior.</p>", color=WHITE, size=16),
    ], flex_gap=gap(16), flex_align_items="center", padding=dims(20, 22, 20, 20), border_radius=dims(18),
        **bg(TEAL))
    side = col([
        add(eyebrow("Para quem é"), anim("fadeInUp")),
        h2('Esta pós é <span class="cz-rose">para você</span> que:', TEAL, size=52),
        add(body("<p>Se você se reconheceu em pelo menos um destes pontos, esta formação foi feita para o seu "
                 "próximo passo.</p>"), anim("fadeInUp", 150)),
        add(note, anim("fadeInUp", 250), {"margin": dims(10, 0, 0, 0)}),
    ], width=px(40, "%"), width_tablet=px(100, "%"), flex_gap=gap(20), css_classes="cz-sticky-col")
    items = col(reveal([for_item(i + 1, *it) for i, it in enumerate(FOR_WHO)]),
                width=px(60, "%"), width_tablet=px(100, "%"), flex_gap=gap(14))
    return section({**bg(MIST), "flex_direction": "row", "flex_direction_tablet": "column",
                    "flex_align_items": "flex-start", "flex_gap": gap(64), "flex_gap_tablet": gap(40)},
                   [side, items], "4 · PARA QUEM É", "cz-para-quem")


# ---------------------------------------------------------------------------
# 5. O QUE VOCÊ VAI DOMINAR (grade)
# ---------------------------------------------------------------------------

BLOCKS = [
    ("fa-microscope", "Base clínica", [
        ("Anatomia e Fisiologia da Pele, do Pé e dos Membros Inferiores",
         "Camadas da pele, microcirculação e a fisiologia avançada da cicatrização: hemostasia, inflamação, "
         "proliferação, remodelamento e por que a ferida crônica trava."),
        ("Semiologia, Anamnese e Avaliação Clínica",
         "Avaliação vascular, neurológica e biomecânica, estratificação de risco do pé diabético e documentação "
         "com raciocínio clínico."),
        ("Biossegurança e Controle de Infecções em Feridas e Cateteres",
         "Microbiologia da pele, biofilme, antissepsia, esterilização e prevenção de infecção relacionada à "
         "assistência."),
        ("Nutrição nas Lesões Cutâneas",
         "Proteínas, vitaminas, minerais e hidratação na cicatrização; desnutrição, sarcopenia e o paciente com "
         "pé diabético."),
        ("Farmacologia no Tratamento de Feridas e Podiatria",
         "Antimicrobianos tópicos, controle da dor, anticoagulantes, anestésicos locais, antifúngicos, "
         "polifarmácia e práticas integrativas com segurança."),
    ]),
    ("fa-band-aid", "Feridas complexas", [
        ("Sistematização da Assistência em Lesões e Feridas",
         "LPP, úlceras venosas, arteriais e mistas, pé diabético, leitura do leito da ferida, TIMERS, "
         "desbridamento e escolha da cobertura certa para cada lesão."),
        ("Queimaduras e Radiodermites",
         "Classificação, extensão e profundidade, atendimento inicial, coberturas, prevenção e tratamento das "
         "radiodermites."),
        ("Feridas Cirúrgicas, Drenos e Estomias",
         "Complicações cirúrgicas, tipos de drenos, cuidados com o estoma e a pele periestomal."),
        ("Ferida Oncológica",
         "Controle de exsudato, odor, sangramento e dor, coberturas e cuidados paliativos com qualidade de "
         "vida."),
    ]),
    ("fa-shoe-prints", "Podiatria", [
        ("Podiatria Clínica, Biomecânica e Avaliação dos Pés",
         "Marcha, pressão plantar, alterações estruturais, calçados e pé de risco."),
        ("Principais Podopatias e Onicopatias",
         "Calosidades, verrugas, micoses, onicomicose, paroníquia e diagnóstico diferencial com sinais de "
         "alerta."),
        ("Alterações Ungueais, Onicocriptose e Técnicas Corretivas",
         "Tratamento conservador, órteses ungueais, técnicas corretivas e pacientes de risco."),
        ("Órteses, Palmilhas e Alívio de Pressão",
         "Offloading, correção funcional, calçados terapêuticos e órteses no pé diabético."),
    ]),
    ("fa-atom", "Tecnologia e inovação", [
        ("Biomateriais e Inovação Tecnológica em Curativos",
         "Coberturas bioativas e antimicrobianas, nanotecnologia, terapia por pressão negativa, laser e LED, "
         "engenharia tecidual e inteligência artificial em feridas."),
    ]),
    ("fa-chart-line", "Carreira e mercado", [
        ("Gestão e Empreendedorismo",
         "Fundamentos e estratégias para montar e fazer crescer o seu negócio em saúde."),
        ("Emergências na Pessoa Idosa e Prevenção de Quedas",
         "Emergências cardiovasculares, respiratórias e neurológicas no idoso e prevenção de trauma."),
        ("Marketing Digital",
         "Jornada do cliente, persona, mídias sociais e métricas para ser encontrado pelo paciente certo."),
    ]),
]


def accordion(items, title_typo, classes, faq=False, title_color=TEAL, answer_color=SLATE):
    acc = widget("nested-accordion", {
        "items": [{"item_title": q, "_id": new_id()} for q, _ in items],
        "title_tag": "h3" if faq else "h4",
        "default_state": "all_collapsed",
        "max_items_expended": "one",
        "faq_schema": "yes" if faq else "",
        "accordion_item_title_position_horizontal": "stretch",
        "accordion_item_title_icon_position": "end",
        "accordion_item_title_icon": fa("fa-plus"),
        "accordion_item_title_icon_active": fa("fa-minus"),
        "accordion_item_title_space_between": px(10),
        "accordion_item_title_distance_from_content": px(0),
        "accordion_padding": dims(20, 22, 20, 22),
        "accordion_padding_mobile": dims(16, 16, 16, 16),
        "accordion_border_radius": dims(14),
        "accordion_border_normal_border": "none",
        "accordion_border_hover_border": "none",
        "accordion_border_active_border": "none",
        "content_border_border": "none",
        **title_typo,
        "normal_title_color": title_color,
        "hover_title_color": TEAL,
        "active_title_color": TEAL,
        "normal_icon_color": TEAL,
        "hover_icon_color": TEAL,
        "active_icon_color": WHITE,
        "icon_size": px(12),
        "icon_spacing": px(16),
        "_css_classes": f"cz-acc {classes}".strip(),
    })
    children = []
    for _, answer in items:
        c = container({"content_width": "full", "flex_direction": "column",
                       "padding": dims(0, 22, 22, 22), "padding_mobile": dims(0, 16, 18, 16)},
                      [body(answer if answer.startswith("<") else f"<p>{answer}</p>", color=answer_color,
                            size=16)])
        children.append(c)
    acc["elements"] = children
    return acc


def counter(end, title, suffix=""):
    w = widget("counter", {
        "starting_number": 0,
        "ending_number": end,
        "suffix": suffix,
        "duration": 2200,
        "thousand_separator": "",
        "title": title,
        "number_color": TEAL,
        "title_color": SLATE,
        **typo("typography_number", 56, 900, lh=56, ls=-2, size_m=40, lh_m=42),
        **typo("typography_title", 14, 700, lh=18, ls=1.4, transform="uppercase", size_m=12),
    })
    return col([w], padding=dims(0, 0, 0, 20), border_border="solid", border_width=dims(0, 0, 0, 2),
               border_color=ROSE, css_classes="cz-stat")


def build_grade():
    head = col([
        add(eyebrow("Grade curricular", align="center"), anim("fadeInUp")),
        h2('17 disciplinas. 400 horas. <span class="cz-rose">Do diagnóstico ao caso mais complexo.</span>',
           TEAL, align="center"),
    ], flex_gap=gap(20), flex_align_items="center", content_width="boxed", boxed_width=px(860))
    head["settings"]["width"] = px(100, "%")

    stats = grid(stagger([counter(17, "Disciplinas"), counter(400, "Horas"), counter(5, "Blocos"),
                          counter(100, "Online", "%")], 0, 100), 4, 4, 2, gap_px=24,
                 margin=dims(56, 0, 64, 0), margin_mobile=dims(40, 0, 44, 0))

    blocks = []
    n = 0
    for b, (icon_name, name, discs) in enumerate(BLOCKS, start=1):
        label = col([
            row([icon(icon_name, WHITE, bg=TEAL, size=18, pad=13, radius=12),
                 heading(f"Bloco {b:02d}", "p", ROSE, typo("typography", 13, 800, lh=16, ls=1.8,
                                                           transform="uppercase"), classes="cz-block-tag")],
                flex_gap=gap(14), flex_align_items="center"),
            heading(name, "h3", TEAL, typo("typography", 28, 800, lh=34, ls=-0.5, size_m=24, lh_m=30)),
            heading(f"{len(discs)} disciplina{'s' if len(discs) > 1 else ''}", "p", SLATE,
                    typo("typography", 15, 400, lh=20)),
        ], width=px(32, "%"), width_tablet=px(100, "%"), flex_gap=gap(12))
        items = [(f'<span class="cz-dn">{n + i + 1:02d}</span> {t}', d) for i, (t, d) in enumerate(discs)]
        n += len(discs)
        acc = accordion(items, typo("title_typography", 18, 700, lh=24, size_m=16, lh_m=22), "cz-grade-acc")
        right = col([acc], width=px(68, "%"), width_tablet=px(100, "%"))
        blocks.append(add(row([add(label, anim("fadeInUp")), add(right, anim("fadeInUp", 150))],
                              flex_direction_tablet="column", flex_gap=gap(40), flex_gap_tablet=gap(22),
                              padding=dims(40, 0, 40, 0), padding_mobile=dims(32, 0, 32, 0),
                              css_classes="cz-block")))

    return section({**bg(WHITE), "flex_align_items": "center"},
                   [head, stats, col(blocks)], "5 · O QUE VOCÊ VAI DOMINAR (grade)", "cz-grade")


# ---------------------------------------------------------------------------
# 6. COMO FUNCIONA
# ---------------------------------------------------------------------------

HOW = [
    ("fa-award", "Certificação", "Diploma de pós-graduação reconhecido pelo MEC, emitido pela Faculdade Anhanguera"),
    ("fa-play-circle", "Formato", "100% online, aulas gravadas para assistir quantas vezes quiser"),
    ("fa-clock", "Carga horária", "400 horas em 17 disciplinas"),
    ("fa-calendar-alt", "Ritmo", "Uma nova disciplina liberada por mês"),
    ("fa-flag", "Início", "Novembro de 2026"),
    ("fa-video", "Ao vivo", "1 encontro ao vivo por mês com o tutor coordenador do curso para tirar dúvidas e "
                            "discutir casos clínicos"),
    ("fa-whatsapp", "Suporte", "Grupo de tutoria no WhatsApp"),
    ("fa-clipboard-check", "Avaliação", "[confirmar: sem TCC, avaliação por disciplina]"),
]


def how_card(icon_name, label, value):
    lib = "fa-brands" if icon_name == "fa-whatsapp" else "fa-solid"
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(12),
        "padding": dims(28, 26, 28, 26),
        "padding_mobile": dims(22, 20, 22, 20),
        "border_radius": dims(20),
        "css_classes": "cz-info cz-tilt",
    }, [
        icon(icon_name, ROSE, bg="rgba(207, 138, 134, 0.14)", size=20, pad=13, radius=12, lib=lib),
        heading(label, "h3", ROSE, typo("typography", 13, 800, lh=16, ls=1.6, transform="uppercase"),
                extra={"_margin": dims(8, 0, 0, 0)}),
        heading(value, "p", WHITE, typo("typography", 18, 700, lh=25, size_m=17, lh_m=24)),
    ])


def build_como_funciona():
    head = col([
        add(eyebrow("Como funciona", align="center"), anim("fadeInUp")),
        h2('Uma pós completa, feita para <span class="cz-rose">caber na sua rotina.</span>', WHITE, align="center"),
    ], flex_gap=gap(20), flex_align_items="center", content_width="boxed", boxed_width=px(820))
    head["settings"]["width"] = px(100, "%")
    cards = grid(reveal([how_card(*h) for h in HOW]), 4, 2, 1, gap_px=18,
                 margin=dims(56, 0, 56, 0), margin_mobile=dims(40, 0, 40, 0))
    return section({**dark_bg(), "flex_align_items": "center"},
                   [head, cards, add(cta(align="center"), anim("zoomIn"))],
                   "6 · COMO FUNCIONA", "cz-dark cz-como")


# ---------------------------------------------------------------------------
# 7. CORPO DOCENTE
# ---------------------------------------------------------------------------

LEAD_DISCS = ["Semiologia e Avaliação Clínica", "Podiatria Clínica e Biomecânica", "Podopatias e Onicopatias",
              "Técnicas Corretivas", "Órteses e Alívio de Pressão", "Biomateriais e Inovação em Curativos"]

TEACHERS = [
    ("Profa. Me. Cibele dos Anjos Marcondes",
     "Mestre em Morfologia e Biologia Molecular pela UNICAMP, pós-graduada em Cuidados Paliativos pelo Hospital "
     "Albert Einstein e habilitada em Laserterapia.",
     "Anatomia, Fisiologia da Cicatrização e Biossegurança."),
    ("Profa. Dra. Maria Carliana Mota",
     "Nutricionista, Mestre, Doutora e Pós-Doutora em Ciências da Saúde pela UFU.",
     "Nutrição nas Lesões Cutâneas."),
    ("Profa. Patricia Lasmar Buiatti",
     "Graduada pela UFU, especialista em Educação do Ensino Superior.",
     "Farmacologia no Tratamento de Feridas e Podiatria."),
    ("Profa. Rosângela Maria Pereira",
     "Enfermeira Especialista em Estomaterapia pela Escola de Enfermagem da USP.",
     "Feridas Complexas, Queimaduras e Radiodermites, Estomias e Ferida Oncológica."),
    ("Profa. Dra. Danielle Cristina Garbuio",
     "",  # titulação detalhada não veio na copy
     "Emergências na Pessoa Idosa e Prevenção de Quedas."),
    ("Profa. Me. Thais Cereda Ravasi",
     "",  # titulação detalhada não veio na copy
     "Gestão e Empreendedorismo e Marketing Digital."),
]


def teacher_card(name, cred, teaches):
    info = [heading(name, "h3", TEAL, typo("typography", 20, 800, lh=26, ls=-0.2, size_m=19, lh_m=25))]
    if cred:
        info.append(heading(cred, "p", ROSE, typo("typography", 14, 700, lh=20)))
    info.append(text(f"<p><strong>Ensina:</strong> {teaches}</p>", SLATE, typo("typography", 15, 400, lh=23)))
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "border_radius": dims(22),
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(15, 79, 92, 0.1)",
        **bg(WHITE),
        "css_classes": "cz-prof",
    }, [
        photo(f"FOTO: {name}", kind="prof", radius=0, classes="cz-prof-photo", title=f"📷 Foto — {name}"),
        col(info, flex_gap=gap(10), padding=dims(24, 24, 28, 24)),
    ])


def build_docentes():
    head = col([
        add(eyebrow("Corpo docente", align="center"), anim("fadeInUp")),
        h2('Você vai aprender com quem vive a prática — <span class="cz-rose">e tem titulação para '
           "provar.</span>", TEAL, align="center"),
    ], flex_gap=gap(20), flex_align_items="center", content_width="boxed", boxed_width=px(900))
    head["settings"]["width"] = px(100, "%")

    chips = icon_list([{"text": d, "icon": fa("fa-check")} for d in LEAD_DISCS], TEAL,
                      typo("icon_typography", 14, 700, lh=18), inline=True, icon_size=11, indent=8, space=8,
                      classes="cz-chips")
    lead_info = col([
        row([heading("Coordenador", "p", WHITE, typo("typography", 12, 800, lh=14, ls=1.6, transform="uppercase"),
                     classes="cz-price-badge", extra={"_flex_size": "none"}),
             heading("Leciona 6 disciplinas", "p", ROSE, typo("typography", 13, 800, lh=16, ls=1.2,
                                                                transform="uppercase"), extra={"_flex_size": "none"})],
            flex_gap=gap(14), flex_align_items="center", flex_wrap="wrap"),
        heading("Dr. Cicatriz <span class=\"cz-rose\">(Abdeel Oliveira Martins Junior)</span>", "h3", TEAL,
                typo("typography", 30, 800, lh=36, ls=-0.5, size_m=24, lh_m=30)),
        body("<p>Enfermeiro, especialista em Enfermagem Dermatológica com ênfase em Tratamento de Feridas. "
             "Coordena a pós e leciona pessoalmente 6 disciplinas:</p>"),
        chips,
    ], width=px(58, "%"), width_tablet=px(100, "%"), flex_gap=gap(16), flex_justify_content="center",
        padding=dims(44, 44, 44, 8), padding_tablet=dims(8, 32, 36, 32), padding_mobile=dims(4, 20, 28, 20))
    lead = row([
        col([photo("FOTO DO EXPERT (Dr. Cicatriz) — horizontal ou retrato", radius=0, classes="cz-lead-photo")],
            width=px(42, "%"), width_tablet=px(100, "%"), overflow="hidden", border_radius=dims(20),
            css_classes="cz-ph-wrap"),
        lead_info,
    ], flex_direction_tablet="column", flex_gap=gap(32), flex_gap_tablet=gap(24), padding=dims(14),
        border_radius=dims(28), border_border="solid", border_width=dims(1), border_color="rgba(15, 79, 92, 0.1)",
        margin=dims(56, 0, 24, 0), margin_mobile=dims(40, 0, 20, 0), **bg(WHITE), css_classes="cz-prof")

    team = grid(reveal([teacher_card(*t) for t in TEACHERS]), 3, 2, 1, gap_px=24)

    closing = heading('Mestres, doutores e especialista, <span class="cz-rose">reunidos em uma única '
                      "formação.</span>", "p", TEAL,
                      typo("typography", 30, 800, lh=38, ls=-0.5, size_m=22, lh_m=29), align="center",
                      classes="cz-scrub")
    closing_wrap = col([closing], padding=dims(72, 0, 0, 0), padding_mobile=dims(48, 0, 0, 0))

    return section({**bg(MIST)}, [head, add(lead, classes="cz-rv cz-d0"), team, closing_wrap],
                   "7 · CORPO DOCENTE", "cz-docentes")


# ---------------------------------------------------------------------------
# 8. QUEM É O DR. CICATRIZ
# ---------------------------------------------------------------------------

CREDS = [
    ("fa-user-nurse", "Enfermeiro"),
    ("fa-certificate", "Especialista em Enfermagem Dermatológica com ênfase em Tratamento de Feridas"),
    ("fa-stethoscope", "Estudante de Medicina"),
    ("fa-lightbulb", "Criador do Método Cicatrize 3X"),
]


def build_bio():
    photo_col = col([
        photo("FOTO DO EXPERT (retrato vertical 4:5)", radius=24),
    ], width=px(100, "%"), css_classes="cz-bio-photo cz-io")
    creds = icon_list([{"text": t, "icon": fa(i)} for i, t in CREDS], TEAL,
                      typo("icon_typography", 14, 700, lh=19), icon_color=ROSE, inline=True, icon_size=13,
                      indent=8, space=8, classes="cz-chips")
    left = col([add(photo_col, anim("fadeInLeft")), add(creds, anim("fadeInUp", 200))],
               width=px(42, "%"), width_tablet=px(100, "%"), flex_gap=gap(40), css_classes="cz-par-1")

    right = col([
        add(eyebrow("Quem é o Dr. Cicatriz"), anim("fadeInUp")),
        h2('Eu construí a formação que <span class="cz-rose">eu mesmo não encontrava pronta.</span>', TEAL),
        add(body("<p>Na prática, eu vi profissionais excelentes em feridas perderem o caso por não dominarem a "
                 "podiatria. E vi o contrário: quem entendia de podiatria, mas precisava encaminhar a ferida que "
                 "estava na sua frente — <strong>perdendo o paciente, a autoridade e o honorário.</strong></p>",
                 color=SLATE), anim("fadeInUp", 100)),
        add(body("<p>Nunca encontrei uma formação séria que juntasse os dois mundos com respaldo do MEC. "
                 "<strong class=\"cz-rose\">Então eu criei.</strong></p>", color=SLATE), anim("fadeInUp", 150)),
        add(heading("Eu não terceirizei a minha pós.", "p", TEAL,
                    typo("typography", 26, 800, lh=32, ls=-0.4, size_m=22, lh_m=28), classes="cz-quote"),
            anim("fadeInUp", 200), {"_margin": dims(8, 0, 8, 0)}),
        add(body("<p>Leciono pessoalmente 6 disciplinas e montei um time com titulação real: mestres, doutores e "
                 "especialista em Estomaterapia pela USP.</p>", color=SLATE), anim("fadeInUp", 250)),
        heading("Dr. Cicatriz", "p", ROSE, typo("typography", 54, 700, lh=56, family=SCRIPT, size_m=44),
                classes="cz-sign"),
    ], width=px(58, "%"), width_tablet=px(100, "%"), flex_gap=gap(18))

    return section({**bg(WHITE), "flex_direction": "row", "flex_direction_tablet": "column",
                    "flex_align_items": "center", "flex_gap": gap(80), "flex_gap_tablet": gap(56)},
                   [left, right], "8 · QUEM É O DR. CICATRIZ", "cz-bio")


# ---------------------------------------------------------------------------
# 9. OFERTA DE MEMBRO FUNDADOR
# ---------------------------------------------------------------------------

GETS = [
    "Pós-graduação completa: 17 disciplinas, 400 horas, diploma reconhecido pelo MEC",
    "Encontro ao vivo mensal com o tutor coordenador do curso",
    "Isenção da taxa de matrícula [confirmar]",
    "Acesso vitalício ao conteúdo e às atualizações [confirmar]",
]

BONUS = [
    ("fa-stethoscope", "1º inscrito", "Kit de Enfermagem completo (aparelho de pressão + estetoscópio)", "R$ 677"),
    ("fa-gift", "10 primeiros inscritos", "Kit Cicatrize: biscuit + caneca personalizada", "R$ 150"),
    ("fa-book-medical", "Todos os inscritos até 23h59 do dia 27/10",
     "Livro Guia para Tratamento de Feridas, de Marli Aparecida Joaquim Balan", "R$ 50"),
    ("fa-ticket-alt", "Sorteio entre os inscritos nas primeiras 24h", "Doppler Vascular Portátil", "R$ 1.500"),
]

COUNTDOWN = (
    f'<div class="cz-countdown" data-end="{BONUS_END}" data-over="Os bônus da Aula Magna foram encerrados">'
    '<span class="cz-cd-label">Bônus da Aula Magna encerram em</span>'
    '<div class="cz-cd-grid" role="timer" aria-live="off">'
    '<div><b data-u="d">00</b><small>dias</small></div>'
    '<div><b data-u="h">00</b><small>horas</small></div>'
    '<div><b data-u="m">00</b><small>min</small></div>'
    '<div><b data-u="s">00</b><small>seg</small></div>'
    "</div></div>"
)


def bonus_card(icon_name, who, name, value):
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(14),
        "padding": dims(26, 24, 26, 24),
        "border_radius": dims(20),
        "css_classes": "cz-bonus cz-tilt",
    }, [
        row([icon(icon_name, WHITE, bg=ROSE, size=18, pad=13, radius=12),
             heading(f"<small>valor</small> <s>{value}</s>", "p", WHITE_80,
                     typo("typography", 15, 700, lh=20), align="right", classes="cz-bonus-value",
                     extra={"_flex_size": "grow"})],
            flex_justify_content="space-between", flex_align_items="center"),
        heading(who, "p", ROSE, typo("typography", 12, 800, lh=16, ls=1, transform="uppercase"),
                classes="cz-bonus-who"),
        heading(name, "h4", WHITE, typo("typography", 18, 800, lh=24, size_m=17, lh_m=23)),
    ])


def build_oferta():
    head = col([
        add(eyebrow("Oferta de Membro Fundador", align="center"), anim("fadeInUp")),
        h2('Está aberta a oportunidade, uma única vez, da <span class="cz-rose">turma de Membros '
           "Fundadores.</span>", WHITE, align="center"),
        add(body("<p>Não é uma promoção. É a primeira e única vez que esta pós existe com este preço e este grupo. "
                 "Depois desta turma, quem entrar paga o valor integral, sem bônus e sem isenção de "
                 "matrícula.</p>", color=WHITE_80, align="center"), anim("fadeInUp", 150)),
    ], flex_gap=gap(20), flex_align_items="center", content_width="boxed", boxed_width=px(880))
    head["settings"]["width"] = px(100, "%")

    price = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(14),
        "padding": dims(40, 38, 36, 38),
        "padding_mobile": dims(30, 22, 28, 22),
        "border_radius": dims(28),
        "width": px(52, "%"),
        "width_tablet": px(100, "%"),
        "css_classes": "cz-price",
    }, [
        heading("Membro Fundador", "p", WHITE, typo("typography", 12, 800, lh=14, ls=1.6, transform="uppercase"),
                classes="cz-price-badge"),
        heading("Valor da pós-graduação: <s>R$ 11.800</s>", "p", SLATE, typo("typography", 17, 400, lh=24),
                classes="cz-strike"),
        heading("12x de R$ [valor]", "p", TEAL,
                typo("typography", 52, 900, lh=56, ls=-1.6, size_m=38, lh_m=42),
                classes="cz-big-price", title_nav="Preço parcelado (preencher valor com juros da plataforma)"),
        heading('no cartão ou <span class="cz-rose">R$ 3.500 à vista no Pix</span>', "p", TEAL,
                typo("typography", 20, 800, lh=26, size_m=18, lh_m=24)),
        text("<p>Boleto parcelado e cartão sem comprometer o limite: [confirmar condições]</p>", SLATE,
             typo("typography", 14, 400, lh=21)),
        add(cta(CTA_OFFER, CHECKOUT, full=True), {"_margin": dims(10, 0, 0, 0)}),
        micro("Vagas limitadas. Ao encerrar a turma, o valor volta para R$ 11.800.", "fa-lock", SLATE),
    ])

    gets = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(22),
        "padding": dims(40, 36, 40, 36),
        "padding_mobile": dims(28, 22, 28, 22),
        "border_radius": dims(28),
        "width": px(48, "%"),
        "width_tablet": px(100, "%"),
        "css_classes": "cz-gets",
    }, [
        heading("Tudo o que o Membro Fundador recebe:", "h3", WHITE,
                typo("typography", 24, 800, lh=30, ls=-0.3, size_m=21, lh_m=27)),
        icon_list([{"text": g, "icon": fa("fa-check-circle")} for g in GETS], WHITE,
                  typo("icon_typography", 17, 400, lh=25, size_m=16, lh_m=24), icon_size=20, indent=14,
                  space=18, extra={"icon_self_vertical_align": "start"}),
    ])

    deal = row([add(price, anim("fadeInLeft")), add(gets, anim("fadeInRight", 150))],
               flex_direction_tablet="column", flex_gap=gap(28), flex_align_items="stretch",
               margin=dims(56, 0, 96, 0), margin_mobile=dims(40, 0, 72, 0))

    bonus_head = col([
        heading("Bônus exclusivos da Aula Magna <span class=\"cz-rose\">(27/10)</span>", "h3", WHITE,
                typo("typography", 34, 800, lh=40, ls=-0.6, size_m=26, lh_m=32), align="center",
                classes="cz-split"),
        html_widget(COUNTDOWN, title="Contagem regressiva (data-end)"),
    ], flex_gap=gap(24), flex_align_items="center")
    bonus = grid(reveal([bonus_card(*b) for b in BONUS]), 4, 2, 1, gap_px=18,
                 margin=dims(40, 0, 56, 0))

    return section({**dark_bg(), "flex_align_items": "center", "_element_id": "oferta"},
                   [head, deal, bonus_head, bonus,
                    add(cta(CTA_OFFER, CHECKOUT, align="center"), anim("zoomIn")),
                    add(micro("Vagas limitadas. Ao encerrar a turma, o valor volta para R$ 11.800.", "fa-lock",
                              align="center"), {"_margin": dims(14, 0, 0, 0)})],
                   "9 · OFERTA DE MEMBRO FUNDADOR (#oferta)", "cz-dark cz-oferta")


# ---------------------------------------------------------------------------
# 10. FAQ + CTA FINAL
# ---------------------------------------------------------------------------

FAQ = [
    ("A pós é reconhecida pelo MEC?",
     "Sim. O diploma é emitido pela Faculdade Anhanguera, instituição credenciada pelo MEC."),
    ("Quem pode fazer?", "Profissionais graduados em [confirmar cursos aceitos]."),
    ("As aulas são ao vivo?",
     "As aulas são gravadas e ficam disponíveis para você assistir quando e quantas vezes quiser. Todo mês há um "
     "encontro ao vivo com o tutor coordenador do curso."),
    ("Quando começa e quanto tempo dura?",
     "As aulas começam em novembro de 2026, com uma nova disciplina liberada por mês, em 17 disciplinas e "
     "400 horas."),
    ("Preciso fazer TCC?", "[confirmar]"),
    ("Quais as formas de pagamento?",
     "Cartão de crédito em até 12x, Pix à vista e [confirmar boleto parcelado / cartão sem comprometer o "
     "limite]."),
    ("E se eu entrar depois da turma de fundadores?",
     "Você paga o valor integral de R$ 11.800, sem os bônus da Aula Magna e sem isenção da taxa de matrícula."),
    ("Tenho outra dúvida. Com quem falo?",
     f'Chame nossa equipe no WhatsApp: <a href="{WHATSAPP}" target="_blank" rel="noopener">[link do '
     "atendimento]</a>."),
]


def build_faq():
    help_card = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(14),
        "padding": dims(30, 28, 30, 28),
        "padding_mobile": dims(24, 20, 24, 20),
        "margin": dims(12, 0, 0, 0),
        "border_radius": dims(22),
        **dark_bg(),
        "css_classes": "cz-help",
    }, [
        heading("Ainda com dúvidas?", "h3", WHITE, typo("typography", 24, 800, lh=30, ls=-0.3)),
        body("<p>Chame nossa equipe no WhatsApp e tire suas dúvidas antes de garantir a sua vaga.</p>",
             color=WHITE_80, size=16),
        add(ghost_button("Falar no WhatsApp", WHATSAPP, "fa-whatsapp", dark=True), {"_margin": dims(6, 0, 0, 0)}),
    ])
    side = col([
        add(eyebrow("Perguntas frequentes"), anim("fadeInUp")),
        h2('Tire suas <span class="cz-rose">dúvidas.</span>', TEAL),
        add(help_card, anim("fadeInUp", 200)),
    ], width=px(38, "%"), width_tablet=px(100, "%"), flex_gap=gap(16), css_classes="cz-sticky-col")

    faq_items = [(q, f"<p>{a}</p>") for q, a in FAQ]
    acc = accordion(faq_items, typo("title_typography", 19, 800, lh=26, size_m=17, lh_m=23), "cz-faq-acc", faq=True)
    main = col([add(acc, anim("fadeInUp", 150))], width=px(62, "%"), width_tablet=px(100, "%"))

    return section({**bg(MIST), "flex_direction": "row", "flex_direction_tablet": "column",
                    "flex_align_items": "flex-start", "flex_gap": gap(64), "flex_gap_tablet": gap(36)},
                   [side, main], "10 · PERGUNTAS FREQUENTES", "cz-faq")


def build_final():
    return section({
        **dark_bg(),
        "flex_align_items": "center",
        "flex_gap": gap(22),
        "padding": dims(130, 24, 130, 24),
        "padding_mobile": dims(88, 16, 88, 16),
    }, [
        add(eyebrow("Turma de Membros Fundadores", align="center"), anim("fadeInUp")),
        col([heading('A única pergunta é: <span class="cz-rose">quando VOCÊ vai assumir esse lugar?</span>', "h2",
                     WHITE, typo("typography", 50, 900, lh=58, ls=-1.4, size_t=40, lh_t=48, size_m=31, lh_m=38,
                                 ls_m=-0.6),
                     align="center", classes="cz-split")],
            content_width="boxed", boxed_width=px(900)),
        add(body("<p>Especialização em Tratamento de Feridas e Podiatria, diploma reconhecido pelo MEC e a condição "
                 "exclusiva da primeira turma.</p>", color=WHITE_80, align="center"), anim("fadeInUp", 150)),
        add(cta(align="center"), anim("zoomIn", 250), {"_margin": dims(12, 0, 0, 0)}),
        add(micro("Condição exclusiva da primeira turma. Não vai se repetir.", align="center"), anim("fadeIn", 400)),
    ], "11 · CTA FINAL", "cz-dark cz-final")


def build_footer():
    return container({
        "content_width": "boxed",
        "boxed_width": px(1200),
        "html_tag": "footer",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_justify_content": "space-between",
        "flex_align_items": "center",
        "flex_gap": gap(12),
        "padding": dims(28, 24, 28, 24),
        "padding_mobile": dims(24, 16, 96, 16),  # espaço para o CTA fixo do celular
        **bg(TEAL_DEEP),
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "rgba(255, 255, 255, 0.08)",
        "css_classes": "cz",
    }, [
        heading("© 2026 Método Cicatrize 3X · Pós-graduação em Tratamento de Feridas e Podiatria", "p", WHITE_60,
                typo("typography", 13, 400, lh=19)),
        heading("Diploma emitido pela Faculdade Anhanguera", "p", WHITE_60, typo("typography", 13, 400, lh=19)),
    ], inner=False, title="Rodapé")


# ---------------------------------------------------------------------------

def main():
    content = [
        build_assets(),
        build_hero(),
        build_paradoxo(),
        build_marquee(),
        build_dois_em_um(),
        build_para_quem(),
        build_grade(),
        build_como_funciona(),
        build_docentes(),
        build_bio(),
        build_oferta(),
        build_faq(),
        build_final(),
        build_footer(),
    ]
    data = {
        "content": content,
        "page_settings": {"hide_title": "yes", "template": "elementor_canvas"},
        "version": "0.4",
        "title": "Cicatrize 3X - Pós-graduação (Página de Vendas)",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)} ({_counter[0]} ids)")

    # só o container "⚙ Estilos e animações", para atualizar o CSS/JS numa página já montada
    assets = {"content": [build_assets()], "page_settings": [], "version": "0.4",
              "title": "Cicatrize - Estilos e animações", "type": "container"}
    with open(OUT_ASSETS, "w", encoding="utf-8") as fh:
        json.dump(assets, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT_ASSETS)}")


if __name__ == "__main__":
    main()
