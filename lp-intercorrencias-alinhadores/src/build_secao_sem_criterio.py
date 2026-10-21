#!/usr/bin/env python3
"""Só a seção 03b ("Sem critério, a consulta vira improviso:"), fundo turquesa e transições no scroll.

Saída: ../secao-03b-sem-criterio-elementor.json
Uso:   python3 build_secao_sem_criterio.py
"""
import json
import os

import build_lp
import el

OUT = os.path.join(build_lp.HERE, "..", "secao-03b-sem-criterio-elementor.json")


def main():
    el._counter[0] = 60000  # faixa própria de IDs
    sec = build_lp.fix_rows(build_lp.s03b_impact())
    data = {"content": [sec], "page_settings": [], "version": "0.4",
            "title": "LP Alinhadores · 03b Sem critério (improviso)", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
