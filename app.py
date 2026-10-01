import streamlit as st
import streamlit.components.v1 as components
import os
import re
import glob
from google import genai
from google.genai import types

st.set_page_config(page_title="Kartarpur-0 | Sangat-Sim", page_icon="🌾", layout="wide")

st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: 700; color: #E0A96D; margin-bottom: 0px;}
    .sub-header {font-size: 1.05rem; color: #A0AAB2; margin-bottom: 16px;}
    .narrative-card {background: #1e222b; padding: 20px; border-radius: 8px; border-left: 4px solid #E0A96D; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

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

tab_chat, tab_arch, tab_narrative = st.tabs(["🎙️ Civic Oracle & Voice", "📐 Architectural Schematics & Art", "📖 The Graphic Novel Blueprint"])

# ----------------- TAB 1: ORACLE & VOICE PROMPTING -----------------
with tab_chat:
    st.markdown('<div class="main-header">🌾 Kartarpur-0: Sangat-Sim</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Voice-Enabled Civic Intelligence (English & Punjabi)</div>', unsafe_allow_html=True)

    # Browser-native Web Speech STT Microphone Component
    st.markdown("##### 🎙️ Voice Input (Tap and Speak)")
    components.html("""
    <div style="font-family: sans-serif; display: flex; align-items: center; gap: 10px;">
        <button id="recordBtn" style="background-color: #E0A96D; color: #111; border: none; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: pointer;">
            🎤 Tap to Speak
        </button>
        <span id="recordStatus" style="color: #aaa; font-size: 13px;">Microphone idle</span>
    </div>
    <script>
        const btn = document.getElementById('recordBtn');
        const status = document.getElementById('recordStatus');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            status.innerText = "Speech API not supported in this browser. Use Chrome/Android Chrome.";
            btn.disabled = true;
        } else {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US'; // Supports 'pa-IN' or 'en-US'

            btn.onclick = () => {
                recognition.start();
                status.innerText = "Listening... speak now";
                btn.style.backgroundColor = "#ff4b4b";
            };

            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                status.innerText = 'Captured: "' + text + '"';
                btn.style.backgroundColor = "#E0A96D";
                // Copy transcript to clipboard for quick paste or prompt dispatch
                navigator.clipboard.writeText(text);
                status.innerText = 'Captured & copied to clipboard! Paste into chat below.';
            };

            recognition.onerror = (e) => {
                status.innerText = "Error: " + e.error;
                btn.style.backgroundColor = "#E0A96D";
            };
        }
    </script>
    """, height=65)

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

                    # Native Web Speech TTS Trigger
                    clean_audio_js = clean_text.replace('"', '\\"').replace('\n', ' ')[:400]
                    components.html(f"""
                    <script>
                        if ('speechSynthesis' in window) {{
                            const utterance = new SpeechSynthesisUtterance("{clean_audio_js}");
                            utterance.rate = 1.0;
                            utterance.pitch = 1.0;
                            window.speechSynthesis.speak(utterance);
                        }}
                    </script>
                    """, height=0)

                    if rfc_match:
                        st.warning(f"⚠️ **Edge Case Logged for Repository RFC:**\n`{rfc_match.group(1)}`")

                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                else:
                    st.error(f"Error querying Gemini: {last_error}")

# ----------------- TAB 2: ARCHITECTURE & SCHEMATICS -----------------
with tab_arch:
    st.header("📐 Physical & Systems Architecture")
    st.write("Kartarpur-0 utilizes a **concentric, biophilic layout** engineered for Canadian subarctic extremes (-50°C to +35°C). All mechanical machinery and compute loops are subterranean, leaving the surface dedicated to human community, craft, and ecology.")

    # High-fidelity SVG Schematics
    st.markdown("### Cross-Sectional Subterranean Schematic")
    st.markdown("""
    <svg viewBox="0 0 900 380" width="100%" style="background-color: #11141a; border-radius: 8px; border: 1px solid #30363d;">
        <!-- Ground Level -->
        <rect x="0" y="140" width="900" height="240" fill="#1b2028"/>
        <line x1="0" y1="140" x2="900" y2="140" stroke="#E0A96D" stroke-width="3"/>
        <text x="20" y="130" fill="#E0A96D" font-size="14" font-weight="bold">SURFACE (-40°C WINTER BOREAL TUNDRA)</text>
        
        <!-- Surface Dwellings & Atrium -->
        <path d="M 330 140 Q 450 40 570 140 Z" fill="#2d3748" stroke="#63b3ed" stroke-width="2"/>
        <text x="400" y="115" fill="#e2e8f0" font-size="13">Central Atrium (Ring 1)</text>

        <rect x="120" y="100" width="160" height="40" rx="6" fill="#2d3748" stroke="#a0aec0"/>
        <text x="135" y="125" fill="#edf2f7" font-size="12">Living Hearths (Ring 3)</text>

        <rect x="620" y="100" width="160" height="40" rx="6" fill="#2d3748" stroke="#a0aec0"/>
        <text x="645" y="125" fill="#edf2f7" font-size="12">Agora & Langar (Ring 2)</text>

        <!-- Subterranean Systems -->
        <text x="20" y="170" fill="#718096" font-size="14" font-weight="bold">SUBTERRANEAN AUTOMATION (PROTECTED +18°C)</text>

        <!-- CEA Farm -->
        <rect x="100" y="200" width="300" height="120" rx="8" fill="#1a2e22" stroke="#48bb78" stroke-width="2"/>
        <text x="120" y="230" fill="#9ae6b4" font-size="14" font-weight="bold">Closed-Loop Aeroponics / CEA</text>
        <text x="120" y="255" fill="#cbd5e0" font-size="12">• Continuous caloric Langar buffer</text>
        <text x="120" y="275" fill="#cbd5e0" font-size="12">• Automated nutrient telemetry</text>
        <text x="120" y="295" fill="#cbd5e0" font-size="12">• Root-zone thermal isolation</text>

        <!-- Compute & Energy -->
        <rect x="500" y="200" width="300" height="120" rx="8" fill="#2a2035" stroke="#9f7aea" stroke-width="2"/>
        <text x="520" y="230" fill="#d6bcfa" font-size="14" font-weight="bold">Compute Core & Geothermal Sync</text>
        <text x="520" y="255" fill="#cbd5e0" font-size="12">• Anandgarh edge compute nodes</text>
        <text x="520" y="275" fill="#cbd5e0" font-size="12">• Hydronic 55°C heat reclamation</text>
        <text x="520" y="295" fill="#cbd5e0" font-size="12">• Air-gapped mechanical bypasses</text>

        <!-- Hydronic Piping Line -->
        <line x1="500" y1="260" x2="400" y2="260" stroke="#f56565" stroke-width="4" stroke-dasharray="6,4"/>
        <text x="415" y="250" fill="#feb2b2" font-size="11">Hydronic Loop</text>
    </svg>
    """, unsafe_allow_html=True)

# ----------------- TAB 3: GRAPHIC NOVEL BLUEPRINT -----------------
with tab_narrative:
    st.header("📖 The Graphic Novel: 'The Hearth at -40'")
    st.caption("Visual Storyboard & Multi-Generational Narrative Outline")

    st.markdown("""
    <div class="narrative-card">
        <h3>Act I: The Long Frost (The Physical Hearth)</h3>
        <p><b>Visual Tone:</b> Stark contrast between blinding -42°C white blizzards over the Canadian Shield and the warm amber, cedar, and deep emerald interior of the subterranean Agora.</p>
        <p><b>Scene 1:</b> An elder (Baba Ji) sits near a massive hydronic hearth in the Central Atrium, hand-carving wooden joints for a greenhouse cradle with an 8-year-old child. A robotic cart silently delivers fresh kale and root vegetables from the aeroponics bay beneath their feet.</p>
        <p><b>The Conflict:</b> An alarm pulses gently—a deep mechanical vibration. A rupture in an auxiliary geothermal heat valve. For the first time, a newcomer experiences the Sant-Sipahi rapid-response: no panic, no screaming police sirens, but a calm, coordinated mobilization of cross-trained community engineers.</p>
    </div>

    <div class="narrative-card">
        <h3>Act II: The Darbar (The Trial of Purpose)</h3>
        <p><b>Visual Tone:</b> Circular tiered wooden amphitheater. No judge's bench. Equal eye-level seating.</p>
        <p><b>The Crisis:</b> A group of young residents questions the value of contributing Seva when the automation can already feed and clothe them indefinitely. The community holds a Restorative Darbar—not to punish or shame, but to explore identity, existential purpose, and the boundary between freedom and alienation.</p>
    </div>
    """, unsafe_allow_html=True)
