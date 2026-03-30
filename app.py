import streamlit as st
from datetime import datetime


st.set_page_config(
    page_title="DEFERA Content Generator",
    page_icon="🏟️",
    layout="wide"
)

POST_TYPES = ["Post único", "Carrossel", "Story", "Reel"]
NETWORKS = ["Instagram", "LinkedIn", "Facebook"]
VISUAL_STYLES = [
    "Escuro, premium e desportivo",
    "Minimalista e clean",
    "Impactante e energético"
]


def default_num_images(post_type):
    if post_type == "Post único":
        return 1
    if post_type == "Carrossel":
        return 5
    return 3


def build_structure(theme, post_type, num):
    base = [
        "Gancho",
        "Contexto",
        "Problema",
        "Solução",
        "Ação"
    ]

    structure = []
    for i in range(num):
        title = base[i] if i < len(base) else f"Slide {i+1}"
        structure.append(f"{i+1}. {title} sobre {theme}")
    return structure


def build_copy(data, structure):
    copy = {}

    if "Instagram" in data["networks"]:
        copy["Instagram"] = f"""
{data['theme']}

Muitos clubes continuam a comunicar sem estratégia.

Publicar não é comunicar.
Comunicar não é influenciar.
E influenciar é o que gera crescimento.

Se quer mais resultados, precisa de mais do que presença.
Precisa de direção.

Fale com a DEFERA.
"""

    if "LinkedIn" in data["networks"]:
        copy["LinkedIn"] = f"""
No desporto, muitos clubes continuam a comunicar sem estratégia.

A presença digital existe.
Mas a intenção estratégica não.

E isso reflete-se em três pontos críticos:
- baixa perceção de valor
- dificuldade em atrair parceiros
- fraca ligação com a comunidade

Comunicar bem não é publicar mais.
É publicar com propósito.

Se faz sentido para o seu clube, vale a pena falar.
"""

    if "Facebook" in data["networks"]:
        copy["Facebook"] = f"""
Muitos clubes continuam a comunicar sem estratégia.

E isso acaba por limitar o seu crescimento.

Hoje, comunicar bem faz toda a diferença.
"""

    return copy


def build_image_prompts(data, structure):
    prompts = []

    for i, item in enumerate(structure):
        prompt = f"""
Imagem {i+1} de {len(structure)} para a marca DEFERA.

Tema: {data['theme']}

Objetivo visual:
{item}

Estilo:
{data['visual_style']}

Regras:
- Fundo escuro ou visual premium
- Estética desportiva e profissional
- Alta qualidade
- Sem texto na imagem
- Coerência com as restantes imagens
"""
        prompts.append(prompt.strip())

    return prompts


# UI
st.title("DEFERA Content Generator")

with st.form("form"):
    objective = st.text_input("Objetivo")
    theme = st.text_input("Tema")
    audience = st.text_input("Público")
    networks = st.multiselect("Redes", NETWORKS)
    post_type = st.selectbox("Formato", POST_TYPES)
    visual_style = st.selectbox("Estilo visual", VISUAL_STYLES)

    num_images = st.slider(
        "Número de imagens",
        1,
        10,
        default_num_images(post_type)
    )

    submitted = st.form_submit_button("Gerar")

if submitted:
    data = {
        "objective": objective,
        "theme": theme,
        "audience": audience,
        "networks": networks,
        "post_type": post_type,
        "visual_style": visual_style,
        "num_images": num_images
    }

    structure = build_structure(theme, post_type, num_images)
    copy = build_copy(data, structure)
    prompts = build_image_prompts(data, structure)

    st.success("Conteúdo gerado")

    # COPY
    st.subheader("Copy final")

    for net, text in copy.items():
        st.markdown(f"### {net}")
        st.text_area("", text, height=200)

        st.download_button(
            f"Descarregar {net}",
            text,
            file_name=f"{net}_copy.txt"
        )

    # PROMPTS
    st.subheader("Prompts de imagem")

    for i, p in enumerate(prompts):
        st.markdown(f"### Imagem {i+1}")
        st.text_area("", p, height=150)

        st.download_button(
            f"Download imagem {i+1}",
            p,
            file_name=f"imagem_{i+1}.txt"
        )
