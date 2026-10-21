#!/usr/bin/env python3
"""Só a seção 04 (Apresentação) com o notebook que abre no scroll, para importar avulsa.

Saída: ../secao-04-apresentacao-notebook-elementor.json
Uso:   python3 build_secao_apresentacao.py
"""
import json
import os

import build_lp
import el

OUT = os.path.join(build_lp.HERE, "..", "secao-04-apresentacao-notebook-elementor.json")


def main():
    el._counter[0] = 40000  # faixa própria de IDs, para não colidir com a página já importada
    sec = build_lp.fix_rows(build_lp.s04_apresentacao())
    data = {"content": [sec], "page_settings": [], "version": "0.4",
            "title": "LP Alinhadores · 04 Apresentação (notebook)", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
