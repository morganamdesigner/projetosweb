#!/usr/bin/env python3
"""Gera o JSON de importação do Elementor para a página "Garatuja" (Colégio Unicultura).

Fonte do design: Figma - arquivo lJJPm2MeiSx9EiGFABkx29, frame 145:5 ("Garatuja", 1920 x 7027).
Saída: ../garatuja-elementor.json (formato de template exportado pelo Elementor, version 0.4).

Uso:  python3 build_elementor_json.py
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "garatuja-elementor.json")
OUT_NAV = os.path.join(HERE, "..", "garatuja-menu-navbar.json")
CSS_FILE = os.path.join(HERE, "gt-page.css")

# ---------------------------------------------------------------------------
# Tokens do Figma
# ---------------------------------------------------------------------------
NAVY = "#010658"        # texto/fundos principais
NAVY_2 = "#020659"      # hero, card Educação Infantil, botões
NAVY_3 = "#1B1F76"      # card Ensino Fundamental
NAVY_HEAD = "#010558"   # título "Duas etapas"
YELLOW = "#F2CA50"
PAGE_BG = "#EEEFF4"     # fundo do topo (amostrado do render; ver README)
WHITE = "#FFFFFF"

HANKEN = "Hanken Grotesk"
DMSANS = "DM Sans"
INTER = "Inter"

PLACEHOLDER = "https://example.com/substituir-asset-figma/{}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"garatuja-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    linked = top == right == bottom == left
    return {
        "unit": unit,
        "top": str(top),
        "right": str(right),
        "bottom": str(bottom),
        "left": str(left),
        "isLinked": linked,
    }


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def typo(prefix, family, size, weight, lh=None, ls=None, transform=None, style=None,
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
    """Anula os valores globais padrão (kit) dos controles de cor/tipografia definidos,
    como o Elementor faz ao exportar um widget com estilos customizados."""
    g = {}
    for k in settings:
        if k.endswith("_typography") or k.endswith("color") or k.endswith("_color_b"):
            if not k.endswith("_tablet") and not k.endswith("_mobile"):
                g[k] = ""
    if g:
        settings["__globals__"] = g
    return settings


def container(settings, children, inner=True):
    base = {
        "flex_gap": gap(0),
        "padding": dims(0),
    }
    base.update(settings)
    return {
        "id": new_id(),
        "elType": "container",
        "isInner": inner,
        "settings": _globals(base),
        "elements": children,
    }


def widget(widget_type, settings):
    return {
        "id": new_id(),
        "elType": "widget",
        "isInner": False,
        "widgetType": widget_type,
        "settings": _globals(settings),
        "elements": [],
    }


def link(url=""):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def image_setting(filename, alt):
    return {"url": PLACEHOLDER.format(filename), "id": "", "size": "", "alt": alt}


# ---------------------------------------------------------------------------
# Animações
# ---------------------------------------------------------------------------

def anim(name, delay=0, duration="fast"):
    """Entrance Animation nativa (widgets usam prefixo "_", containers não).
    As distâncias/escala de fadeInUp, fadeInLeft e zoomIn são suavizadas no CSS (gt-page.css)."""
    return {"__anim__": (name, delay, duration)}


def parallax(speed=1):
    """Elementor Pro > Motion Effects > Scrolling Effects > Vertical Scroll (só desktop)."""
    return {
        "motion_fx_motion_fx_scrolling": "yes",
        "motion_fx_translateY_effect": "yes",
        "motion_fx_translateY_speed": px(speed),
        "motion_fx_translateY_affectedRange": {"unit": "%", "size": "", "sizes": {"start": 0, "end": 100}},
        "motion_fx_devices": ["desktop"],
    }


def add(el, *parts, classes=""):
    """Acrescenta configurações (animação, efeitos, classes) a um elemento já criado."""
    is_widget = el["elType"] == "widget"
    for part in parts:
        part = dict(part)
        if "__anim__" in part:
            name, delay, duration = part.pop("__anim__")
            prefix = "_" if is_widget else ""
            el["settings"][f"{prefix}animation"] = name
            el["settings"]["animation_duration"] = duration
            if delay:
                el["settings"][f"{prefix}animation_delay"] = delay
        el["settings"].update(part)
    if classes:
        key = "_css_classes" if is_widget else "css_classes"
        el["settings"][key] = (el["settings"].get(key, "") + " " + classes).strip()
    return el


# ---------------------------------------------------------------------------
# Widgets reutilizáveis
# ---------------------------------------------------------------------------

def heading(title, tag, color, typography, align="left", extra=None):
    s = {"title": title, "header_size": tag, "align": align, "title_color": color}
    s.update(typography)
    if extra:
        s.update(extra)
    return widget("heading", s)


def text(html, color, typography, align="left", extra=None):
    s = {"editor": html, "align": align, "text_color": color}
    s.update(typography)
    if extra:
        s.update(extra)
    return widget("text-editor", s)


def button(label, bg, color, typography, padding, radius="999", shadow=None, icon=False,
           css_classes="", extra=None, gradient=None, align="left"):
    s = {
        "text": label,
        "link": link(),
        "align": align,
        "size": "md",
        "button_text_color": color,
        "hover_color": color,
        "text_padding": padding,
        "border_radius": dims(radius),
    }
    if gradient:
        s.update({
            "background_background": "gradient",
            "background_color": gradient[0],
            "background_color_stop": px(0, "%"),
            "background_color_b": gradient[1],
            "background_color_b_stop": px(100, "%"),
            "background_gradient_type": "linear",
            "background_gradient_angle": px(90, "deg"),
            "button_background_hover_background": "gradient",
            "button_background_hover_color": gradient[0],
            "button_background_hover_color_b": gradient[1],
            "button_background_hover_gradient_angle": px(90, "deg"),
        })
    else:
        s.update({
            "background_background": "classic",
            "background_color": bg,
            "button_background_hover_background": "classic",
            "button_background_hover_color": bg,
        })
    s.update(typography)
    if shadow:
        s["button_box_shadow_box_shadow_type"] = "yes"
        s["button_box_shadow_box_shadow"] = shadow
    if icon:
        s.update({
            "selected_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
            "icon_align": "right",
            "icon_indent": px(icon if isinstance(icon, (int, float)) and icon is not True else 12),
        })
    if css_classes:
        s["_css_classes"] = css_classes
    if extra:
        s.update(extra)
    return widget("button", s)


def social_icons(extra=None):
    items = []
    for value, label in (("fab fa-facebook-f", "Facebook"),
                         ("fab fa-instagram", "Instagram"),
                         ("fab fa-linkedin-in", "LinkedIn")):
        items.append({
            "_id": new_id(),
            "social_icon": {"value": value, "library": "fa-brands"},
            "link": link(),
            "item_icon_color": "default",
        })
    s = {
        "social_icon_list": items,
        "shape": "rounded",
        "align": "left",
        "icon_color": "custom",
        "icon_primary_color": YELLOW,
        "icon_secondary_color": NAVY,
        "icon_size": px(10),
        "icon_padding": px(0.9, "em"),
        "icon_spacing": px(12.3),
        "border_radius": dims(10),
        "image_border_border": "solid",
        "image_border_width": dims(0.77),
        "image_border_color": "rgba(1, 6, 88, 0.14)",
    }
    if extra:
        s.update(extra)
    return widget("social-icons", s)


def icon_list(items, typography, text_color, icon_color=None, inline=False, space=12,
              icon_size=14, text_indent=12, extra=None):
    lst = []
    for it in items:
        if isinstance(it, str):
            it = {"text": it}
        lst.append({
            "_id": new_id(),
            "text": it["text"],
            "selected_icon": it.get("icon", {"value": "", "library": ""}),
            "link": link(it.get("url", "")),
        })
    s = {
        "view": "inline" if inline else "traditional",
        "icon_list": lst,
        "space_between": px(space),
        "text_color": text_color,
        "text_color_hover": text_color,
        "icon_size": px(icon_size),
        "text_indent": px(text_indent),
    }
    if icon_color:
        s["icon_color"] = icon_color
        s["icon_color_hover"] = icon_color
    s.update(typography)
    if extra:
        s.update(extra)
    return widget("icon-list", s)


def image(filename, alt, width_px=None, height=None, radius=None, extra=None):
    s = {
        "image": image_setting(filename, alt),
        "image_size": "full",
        "align": "left",
        "link_to": "none",
        "width": px(100, "%"),
    }
    if height is not None:
        s["height"] = px(height)
        s["object-fit"] = "cover"
        s["object-position"] = "center center"
    if radius is not None:
        s["image_border_radius"] = dims(radius)
    if width_px is not None:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = px(width_px)
    if extra:
        s.update(extra)
    return widget("image", s)


# ---------------------------------------------------------------------------
# 1. TOPO (fundo cinza): HERO + "Duas etapas"
# ---------------------------------------------------------------------------

def build_top():
    # --- Recorte superior esquerdo com os logos -------------------------------
    notch_tl = container({
        "content_width": "full",
        "width": px(435),
        "width_tablet": px(435),
        "width_mobile": px(210),
        "min_height": px(85),
        "min_height_mobile": px(56),
        "flex_direction": "row",
        "flex_align_items": "flex-end",
        "flex_gap": gap(10),
        "flex_gap_mobile": gap(8),
        "padding": dims(0, 0, 21, 175),
        "padding_tablet": dims(0, 0, 21, 40),
        "padding_mobile": dims(0, 0, 8, 16),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-notch gt-notch--tl",
    }, [
        image("logo-colegio-unicultura.svg", "Colégio Unicultura", width_px=123,
              extra={"_element_custom_width_mobile": px(86), "_flex_align_self": "flex-start"}),
        image("logo-garatuja.png", "Garatuja - Educação Infantil e Fundamental I", width_px=99,
              extra={"_element_custom_width_mobile": px(70)}),
    ])

    # --- Navbar (vidro) ---------------------------------------------------------
    # Espaço para os logos que aparecem SÓ quando o menu fica fixo (após o scroll).
    # Ficam ocultos no topo da página e visíveis no editor para permitir trocar as imagens.
    nav_logos = container({
        "content_width": "full",
        "width": px(172),
        "flex_direction": "row",
        "flex_justify_content": "flex-start",
        "flex_align_items": "center",
        "flex_gap": gap(14),
        "_flex_size": "none",
        "css_classes": "gt-navbar-logos",
    }, [
        image("logo-colegio-unicultura-menu.svg", "Colégio Unicultura", width_px=77),
        image("logo-garatuja-menu.png", "Garatuja - Educação Infantil e Fundamental I", width_px=81),
    ])
    nav_links = icon_list(
        ["Home", "Unicultura", "Garatuja", "Diferenciais", "Parceiros", "Contato"],
        typo("icon_typography", DMSANS, 13, 700, lh=17.315),
        WHITE, inline=True, space=24, text_indent=0,
        extra={
            "space_between_mobile": px(16),
            "_margin": dims(0, 10, 0, 0),
            "_margin_mobile": dims(0),
            "icon_align": "left",
            "icon_align_mobile": "center",
            "_flex_size": "none",
        },
    )
    nav_social = social_icons(extra={"_flex_size": "none"})
    nav_cta = button(
        "Matricule-se", WHITE, NAVY,
        typo("typography", DMSANS, 10.004, 700, lh=15.007),
        dims(8.66, 12.3, 8.66, 16.87),
        radius="769",
        shadow={"horizontal": 0, "vertical": 1.539, "blur": 3.078, "spread": 0, "color": YELLOW},
        icon=7,
        css_classes="gt-btn-arrow gt-btn-arrow--light",
        extra={"_flex_size": "none"},
    )
    navbar = container({
        "content_width": "full",
        "html_tag": "nav",
        "width": px(803),
        "width_tablet": px(100, "%"),
        "min_height": px(72),
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_justify_content": "flex-start",
        "flex_justify_content_tablet": "space-between",
        "flex_align_items": "center",
        "flex_wrap_mobile": "wrap",
        "flex_gap": gap(12.3),
        "flex_gap_mobile": gap(14),
        "padding": dims(0, 39, 0, 96),
        "padding_tablet": dims(0, 24, 0, 24),
        "padding_mobile": dims(16),
        "_flex_align_self": "flex-end",
        "_flex_align_self_tablet": "stretch",
        "background_background": "classic",
        "background_color": "rgba(2, 6, 89, 0.02)",
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(255, 255, 255, 0.11)",
        "border_radius": dims(40),
        "border_radius_mobile": dims(24),
        "css_classes": "gt-navbar",
        # Elementor Pro > Sticky: a navbar acompanha o scroll (desktop e tablet).
        # Após 40px de scroll o Pro adiciona .elementor-sticky--effects, usado no CSS
        # para escurecer o vidro, centralizar o menu e mostrar os logos.
        "sticky": "top",
        "sticky_on": ["desktop", "tablet"],
        "sticky_offset": 16,
        "sticky_effects_offset": 40,
    }, [nav_logos, nav_links, nav_social, nav_cta])

    # --- Conteúdo do hero ---------------------------------------------------
    hero_tag = heading(
        "Educação Infantil ao 2º ano - Fundamental", "p", NAVY,
        typo("typography", DMSANS, 15, 600, lh=14.324, ls=0.7639, transform="uppercase",
             size_t=14, size_m=11, lh_m=14, ls_m=0.4),
        extra={
            "_element_width": "auto",
            "_background_background": "classic",
            "_background_color": YELLOW,
            "_border_radius": dims(795),
            "_padding": dims(4.77, 14.8, 4.91, 14.8),
            "_padding_mobile": dims(5, 10, 5, 10),
        },
    )
    hero_h1 = heading(
        'Onde começam as <span style="color:#F2CA50">grandes descobertas</span>', "h1", WHITE,
        typo("typography", HANKEN, 55, 700, lh=51.7, ls=-2.75,
             size_t=48, size_m=36, lh_t=46, lh_m=36, ls_m=-1.5),
        extra={"_element_width": "initial", "_element_custom_width": px(537),
               "_element_custom_width_mobile": px(100, "%")},
    )
    hero_p = text(
        "<p>Brincar, imaginar, perguntar, experimentar, criar, conviver e descobrir. Aqui é onde a "
        "jornada escolar do seu filho começa — com acolhimento, curiosidade e muita intencionalidade "
        "pedagógica.</p>",
        WHITE,
        typo("typography", HANKEN, 17, 300, lh=21.879, size_m=16, lh_m=22),
        extra={"_element_width": "initial", "_element_custom_width": px(445),
               "_element_custom_width_mobile": px(100, "%")},
    )
    hero_btn = button(
        "Agendar uma visita", None, NAVY,
        typo("typography", HANKEN, 19, 500, lh=16, ls=-0.1, size_m=17),
        dims(30, 46.5, 30, 46.5),
        radius="8888",
        gradient=("#FFE900", "#FBBC04"),
        shadow={"horizontal": 0, "vertical": 4, "blur": 30, "spread": 0, "color": "rgba(253, 211, 3, 0.3)"},
        extra={"text_padding_mobile": dims(24, 36, 24, 36)},
    )
    hero_content = container({
        "content_width": "full",
        "width": px(570),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(22),
        "flex_gap_mobile": gap(18),
        "margin": dims(146, 0, 0, 0),
        "margin_tablet": dims(90, 0, 0, 0),
        "margin_mobile": dims(40, 0, 0, 0),
    }, [
        add(hero_tag, anim("fadeInUp")),
        add(hero_h1, anim("fadeInUp", 120)),
        add(hero_p, anim("fadeInUp", 240)),
        add(hero_btn, anim("fadeInUp", 360), classes="gt-btn-shine"),
    ])

    # --- Recorte inferior direito (decorativo) ------------------------------
    notch_br = container({
        "content_width": "full",
        "width": px(180),
        "min_height": px(100),
        "padding": dims(0),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-notch gt-notch--br",
        "hide_mobile": "hidden-mobile",
    }, [])

    hero = container({
        "content_width": "full",
        "html_tag": "header",
        "width": px(100, "%"),
        "min_height": px(768),
        "min_height_tablet": px(0),
        "min_height_mobile": px(0),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(0),
        "padding": dims(19, 178, 172, 173),
        "padding_tablet": dims(105, 24, 120, 40),
        "padding_mobile": dims(72, 16, 40, 20),
        "overflow": "hidden",
        # cantos sob os recortes ficam retos (evita linha de antialiasing)
        "border_radius": dims(0, 40, 0, 40),
        "border_radius_mobile": dims(0, 24, 24, 24),
        "background_background": "classic",
        "background_color": NAVY_2,
        "background_image": image_setting("hero-firefly-6.jpg", "Criança sorrindo em sala de aula da Garatuja"),
        "background_position": "initial",
        "background_xpos": px(-8),
        "background_ypos": px(-201),
        "background_repeat": "no-repeat",
        "background_size": "initial",
        "background_bg_width": px(123, "%"),
        "background_position_tablet": "center right",
        "background_size_tablet": "cover",
        "background_position_mobile": "center center",
        "background_size_mobile": "cover",
        "background_overlay_background": "gradient",
        "background_overlay_color": "#060720",
        "background_overlay_color_stop": px(0, "%"),
        "background_overlay_color_b": "rgba(1, 6, 88, 0)",
        "background_overlay_color_b_stop": px(52.108, "%"),
        "background_overlay_color_b_stop_tablet": px(80, "%"),
        "background_overlay_color_b_stop_mobile": px(130, "%"),
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": px(90, "deg"),
        "background_overlay_opacity": px(1),
        "css_classes": "gt-hero",
    }, [notch_tl, navbar, hero_content, notch_br])

    # --- Seção "Duas etapas, uma transição cuidada" --------------------------
    duas_title = heading(
        'Duas etapas, uma <span class="gt-highlight">transição cuidada</span>', "h2", NAVY_HEAD,
        typo("typography", HANKEN, 62, 700, lh=66, ls=-3.1,
             size_t=52, size_m=38, lh_t=58, lh_m=46, ls_m=-1.5),
        extra={
            "_element_width": "initial",
            "_element_custom_width": px(500),
            "_element_custom_width_tablet": px(100, "%"),
            "_padding": dims(0, 0, 0, 17),
            "_padding_mobile": dims(0, 0, 0, 10),
        },
    )
    duas_text = text(
        "<p>Nossa proposta contempla a Educação Infantil e o 1º e 2º anos do Ensino Fundamental — Anos "
        "Iniciais. Cada etapa tem seus próprios objetivos, respeitando o desenvolvimento da criança e "
        "garantindo uma transição cuidadosa e progressiva entre elas.</p>",
        NAVY_2,
        typo("typography", HANKEN, 18, 400, lh=25.2, ls=-0.1, size_m=16, lh_m=24),
    )
    duas_btn = button(
        "Agendar visita", NAVY_2, WHITE,
        typo("typography", DMSANS, 14.115, 700, lh=21.173),
        dims(13.9, 28.6, 13.9, 28.4),
        radius="881",
        shadow={"horizontal": 0, "vertical": 1.764, "blur": 3.529, "spread": 0, "color": "rgba(241, 5, 5, 0.2)"},
        icon=11.8,
        css_classes="gt-btn-arrow",
    )
    duas_right = container({
        "content_width": "full",
        "width": px(504),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(38),
        "flex_gap_mobile": gap(28),
    }, [duas_text, duas_btn])
    duas = container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(1048),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_justify_content": "space-between",
        "flex_align_items": "center",
        "flex_align_items_tablet": "flex-start",
        "flex_gap": gap(40),
        "flex_gap_mobile": gap(28),
        "padding": dims(129, 0, 137, 0),
        "padding_tablet": dims(80, 20, 90, 20),
        "padding_mobile": dims(56, 4, 64, 4),
    }, [
        # a animação de entrada também dispara o "desenho" da faixa amarela (CSS .animated .gt-highlight)
        add(duas_title, anim("fadeIn")),
        add(duas_right, anim("fadeInUp", 150)),
    ])

    return container({
        "content_width": "boxed",
        "boxed_width": px(1480),
        "flex_direction": "column",
        "flex_gap": gap(0),
        "padding": dims(27, 20, 0, 20),
        "padding_mobile": dims(12, 12, 0, 12),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root gt-top",
    }, [hero, duas], inner=False)


# ---------------------------------------------------------------------------
# 2. ETAPAS (fundo amarelo): Educação Infantil + 1º e 2º anos
# ---------------------------------------------------------------------------

def check_item(label, delay=0):
    return add(container({
        "content_width": "full",
        "min_height": px(71.59),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "padding": dims(0, 18, 0, 18),
        "padding_mobile": dims(14, 18, 14, 18),
        "background_background": "classic",
        "background_color": WHITE,
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(1, 6, 88, 0.32)",
        "border_radius": dims(12),
    }, [
        icon_list(
            [{"text": label, "icon": {"value": "far fa-dot-circle", "library": "fa-regular"}}],
            typo("icon_typography", INTER, 14, 400, lh=19.6, ls=-0.1),
            NAVY, icon_color=YELLOW, icon_size=16, text_indent=11,
        ),
    ]), anim("fadeInUp", delay))


def check_grid(labels):
    return container({
        "content_width": "full",
        "container_type": "grid",
        "width": px(100, "%"),
        "grid_columns_grid": px(2, "fr"),
        "grid_columns_grid_mobile": px(1, "fr"),
        "grid_rows_grid": px(len(labels) // 2, "fr"),
        "grid_rows_grid_mobile": px(len(labels), "fr"),
        "grid_gaps": {"column": "16", "row": "16", "isLinked": True, "unit": "px"},
        "grid_auto_flow": "row",
    }, [check_item(l, (i // 2) * 80 + (i % 2) * 40) for i, l in enumerate(labels)])


def eyebrow(label):
    return add(heading(
        label, "p", YELLOW,
        typo("typography", INTER, 12, 700, lh=12, ls=1.4, transform="uppercase"),
    ), anim("fadeInUp"))


def etapa_title(html, lh):
    return add(heading(
        html, "h2", WHITE,
        typo("typography", HANKEN, 60, 600, lh=lh, ls=-2.4,
             size_t=48, size_m=36, lh_t=50, lh_m=38, ls_m=-1.4),
    ), anim("fadeInUp", 100))


def etapa_text(html):
    return add(text(html, WHITE, typo("typography", HANKEN, 18, 400, lh=25.2, ls=-0.1, size_m=16, lh_m=24)),
               anim("fadeInUp", 200))


def build_etapas():
    # --- Card 1: Educação Infantil -----------------------------------------
    infantil_col = container({
        "content_width": "full",
        "width": px(566),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(26),
        "flex_gap_mobile": gap(20),
        "margin": dims(18, 0, 0, 0),
        "margin_tablet": dims(0),
    }, [
        eyebrow("Educação Infantil"),
        etapa_title('Infância é tempo de <span style="color:#F2CA50">descobrir</span>', 53),
        etapa_text(
            "<p>Na Educação Infantil, entendemos a criança como protagonista do próprio processo de "
            "aprendizagem. Nossa proposta respeita os direitos de aprendizagem previstos pela BNCC — "
            "conviver, brincar, participar, explorar, expressar-se e conhecer-se — e transforma o "
            "cotidiano em oportunidades de desenvolvimento.</p>"),
        check_grid([
            "Identidade e autonomia", "Linguagem oral",
            "Aproximação com a cultura escrita", "Pensamento lógico",
            "Coordenação motora", "Criatividade e expressão artística",
            "Desenvolvimento socioemocional", "Interação e convivência",
            "Investigação e curiosidade", "Contato com a literatura",
        ]),
    ])
    card_infantil = container({
        "content_width": "full",
        "html_tag": "section",
        "width": px(100, "%"),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_justify_content": "center",
        "flex_align_items": "flex-start",
        "flex_gap": gap(33),
        "flex_gap_tablet": gap(40),
        "flex_gap_mobile": gap(28),
        "padding": dims(119, 20, 189, 20),
        "padding_tablet": dims(64, 40, 169, 40),
        "padding_mobile": dims(24, 16, 153, 16),
        "background_background": "classic",
        "background_color": NAVY_2,
        "border_radius": dims(40),
        "border_radius_mobile": dims(24),
    }, [
        add(image("img-1142-educacao-infantil.jpg", "Menino brincando com massinha em atividade da Educação Infantil",
              width_px=541, height=812, radius=20,
              extra={"_element_custom_width_tablet": px(100, "%"),
                     "height_tablet": px(560), "height_mobile": px(380)}),
            anim("fadeIn"), parallax(1)),
        infantil_col,
    ])

    # --- Card 2: 1º e 2º anos do Ensino Fundamental --------------------------
    fundamental_col = container({
        "content_width": "full",
        "width": px(566),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(20),
    }, [
        eyebrow("1º e 2º anos do Ensino Fundamental"),
        etapa_title('Das descobertas às primeiras grandes <span style="color:#F2CA50">aprendizagens</span>', 58),
        etapa_text(
            "<p>A entrada no Ensino Fundamental é uma transformação importante. Acolhemos essa transição "
            "com cuidado, garantindo continuidade entre as experiências vividas na Educação Infantil e os "
            "novos desafios acadêmicos — um período especialmente importante para a alfabetização, o "
            "letramento e o raciocínio lógico-matemático.</p>"),
        check_grid([
            "Alfabetização e letramento", "Leitura e interpretação",
            "Produção escrita", "Raciocínio lógico-matemático",
            "Investigação e iniciação científica", "Formação do hábito de estudo",
            "Literatura e criatividade", "Autonomia e responsabilidade",
            "Desenvolvimento socioemocional", "Educação financeira e empreendedora",
            "Língua inglesa", "Tecnologia e robótica",
        ]),
    ])
    card_fundamental = container({
        "content_width": "full",
        "html_tag": "section",
        "width": px(100, "%"),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_justify_content": "center",
        "flex_align_items": "flex-start",
        "flex_gap": gap(35),
        "flex_gap_tablet": gap(40),
        "flex_gap_mobile": gap(28),
        "margin": dims(-121, 0, 0, 0),
        "padding": dims(134, 20, 78, 20),
        "padding_tablet": dims(64, 40, 64, 40),
        "padding_mobile": dims(36, 16, 32, 16),
        "background_background": "classic",
        "background_color": NAVY_3,
        "border_border": "solid",
        "border_width": dims(5, 0, 0, 0),
        "border_color": YELLOW,
        "border_radius": dims(40),
        "border_radius_mobile": dims(24),
    }, [
        fundamental_col,
        add(image("img-1142-ensino-fundamental.jpg", "Crianças do 1º e 2º anos em atividade em sala de aula",
              width_px=541, height=812, radius=20,
              extra={"_element_custom_width_tablet": px(100, "%"),
                     "height_tablet": px(560), "height_mobile": px(380),
                     "_margin": dims(36, 0, 0, 0), "_margin_tablet": dims(0)}),
            anim("fadeIn"), parallax(1)),
    ])

    etapas_btn = button(
        "Agendar visita", NAVY_2, WHITE,
        typo("typography", DMSANS, 18, 700, lh=21.173, size_m=16),
        dims(13.9, 24, 13.9, 37.4),
        radius="881",
        shadow={"horizontal": 0, "vertical": 1.764, "blur": 3.529, "spread": 0, "color": "rgba(241, 5, 5, 0.2)"},
        icon=19,
        css_classes="gt-btn-arrow",
        align="center",
        extra={"_margin": dims(42, 0, 0, 0), "_margin_mobile": dims(32, 0, 0, 0)},
    )

    return container({
        "content_width": "boxed",
        "boxed_width": px(1488),
        "flex_direction": "column",
        "flex_align_items": "stretch",
        "flex_gap": gap(0),
        "padding": dims(51, 24, 74, 24),
        "padding_mobile": dims(24, 12, 48, 12),
        "background_background": "classic",
        "background_color": YELLOW,
        "css_classes": "gt-root gt-etapas",
    }, [card_infantil, card_fundamental, add(etapas_btn, anim("fadeInUp"))], inner=False)


# ---------------------------------------------------------------------------
# 3. GALERIA (4 fotos lado a lado)
# ---------------------------------------------------------------------------

def build_gallery():
    photos = [
        ("espaco-unicultura.jpg", "Corredor da Garatuja com árvore decorativa"),
        ("acesso-facilitado.jpg", "Crianças em atividade de movimento"),
        ("infraestrutura-urbana.jpg", "Duas alunas sorrindo durante atividade"),
        ("comunidade-seleta.jpg", "Espaço de brincar temático com bombeiros"),
    ]
    imgs = [
        add(image(f, alt, height=652, extra={
            "_element_width": "initial",
            "_element_custom_width": px(25, "%"),
            "_element_custom_width_tablet": px(50, "%"),
            "_element_custom_width_mobile": px(50, "%"),
            "height_tablet": px(480),
            "height_mobile": px(240),
        }), anim("fadeIn", i * 100), classes="gt-zoom") for i, (f, alt) in enumerate(photos)
    ]
    return container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_wrap": "wrap",
        "flex_gap": gap(0),
        "padding": dims(0),
        "css_classes": "gt-root gt-galeria",
    }, imgs, inner=False)


# ---------------------------------------------------------------------------
# 4. EXPERIÊNCIAS (fundo azul)
# ---------------------------------------------------------------------------

def exp_card(i, icon, title, desc):
    box = widget("icon-box", {
        "selected_icon": icon,
        "view": "stacked",
        "shape": "rounded",
        "title_text": title,
        "description_text": desc,
        "title_size": "h3",
        "text_align": "center",
        "primary_color": YELLOW,
        "secondary_color": NAVY,
        "icon_space": px(33),
        "icon_size": px(30),
        "icon_padding": px(17),
        "border_radius": dims(14),
        "title_bottom_space": px(18),
        "title_color": NAVY,
        **typo("title_typography", HANKEN, 25, 700, lh=21.38, ls=-0.1, size_m=22, lh_m=26),
        "description_color": NAVY,
        **typo("description_typography", HANKEN, 15, 400, lh=21, ls=-0.1),
    })
    return add(container({
        "content_width": "full",
        "min_height": px(272.75),
        "min_height_mobile": px(0),
        "flex_direction": "column",
        "flex_align_items": "stretch",
        "padding": dims(32, 21, 21, 21),
        "padding_mobile": dims(28, 20, 28, 20),
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dims(16),
    }, [box]), anim("fadeInUp", (i % 3) * 120 + (i // 3) * 80), classes="gt-card-hover")


def build_experiencias():
    title = heading(
        'Experiências que enriquecem <span style="color:#F2CA50;font-weight:700">a aprendizagem</span>',
        "h2", WHITE,
        typo("typography", HANKEN, 40, 400, lh=48, ls=-1.6, size_m=32, lh_m=38, ls_m=-1.2),
        align="center",
        extra={"_element_width": "initial", "_element_custom_width": px(498),
               "_element_custom_width_mobile": px(100, "%")},
    )
    cards = [
        exp_card(0, {"value": "fas fa-brain", "library": "fa-solid"}, "Educação Criativa",
                 "Experiências que estimulam imaginação, autoria, expressão, experimentação e diferentes "
                 "maneiras de solucionar problemas."),
        exp_card(1, {"value": "fas fa-language", "library": "fa-solid"}, "Sistema Bilíngue",
                 "Contato progressivo e significativo com a língua inglesa, ampliando comunicação, "
                 "repertório cultural e possibilidades de interação com o mundo."),
        exp_card(2, {"value": "fas fa-robot", "library": "fa-solid"}, "Robótica Educacional",
                 "Experiências baseadas em tecnologia, Cultura Maker e resolução de problemas, "
                 "desenvolvendo raciocínio lógico, criatividade e pensamento computacional."),
        exp_card(3, {"value": "far fa-heart", "library": "fa-regular"}, "Educação Abrangente",
                 "Desenvolvimento do autoconhecimento, das relações, da responsabilidade, do planejamento, "
                 "da criatividade, da tomada de decisões e do protagonismo."),
        exp_card(4, {"value": "fas fa-cubes", "library": "fa-solid"}, "Projetos Pedagógicos",
                 "Propostas que conectam diferentes áreas do conhecimento e permitem que as crianças "
                 "pesquisem, experimentem, construam e compartilhem suas descobertas."),
        exp_card(5, {"value": "fas fa-volleyball-ball", "library": "fa-solid"}, "Escola de Esportes",
                 "O movimento integra a formação da criança, contribuindo para o desenvolvimento físico, "
                 "social e emocional."),
    ]
    grid = container({
        "content_width": "full",
        "container_type": "grid",
        "width": px(1129),
        "width_tablet": px(100, "%"),
        "grid_columns_grid": px(3, "fr"),
        "grid_columns_grid_tablet": px(2, "fr"),
        "grid_columns_grid_mobile": px(1, "fr"),
        "grid_rows_grid": px(2, "fr"),
        "grid_rows_grid_tablet": px(3, "fr"),
        "grid_rows_grid_mobile": px(6, "fr"),
        "grid_gaps": {"column": "32", "row": "21.5", "isLinked": False, "unit": "px"},
        "grid_gaps_mobile": {"column": "16", "row": "16", "isLinked": True, "unit": "px"},
        "grid_auto_flow": "row",
    }, cards)
    btn = button(
        "Agendar uma visita", None, NAVY,
        typo("typography", HANKEN, 19, 500, lh=16, ls=-0.1, size_m=17),
        dims(30, 46.5, 30, 46.5),
        radius="8888",
        gradient=("#FFE900", "#FBBC04"),
        shadow={"horizontal": 0, "vertical": 4, "blur": 30, "spread": 0, "color": "rgba(253, 211, 3, 0.3)"},
        align="center",
        extra={"_margin": dims(4, 0, 0, 0), "text_padding_mobile": dims(24, 36, 24, 36)},
    )
    return container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(1129),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(40),
        "flex_gap_mobile": gap(32),
        "padding": dims(108, 24, 4, 24),
        "padding_tablet": dims(80, 24, 4, 24),
        "padding_mobile": dims(64, 16, 4, 16),
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "gt-root gt-experiencias",
    }, [
        add(title, anim("fadeInUp")),
        grid,
        add(btn, anim("fadeInUp"), classes="gt-btn-shine"),
    ], inner=False)


# ---------------------------------------------------------------------------
# 5. "E DEPOIS DA GARATUJA?" (fundo branco + curva azul no topo)
# ---------------------------------------------------------------------------

def build_depois():
    lion = image("leao-unicultura.svg", "Leão, símbolo do Colégio Unicultura", width_px=462,
                 extra={"_element_custom_width_tablet": px(320), "_element_custom_width_mobile": px(200),
                        "_flex_size": "none"})
    col = container({
        "content_width": "full",
        "width": px(593),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_align_items_tablet": "center",
        "flex_gap": gap(20),
    }, [
        heading("E depois da Garatuja?", "h2", NAVY,
                typo("typography", HANKEN, 62, 700, lh=66, ls=-3.1,
                     size_t=52, size_m=36, lh_t=58, lh_m=40, ls_m=-1.5),
                extra={"align_tablet": "center"}),
        text("<p>A jornada não para no 2º ano. A partir do 3º ano do Ensino Fundamental, seu filho segue "
             "crescendo — com a mesma essência, novos desafios — no Colégio Unicultura.</p>",
             NAVY,
             typo("typography", HANKEN, 30, 300, lh=1.25, style="italic",
                  size_t=26, size_m=20, lh_unit="em"),
             extra={"_element_width": "initial", "_element_custom_width": px(535),
                    "_element_custom_width_tablet": px(100, "%"), "align_tablet": "center"}),
    ])
    return container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(1148),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_justify_content": "flex-start",
        "flex_align_items": "center",
        "flex_gap": gap(40),
        "flex_gap_mobile": gap(32),
        "padding": dims(97, 24, 54, 24),
        "padding_tablet": dims(96, 24, 64, 24),
        "padding_mobile": dims(64, 16, 56, 16),
        "background_background": "classic",
        "background_color": WHITE,
        "shape_divider_top": "curve",
        "shape_divider_top_color": NAVY,
        "shape_divider_top_width": px(104, "%"),
        "shape_divider_top_height": px(66),
        "shape_divider_top_height_mobile": px(28),
        "css_classes": "gt-root gt-depois",
    }, [
        add(lion, anim("zoomIn"), classes="gt-lion"),
        add(col, anim("fadeInUp", 150)),
    ], inner=False)


# ---------------------------------------------------------------------------
# 6. CTA com formulário (fundo amarelo)
# ---------------------------------------------------------------------------

def build_cta():
    quote = container({
        "content_width": "full",
        "width": px(335),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(9.71),
        "padding": dims(19.42, 24.275, 19.42, 24.275),
        "background_background": "classic",
        "background_color": "rgba(1, 6, 88, 0.77)",
        "border_radius": dims(19.42),
        "css_classes": "gt-glass",
        "animation": "fadeInLeft",
        "animation_duration": "fast",
        "animation_delay": 450,
    }, [
        text("<p>\"A melhor decisão que tomamos pela nossa família foi escolher a Garatuja\"</p>",
             "rgba(255, 255, 255, 0.9)", typo("typography", DMSANS, 15.779, 400, lh=23.668)),
        text("<p>— Família Mendes, turma 2025</p>",
             YELLOW, typo("typography", DMSANS, 14.565, 700, lh=21.848)),
    ])
    left = container({
        "content_width": "full",
        "width": px(516),
        "width_tablet": px(50, "%"),
        "width_mobile": px(100, "%"),
        "min_height": px(463),
        "min_height_mobile": px(420),
        "flex_direction": "column",
        "flex_justify_content": "flex-end",
        "flex_align_items": "flex-start",
        "padding": dims(24),
        "padding_mobile": dims(16),
        "_flex_size": "none",
        "background_background": "classic",
        "background_color": "#1B4FD9",
        "background_image": image_setting("cta-crianca-sorrindo.jpg", "Menino sorrindo com uniforme da Garatuja"),
        "background_position": "initial",
        "background_xpos": px(50, "%"),
        "background_ypos": px(35, "%"),
        "background_repeat": "no-repeat",
        "background_size": "cover",
    }, [quote])

    form = widget("form", {
        "form_name": "Agendar visita - Garatuja",
        "form_fields": [
            {"_id": new_id(), "custom_id": "name", "field_type": "text", "field_label": "Nome completo",
             "placeholder": "Seu nome completo", "required": "true", "width": "100"},
            {"_id": new_id(), "custom_id": "phone", "field_type": "tel", "field_label": "Telefone / WhatsApp",
             "placeholder": "Telefone / WhatsApp", "required": "true", "width": "100"},
        ],
        "show_labels": "",
        "input_size": "md",
        "button_text": "Agendar minha visita",
        "button_size": "md",
        "button_width": "100",
        "button_align": "stretch",
        "selected_button_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
        "button_icon_align": "right",
        "button_icon_indent": px(21),
        "column_gap": px(0),
        "row_gap": px(12),
        "field_text_color": WHITE,
        "field_background_color": "rgba(255, 255, 255, 0.15)",
        "field_border_color": "rgba(255, 255, 255, 0)",
        "field_border_width": dims(0),
        "field_border_radius": dims(999),
        **typo("field_typography", DMSANS, 15, 400, lh=20),
        "button_background_color": WHITE,
        "button_text_color": NAVY,
        "button_background_hover_color": WHITE,
        "button_hover_color": NAVY,
        "button_border_radius": dims(999),
        "button_text_padding": dims(14, 24, 14, 24),
        **typo("button_typography", DMSANS, 15, 700, lh=22.5),
        "button_box_shadow_box_shadow_type": "yes",
        "button_box_shadow_box_shadow": {"horizontal": 0, "vertical": 2, "blur": 4, "spread": 0,
                                          "color": "rgba(245, 140, 40, 0.2)"},
        "_element_width": "initial",
        "_element_custom_width": px(324),
        "_element_custom_width_tablet": px(100, "%"),
        "_css_classes": "gt-form gt-btn-arrow",
    })
    right = container({
        "content_width": "full",
        "width": px(404),
        "width_tablet": px(50, "%"),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(0),
        "padding": dims(87, 13, 48, 40),
        "padding_tablet": dims(48, 24, 40, 32),
        "padding_mobile": dims(36, 20, 36, 20),
        "_flex_size": "grow",
    }, [
        heading('Vem descobrir a <span style="color:#F2CA50;font-weight:600">Garatuja de perto?</span>', "h2", WHITE,
                typo("typography", HANKEN, 38.216, 500, lh=33, size_t=32, size_m=30, lh_m=32)),
        text("<p>Agende uma visita e conheça nosso espaço, nossa equipe e nossa proposta pedagógica.</p>",
             WHITE, typo("typography", DMSANS, 15, 400, lh=18),
             extra={"_element_width": "initial", "_element_custom_width": px(324),
                    "_element_custom_width_tablet": px(100, "%"),
                    "_margin": dims(19.5, 0, 26.5, 0)}),
        form,
    ])
    card = container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_gap": gap(17),
        "flex_gap_tablet": gap(0),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(40),
        "border_radius_mobile": dims(24),
    }, [left, right])
    return container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(960),
        "flex_direction": "column",
        "flex_gap": gap(0),
        "padding": dims(64, 48, 30, 48),
        "padding_tablet": dims(56, 24, 30, 24),
        "padding_mobile": dims(40, 12, 30, 12),
        "background_background": "classic",
        "background_color": YELLOW,
        "css_classes": "gt-root gt-cta",
    }, [add(card, anim("fadeInUp"))], inner=False)


# ---------------------------------------------------------------------------
# 7. RODAPÉ
# ---------------------------------------------------------------------------

def footer_title(label):
    return heading(label, "h2", WHITE,
                   typo("typography", DMSANS, 14, 700, lh=21, ls=0.56, transform="uppercase"))


def build_footer():
    col1 = container({
        "content_width": "full",
        "width": px(322),
        "width_tablet": px(30, "%"),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(28),
    }, [
        image("logo-garatuja-rodape.png", "Garatuja", width_px=222,
              extra={"_margin": dims(0, 0, 0, -6)}),
        social_icons(),
        icon_list(["Política de privacidade", "Termos de uso"],
                  typo("icon_typography", DMSANS, 13, 400, lh=19.5),
                  "rgba(255, 255, 255, 0.45)", space=4, text_indent=0,
                  extra={"_margin": dims(4, 0, 0, 0)}),
    ])
    col2 = container({
        "content_width": "full",
        "width": px(322),
        "width_tablet": px(30, "%"),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(20),
        "margin": dims(42, 0, 0, 0),
        "margin_mobile": dims(0),
    }, [
        footer_title("Contato"),
        icon_list([
            {"text": "(11) 12345-6789", "url": "tel:+551112345678",
             "icon": {"value": "fas fa-phone-alt", "library": "fa-solid"}},
            {"text": "(11) 12345-6789", "url": "tel:+551112345678",
             "icon": {"value": "fas fa-phone-alt", "library": "fa-solid"}},
            {"text": "contato@colegiounicultura.com.br", "url": "mailto:contato@colegiounicultura.com.br",
             "icon": {"value": "fas fa-envelope", "library": "fa-solid"}},
            {"text": "Endereço Completo",
             "icon": {"value": "fas fa-map-marker-alt", "library": "fa-solid"}},
        ], typo("icon_typography", DMSANS, 14, 400, lh=21),
            "rgba(255, 255, 255, 0.7)", icon_color="rgba(255, 255, 255, 0.7)",
            space=12, icon_size=14, text_indent=12),
    ])
    col3 = container({
        "content_width": "full",
        "width": px(322),
        "width_tablet": px(30, "%"),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(20),
        "margin": dims(42, 0, 0, 0),
        "margin_mobile": dims(0),
    }, [
        footer_title("Navegação"),
        icon_list(["Unicultura", "Garatuja", "Diferenciais", "Parceiros", "Contato"],
                  typo("icon_typography", DMSANS, 15, 400, lh=22.5),
                  "rgba(255, 255, 255, 0.7)", space=12, text_indent=0),
    ])
    cols = container({
        "content_width": "full",
        "width": px(100, "%"),
        "min_height": px(314),
        "min_height_mobile": px(0),
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_justify_content": "flex-start",
        "flex_justify_content_tablet": "space-between",
        "flex_align_items": "flex-start",
        "flex_gap": gap(76),
        "flex_gap_tablet": gap(24),
        "flex_gap_mobile": gap(40),
        "padding": dims(0, 0, 0, 22),
        "padding_tablet": dims(0),
    }, [col1, col2, col3])
    bottom = container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "row",
        "padding": dims(24, 0, 0, 0),
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "rgba(255, 255, 255, 0.1)",
    }, [
        text("<p>© 2026 Colégio Unicultura. Todos os direitos reservados.</p>",
             "rgba(255, 255, 255, 0.4)", typo("typography", DMSANS, 13, 400, lh=19.5)),
    ])
    return container({
        "content_width": "boxed",
        "html_tag": "footer",
        "boxed_width": px(1140),
        "flex_direction": "column",
        "flex_gap": gap(56),
        "flex_gap_mobile": gap(40),
        "padding": dims(86, 24, 21.5, 24),
        "padding_mobile": dims(56, 16, 24, 16),
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "gt-root gt-footer",
    }, [cols, bottom], inner=False)


# ---------------------------------------------------------------------------
# 8. CSS complementar (widget HTML único, sem altura visível)
# ---------------------------------------------------------------------------

def build_css_holder():
    with open(CSS_FILE, encoding="utf-8") as fh:
        css = fh.read().strip()
    return container({
        "content_width": "full",
        "padding": dims(0),
        "min_height": px(0),
        "css_classes": "gt-root gt-css",
    }, [widget("html", {"html": "<style>\n" + css + "\n</style>"})], inner=False)


def export_navbar(page_content):
    """Grava só o container da navbar como template "container" para substituir o menu."""
    hero = page_content[0]["elements"][0]
    navbar = next(e for e in hero["elements"] if "gt-navbar" in e["settings"].get("css_classes", ""))
    navbar = json.loads(json.dumps(navbar))
    navbar["isInner"] = False
    data = {
        "content": [navbar],
        "page_settings": [],
        "version": "0.4",
        "title": "Garatuja - Menu (navbar)",
        "type": "container",
    }
    with open(OUT_NAV, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def main():
    content = [
        build_top(),
        build_etapas(),
        build_gallery(),
        build_experiencias(),
        build_depois(),
        build_cta(),
        build_footer(),
        build_css_holder(),
    ]
    data = {
        "content": content,
        "page_settings": {
            "hide_title": "yes",
            "template": "elementor_canvas",
        },
        "version": "0.4",
        "title": "Garatuja - Colégio Unicultura",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    export_navbar(content)
    print(f"OK: {os.path.normpath(OUT)} ({_counter[0]} ids)")
    print(f"OK: {os.path.normpath(OUT_NAV)}")


if __name__ == "__main__":
    main()
