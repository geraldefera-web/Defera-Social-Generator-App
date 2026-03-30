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
        "Instagram": "Copy mais emocional, envolvente, direto e com ritmo. Deve captar atenção rapidamente e gerar interação.",
        "LinkedIn": "Copy mais reflexivo, profissional, estratégico e credível. Deve reforçar autoridade e posicionamento.",
        "Facebook": "Copy mais próximo, claro, acessível e comunitário. Deve ser fácil de ler e gerar identificação."
    }

    rules = []
    for network in selected_networks:
        if network in style_map:
            rules.append(f"- {network}: {style_map[network]}")
    return "\n".join(rules)


def build_master_angle(data):
    service_focus = data.get("service_focus", "").strip()
    tone = data.get("tone", "profissional").strip()
    selected_networks = ", ".join(data["networks"])

    return (
        f"Conteúdo orientado para {data['objective'].lower()}, centrado no tema '{data['theme']}', "
        f"dirigido a {data['audience'].lower()}, com foco em {service_focus.lower() if service_focus else 'posicionamento da DEFERA'}, "
        f"num registo {tone.lower()}, pensado para {selected_networks} e com chamada à ação orientada para '{data['cta']}'."
    )


def build_headlines(data):
    theme = data["theme"]
    return [
        f"{theme} com mais intenção e menos ruído",
        f"O que ainda está a falhar em {theme.lower()}",
        f"Como a DEFERA olha para {theme.lower()}"
    ]


def build_hashtags():
    return [
        "#DEFERA",
        "#MarketingDesportivo",
        "#GestaoDesportiva",
        "#Desporto",
        "#Comunicacao",
        "#RedesSociais"
    ]


def build_structure(data):
    n = data.get("num_images", default_num_images(data["post_type"]))
    theme = data["theme"]
    objective = data["objective"]
    cta = data["cta"]

    if data["post_type"] == "Post único":
        return [{
            "slide_number": 1,
            "title": theme,
            "message": f"Mensagem central orientada para {objective.lower()}."
        }]

    if data["post_type"] == "Carrossel":
        base = [
            {"title": "Gancho", "message": f"Abrir com uma ideia forte sobre {theme.lower()}"},
            {"title": "Contexto", "message": "Enquadrar o problema ou a oportunidade"},
            {"title": "Problema", "message": "Evidenciar o erro, bloqueio ou desafio mais comum"},
            {"title": "Solução", "message": "Apresentar a lógica, visão ou proposta da DEFERA"},
            {"title": "Ação", "message": f"Fechar com chamada à ação orientada para {cta.lower()}"}
        ]
    elif data["post_type"] == "Story":
        base = [
            {"title": "Entrada", "message": f"Introduzir rapidamente o tema '{theme}'"},
            {"title": "Desenvolvimento", "message": "Desenvolver a ideia com clareza e ritmo"},
            {"title": "Fecho", "message": f"Terminar com CTA orientado para {cta.lower()}"}
        ]
    else:
        base = [
            {"title": "Abertura", "message": f"Frame inicial para captar atenção sobre {theme.lower()}"},
            {"title": "Desenvolvimento", "message": "Frame intermédio para desenvolver a narrativa"},
            {"title": "CTA final", "message": f"Frame final com intenção de {cta.lower()}"}
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
            "slide_number": i + 1,
            "title": item["title"],
            "message": item["message"]
        })

    return structure


def build_master_prompt(data, structure):
    networks_text = ", ".join(data["networks"])
    network_rules = network_style_rules(data["networks"])

    return f"""
Atua como copywriter estratégico e diretor criativo especializado em marketing desportivo e cria conteúdo para a marca DEFERA.

Contexto da marca:
- Marca: {DEFERA_BRAND_GUIDE['marca']}
- Tom base: {DEFERA_BRAND_GUIDE['tom']}
- Linguagem: {DEFERA_BRAND_GUIDE['linguagem']}
- Identidade visual: {DEFERA_BRAND_GUIDE['visual']}

Briefing:
- Objetivo: {data['objective']}
- Redes sociais selecionadas: {networks_text}
- Formato: {data['post_type']}
- Categoria: {data['category']}
- Tema: {data['theme']}
- Público-alvo: {data['audience']}
- Serviço ou foco: {data['service_focus']}
- Tom pretendido: {data['tone']}
- Estilo visual: {data['visual_style']}
- CTA: {data['cta']}
- Notas adicionais: {data['context_notes']}
- Número de peças/slides/frames: {data['num_images']}

Estrutura sugerida:
{json.dumps(structure, ensure_ascii=False, indent=2)}

Adaptação obrigatória por rede social:
{network_rules}

Entrega exatamente nesta ordem:
1. Ângulo estratégico do conteúdo
2. 3 headlines alternativas
3. 8 hashtags coerentes
4. Estrutura final por peça/slide/frame
5. Copy separado por rede social selecionada
6. Prompt visual geral para gerar imagens
7. Prompt visual específico por peça/slide/frame

Regras:
- Escrever sempre em português de Portugal
- Soar natural e humano
- Respeitar diferenças claras entre as redes sociais selecionadas
- Se Instagram e LinkedIn estiverem ambos selecionados, o copy deve ser claramente diferente entre ambos
- Não usar tom excessivamente institucional
- Não incluir explicações sobre o processo
- Organizar a resposta com títulos claros
""".strip()


def build_visual_prompt(data, structure):
    return f"""
Cria um conceito visual para conteúdo da marca DEFERA.

Identidade visual da marca:
- {DEFERA_BRAND_GUIDE['visual']}
- Sem excesso de elementos
- Imagem forte, moderna e profissional
- Ligação clara ao universo do desporto e do marketing

Briefing:
- Tema: {data['theme']}
- Formato: {data['post_type']}
- Número de peças: {data['num_images']}
- Público-alvo: {data['audience']}
- Estilo visual pretendido: {data['visual_style']}
- Notas adicionais: {data['context_notes']}

Estrutura pretendida:
{json.dumps(structure, ensure_ascii=False, indent=2)}

Entrega:
- Um prompt visual geral
- Um prompt visual por slide/frame
- Sugestão de composição, ambiente, enquadramento, luz e elementos visuais
- Sem texto embutido nas imagens
""".strip()


def build_canva_prompts(data, structure):
    prompts = []
    for item in structure:
        prompt = (
            f"Criar imagem para a marca DEFERA, estilo {data['visual_style'].lower()}, "
            f"tema '{data['theme']}', peça {item['slide_number']} de um formato {data['post_type'].lower()}, "
            f"com foco em {item['message'].lower()}, ambiente desportivo, fundo escuro, contraste elevado, "
            f"estética premium, composição clean, sem texto na imagem."
        )
        prompts.append({
            "slide_number": str(item["slide_number"]),
            "title": item["title"],
            "prompt": prompt
        })
    return prompts


def build_publication_checklist():
    return [
        "Validar se o copy está adaptado a cada rede selecionada",
        "Confirmar coerência com a identidade visual da DEFERA",
        "Verificar se a chamada à ação está clara",
        "Gerar ou ajustar imagens com base nos prompts",
        "Rever ortografia e legibilidade final",
        "Descarregar criativos e copy final",
        "Publicar manualmente no canal adequado"
    ]


def build_pack(data):
    structure = build_structure(data)

    return {
        "master_angle": build_master_angle(data),
        "headlines": build_headlines(data),
        "hashtags": build_hashtags(),
        "structure": structure,
        "master_prompt": build_master_prompt(data, structure),
        "visual_prompt": build_visual_prompt(data, structure),
        "canva_prompts": build_canva_prompts(data, structure),
        "publication_checklist": build_publication_checklist(),
    }


def build_zip_bytes(pack):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("pack_completo.json", json.dumps(pack, ensure_ascii=False, indent=2))
        zf.writestr("01_prompt_mestre.txt", pack["master_prompt"])
        zf.writestr("02_prompt_visual.txt", pack["visual_prompt"])
        zf.writestr("03_checklist_publicacao.txt", "\n".join(pack["publication_checklist"]))
        zf.writestr("04_headlines.txt", "\n".join(pack["headlines"]))
        zf.writestr("05_hashtags.txt", " ".join(pack["hashtags"]))

        for item in pack["canva_prompts"]:
            zf.writestr(
                f"prompts_visuais/slide_{item['slide_number']}.txt",
                item["prompt"]
            )

    buffer.seek(0)
    return buffer.read()


init_state()

st.title("DEFERA Social Planner")
st.caption("Ferramenta para gerar um prompt mestre único, ajustado ao briefing e às redes sociais selecionadas")

with st.sidebar:
    st.subheader("Modo de utilização")
    st.write(
        "1. Preencher o briefing\n"
        "2. Selecionar uma ou várias redes sociais\n"
        "3. Gerar o prompt mestre\n"
        "4. Colar o prompt no ChatGPT\n"
        "5. Obter copy e imagens com base nesse prompt"
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

    submitted = st.form_submit_button("Gerar prompt mestre")

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
            "service_focus": service_focus,
            "tone": tone if tone else "profissional",
            "visual_style": visual_style,
            "cta": cta,
            "context_notes": context_notes,
            "num_images": num_images,
        }

        st.session_state.generated_pack = build_pack(data)
        st.success("Prompt mestre gerado com sucesso.")

pack = st.session_state.generated_pack

if pack:
    st.divider()
    st.subheader("Ângulo estratégico")
    st.write(pack["master_angle"])

    tab1, tab2, tab3, tab4 = st.tabs([
        "Prompt mestre",
        "Estrutura",
        "Visual",
        "Checklist"
    ])

    with tab1:
        st.text_area("Prompt mestre para ChatGPT", pack["master_prompt"], height=420)
        st.download_button(
            "Descarregar prompt mestre",
            data=pack["master_prompt"].encode("utf-8"),
            file_name="prompt_mestre_chatgpt.txt",
            mime="text/plain"
        )

    with tab2:
        st.write("**Headlines sugeridas**")
        for item in pack["headlines"]:
            st.write(f"- {item}")

        st.write("**Hashtags sugeridas**")
        st.write(" ".join(pack["hashtags"]))

        st.write("**Estrutura sugerida**")
        st.json(pack["structure"])

    with tab3:
        st.text_area("Prompt visual geral", pack["visual_prompt"], height=260)
        st.write("**Prompts visuais por peça**")
        for item in pack["canva_prompts"]:
            st.markdown(f"### Peça {item['slide_number']} — {item['title']}")
            st.code(item["prompt"], language="text")

    with tab4:
        for item in pack["publication_checklist"]:
            st.write(f"- {item}")

    zip_bytes = build_zip_bytes(pack)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    st.download_button(
        "Descarregar pack completo ZIP",
        data=zip_bytes,
        file_name=f"defera_prompt_pack_{timestamp}.zip",
        mime="application/zip"
    )
