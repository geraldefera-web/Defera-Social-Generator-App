import streamlit as st


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


def get_layout_format(post_type):
    if post_type in ["Post único", "Carrossel"]:
        return "1080 x 1350"
    return "1080 x 1920"


def build_hashtags(data):
    base = [
        "#DEFERA",
        "#MarketingDesportivo",
        "#GestaoDesportiva",
        "#Desporto",
        "#Comunicacao",
        "#RedesSociais"
    ]

    audience = data["audience"].lower()
    theme = data["theme"].lower()

    if "clube" in audience or "clubes" in audience:
        base.append("#ClubesDesportivos")

    if "estratégia" in theme or "estrategia" in theme:
        base.append("#EstrategiaDigital")

    return " ".join(base[:8])


def build_structure(theme, post_type, num, cta):
    if post_type == "Post único":
        return [
            {
                "piece_number": 1,
                "label": "Peça única",
                "title": theme,
                "text": f"Mensagem central sobre {theme.lower()}",
                "support_text": "",
                "cta": cta,
                "layout": "Título no topo esquerdo, texto principal ao centro ou à esquerda, área visual limpa do lado oposto, CTA discreto no rodapé.",
                "visual_goal": "Criar impacto imediato e reforçar o tema central."
            }
        ]

    if post_type == "Carrossel":
        base = [
            {
                "label": "Gancho",
                "title": "O problema não é falta de esforço",
                "text": f"Muitos continuam a lidar com {theme.lower()} sem uma direção clara.",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo esquerdo, texto principal abaixo, imagem com espaço livre à esquerda.",
                "visual_goal": "Criar impacto e captar atenção logo na primeira peça."
            },
            {
                "label": "Contexto",
                "title": "Publicar não chega",
                "text": "Sem intenção, a comunicação perde força, consistência e valor.",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo, texto principal a meio do lado esquerdo, fundo visual limpo.",
                "visual_goal": "Mostrar enquadramento e contexto do problema."
            },
            {
                "label": "Problema",
                "title": "O custo é maior do que parece",
                "text": "Perde-se ligação, impacto e capacidade para crescer com consistência.",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo esquerdo, texto central curto, composição forte com contraste elevado.",
                "visual_goal": "Evidenciar consequências e criar tensão narrativa."
            },
            {
                "label": "Solução",
                "title": "Com estratégia, o jogo muda",
                "text": "Comunicar melhor é criar clareza, reforçar marca e abrir oportunidades.",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo, texto principal ao centro, espaço livre para leitura simples.",
                "visual_goal": "Introduzir solução, clareza e sentido de caminho."
            },
            {
                "label": "Ação",
                "title": "A DEFERA pode ajudar",
                "text": "Se quer comunicar com mais intenção, este pode ser um bom momento para ajustar.",
                "support_text": "",
                "cta": cta,
                "layout": "Título no topo esquerdo, texto principal ao centro, CTA no rodapé.",
                "visual_goal": "Fechar a narrativa e conduzir à ação."
            }
        ]
    else:
        base = [
            {
                "label": "Abertura",
                "title": theme,
                "text": f"Introdução rápida sobre {theme.lower()}",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo, texto curto ao centro, imagem com bastante espaço negativo.",
                "visual_goal": "Captar atenção rapidamente."
            },
            {
                "label": "Desenvolvimento",
                "title": "O que está em causa",
                "text": "A forma como se comunica influencia diretamente a perceção de valor.",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo esquerdo, texto principal abaixo, leitura rápida.",
                "visual_goal": "Desenvolver a narrativa com clareza."
            },
            {
                "label": "Fecho",
                "title": "É tempo de ajustar",
                "text": "Mais intenção. Mais clareza. Mais impacto.",
                "support_text": "",
                "cta": cta,
                "layout": "Título no topo, texto principal a meio, CTA no rodapé.",
                "visual_goal": "Fechar com força e orientar para ação."
            }
        ]

    structure = []
    for i in range(num):
        if i < len(base):
            item = base[i]
        else:
            item = {
                "label": f"Peça {i+1}",
                "title": f"Desenvolvimento {i+1}",
                "text": f"Conteúdo complementar sobre {theme.lower()}",
                "support_text": "",
                "cta": "",
                "layout": "Título no topo, texto principal ao centro, composição simples e limpa.",
                "visual_goal": "Reforçar a continuidade da narrativa."
            }

        structure.append({
            "piece_number": i + 1,
            **item
        })

    return structure


def build_copy(data, structure):
    hashtags = build_hashtags(data)
    theme = data["theme"]
    cta = data["cta"]

    copy = {}

    if "Instagram" in data["networks"]:
        copy["Instagram"] = (
            f"{theme}\n\n"
            "Há quem continue a comunicar por rotina.\n"
            "Mas hoje isso já não chega.\n\n"
            "Quando falta direção, perde-se impacto, coerência e valor percebido.\n\n"
            "Comunicar melhor não é publicar mais.\n"
            "É saber o que dizer, como dizer e para quem dizer.\n\n"
            f"{cta}\n\n"
            f"{hashtags}"
        )

    if "LinkedIn" in data["networks"]:
        copy["LinkedIn"] = (
            f"{theme}\n\n"
            "No desporto, continua a existir um padrão que limita o crescimento de muitas organizações.\n\n"
            "A comunicação existe.\n"
            "Mas nem sempre existe com intenção estratégica.\n\n"
            "E quando isso acontece, perde-se clareza, consistência e capacidade para gerar valor.\n\n"
            "Hoje, comunicar bem não é estar apenas presente.\n"
            "É ser relevante.\n\n"
            f"{cta}\n\n"
            f"{hashtags}"
        )

    if "Facebook" in data["networks"]:
        copy["Facebook"] = (
            f"{theme}\n\n"
            "Nem sempre o problema está na falta de vontade.\n"
            "Muitas vezes está na falta de direção.\n\n"
            "Comunicar melhor pode fazer toda a diferença.\n\n"
            f"{cta}\n\n"
            f"{hashtags}"
        )

    return copy


def build_image_prompts(data, structure):
    prompts = []

    for item in structure:
        prompt = f"""Criar imagem {item['piece_number']} de {len(structure)} para a marca DEFERA.

Tema geral:
{data['theme']}

Função narrativa desta peça:
{item['label']} — {item['visual_goal']}

Mensagem desta peça:
{item['text']}

Estilo visual:
{data['visual_style']}

Regras:
- fundo escuro ou visual premium
- estética desportiva, moderna e profissional
- contraste elevado
- composição clean
- sem texto na imagem
- garantir espaço livre para lettering posterior
- coerência visual com as restantes peças da publicação

Formato recomendado:
{get_layout_format(data['post_type'])}
"""
        prompts.append(prompt)

    return prompts


st.title("DEFERA Content Generator")
st.caption("Geração de copy final, hashtags, plano de lettering por imagem e prompts visuais")

with st.form("content_form"):
    col1, col2 = st.columns(2)

    with col1:
        objective = st.text_input("Objetivo", placeholder="Ex: gerar leads para serviços de marketing desportivo")
        theme = st.text_input("Tema", placeholder="Ex: muitos clubes continuam a comunicar sem estratégia")
        audience = st.text_input("Público", placeholder="Ex: clubes desportivos, dirigentes e responsáveis de comunicação")
        networks = st.multiselect("Redes sociais", NETWORKS, default=["Instagram"])
        post_type = st.selectbox("Formato", POST_TYPES)

    with col2:
        visual_style = st.selectbox("Estilo visual", VISUAL_STYLES)
        cta = st.text_input("CTA", value="Fale com a DEFERA.")
        context_notes = st.text_area("Notas adicionais", placeholder="Ex: foco em credibilidade, linguagem simples, tom profissional")

    num_images = st.slider(
        "Número de imagens",
        min_value=1,
        max_value=10,
        value=default_num_images(post_type)
    )

    submitted = st.form_submit_button("Gerar conteúdo")

if submitted:
    if not objective or not theme or not audience:
        st.error("Preencha pelo menos objetivo, tema e público.")
    elif not networks:
        st.error("Selecione pelo menos uma rede social.")
    else:
        data = {
            "objective": objective,
            "theme": theme,
            "audience": audience,
            "networks": networks,
            "post_type": post_type,
            "visual_style": visual_style,
            "cta": cta,
            "context_notes": context_notes,
            "num_images": num_images
        }

        structure = build_structure(theme, post_type, num_images, cta)
        copy = build_copy(data, structure)
        prompts = build_image_prompts(data, structure)
        layout_format = get_layout_format(post_type)

        st.success("Conteúdo gerado com sucesso.")

        tab1, tab2, tab3 = st.tabs(["Copy final", "Plano por imagem", "Prompts de imagem"])

        with tab1:
            st.markdown(f"**Formato recomendado das artes:** {layout_format}")

            for net, text in copy.items():
                st.markdown(f"### {net}")
                st.text_area(f"Copy {net}", text, height=260, key=f"copy_{net}")
                st.download_button(
                    f"Descarregar copy {net}",
                    text,
                    file_name=f"{net.lower()}_copy.txt"
                )

        with tab2:
            st.markdown(f"**Formato recomendado das artes:** {layout_format}")

            for item in structure:
                st.markdown(f"### Imagem {item['piece_number']} — {item['label']}")
                st.write(f"**Objetivo visual:** {item['visual_goal']}")
                st.write(f"**Título a aplicar:** {item['title']}")
                st.write(f"**Texto principal:** {item['text']}")

                if item["support_text"]:
                    st.write(f"**Texto de apoio:** {item['support_text']}")

                if item["cta"]:
                    st.write(f"**CTA na imagem:** {item['cta']}")

                st.write(f"**Layout recomendado:** {item['layout']}")

        with tab3:
            st.markdown(f"**Formato recomendado das artes:** {layout_format}")

            for i, p in enumerate(prompts):
                st.markdown(f"### Prompt imagem {i+1}")
                st.text_area(f"Prompt {i+1}", p, height=220, key=f"prompt_{i+1}")
                st.download_button(
                    f"Descarregar prompt imagem {i+1}",
                    p,
                    file_name=f"imagem_{i+1}_prompt.txt"
                )
