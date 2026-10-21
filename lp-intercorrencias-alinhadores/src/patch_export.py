#!/usr/bin/env python3
"""Aplica a versão atual dos widgets de animação num JSON exportado do site, mantendo as imagens e edições.

Uso: python3 patch_export.py <export-do-site.json> ../lp-intercorrencias-alinhadores-elementor.json <saída.json>
Também remove a seção 09 antiga (clara) se estiver duplicada e preenche o texto alternativo das imagens.
"""
import json, sys
src, ref, out = sys.argv[1:4]
d = json.load(open(src)); r = json.load(open(ref))
new = {}
def collect(e):
    if e.get('widgetType') == 'html': new[e['settings'].get('_title')] = e['settings']['html']
    for c in e['elements']: collect(c)
for sec in r['content']: collect(sec)
log = []
def patch(e):
    if e.get('widgetType') == 'html':
        t = e['settings'].get('_title')
        if t in new and e['settings']['html'] != new[t]:
            e['settings']['html'] = new[t]; log.append('html atualizado: ' + t)
    for c in e['elements']: patch(c)
for sec in d['content']: patch(sec)
# Seção 09 duplicada: fica a nova (escura, com a moeda); sai a antiga (clara).
seen = False; keep = []
for sec in d['content']:
    if sec['settings'].get('_title', '').startswith('09 ·'):
        has_coin = 'lp-coin' in json.dumps(sec)
        if not has_coin:
            log.append('removida a seção 09 antiga (clara, duplicada)'); continue
    keep.append(sec)
d['content'] = keep
ALT = {
    'hero-composicao': 'Dra. Joyce Duarte com páginas do guia Intercorrências com Alinhadores, o ebook e um tablet',
    'guia-pagina-intercorrencia': 'Página do guia: Intercorrência 01, Alinhador não encaixa de forma generalizada',
    'oferta-mockup': 'Guia Intercorrências com Alinhadores no tablet, o ebook impresso e o selo de +2 aulas bônus',
    'garantia': 'Selo de 7 dias de garantia',
    'autora': 'Dra. Joyce Duarte, autora do guia',
}
def alts(e):
    if e.get('widgetType') == 'image':
        img = e['settings'].get('image', {})
        url = img.get('url', '')
        if not img.get('alt'):
            for k, v in ALT.items():
                if k in url:
                    img['alt'] = v; log.append('texto alternativo: ' + url.rsplit('/', 1)[1]); break
    for c in e['elements']: alts(c)
for sec in d['content']: alts(sec)
json.dump(d, open(out, 'w'), ensure_ascii=False, indent=2)
print('\n'.join(log))
