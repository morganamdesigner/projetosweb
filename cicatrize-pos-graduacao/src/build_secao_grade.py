#!/usr/bin/env python3
"""Grade curricular (seção 5) reorganizada com o conteúdo programático novo (17 módulos).

Parte da seção exportada do site (entrada/grade-2026-10-09.json): mantém o fundo, o título, os
contadores e as imagens (mockups) de cada bloco, e troca os blocos:
  - 5 blocos temáticos, módulos em ordem crescente:
      Base clínica 01–06 · Feridas complexas 07–10 · Podiatria 11–14 · Tecnologia 15 · Carreira 16–17
    (o Módulo 02, Emergências na pessoa idosa, foi para Base clínica para manter a sequência);
  - o mockup do bloco deixa de ser fundo gigante e vira uma imagem pequena (240 px no computador,
    miniatura ao lado do título no celular), sobre um quadro claro (#D1E3E6, o fundo original);
  - cada módulo fechado mostra só "Módulo 01 · 20 h" + nome; aberto, os tópicos em lista compacta
    (2 colunas no computador) e quem ensina. Módulos com duas disciplinas trazem as duas, com subtítulo.
Fonte: CONTEUDO_PROGRAMATICO_POS_GRADUAÇÃO (atualizado). CPFs, e-mails e bibliografia ficam de fora.
As regras de CSS novas vão num widget HTML dentro da própria seção.
Saída: ../secao-grade-elementor.json

Uso:  python3 build_secao_grade.py [export-da-secao.json]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entrada", "grade-2026-10-09.json")
OUT = os.path.join(HERE, "..", "secao-grade-elementor.json")
CSS_FILE = os.path.join(HERE, "cz-grade.css")

TEAL, SLATE, ROSE, WHITE = "#0F4F5C", "#3B5C66", "#CF8A86", "#FFFFFF"
LATO = "Lato"

DR = "Dr. Cicatriz (Abdeel Oliveira Martins Junior)"
CIBELE = "Profa. Me. Cibele dos Anjos Marcondes"
ROSANGELA = "Profa. Rosângela Maria Pereira"
THAIS = "Profa. Me. Thais Cereda Ravasi"

# (número, nome, horas, professor(a), [(subtítulo ou None, [tópicos])])
MODULES = {
    1: ("Semiologia, Anamnese e Avaliação Clínica na Enfermagem e Podiatria", 20, DR, [(None, [
        "Fundamentos da Semiologia e Anamnese", "Avaliação Clínica e Exame Físico",
        "Semiologia do Pé, Pele e Unhas", "Avaliação Vascular e Neurológica",
        "Avaliação Biomecânica e Musculoesquelética", "Avaliação de Feridas e Lesões Cutâneas",
        "Pé Diabético e Estratificação de Risco", "Úlceras Vasculares, Dor e Infecção",
        "Documentação, Raciocínio Clínico e Encaminhamento", "Prevenção, Educação e Casos Clínicos"])]),
    2: ("Emergências na Pessoa Idosa e Prevenção de Quedas", 40, "Profa. Dra. Danielle Cristina Garbuio", [(None, [
        "Epidemiologia das emergências na pessoa idosa", "Avaliação clínica da pessoa idosa",
        "Emergências cardiovasculares e seu atendimento", "Emergências respiratórias e seu atendimento",
        "Emergências neurológicas e psiquiátricas", "Prevenção de trauma e quedas na pessoa idosa"])]),
    3: ("Anatomia e Fisiologia do Pé, dos Membros Inferiores e da Pele", 20, CIBELE, [
        ("Anatomia e fisiologia", [
            "Epiderme, derme e hipoderme", "Anexos cutâneos", "Vascularização e inervação",
            "Barreira cutânea", "Microcirculação", "Envelhecimento da pele"]),
        ("Fisiologia avançada da cicatrização", [
            "Fundamentos da reparação tecidual", "Hemostasia e fase inflamatória",
            "Células, citocinas e fatores de crescimento",
            "Proliferação, fibroblastos, colágeno e matriz extracelular",
            "Angiogênese, reepitelização e contração", "Remodelamento, MMPs e TIMPs",
            "Feridas crônicas, inflamação persistente e biofilme",
            "Diabetes, neuropatia e alterações vasculares",
            "Nutrição, envelhecimento e fatores sistêmicos", "Aplicação da fisiologia à prática podiátrica"])]),
    4: ("Biossegurança e Controle de Infecções em Feridas e Cateteres", 20, CIBELE, [
        ("Biossegurança e controle de infecções", [
            "Biossegurança e Segurança do Paciente", "Higienização das Mãos, EPIs e Precauções",
            "Prevenção e Controle de Infecções em Feridas", "Microbiologia, Biofilme e Infecção",
            "Limpeza, Antissepsia, Desinfecção e Esterilização", "Biossegurança no Tratamento de Feridas",
            "Cateteres e Prevenção de Infecções", "Complicações e Lesões por Dispositivos",
            "Resíduos e Acidentes com Material Biológico", "Biossegurança em Podiatria e Casos Clínicos"]),
        ("Microbiologia da pele e epidemiologia das doenças cutâneas", [
            "Microbiota e barreira cutânea", "Bactérias e infecções bacterianas",
            "Fungos, micoses e onicomicoses", "Vírus e parasitos de importância podiátrica",
            "Epidemiologia das doenças cutâneas", "Cadeia epidemiológica e transmissão",
            "Biofilme, feridas e pé diabético", "Biossegurança e prevenção de infecções"])]),
    5: ("Aspectos Nutricionais nas Lesões Cutâneas", 20, "Profa. Dra. Maria Carliana Mota", [(None, [
        "Nutrição, Pele e Cicatrização", "Avaliação e Risco Nutricional", "Proteínas, Energia e Aminoácidos",
        "Vitaminas, Minerais e Hidratação", "Nutrição, Imunidade e Inflamação",
        "Desnutrição, Sarcopenia e Feridas", "Nutrição no Pé Diabético e Feridas Crônicas",
        "Nutrição no Idoso, Obesidade e Doenças Crônicas", "Suplementação e Abordagem Multiprofissional",
        "Educação Nutricional e Casos Clínicos"])]),
    6: ("Farmacologia no Tratamento de Feridas e Podiatria", 20, "Profa. Patricia Lasmar Buiatti", [
        ("Farmacologia", [
            "Fundamentos de Farmacologia Aplicada às Feridas", "Farmacologia da Cicatrização e Controle da Dor",
            "Antibióticos, Antissépticos e Antimicrobianos Tópicos", "Farmacologia do Pé Diabético",
            "Farmacologia Vascular e Neuroisquemia",
            "Anticoagulantes, Antiagregantes e Segurança em Procedimentos",
            "Farmacologia Dermatológica, Antifúngicos e Afecções Ungueais",
            "Anestésicos Locais e Procedimentos Podiátricos", "Interações, Polifarmácia e Farmacovigilância",
            "Feridas Complexas e Casos Clínicos"]),
        ("Homeopatia no tratamento de feridas e podiatria", [
            "Fundamentos da Homeopatia e Práticas Integrativas", "Pele, Pé e Cicatrização",
            "Avaliação de Feridas e Lesões Cutâneas", "Homeopatia Aplicada à Podiatria",
            "Pé Diabético e Feridas Vasculares", "Segurança, Ética e Prática Baseada em Evidências",
            "Abordagem Multiprofissional e Educação em Saúde"])]),
    7: ("Sistematização da Assistência ao Paciente com Lesões e Feridas", 20, ROSANGELA, [
        ("Avaliação, classificação e manejo clínico", [
            "LPP – Lesão por Pressão", "Úlceras venosas, arteriais e mistas",
            "Pé diabético, neuropatia, isquemia e neuroisquemia", "Feridas traumáticas e cirúrgicas",
            "Leitura do leito da ferida", "Lesões dermatológicas e infecciosas",
            "Escolha do tratamento mais indicado para cada lesão",
            "Preparo do leito, sistema TIMERS e técnicas de desbridamento", "Casos clínicos"]),
        ("Abordagem e intervenção com familiares de pessoas com lesão", [
            "Família, Cuidador e Impacto das Feridas", "Avaliação e Sobrecarga do Cuidador",
            "Aspectos Psicológicos, Sociais e Econômicos", "Comunicação e Educação em Saúde",
            "Capacitação e Adesão ao Tratamento", "Prevenção e Cuidados Domiciliares",
            "Plano de Intervenção Familiar", "Abordagem Multiprofissional e Rede de Apoio",
            "Ética, Segurança e Continuidade do Cuidado", "Avaliação e Estudos de Caso"])]),
    8: ("Queimaduras e Radiodermites", 20, ROSANGELA, [(None, [
        "Fundamentos e Classificação das Queimaduras", "Avaliação, Extensão e Profundidade",
        "Atendimento Inicial e Controle da Dor", "Sistematização da Assistência e Tratamento",
        "Coberturas, Desbridamento e Controle de Infecção", "Nutrição e Cicatrização",
        "Radiodermites: Avaliação e Classificação", "Prevenção e Tratamento das Radiodermites",
        "Complicações, Reabilitação e Qualidade de Vida"])]),
    9: ("Feridas Cirúrgicas, Drenos e Estomias", 20, ROSANGELA, [(None, [
        "Avaliação e Cicatrização de Feridas Cirúrgicas", "Complicações e Tratamento de Feridas Cirúrgicas",
        "Drenos: Tipos, Cuidados e Complicações", "Estomias: Tipos e Avaliação",
        "Cuidados com Estoma e Pele Periestomal", "Complicações e Manejo das Estomias",
        "Dispositivos, Autocuidado e Educação", "Nutrição, Aspectos Psicossociais e Qualidade de Vida",
        "Biossegurança, Infecção e Documentação", "Casos Clínicos e Abordagem Multiprofissional"])]),
    10: ("Ferida Oncológica", 20, ROSANGELA, [(None, [
        "Fundamentos e Avaliação das Feridas Oncológicas", "Sistematização da Assistência e Documentação",
        "Preparação do Leito e Controle do Exsudato", "Odor, Infecção e Biofilme",
        "Dor e Controle do Sangramento", "Coberturas e Desbridamento",
        "Tratamentos Oncológicos e Complicações Cutâneas", "Nutrição e Cicatrização",
        "Cuidados Paliativos e Qualidade de Vida", "Família, Abordagem Multiprofissional e Casos Clínicos"])]),
    11: ("Podiatria Clínica, Biomecânica e Avaliação dos Pés", 20, DR, [(None, [
        "Podiatria Clínica e Avaliação dos Pés", "Anatomia, Avaliação Vascular e Neurológica",
        "Biomecânica e Alterações Estruturais", "Marcha e Pressão Plantar", "Calçados, Palmilhas e Prevenção",
        "Podopatias e Deformidades", "Pé Diabético e Pé de Risco", "Avaliação Funcional e Tecnologias",
        "Planejamento e Encaminhamento", "Casos Clínicos e Prática Podiátrica"])]),
    12: ("Principais Podopatias, Diagnóstico Diferencial e Onicopatias", 20, DR, [(None, [
        "Avaliação e Principais Podopatias", "Calosidades, Hiperqueratoses e Verrugas",
        "Micoses e Dermatoses dos Pés", "Pé Diabético e Alterações Vasculares",
        "Fundamentos e Classificação das Onicopatias", "Onicomicose, Onicocriptose e Paroníquia",
        "Traumas e Distrofias Ungueais", "Diagnóstico Diferencial e Sinais de Alerta",
        "Prevenção, Cuidados Podiátricos e Encaminhamento", "Instrumentais e Equipamentos em Podiatria",
        "Casos Clínicos e Raciocínio Diagnóstico"])]),
    13: ("Alterações Ungueais, Onicocriptose e Técnicas Corretivas", 20, DR, [(None, [
        "Anatomia e Avaliação das Unhas", "Onicopatias e Diagnóstico Diferencial", "Onicocriptose e Classificação",
        "Tratamento Conservador e Prevenção", "Técnicas Corretivas e Órteses", "Infecções, Dor e Complicações",
        "Pacientes de Risco e Encaminhamento", "Biossegurança e Documentação", "Acompanhamento e Resultados",
        "Casos Clínicos e Prática Podiátrica"])]),
    14: ("Órteses, Palmilhas, Alívio de Pressão e Correção Funcional", 20, DR, [(None, [
        "Órteses, Palmilhas e Avaliação Funcional", "Biomecânica e Pressão Plantar", "Alívio de Pressão e Offloading",
        "Correção Funcional e Podopatias", "Órteses no Pé Diabético", "Materiais, Confecção e Adaptação",
        "Calçados Terapêuticos", "Monitoramento e Prevenção", "Educação e Critérios de Encaminhamento",
        "Casos Clínicos e Aplicação Prática"])]),
    15: ("Biomateriais e Inovação Tecnológica em Curativos", 20, DR, [(None, [
        "Fundamentos dos Biomateriais e Curativos Avançados", "Biomateriais Bioativos e Matrizes Extracelulares",
        "Coberturas Antimicrobianas e Sistemas de Liberação Controlada", "Nanotecnologia e Curativos Inteligentes",
        "Terapia por Pressão Negativa e Tecnologias de Suporte", "Fotobiomodulação, Laser, LED e Oxigenoterapia",
        "Engenharia Tecidual, Regeneração e Bioimpressão",
        "Inteligência Artificial e Tecnologias Digitais em Feridas",
        "Prática Baseada em Evidências, Segurança e Custo-Efetividade",
        "Aplicação Clínica, Personalização e Casos de Feridas Complexas"])]),
    16: ("Gestão e Empreendedorismo", 40, THAIS, [(None, [
        "Fundamentos e processos do empreendedorismo", "Tendências e leitura de mercado",
        "Estratégias de negócio para obter resultados"])]),
    17: ("Marketing Digital", 40, THAIS, [(None, [
        "Comunicação integrada de marketing", "Ambiente digital", "Jornada do cliente online",
        "Planejamento de marketing digital", "Construção de persona",
        "Mídias sociais, mecanismos de busca, métricas e monitoramento"])]),
}

# (nome do bloco, módulos, alt da imagem)
BLOCKS = [
    ("Base clínica", [1, 2, 3, 4, 5, 6], "Mockup do bloco Base clínica"),
    ("Feridas complexas", [7, 8, 9, 10], "Mockup do bloco Feridas complexas"),
    ("Podiatria", [11, 12, 13, 14], "Mockup do bloco Podiatria"),
    ("Tecnologia e inovação", [15], "Mockup do bloco Tecnologia e inovação"),
    ("Carreira e mercado", [16, 17], "Mockup do bloco Carreira e mercado"),
]

_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"cicatrize-grade-v2-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
            "isLinked": top == right == bottom == left}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def typo(prefix, size, weight, lh, ls=None, transform=None, size_m=None, lh_m=None):
    s = {f"{prefix}_typography": "custom", f"{prefix}_font_family": LATO, f"{prefix}_font_size": px(size),
         f"{prefix}_font_weight": str(weight), f"{prefix}_line_height": px(lh)}
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = px(ls)
    if transform:
        s[f"{prefix}_text_transform"] = transform
    if size_m:
        s[f"{prefix}_font_size_mobile"] = px(size_m)
    if lh_m:
        s[f"{prefix}_line_height_mobile"] = px(lh_m)
    return s


def widget(kind, settings, title=None):
    if title:
        settings["_title"] = title
    return {"id": new_id(), "elType": "widget", "isInner": False, "widgetType": kind, "elements": [],
            "settings": settings}


def container(children, title=None, **settings):
    s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0), "padding": dims(0)}
    s.update(settings)
    if title:
        s["_title"] = title
    return {"id": new_id(), "elType": "container", "isInner": True, "elements": children, "settings": s}


def heading(title, color, typography, classes="", tag="p"):
    s = {"title": title, "header_size": tag, "align": "left", "title_color": color,
         "__globals__": {"title_color": "", "typography_typography": ""}}
    s.update(typography)
    if classes:
        s["_css_classes"] = classes
    return widget("heading", s)


def module_body(num):
    name, hours, prof, parts = MODULES[num]
    html = []
    for sub, topics in parts:
        if sub:
            html.append(f'<p class="cz-msub">{sub}</p>')
        html.append('<ul class="cz-topics">' + "".join(f"<li>{t}</li>" for t in topics) + "</ul>")
    html.append(f'<p class="cz-mprof"><span>Com</span> {prof}</p>')
    text = widget("text-editor", {
        "editor": "".join(html), "align": "left", "text_color": SLATE,
        **typo("typography", 15, 400, 22, size_m=14, lh_m=20),
        "_css_classes": "cz-mbody",
        "__globals__": {"text_color": "", "typography_typography": ""},
    })
    return container([text], padding=dims(0, 22, 22, 22), padding_mobile=dims(0, 16, 18, 16))


def accordion(nums):
    acc = widget("nested-accordion", {
        "items": [{"item_title": f'<span class="cz-dn">Módulo {n:02d} · {MODULES[n][1]} h</span>{MODULES[n][0]}',
                   "_id": new_id()} for n in nums],
        "title_tag": "h4",
        "default_state": "all_collapsed",
        "max_items_expended": "one",
        "accordion_item_title_position_horizontal": "stretch",
        "accordion_item_title_icon_position": "end",
        "accordion_item_title_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "accordion_item_title_icon_active": {"value": "fas fa-minus", "library": "fa-solid"},
        "accordion_item_title_space_between": px(8),
        "accordion_item_title_distance_from_content": px(0),
        "accordion_padding": dims(16, 20, 16, 20),
        "accordion_padding_mobile": dims(14, 14, 14, 16),
        "accordion_border_radius": dims(14),
        "accordion_border_normal_border": "none",
        "accordion_border_hover_border": "none",
        "accordion_border_active_border": "none",
        "content_border_border": "none",
        **typo("title_typography", 16, 800, 22, size_m=15, lh_m=20),
        "normal_title_color": TEAL, "hover_title_color": TEAL, "active_title_color": TEAL,
        "normal_icon_color": TEAL, "hover_icon_color": TEAL, "active_icon_color": WHITE,
        "icon_size": px(11), "icon_spacing": px(14),
        "_css_classes": "cz-acc cz-grade-acc",
        "__globals__": {"title_typography_typography": "", "normal_title_color": "", "hover_title_color": "",
                        "active_title_color": "", "normal_icon_color": "", "hover_icon_color": "",
                        "active_icon_color": ""},
    }, title="Módulos (clique para abrir)")
    acc["elements"] = [module_body(n) for n in nums]
    return acc


def block(index, name, nums, image, alt):
    hours = sum(MODULES[n][1] for n in nums)
    count = f"{len(nums)} módulo{'s' if len(nums) > 1 else ''} · {hours} h"
    img = widget("image", {
        "image": {"url": image["url"], "id": image.get("id", ""), "size": "", "alt": alt, "source": "library"},
        "image_size": "full", "align": "center", "width": px(100, "%"),
        "_css_classes": "cz-block-img",
    }, title=f"Mockup do bloco {index:02d}")
    media = container([img], title="Mockup (quadro claro)", css_classes="cz-block-media",
                      background_background="classic", background_color="#D1E3E6",
                      border_radius=dims(18), padding=dims(14), padding_mobile=dims(8),
                      __globals__={"background_color": ""})
    info = container([
        heading(f"Bloco {index:02d}", ROSE, typo("typography", 12, 900, 14, ls=1.8, transform="uppercase")),
        heading(name, WHITE, typo("typography", 24, 800, 29, ls=-0.4, size_m=19, lh_m=23), tag="h3"),
        heading(count, "rgba(255, 255, 255, 0.72)", typo("typography", 14, 700, 18, size_m=13)),
    ], title="Nome do bloco", flex_gap=gap(8), flex_gap_mobile=gap(4), css_classes="cz-block-info",
        flex_justify_content="center")
    side = container([media, info], title="Mockup + nome", css_classes="cz-block-side",
                     width=px(30, "%"), width_tablet=px(100, "%"),
                     flex_gap=gap(18), flex_direction_tablet="row", flex_align_items_tablet="center",
                     flex_gap_mobile=gap(14))
    main = container([accordion(nums)], title="Módulos", css_classes="cz-block-main",
                     width=px(70, "%"), width_tablet=px(100, "%"))
    return container([side, main], title=f"Bloco {index:02d} · {name}", css_classes="cz-block cz-block2",
                     flex_direction="row", flex_direction_tablet="column", flex_wrap="nowrap",
                     flex_gap=gap(36), flex_gap_tablet=gap(20), flex_gap_mobile=gap(16),
                     padding=dims(28), padding_tablet=dims(24), padding_mobile=dims(16, 14, 16, 14),
                     border_radius=dims(24), border_radius_mobile=dims(20),
                     background_background="classic", background_color="rgba(255, 255, 255, 0.04)",
                     border_border="solid", border_width=dims(1), border_color="rgba(255, 255, 255, 0.1)",
                     animation="fadeInUp",
                     __globals__={"background_color": "", "border_color": ""})


def find_all(el, pred):
    out = []
    if pred(el):
        out.append(el)
    for c in el.get("elements", []):
        out += find_all(c, pred)
    return out


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    sec = data["content"][0]
    head, stats, blocks_wrap = sec["elements"][0], sec["elements"][1], sec["elements"][2]

    # título e contadores
    title = find_all(head, lambda e: e.get("widgetType") == "heading")[0]
    title["settings"]["title"] = ('17 módulos. 400 horas. <span class="cz-rose">Do diagnóstico ao caso mais '
                                  'complexo.</span>')
    for c in find_all(stats, lambda e: e.get("widgetType") == "counter"):
        if c["settings"].get("title") == "Disciplinas":
            c["settings"]["title"] = "Módulos"

    # imagens atuais (fundo de cada bloco), na ordem
    images = [b["settings"].get("background_image", {"url": ""}) for b in blocks_wrap["elements"]]
    blocks_wrap["elements"] = [block(i + 1, name, nums, images[i], alt)
                               for i, (name, nums, alt) in enumerate(BLOCKS)]
    blocks_wrap["settings"]["flex_gap"] = gap(20)
    blocks_wrap["settings"]["flex_gap_mobile"] = gap(14)

    total = sum(m[1] for m in MODULES.values())
    assert total == 400 and len(MODULES) == 17, total

    css = open(CSS_FILE, encoding="utf-8").read().strip()
    sec["elements"].insert(0, widget("html", {"html": "<style>\n" + css + "\n</style>",
                                              "_css_classes": "cz-assets"}, title="CSS da grade (não apagar)"))
    data["title"] = "Cicatrize - Grade curricular (17 módulos)"
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)} ({len(MODULES)} módulos, {total} h)")


if __name__ == "__main__":
    main()
