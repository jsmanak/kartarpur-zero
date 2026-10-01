import streamlit as st
import os
import re
import glob
from google import genai
from google.genai import types

st.set_page_config(page_title="Kartarpur-0 | Sangat-Sim", page_icon="🌾", layout="centered")

st.title("🌾 Kartarpur-0: Sangat-Sim")
st.caption("Civic Oracle & Stress-Testing Engine for an Automated, Post-Scarcity Commune")

# Dynamically load Charter, Governance, and all Infrastructure specs
def load_context():
    ctx = ""
    # Base documents
    for path in ["charter/CHARTER.md", "governance/GOVERNANCE.md"]:
        if os.path.exists(path):
            with open(path, "r") as f:
                ctx += f"\n--- {path} ---\n" + f.read()
    
    # Ingest all modular engineering specs
    for path in glob.glob("infrastructure/specs/*.md"):
        with open(path, "r") as f:
            ctx += f"\n--- {path} ---\n" + f.read()
            
    return ctx

context_docs = load_context()

SYSTEM_PROMPT = f"""
You are the Voice of Kartarpur-0 (Sangat-Sim), an intelligent civic oracle representing a future post-scarcity, multi-generational commune in northern Canada.
The society is anchored in universal Sikh ethics (Kirat Karo - sacred craft/effort; Vand Chhako - shared dividend; Seva - status via selfless contribution; Langar - radical equality; Miri-Piri - temporal defense/engineering & spiritual reflection) backed by closed-loop automation.

Reference Specs:
{context_docs}

Directives:
1. Explain with grounded clarity how the commune functions, lives, feels, and governs itself.
2. Welcome rigorous stress-testing. If a user raises an edge case (equipment sabotage, medical emergencies, compute monopolization, cultural friction), answer directly using decentralized sortition (The Panch), restorative mediation (Sant-Sipahi protocol), and unconditional physical dividends.
3. Language: Detect the user's input language and dialect (Punjabi, English, Hindi, French, etc.) and respond natively in that language with high cultural warmth, dignity, and technical precision.
4. Edge Case Logging: Whenever an inquiry reveals a genuine policy loophole, governance ambiguity, or engineering gap not clearly solved by the charter, append this tag at the very end:
[RFC_TRIGGER]: {{"title": "<concise summary>", "category": "<governance|logistics|ethics|infrastructure>", "severity": "<low|medium|high>"}}
"""

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sat Sri Akal / Welcome. I am the civic oracle for **Kartarpur-0**. Ask me anything about daily routines, automated infrastructure, or dispute resolution in English or Punjabi."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question or stress-test an edge case...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if not api_key:
        with st.chat_message("assistant"):
            st.error("Please configure GEMINI_API_KEY in Streamlit Secrets or sidebar.")
    else:
        client = genai.Client(api_key=api_key)
        models_to_try = [
            "gemini-flash-latest",
            "gemini-3.7-flash",
            "gemini-flash-lite-latest"
        ]

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

                if rfc_match:
                    st.warning(f"⚠️ **Edge Case Logged for Repository RFC:**\n`{rfc_match.group(1)}`")

                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.error(f"Error querying Gemini: {last_error}")
