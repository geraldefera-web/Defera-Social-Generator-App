import io
import json
import zipfile
from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="DEFERA Social Planner",
    page_icon="🏟️",
    layout="wide"
)

BRAND_NAME = "DEFERA"

POST_TYPES = ["Post único", "Carrossel", "Story", "Reel"]
NETWORKS = ["Instagram", "LinkedIn", "Facebook"]
CATEGORIES = [
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

CTA_SUGGESTIONS = [
    "Fale com a DEFERA.",
    "Envie mensagem para saber mais.",
    "Se fizer sentido para o seu contexto, fale connosco.",
    "Se quer comunicar melhor, este pode ser o momento certo.",
    "Vamos conversar."
]


def init_state():
    if "generated" not in st.session_state:
        st.session_state.generated = None


def default_num_images(post_type: str) -> int:
    if post_type == "Post único":
        return 1
    if post_type == "Carrossel":
        return 5
    return 3


def get_art_format(post_type: str) -> str:
    if post_type in ["Post único", "Carrossel"]:
        return "1080 x 1350"
    return "1080 x 1920"


def network_rules(networks: list[str]) -> str:
    rules = {
        "Instagram": "copy mais emocional, envolvente, fluido e direto, com boa leitura visual e ritmo natural",
        "LinkedIn": "copy mais reflexivo, profissional, credível e estratégico, sem soar institucional em excesso",
        "Facebook": "copy mais próximo, simples, acessível e comunitário"
    }
    return "\n".join([f"- {n}: {rules[n]}" for n in networks])


def build_slide_plan(theme: str, post_type: str, num_images: int, cta: str) -> list[dict]:
    if post_type == "Post único":
        return [
            {
                "piece_number": 1,
                "label": "Peça única",
                "title": theme,
                "text": f"Mensagem principal sobre {theme.lower()}",
                "cta": cta,
                "layout": "Título no topo esquerdo, texto principal abaixo, espaço visual livre no lado oposto, CTA discreto no rodapé.",
                "visual_goal": "Criar impacto imediato e reforçar a ideia central."
            }
        ]

    if post_type == "Carrossel":
        base = [
            {
                "label": "Gancho",
                "title": "O problema nem sempre está onde parece",
                "text": f"Muitos continuam a lidar com {theme.lower()} sem uma direção clara.",
                "cta": "",
                "layout": "Título no topo esquerdo, texto principal logo abaixo, bastante espaço negativo para reforçar impacto.",
                "visual_goal": "Captar atenção logo na primeira peça."
            },
            {
                "label": "Contexto",
                "title": "Publicar não chega",
                "text": "Sem intenção, a comunicação perde força, consistência e valor percebido.",
                "cta": "",
                "layout": "Título no topo, texto a meio do lado esquerdo, fundo visual limpo e legível.",
                "visual_goal": "Enquadrar o contexto e tornar o problema claro."
            },
            {
                "label": "Problema",
                "title": "O custo é maior do que parece",
                "text": "Perde-se ligação, impacto e capacidade para crescer com consistência.",
                "cta": "",
                "layout": "Título no topo esquerdo, texto curto ao centro, composição forte e contraste elevado.",
                "visual_goal": "Mostrar as consequências."
            },
            {
                "label": "Solução",
                "title": "Com estratégia, o jogo muda",
                "text": "Comunicar melhor é criar clareza, reforçar marca e abrir oportunidades.",
                "cta": "",
                "layout": "Título no topo, texto ao centro, leitura simples e espaço visual limpo.",
                "visual_goal": "Introduzir solução e sentido de caminho."
            },
            {
                "label": "Ação",
                "title": "A DEFERA pode ajudar",
                "text": "Se quer comunicar com mais intenção, este pode ser um bom momento para ajustar.",
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
                "cta": "",
                "layout": "Título no topo, texto curto ao centro, imagem com espaço negativo.",
                "visual_goal": "Captar atenção rapidamente."
            },
            {
                "label": "Desenvolvimento",
                "title": "O que está em causa",
                "text": "A forma como se comunica influencia a perceção de valor.",
                "cta": "",
                "layout": "Título no topo esquerdo, texto logo abaixo, leitura rápida.",
                "visual_goal": "Desenvolver a ideia com clareza."
            },
            {
                "label": "Fecho",
                "title": "É tempo de ajustar",
                "text": "Mais intenção. Mais clareza. Mais impacto.",
                "cta": cta,
                "layout": "Título no topo, texto principal a meio, CTA no rodapé.",
                "visual_goal": "Fechar com força e orientar para ação."
            }
        ]

    plan = []
    for i in range(num_images):
        if i < len(base):
            item = base[i]
        else:
            item = {
                "label": f"Peça {i+1}",
                "title": f"Desenvolvimento {i+1}",
                "text": f"Conteúdo complementar sobre {theme.lower()}",
                "cta": "",
                "layout": "Título no topo, texto principal ao centro, composição simples e limpa.",
                "visual_goal": "Reforçar a continuidade da narrativa."
            }

        plan.append({
            "piece_number": i + 1,
            **item
        })

    return plan


def build_copy_prompt(data: dict, slide_plan: list[dict]) -> str:
    slide_summary = "\n".join(
        [f"{item['piece_number']}. {item['title']} — {item['text']}" for item in slide_plan]
    )

    notes = data["context_notes"].strip()
    notes_block = f"- Notas adicionais: {notes}\n" if notes else ""

    return f"""
Atua como copywriter sénior especializado em marketing desportivo e cria copy pronto a publicar para a marca {BRAND_NAME}.

Identidade da marca:
- comunicação humana, próxima, clara e impactante
- ligada a desporto, marketing, crescimento e posicionamento
- evitar tom excessivamente institucional
- escrever sempre em português de Portugal
- o texto deve soar natural, credível e escrito por uma pessoa real
- não incluir qualquer explicação do processo
- não incluir labels internos como “estrutura da publicação”, “gancho”, “problema” ou semelhantes no copy final

Briefing:
- Objetivo: {data['objective']}
- Tema: {data['theme']}
- Público-alvo: {data['audience']}
- Redes sociais: {", ".join(data['networks'])}
- Formato: {data['post_type']}
- Categoria: {data['category']}
- Foco do serviço/conteúdo: {data['service_focus']}
- Tom pretendido: {data['tone']}
- CTA final: {data['cta']}
{notes_block}
Adaptação obrigatória por rede:
{network_rules(data['networks'])}

Narrativa base da publicação:
{slide_summary}

Entrega exatamente nesta ordem:
1. 3 headlines alternativas
2. texto curto por cada slide/peça, alinhado com a narrativa
3. copy final completo para cada rede social selecionada
4. 8 hashtags coerentes e utilizáveis

Regras críticas:
- o copy final deve estar pronto a publicar
- o copy de cada rede deve ser claramente diferente e adequado ao canal
- não repetir frases feitas nem blocos artificiais
- evitar qualquer texto genérico ou robótico
- o copy não deve incluir a enumeração dos slides
- o copy deve ser variado, estimulante, humano e impactante
""".strip()


def build_image_prompts(data: dict, slide_plan: list[dict]) -> list[dict]:
    prompts = []
    total = len(slide_plan)
    art_format = get_art_format(data["post_type"])

    full_narrative = "\n".join(
        [f"{item['piece_number']}. {item['title']} — {item['text']}" for item in slide_plan]
    )

    for item in slide_plan:
        prompt = f"""
Criar imagem {item['piece_number']} de {total} para a marca {BRAND_NAME}.

Tema geral:
{data['theme']}

Função desta peça:
{item['label']} — {item['visual_goal']}

Mensagem que esta imagem acompanha:
{item['text']}

Direção visual:
- estilo {data['visual_style']}
- ambiente premium, moderno e ligado ao desporto, marketing e performance
- contraste elevado
- composição clean
- sem texto na imagem
- deixar espaço livre para lettering posterior
- garantir coerência visual com as restantes peças da série

Narrativa completa da série:
{full_narrative}

Formato recomendado:
{art_format}
""".strip()

        prompts.append({
            "piece_number": item["piece_number"],
            "title": item["title"],
            "prompt": prompt
        })

    return prompts


def build_zip(copy_prompt: str, slide_plan: list[dict], image_prompts: list[dict]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("01_prompt_copy.txt", copy_prompt)
        zf.writestr("02_plano_por_imagem.json", json.dumps(slide_plan, ensure_ascii=False, indent=2))
        for item in image_prompts:
            zf.writestr(
                f"prompts_imagem/imagem_{item['piece_number']}.txt",
                item["prompt"]
            )
    buffer.seek(0)
    return buffer.read()


init_state()

st.title("DEFERA Social Planner")
st.caption("Gera um Prompt Copy forte, um plano de lettering por imagem e um prompt de imagem por slide.")

with st.sidebar:
    st.subheader("Como usar")
    st.write(
        "1. Preencha o briefing\n"
        "2. Gere o Prompt Copy\n"
        "3. Cole esse prompt no ChatGPT para obter o copy final\n"
        "4. Gere as imagens uma a uma com os prompts por slide\n"
        "5. Monte o lettering no Canva com base no plano por imagem"
    )

with st.form("planner_form"):
    col1, col2 = st.columns(2)

    with col1:
        objective = st.text_input("Objetivo", placeholder="Ex: gerar leads para serviços de marketing desportivo")
        theme = st.text_input("Tema", placeholder="Ex: muitos clubes continuam a comunicar sem estratégia")
        audience = st.text_input("Público", placeholder="Ex: clubes desportivos, dirigentes e responsáveis de comunicação")
        networks = st.multiselect("Redes sociais", NETWORKS, default=["Instagram", "LinkedIn"])
        post_type = st.selectbox("Formato", POST_TYPES)
        category = st.selectbox("Categoria", CATEGORIES)

    with col2:
        service_focus = st.text_input("Foco do serviço/conteúdo", placeholder="Ex: estratégia e comunicação digital")
        tone = st.text_input("Tom pretendido", value="Humano, próximo, profissional e impactante")
        visual_style = st.selectbox("Estilo visual", VISUAL_STYLES)
        cta = st.selectbox("CTA sugerido", CTA_SUGGESTIONS)
        context_notes = st.text_area("Notas adicionais", placeholder="Ex: evitar tom institucional, frases curtas, foco em clareza e credibilidade")

    num_images = st.slider(
        "Número de imagens",
        min_value=1,
        max_value=10,
        value=default_num_images(post_type)
    )

    submitted = st.form_submit_button("Gerar estrutura")

if submitted:
    if not objective or not theme or not audience:
        st.error("Preencha pelo menos objetivo, tema e público.")
    elif not networks:
        st.error("Selecione pelo menos uma rede social.")
    else:
        data = {
            "objective": objective.strip(),
            "theme": theme.strip(),
            "audience": audience.strip(),
            "networks": networks,
            "post_type": post_type,
            "category": category,
            "service_focus": service_focus.strip() if service_focus else "Posicionamento e comunicação",
            "tone": tone.strip() if tone else "Humano, próximo, profissional e impactante",
            "visual_style": visual_style,
            "cta": cta.strip(),
            "context_notes": context_notes.strip(),
            "num_images": num_images,
        }

        slide_plan = build_slide_plan(theme, post_type, num_images, cta)
        copy_prompt = build_copy_prompt(data, slide_plan)
        image_prompts = build_image_prompts(data, slide_plan)

        st.session_state.generated = {
            "data": data,
            "slide_plan": slide_plan,
            "copy_prompt": copy_prompt,
            "image_prompts": image_prompts,
            "art_format": get_art_format(post_type),
        }

        st.success("Estrutura gerada com sucesso.")

generated = st.session_state.generated

if generated:
    tab1, tab2, tab3 = st.tabs(["Prompt Copy", "Plano por imagem", "Prompts de imagem"])

    with tab1:
        st.markdown(f"**Formato recomendado das artes:** {generated['art_format']}")
        st.code(generated["copy_prompt"], language="text")
        st.download_button(
            "Descarregar Prompt Copy",
            data=generated["copy_prompt"].encode("utf-8"),
            file_name="prompt_copy.txt",
            mime="text/plain"
        )

    with tab2:
        st.markdown(f"**Formato recomendado das artes:** {generated['art_format']}")
        for item in generated["slide_plan"]:
            st.markdown(f"### Imagem {item['piece_number']} — {item['label']}")
            st.write(f"**Objetivo visual:** {item['visual_goal']}")
            st.write(f"**Título a aplicar:** {item['title']}")
            st.write(f"**Texto principal:** {item['text']}")
            if item["cta"]:
                st.write(f"**CTA na imagem:** {item['cta']}")
            st.write(f"**Layout recomendado:** {item['layout']}")

    with tab3:
        st.markdown(f"**Formato recomendado das artes:** {generated['art_format']}")
        for item in generated["image_prompts"]:
            st.markdown(f"### Prompt imagem {item['piece_number']} — {item['title']}")
            st.code(item["prompt"], language="text")
            st.download_button(
                f"Descarregar prompt imagem {item['piece_number']}",
                data=item["prompt"].encode("utf-8"),
                file_name=f"prompt_imagem_{item['piece_number']}.txt",
                mime="text/plain",
                key=f"download_prompt_{item['piece_number']}"
            )

    zip_bytes = build_zip(
        generated["copy_prompt"],
        generated["slide_plan"],
        generated["image_prompts"]
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    st.download_button(
        "Descarregar pack completo ZIP",
        data=zip_bytes,
        file_name=f"defera_pack_{timestamp}.zip",
        mime="application/zip"
    )
