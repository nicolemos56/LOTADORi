import folium
import requests
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="Kalawenda", page_icon="🧭", layout="wide")

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #0f766e, #2563eb);
        padding: 1.3rem 1.4rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1rem;
    }
    .bubble {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.7rem;
    }
    .pill {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        margin: 0.2rem 0.2rem 0.2rem 0;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin:0 0 0.3rem 0;">Kalawenda Turístico Inteligente</h1>
        <p style="margin:0; font-size:1rem;">Uma conversa guiada que transforma a intenção do turista em ações: destinos, guias, rotas e transporte.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='pill'>Chat inicial</div><div class='pill'>Descoberta</div><div class='pill'>Guia & transporte</div>", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000/intent"
PLACES_URL = "http://127.0.0.1:8000/places"
GUIDES_URL = "http://127.0.0.1:8000/guides"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "guide_selected" not in st.session_state:
    st.session_state.guide_selected = False

left_col, right_col = st.columns([1.05, 0.95])

with left_col:
    st.subheader("Fluxo turístico em conversa")
    st.markdown(
        """
        <div class="bubble">
            <strong>Exemplo de jornada</strong><br>
            1. O turista inicia com um olá.<br>
            2. A IA responde com acolhimento e sugere destinos.<br>
            3. Ao identificar um destino como Kalandula, oferece imagem e a possibilidade de chamar guias.<br>
            4. O sistema exibe guias e, se selecionado, prepara a ação de transporte.
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        places_response = requests.get(PLACES_URL, timeout=10)
        places_response.raise_for_status()
        places = places_response.json().get("places", [])
    except requests.RequestException:
        places = []

    if places:
        map_center = [places[0]["lat"], places[0]["lng"]]
        tourist_map = folium.Map(location=map_center, zoom_start=13, tiles="CartoDB positron")
        for place in places:
            folium.Marker(
                location=[place["lat"], place["lng"]],
                popup=f"<b>{place['name']}</b><br/>{place['description']}",
                tooltip=place["name"],
            ).add_to(tourist_map)
        st_folium(tourist_map, width=700, height=360)
    else:
        st.info("Ainda não há pontos de interesse disponíveis.")

with right_col:
    st.subheader("Chat do turista")
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="bubble">
                <strong>Kalawenda:</strong> Olá! Eu sou a Kalawenda, a sua assistente turística em Angola. Em que posso ajudar hoje?
            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.guide_selected:
        st.markdown("<div class='bubble'><strong>Estado:</strong> guia selecionado. O taxi está a caminho.</div>", unsafe_allow_html=True)
        try:
            guides_response = requests.get(GUIDES_URL, timeout=10)
            guides_response.raise_for_status()
            guides = guides_response.json().get("guides", [])
        except requests.RequestException:
            guides = []

        if guides:
            guide = guides[0]
            taxi_map = folium.Map(location=[-8.839, 13.289], zoom_start=13, tiles="CartoDB positron")
            folium.Marker([-8.839, 13.289], popup="Você", tooltip="Você").add_to(taxi_map)
            folium.Marker([-8.845, 13.296], popup=f"{guide['name']} — {guide['specialty']}", tooltip=guide["name"]).add_to(taxi_map)
            st_folium(taxi_map, width=650, height=260)
        st.caption("O motorista está a chegar ao ponto de encontro.")

    prompt = st.chat_input("Escreva algo como: oi, Kalandula, guia, taxi")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = requests.post(BACKEND_URL, json={"message": prompt}, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            data = {
                "message": "Não consegui contactar o backend. Verifique se o servidor está em execução.",
                "recommendations": [],
                "next_action": None,
                "image_url": None,
            }

        assistant_text = data.get("message", "Posso ajudar com isso.")
        with st.chat_message("assistant"):
            st.markdown(assistant_text)
            if data.get("image_url"):
                st.image(data["image_url"], caption="Destino sugerido")
            if data.get("recommendations"):
                st.markdown("**Sugestões:**")
                for recommendation in data["recommendations"]:
                    st.markdown(f"- {recommendation['title']}: {recommendation['description']}")
            if data.get("next_action") == "offer_guides":
                st.markdown("👉 Próximo passo: mostrar guias drivers disponíveis para esta experiência.")
            if data.get("next_action") == "show_guides":
                try:
                    guides_response = requests.get(GUIDES_URL, timeout=10)
                    guides_response.raise_for_status()
                    guides = guides_response.json().get("guides", [])
                except requests.RequestException:
                    guides = []
                if guides:
                    st.markdown("**Guias disponíveis:**")
                    for guide in guides:
                        st.markdown(f"- {guide['name']} · {guide['specialty']} · ★ {guide['rating']} · chega em {guide['eta_minutes']} min")
                    if st.button("Selecionar Ana da Serra"):
                        st.session_state.guide_selected = True
                        st.session_state.messages.append({"role": "assistant", "content": "Ana da Serra foi selecionada. O taxi está a caminho."})
                        st.rerun()

        st.session_state.messages.append({"role": "assistant", "content": assistant_text})
