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


def network_style_rules(selected_networks):
    style_map = {
        "Instagram": "Copy mais emocional, envolvente, direto e com ritmo.",
        "LinkedIn": "Copy mais reflexivo, profissional, estratégico e credível.",
        "Facebook": "Copy mais próximo, claro, acessível e comunitário."
    }

    rules = []
    for network in selected_networks:
        if network in style_map:
            rules.append(f"- {network}: {style_map[network]}")
    return "\n".join(rules)


def build_structure(data):
    n = data.get("num_images", default_num_images(data["post_type"]))
    theme = data["theme"]
    cta = data["cta"]

    if data["post_type"] == "Post único":
        return [{
            "piece_number": 1,
            "title": theme,
            "message": f"Mensagem visual única centrada no tema '{theme}'."
        }]

    if data["post_type"] == "Carrossel":
        base = [
            {"title": "Gancho", "message": f"Abertura forte sobre {theme.lower()}"},
            {"title": "Contexto", "message": "Enquadrar o problema ou a oportunidade"},
            {"title": "Problema", "message": "Evidenciar o erro, bloqueio ou desafio"},
            {"title": "Solução", "message": "Apresentar visão, estratégia ou caminho"},
            {"title": "Ação", "message": f"Fecho com chamada à ação orientada para {cta.lower()}"}
        ]
    elif data["post_type"] == "Story":
        base = [
            {"title": "Entrada", "message": f"Introduzir o tema '{theme}'"},
            {"title": "Desenvolvimento", "message": "Desenvolver a ideia de forma simples e rápida"},
            {"title": "Fecho", "message": f"Terminar com chamada à ação orientada para {cta.lower()}"}
        ]
    else:
        base = [
            {"title": "Abertura", "message": f"Frame inicial sobre {theme.lower()}"},
            {"title": "Desenvolvimento", "message": "Frame intermédio para desenvolver a narrativa"},
            {"title": "Fecho", "message": f"Frame final com intenção de {cta.lower()}"}
        ]

    structure = []
    for i in range(n):
        if i < len(base):
            item = base[i]
        else:
            item = {
                "title": f"Peça {i + 1}",
                "message": f"Conteúdo complementar relacionado com {theme.lower()}"
            }

        structure.append({
            "piece_number": i + 1,
            "title": item["title"],
            "message": item["message"]
        })

    return structure


def build_global_image_prompt(data, structure):
    pieces_text = "\n".join(
        [f"{item['piece_number']}. {item['title']} — {item['message']}" for item in structure]
    )

    return f"""
Cria a direção visual de uma publicação da marca DEFERA.

Contexto da marca:
- Marca: {DEFERA_BRAND_GUIDE['marca']}
- Identidade visual: {DEFERA_BRAND_GUIDE['visual']}
- Linguagem visual: moderna, desportiva, profissional e coerente
- Sem texto embutido nas imagens

Briefing:
- Tema: {data['theme']}
- Formato: {data['post_type']}
- Número de peças/imagens: {data['num_images']}
- Público-alvo: {data['audience']}
- Categoria: {data['category']}
- Estilo visual pretendido: {data['visual_style']}
- Notas adicionais: {data['context_notes']}

Instruções obrigatórias:
- As imagens devem manter coerência visual entre si
- Fundo preferencialmente escuro ou visual premium compatível com a identidade da DEFERA
- Estética clean, contraste elevado e linguagem ligada ao desporto, marketing e performance
- Não incluir texto dentro das imagens
- Cada imagem deve corresponder a uma etapa da narrativa abaixo

Estrutura visual:
{pieces_text}
""".strip()


def build_individual_image_prompts(data, structure):
    prompts = []
    total = len(structure)

    narrative = "\n".join(
        [f"{item['piece_number']}. {item['title']} — {item['message']}" for item in structure]
    )

    for item in structure:
        prompt = f"""
Cria a imagem {item['piece_number']} de {total} para uma publicação da marca DEFERA.

Objetivo desta imagem:
- {item['title']}
- {item['message']}

Contexto global da publicação:
- Tema: {data['theme']}
- Formato: {data['post_type']}
- Público-alvo: {data['audience']}
- Categoria: {data['category']}
- Estilo visual: {data['visual_style']}
- Identidade da marca: {DEFERA_BRAND_GUIDE['visual']}
- Notas adicionais: {data['context_notes']}

Regras obrigatórias:
- Esta imagem deve parecer parte da mesma série visual das restantes
- Manter coerência estética com as outras imagens da publicação
- Ambiente premium, moderno, ligado ao desporto, marketing e performance
- Fundo escuro ou linguagem visual coerente com a DEFERA
- Contraste elevado
- Composição clean
- Sem texto dentro da imagem
- A imagem deve transmitir claramente a função narrativa desta peça

Narrativa completa da série:
{narrative}

Agora gera apenas a imagem {item['piece_number']} de {total}, respeitando a coerência com o conjunto.
""".strip()

        prompts.append({
            "piece_number": item["piece_number"],
            "title": item["title"],
            "prompt": prompt
        })

    return prompts


def build_copy_prompt(data, structure):
    pieces_text = "\n".join(
        [f"{item['piece_number']}. {item['title']} — {item['message']}" for item in structure]
    )

    selected_networks = ", ".join(data["networks"])
    rules = network_style_rules(data["networks"])

    return f"""
Atua como copywriter estratégico especializado em marketing desportivo e cria o copy para uma publicação da DEFERA.

Contexto da marca:
- Marca: {DEFERA_BRAND_GUIDE['marca']}
- Tom base: {DEFERA_BRAND_GUIDE['tom']}
- Linguagem: {DEFERA_BRAND_GUIDE['linguagem']}

Briefing:
- Objetivo: {data['objective']}
- Redes sociais selecionadas: {selected_networks}
- Formato: {data['post_type']}
- Categoria: {data['category']}
- Tema: {data['theme']}
- Público-alvo: {data['audience']}
- Serviço ou foco: {data['service_focus']}
- Tom pretendido: {data['tone']}
- CTA: {data['cta']}
- Notas adicionais: {data['context_notes']}
- Número de peças/slides/frames: {data['num_images']}

Estrutura da publicação:
{pieces_text}

Adaptação obrigatória por rede social:
{rules}

Entrega exatamente nesta ordem:
1. Ângulo estratégico do conteúdo
2. 3 headlines alternativas
3. Estrutura textual resumida por peça
4. Copy separado por cada rede social selecionada
5. CTA final
6. 8 hashtags coerentes

Regras:
- Escrever sempre em português de Portugal
- Soar natural e humano
- O copy deve alinhar com a estrutura da publicação
- Se mais do que uma rede social estiver selecionada, o copy deve ser diferente e adequado a cada uma
- Não incluir explicações sobre o processo
- Organizar a resposta com títulos claros
""".strip()


def build_publication_checklist():
    return [
        "Gerar o copy com o Prompt Copy",
        "Gerar cada imagem separadamente com o respetivo Prompt Imagem",
        "Confirmar coerência entre copy e narrativa visual",
        "Validar se o copy está adaptado a cada rede selecionada",
        "Rever ortografia e legibilidade final",
        "Descarregar os criativos finais",
        "Publicar manualmente nos canais selecionados"
    ]


def build_pack(data):
    structure = build_structure(data)

    return {
        "structure": structure,
        "global_image_prompt": build_global_image_prompt(data, structure),
        "individual_image_prompts": build_individual_image_prompts(data, structure),
        "copy_prompt": build_copy_prompt(data, structure),
        "publication_checklist": build_publication_checklist(),
    }


def build_zip_bytes(pack):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("pack_completo.json", json.dumps(pack, ensure_ascii=False, indent=2))
        zf.writestr("01_prompt_copy.txt", pack["copy_prompt"])
        zf.writestr("02_prompt_imagens_global.txt", pack["global_image_prompt"])
        zf.writestr("03_checklist_publicacao.txt", "\n".join(pack["publication_checklist"]))

        for item in pack["individual_image_prompts"]:
            zf.writestr(
                f"prompts_imagens/imagem_{item['piece_number']}.txt",
                item["prompt"]
            )

    buffer.seek(0)
    return buffer.read()


init_state()

st.title("DEFERA Social Planner")
st.caption("Ferramenta para gerar 1 Prompt Copy e 1 prompt individual por cada imagem/slide")

with st.sidebar:
    st.subheader("Modo de utilização")
    st.write(
        "1. Preencher o briefing\n"
        "2. Gerar os prompts\n"
        "3. Colar o Prompt Copy no ChatGPT texto\n"
        "4. Gerar cada imagem separadamente com o respetivo prompt\n"
        "5. Publicar manualmente"
    )

with st.form("planner_form"):
    col1, col2 = st.columns(2)

    with col1:
        objective = st.text_input("Objetivo", placeholder="Ex: gerar leads para serviços de marketing desportivo")
        networks = st.multiselect("Redes sociais", NETWORKS, default=["Instagram"])
        post_type = st.selectbox("Formato", POST_TYPES)
        category = st.selectbox("Categoria", CONTENT_CATEGORIES)
        theme = st.text_input("Tema", placeholder="Ex: muitos clubes continuam a comunicar sem estratégia")
        audience = st.text_input("Público", placeholder="Ex: clubes, dirigentes e responsáveis de comunicação")

    with col2:
        service_focus = st.text_input("Serviço ou foco", placeholder="Ex: consultoria, redes sociais, estratégia")
        tone = st.text_input("Tom pretendido", placeholder="Ex: próximo, confiante, profissional e claro")
        visual_style = st.selectbox("Estilo visual", VISUAL_STYLES)
        cta = st.selectbox("CTA principal", CTA_OPTIONS)
        context_notes = st.text_area("Notas adicionais", placeholder="Ex: evitar excesso de texto, foco em credibilidade")

    num_images = st.slider(
        "Número de peças/slides/frames",
        min_value=1,
        max_value=10,
        value=default_num_images(post_type)
    )

    submitted = st.form_submit_button("Gerar prompts")

if submitted:
    if not objective or not theme or not audience:
        st.error("Preencha pelo menos objetivo, tema e público.")
    elif not networks:
        st.error("Selecione pelo menos uma rede social.")
    else:
        data = {
            "objective": objective,
            "networks": networks,
            "post_type": post_type,
            "category": category,
            "theme": theme,
            "audience": audience,
            "service_focus": service_focus if service_focus else "Posicionamento e comunicação da DEFERA",
            "tone": tone if tone else "Próximo, profissional e claro",
            "visual_style": visual_style,
            "cta": cta,
            "context_notes": context_notes if context_notes else "Manter coerência com a identidade da DEFERA",
            "num_images": num_images,
        }

        st.session_state.generated_pack = build_pack(data)
        st.success("Prompts gerados com sucesso.")

pack = st.session_state.generated_pack

if pack:
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Prompt Copy",
        "Prompt Imagens Global",
        "Prompts por Imagem",
        "Checklist"
    ])

    with tab1:
        st.text_area("Prompt para gerar copy", pack["copy_prompt"], height=420)
        st.download_button(
            "Descarregar Prompt Copy",
            data=pack["copy_prompt"].encode("utf-8"),
            file_name="prompt_copy.txt",
            mime="text/plain"
        )

    with tab2:
        st.text_area("Prompt global de referência visual", pack["global_image_prompt"], height=360)
        st.download_button(
            "Descarregar Prompt Imagens Global",
            data=pack["global_image_prompt"].encode("utf-8"),
            file_name="prompt_imagens_global.txt",
            mime="text/plain"
        )

    with tab3:
        for item in pack["individual_image_prompts"]:
            st.markdown(f"### Imagem {item['piece_number']} — {item['title']}")
            st.text_area(
                f"Prompt imagem {item['piece_number']}",
                item["prompt"],
                height=260,
                key=f"img_prompt_{item['piece_number']}"
            )
            st.download_button(
                f"Descarregar Prompt Imagem {item['piece_number']}",
                data=item["prompt"].encode("utf-8"),
                file_name=f"prompt_imagem_{item['piece_number']}.txt",
                mime="text/plain",
                key=f"download_img_prompt_{item['piece_number']}"
            )

    with tab4:
        for item in pack["publication_checklist"]:
            st.write(f"- {item}")

    zip_bytes = build_zip_bytes(pack)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    st.download_button(
        "Descarregar pack completo ZIP",
        data=zip_bytes,
        file_name=f"defera_prompts_{timestamp}.zip",
        mime="application/zip"
    )
