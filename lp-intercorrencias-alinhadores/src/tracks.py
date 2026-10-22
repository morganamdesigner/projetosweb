"""Estrutura das cenas presas no scroll: trilha alta (.lp-track) por fora e palco sticky (.lp-stage)
por dentro. Funciona tanto no JSON gerado quanto num export do site (mantém configurações e imagens).

- Seções 03 (lp-dor) e 03b (lp-crit): a seção vira o palco (mantém id, estilos e conteúdo) e ganha
  uma trilha nova por fora, que passa a ser o container de topo.
- Notebook (lp-laptop, na seção 04): ganha trilha + palco centralizado em volta só dele.
Idempotente: o que já estiver dentro de uma trilha fica como está."""
import hashlib
import json

_n = [0]


def _id(seed):
    _n[0] += 1
    return hashlib.md5(f"lp-track-{seed}-{_n[0]}".encode()).hexdigest()[:7]


def _classes(el):
    s = el["settings"]
    return (s.get("css_classes") or s.get("_css_classes") or "").split()


def _add_class(el, cls):
    s = el["settings"]
    if cls not in _classes(el):
        s["css_classes"] = (s.get("css_classes", "") + " " + cls).strip()


def _track(kind, child, title, html_tag="div"):
    return {
        "id": _id(child["id"]), "elType": "container", "isInner": False,
        "settings": {"content_width": "full", "flex_direction": "column", "html_tag": html_tag,
                     "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
                     "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
                     "css_classes": f"lp-track lp-track--{kind}", "_title": title},
        "elements": [child],
    }


def apply(data):
    out = []
    for sec in data["content"]:
        cls = _classes(sec)
        if "lp-track" in cls:
            out.append(sec)
            continue
        kind = "dor" if "lp-dor" in cls else "crit" if "lp-crit" in cls else None
        if kind:
            title = sec["settings"].get("_title", "")
            tag = sec["settings"].get("html_tag", "section") or "section"
            sec["settings"]["html_tag"] = "div"
            sec["isInner"] = True
            _add_class(sec, "lp-stage")
            sec["settings"]["_title"] = "Palco (preso na tela)"
            out.append(_track(kind, sec, title + " · trilha do scroll", tag))
            continue
        _wrap_laptop(sec)
        out.append(sec)
    data["content"] = out
    return data


def _wrap_laptop(el):
    for i, ch in enumerate(el["elements"]):
        # Palco do notebook que perdeu a trilha (removida no editor): recoloca a trilha em volta.
        if (ch["elType"] == "container" and "lp-stage" in _classes(ch) and "lp-track" not in _classes(el)
                and any("lp-laptop" in _classes(g) for g in ch["elements"] if g["elType"] == "container")):
            ch["isInner"] = True
            track = _track("laptop", ch, "Trilha do notebook (scroll)")
            track["isInner"] = True
            el["elements"][i] = track
            return
        if ch["elType"] == "container" and "lp-laptop" in _classes(ch):
            if "lp-stage" in _classes(el):
                return
            stage = {"id": _id(ch["id"]), "elType": "container", "isInner": True,
                     "settings": {"content_width": "full", "flex_direction": "column",
                                  "flex_justify_content": "center", "flex_align_items": "center",
                                  "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
                                  "css_classes": "lp-stage lp-stage--center", "_title": "Palco do notebook (preso na tela)"},
                     "elements": [ch]}
            track = _track("laptop", stage, "Trilha do notebook (scroll)")
            track["isInner"] = True
            el["elements"][i] = track
            return
        _wrap_laptop(ch)


if __name__ == "__main__":
    import sys
    d = json.load(open(sys.argv[1]))
    json.dump(apply(d), open(sys.argv[2], "w"), ensure_ascii=False, indent=2)
