#!/usr/bin/env python3
"""Só a seção 09 (Garantia, autora e FAQ) em fundo escuro, com a moeda de 7 dias animada.

Saída: ../secao-09-garantia-moeda-elementor.json
Uso:   python3 build_secao_garantia.py
"""
import json
import os

import build_lp
import el

OUT = os.path.join(build_lp.HERE, "..", "secao-09-garantia-moeda-elementor.json")


def main():
    el._counter[0] = 50000  # faixa própria de IDs
    sec = build_lp.fix_rows(build_lp.s09_confianca())
    data = {"content": [sec], "page_settings": [], "version": "0.4",
            "title": "LP Alinhadores · 09 Garantia, autora e FAQ (moeda)", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
