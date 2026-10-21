"""Helpers para montar JSON de importação do Elementor (containers Flexbox/Grid, version 0.4)."""
import hashlib

MONT = "Montserrat"
_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"lp-alinhadores-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    elif bottom is None:
        bottom, left = top, right
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
            "isLinked": top == right == bottom == left}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def typo(prefix, size, weight, lh=None, ls=None, transform=None, size_t=None, size_m=None, family=MONT):
    """Tipografia custom. lh em "em" (escala junto com a fonte nos breakpoints)."""
    s = {
        f"{prefix}_typography": "custom",
        f"{prefix}_font_family": family,
        f"{prefix}_font_size": px(size),
        f"{prefix}_font_weight": str(weight),
    }
    if lh is not None:
        s[f"{prefix}_line_height"] = px(lh, "em")
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = px(ls)
    if transform:
        s[f"{prefix}_text_transform"] = transform
    if size_t is not None:
        s[f"{prefix}_font_size_tablet"] = px(size_t)
    if size_m is not None:
        s[f"{prefix}_font_size_mobile"] = px(size_m)
    return s


def shadow(x, y, blur, spread, color):
    return {"horizontal": x, "vertical": y, "blur": blur, "spread": spread, "color": color}


def grad(a, b, angle=180, stop_a=0, stop_b=100, kind="linear", position=None, prefix="background"):
    s = {
        f"{prefix}_background": "gradient",
        f"{prefix}_color": a,
        f"{prefix}_color_stop": px(stop_a, "%"),
        f"{prefix}_color_b": b,
        f"{prefix}_color_b_stop": px(stop_b, "%"),
        f"{prefix}_gradient_type": kind,
    }
    if kind == "linear":
        s[f"{prefix}_gradient_angle"] = px(angle, "deg")
    else:
        s[f"{prefix}_gradient_position"] = position or "center center"
    return s


def solid(color, prefix="background"):
    return {f"{prefix}_background": "classic", f"{prefix}_color": color}


def border(width, color, radius=None, on_widget=False):
    """Borda de container (border_*) ou de widget (aba Avançado: _border_*)."""
    p = "_border" if on_widget else "border"
    s = {f"{p}_border": "solid", f"{p}_width": dims(width), f"{p}_color": color}
    if radius is not None:
        s[f"{p}_radius"] = dims(radius)
    return s


def _globals(settings):
    """Anula as cores/tipografias globais do kit nos controles definidos (como o export do Elementor)."""
    g = {}
    for k in settings:
        base = k.replace("_tablet", "").replace("_mobile", "")
        if base != k:
            continue
        if k.endswith("_typography") or k.endswith("color") or k.endswith("_color_b"):
            g[k] = ""
    if g:
        settings["__globals__"] = g
    return settings


def container(settings, children, title=None, inner=True):
    s = {"flex_gap": gap(0), "padding": dims(0), "content_width": "full"}
    s.update(settings)
    if title:
        s["_title"] = title
    return {"id": new_id(), "elType": "container", "isInner": inner, "settings": _globals(s), "elements": children}


def row(children, gap_px=0, title=None, **kw):
    s = {"flex_direction": "row", "flex_gap": gap(gap_px), "flex_wrap": "nowrap"}
    s.update(kw)
    return container(s, children, title)


def col(children, gap_px=0, title=None, **kw):
    s = {"flex_direction": "column", "flex_gap": gap(gap_px)}
    s.update(kw)
    return container(s, children, title)


def widget(kind, settings):
    return {"id": new_id(), "elType": "widget", "isInner": False, "widgetType": kind,
            "settings": _globals(settings), "elements": []}


def link(url="", external=False):
    return {"url": url, "is_external": "on" if external else "", "nofollow": "", "custom_attributes": ""}


def anim(el, name="fadeInUp", delay=0):
    """Entrada nativa (Motion Effects > Entrance Animation). Duração Fast, suavizada no CSS."""
    p = "_" if el["elType"] == "widget" else ""
    el["settings"][f"{p}animation"] = name
    el["settings"]["animation_duration"] = "fast"
    if delay:
        el["settings"][f"{p}animation_delay"] = delay
    return el


def cls(el, classes):
    key = "_css_classes" if el["elType"] == "widget" else "css_classes"
    el["settings"][key] = (el["settings"].get(key, "") + " " + classes).strip()
    return el


def setv(el, **kw):
    el["settings"].update(kw)
    return el


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------

def heading(title, color, typography, tag="p", align="left", **extra):
    s = {"title": title, "header_size": tag, "align": align, "title_color": color}
    s.update(typography)
    s.update(extra)
    return widget("heading", s)


def text(html, color, typography, align="left", **extra):
    s = {"editor": html, "align": align, "text_color": color}
    s.update(typography)
    s.update(extra)
    return widget("text-editor", s)


def button(label, url, colors, typography, padding, icon=True, gradient=None, border_color=None, **extra):
    """colors = (texto, fundo, texto_hover, fundo_hover)."""
    fg, bg, fg_h, bg_h = colors
    s = {
        "text": label,
        "link": link(url),
        "align": "left",
        "size": "md",
        "button_text_color": fg,
        "hover_color": fg_h,
        "text_padding": padding,
        "border_radius": dims(999),
    }
    if gradient:
        s.update(grad(gradient[0], gradient[1], 90))
        s.update({"button_background_hover_background": "gradient",
                  "button_background_hover_color": gradient[0],
                  "button_background_hover_color_b": gradient[1],
                  "button_background_hover_gradient_angle": px(90, "deg")})
    else:
        s.update(solid(bg))
        s.update({"button_background_hover_background": "classic", "button_background_hover_color": bg_h})
    if border_color:
        s.update({"border_border": "solid", "border_width": dims(1), "border_color": border_color,
                  "button_hover_border_color": "rgba(255, 255, 255, 0.6)"})
    if icon:
        s.update({"selected_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
                  "icon_align": "right", "icon_indent": px(10)})
    s.update(typography)
    s.update(extra)
    return widget("button", s)


def image(url, alt, width=None, height=None, radius=None, fit="cover", position="center center", **extra):
    s = {"image": {"url": url, "id": "", "size": "", "alt": alt, "source": "library"},
         "image_size": "full", "align": "center", "link_to": "none"}
    if width is not None:
        s["width"] = px(*width) if isinstance(width, tuple) else px(width, "%")
    if height is not None:
        s["height"] = px(height)
        s["object-fit"] = fit
        s["object-position"] = position
    if radius is not None:
        s["image_border_radius"] = dims(radius)
    s.update(extra)
    return widget("image", s)


def icon(value, color, size, view="default", secondary=None, padding=None, align="left", library="fa-solid", **extra):
    s = {"selected_icon": {"value": value, "library": library}, "view": view, "align": align,
         "primary_color": color, "size": px(size)}
    if view != "default":
        s["shape"] = "circle"
        s["secondary_color"] = secondary
        if padding is not None:
            s["icon_padding"] = px(padding)
    s.update(extra)
    return widget("icon", s)


def icon_list(items, color, typography, icon_value="fas fa-check-circle", icon_color=None, icon_size=16,
              space=12, inline=False, indent=10, **extra):
    lst = []
    for it in items:
        if isinstance(it, str):
            it = {"text": it}
        lst.append({"_id": new_id(), "text": it["text"],
                    "selected_icon": {"value": it.get("icon", icon_value), "library": "fa-solid"},
                    "link": link(it.get("url", ""))})
    s = {"view": "inline" if inline else "traditional", "icon_list": lst, "space_between": px(space),
         "text_color": color, "text_color_hover": color, "icon_size": px(icon_size), "text_indent": px(indent),
         "icon_self_align": "left", "icon_self_vertical_align": "flex-start", "icon_vertical_offset": px(3)}
    if icon_color:
        s["icon_color"] = icon_color
        s["icon_color_hover"] = icon_color
    s.update(typography)
    s.update(extra)
    return widget("icon-list", s)


def counter(start, end, prefix, color, typography, duration=1200, **extra):
    s = {"starting_number": start, "ending_number": end, "prefix": prefix, "suffix": "", "duration": duration,
         "thousand_separator": "", "title": "", "number_color": color}
    s.update(typography)
    s.update(extra)
    return widget("counter", s)


def html(code, **extra):
    s = {"html": code}
    s.update(extra)
    return widget("html", s)
