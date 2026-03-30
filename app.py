import io
import json
import zipfile
from datetime import datetime
from typing import Dict, Any, List

import streamlit as st


st.set_page_config(
    page_title="DEFERA Social Planner",
    page_icon="🏟️",
    layout="wide"
)


DEFERA_BRAND_GUIDE = {
    "marca": "DEFERA",
    "tom": "humano, próximo, confiante, claro, profissional e ligado ao desporto, marketing e gestão",
    "visual": "fundo escuro, aspeto premium, linguagem visual desportiva, contraste elevado, composição clean e moderna",
    "linguagem": "português de Portugal, escrita natural, sem tom excessivamente institucional"
}

POST_TYPES = ["Post único", "Carrossel", "Story", "Reel"]
NETWORKS = ["Instagram", "LinkedIn", "Facebook"]
CONTENT_CATEGORIES = [
    "Autoridade",
    "Serviços",
    "Parceiros",
    "Bastidores",
    "Datas especiais",
    "Eventos",
    "Reflexão",
    "Promoção"
]
VISUAL_STYLES = [
    "Escuro, premium e desportivo",
    "Minimalista e clean",
    "Impactante e energético",
    "Institucional moderno",
    "Emocional e inspirador"
]
CTA_OPTIONS = [
    "Pedir contacto",
    "Enviar mensagem",
    "Comentar",
    "Partilhar",
    "Guardar publicação",
    "Visitar website",
    "Sem CTA forte"
]


def init_state():
    if "generated_pack" not in st.session_state:
        st.session_state.generated_pack = None


def default_num_images(post_type):
    if post_type == "Post único":
        return 1
    if post_type == "Carrossel":
        return 5
    if post_type == "Story":
        return 3
    return 3


def build_master_angle(data):
    return (
        f"Conteúdo orientado para {data['objective'].lower()}, centrado no tema '{data['theme']}', "
        f"dirigido a {data['audience'].lower()}, com foco em {data['service_focus'].lower() or 'posicionamento da DEFERA'}, "
        f"num registo {data['tone'].lower()} e com chamada à ação orientada para '{data['cta']}'."
    )


def build_headlines(data):
    theme = data["theme"]
    return [
        f"{theme} com mais intenção e menos ruído",
        f"O que ainda está a falhar em {theme.lower()}",
        f"Como a DEFERA olha para {theme.lower()}"
    ]


def build_hashtags(data):
    return [
        "#DEFERA",
        "#MarketingDesportivo",
        "#GestaoDesportiva",
        "#Desporto",
        "#Comunicacao",
        "#RedesSociais"
    ]


def build_structure(data):
    n = data["num_images"]
    theme = data["theme"]
    objective = data["objective"]
    cta = data["cta"]

    if data["post_type"] == "Post único":
        return [{
            "slide_number": 1,
            "title": theme,
            "message": f"Mensagem central orientada para {objective.lower()}."
        }]

    structure = []
    for i in range(n):
        structure.append({
            "slide_number": i + 1,
            "title": f"Slide {i+1}",
            "message": f"Conteúdo relacionado com {theme.lower()}"
        })
    return structure


def build_master_prompt(data, structure):
    return f"""
Cria conteúdo para redes sociais da marca DEFERA.

Tema: {data['theme']}
Objetivo: {data['objective']}
Público: {data['audience']}
Formato: {data['post_type']}

Estrutura:
{json.dumps(structure, ensure_ascii=False, indent=2)}

Entrega:
- Copy Instagram
- Copy LinkedIn
- Copy Facebook
- Headlines
- Hashtags
"""


def build_visual_prompt(data, structure):
    return f"""
Cria conceito visual para a marca DEFERA.

Tema: {data['theme']}
Formato: {data['post_type']}
Estilo: {data['visual_style']}

Estrutura:
{json.dumps(structure, ensure_ascii=False, indent=2)}

Sem texto nas imagens.
"""


def build_canva_prompts(data, structure):
    prompts = []
    for item in structure:
        prompts.append({
            "slide": item["slide_number"],
            "prompt": f"Imagem desportiva, fundo escuro, estilo premium, tema {data['theme']}, sem texto"
        })
    return prompts


def build_pack(data):
    structure = build_structure(data)
    return {
        "master_angle": build_master_angle(data),
        "structure": structure,
        "master_prompt": build_master_prompt(data, structure),
        "visual_prompt": build_visual_prompt(data, structure),
        "canva_prompts": build_canva_prompts(data, structure),
        "headlines": build_headlines(data),
        "hashtags": build_hashtags(data)
    }


def build_zip(pack):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("prompt.txt", pack["master_prompt"])
        z.writestr("visual.txt", pack["visual_prompt"])
    buffer.seek(0)
    return buffer


init_state()

st.title("DEFERA Social Planner")

with st.form("form"):
    objective = st.text_input("Objetivo")
    theme = st.text_input("Tema")
    audience = st.text_input("Público")
    post_type = st.selectbox("Formato", POST_TYPES)
    visual_style = st.selectbox("Estilo visual", VISUAL_STYLES)

    submitted = st.form_submit_button("Gerar")

if submitted:
    data = {
        "objective": objective,
        "theme": theme,
        "audience": audience,
        "post_type": post_type,
        "visual_style": visual_style,
        "cta": "Contactar",
        "tone": "profissional",
        "service_focus": ""
    }

    pack = build_pack(data)
    st.session_state.generated_pack = pack

if st.session_state.generated_pack:
    pack = st.session_state.generated_pack

    st.subheader("Prompt")
    st.text_area("", pack["master_prompt"], height=300)

    st.subheader("Visual")
    st.text_area("", pack["visual_prompt"], height=200)

    zip_file = build_zip(pack)
    st.download_button("Download ZIP", zip_file, "pack.zip")
