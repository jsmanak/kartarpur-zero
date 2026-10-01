import streamlit as st
import os
import re
import glob
from google import genai
from google.genai import types

st.set_page_config(page_title="Kartarpur-0 | Sangat-Sim", page_icon="🌾", layout="wide")

# Base styling
st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: 700; color: #E0A96D; margin-bottom: 0px;}
    .sub-header {font-size: 1.1rem; color: #A0AAB2; margin-bottom: 20px;}
    .spec-card {background-color: #1A1C23; padding: 20px; border-radius: 10px; border-left: 4px solid #E0A96D; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# Grounding Documents
def load_context():
    ctx = ""
    for path in ["charter/CHARTER.md", "governance/GOVERNANCE.md"]:
        if os.path.exists(path):
            with open(path, "r") as f:
                ctx += f"\n--- {path} ---\n" + f.read()
    for path in glob.glob("infrastructure/specs/*.md"):
        with open(path, "r") as f:
            ctx += f"\n--- {path} ---\n" + f.read()
    return ctx

context_docs = load_context()

SYSTEM_PROMPT = f"""
You are the Voice of Kartarpur-0 (Sangat-Sim), an intelligent civic oracle representing a future post-scarcity, multi-generational commune in northern Canada.
The society is anchored in universal Sikh ethics (Kirat - craft; Vand Chhako - sovereign dividend; Seva - selfless contribution; Langar - radical equality; Miri-Piri - temporal defense & spiritual reflection) backed by closed-loop automation.

Reference Specs:
{context_docs}

Directives:
1. Explain with grounded clarity how the commune functions, lives, feels, and governs itself.
2. Welcome rigorous stress-testing.
3. Language: Detect input language (Punjabi, English, Hindi, etc.) and respond natively with cultural warmth and engineering precision.
4. Edge Case Logging: Append [RFC_TRIGGER]: {{"title": "<summary>", "category": "<governance|infrastructure|ethics>", "severity": "<low|medium|high>"}} if a systemic policy gap is identified.
"""

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

tab_chat, tab_arch, tab_manifesto = st.tabs(["🌾 Civic Oracle & Voice", "📐 Architectural Schematics", "📜 The Living Charter"])

# ----------------- TAB 1: ORACLE & VOICE -----------------
with tab_chat:
    st.markdown('<div class="main-header">🌾 Kartarpur-0: Sangat-Sim</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive Multi-Generational Civic Intelligence & Voice Interface</div>', unsafe_allow_html=True)

    enable_voice = st.sidebar.checkbox("🔊 Enable Text-to-Speech Voice Responses", value=False)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Sat Sri Akal / Welcome. I am the civic oracle for **Kartarpur-0**. Ask me anything about daily routines, automated infrastructure, or dispute resolution in English or Punjabi."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question, propose a scenario, or stress-test an edge case...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if not api_key:
            with st.chat_message("assistant"):
                st.error("Please configure GEMINI_API_KEY in Streamlit Secrets or sidebar.")
        else:
            client = genai.Client(api_key=api_key)
            models_to_try = ["gemini-flash-latest", "gemini-3.7-flash", "gemini-flash-lite-latest"]

            full_text = None
            last_error = None

            with st.chat_message("assistant"):
                with st.spinner("Reflecting on the commons..."):
                    for model in models_to_try:
                        try:
                            chat = client.chats.create(
                                model=model,
                                config=types.GenerateContentConfig(
                                    system_instruction=SYSTEM_PROMPT,
                                    temperature=0.3
                                )
                            )
                            resp = chat.send_message(user_input)
                            if resp.text:
                                full_text = resp.text.strip()
                                break
                        except Exception as e:
                            last_error = e
                            continue

                if full_text:
                    rfc_match = re.search(r'\[RFC_TRIGGER\]:\s*(\{.*\})', full_text)
                    clean_text = re.sub(r'\[RFC_TRIGGER\]:.*', '', full_text).strip()
                    st.markdown(clean_text)

                    # Optional Voice Synthesis
                    if enable_voice:
                        try:
                            # Generate natural spoken audio for the text
                            voice_resp = client.models.generate_content(
                                model="gemini-2.5-flash-preview-tts",
                                contents=f"Read this clearly and warmly: {clean_text[:400]}",
                                config=types.GenerateContentConfig(response_mime_type="audio/mp3")
                            )
                            if hasattr(voice_resp, "audio_content") and voice_resp.audio_content:
                                st.audio(voice_resp.audio_content, format="audio/mp3")
                        except Exception:
                            # Graceful fallback if TTS endpoint is busy
                            pass

                    if rfc_match:
                        st.warning(f"⚠️ **Edge Case Logged for Repository RFC:**\n`{rfc_match.group(1)}`")

                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                else:
                    st.error(f"Error querying Gemini: {last_error}")

# ----------------- TAB 2: ARCHITECTURE & SCHEMATICS -----------------
with tab_arch:
    st.header("📐 Physical & Systems Architecture")
    st.write("Kartarpur-0 utilizes a **concentric, biophilic layout** designed for extreme Canadian subarctic resilience (-50°C to +35°C). All industrial automation and life-support loops are subterranean, leaving the surface dedicated to community, sacred craft, and nature.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Concentric Node Topography (~150 Residents)
        ```text
        [ OUTSIDE BOREAL FOREST & SOLAR/WIND HARVEST ]
                             │
            ┌────────────────┴────────────────┐
            │   Ring 3: Earth-Sheltered Dwellings  │
            │   (Private Hearths / Soundproofed)  │
            │  ┌───────────────────────────┐  │
            │  │  Ring 2: Community Agora  │  │
            │  │  - Langar Hall & Kitchen  │  │
            │  │  - Darbar Reconciliation │  │
            │  │  - Craft / Kirat Studios  │  │
            │  │  ┌─────────────────────┐  │  │
            │  │  │ Ring 1: Biophilic   │  │  │
            │  │  │ Central Glass Atrium│  │  │
            │  │  └─────────────────────┘  │  │
            │  └───────────────────────────┘  │
            └─────────────────────────────────┘
        ```
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        ### Subterranean Life-Support & Thermal Circuit
        ```text
        [ Compute Cluster Heat Waste (Anandgarh) ]
                             │
                             ▼ (Hydronic Glycol Loop: 55°C)
        [ Subterranean Walipini Greenhouses / CEA Aeroponics ]
                             │
                             ▼ (Residual Heat: 28°C)
        [ Radiant Floor Network in Living Dwellings ]
                             │
                             ▼ (Geothermal Ground Recharge: 12°C)
        [ Deep Earth Bed Absorption / Loop Return ]
        ```
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Subarctic Fail-Safe Specifications")
    st.markdown("""
    * **Thermal Redundancy:** Passive mechanical bypasses activate if power fails, preventing freeze-up down to -50°C without firmware dependency.
    * **Langar Caloric Buffer:** 180-day sealed subterranean seed and dehydrated grain surplus alongside continuous vertical aeroponics.
    * **Zero-Knowledge Privacy:** Dwellings are hardware-isolated from communal telemetry; no cameras or biometric sensors inside the private hearth.
    """)

# ----------------- TAB 3: MANIFESTO & GOVERNANCE -----------------
with tab_manifesto:
    st.header("📜 The Covenant of the Commons")
    for doc_name, path in [("Charter", "charter/CHARTER.md"), ("Governance", "governance/GOVERNANCE.md")]:
        if os.path.exists(path):
            with open(path, "r") as f:
                with st.expander(f"📖 View {doc_name}", expanded=True):
                    st.markdown(f.read())
