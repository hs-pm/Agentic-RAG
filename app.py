import streamlit as st

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Institutional Memory Agent 💬",
    page_icon="💼",
    layout="wide"
)

# --- Session State Initialization ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "bot", "message": "Hi there! I'm your Institutional Memory Agent. Ask me anything about our ML platform."}
    ]

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

# --- Knowledge Base ---
knowledge_base = {
    "What is our MLOps strategy?": "We focus on automated CI/CD, monitoring, and scalable infrastructure using GCP.",
    "How do we ensure data quality?": "We use Great Expectations to validate data contracts at multiple pipeline stages.",
    "Where is the churn model deployed?": "It's on Vertex AI in us-east1, managed via Terraform and Cloud Build.",
    "Do we use a feature store?": "Yes, we leverage a managed feature store for consistent training and inference features.",
    "Why did we move away from LangChain?": "LangChain was opaque. We switched to LlamaIndex for clearer agent debugging.",
}

# --- CSS Styling ---
st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            color: white;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .header {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            font-size: 1.8rem;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            flex-shrink: 0;
        }
        .chat {
            flex-grow: 1;
            overflow-y: auto;
            padding: 1rem 2rem;
            background-color: #1e1e1e;
        }
        .message {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            max-width: 85%;
            line-height: 1.5;
        }
        .user { background-color: #2e7d32; color: white; margin-left: auto; text-align: right; }
        .bot { background-color: #333; color: white; margin-right: auto; text-align: left; }
        .input-container {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            border-top: 1px solid #333;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-shrink: 0;
        }
        input[type="text"] {
            background-color: #222;
            color: white;
            border: 1px solid #444;
            border-radius: 20px;
            padding: 0.6rem 1rem;
            flex-grow: 1;
        }
        button {
            background-color: #3e8e41;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 0.6rem 1.5rem;
            cursor: pointer;
        }
        button:hover {
            background-color: #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- Chat History ---
st.markdown("<div class='chat'>", unsafe_allow_html=True)
for msg in st.session_state['messages']:
    css_class = "user" if msg['role'] == 'user' else "bot"
    st.markdown(f"<div class='message {css_class}'>{msg['message']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Message Sending Logic ---
def handle_message():
    user_text = st.session_state.user_input.strip()
    if user_text:
        st.session_state['messages'].append({"role": "user", "message": user_text})
        response = knowledge_base.get(user_text, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
        st.session_state['messages'].append({"role": "bot", "message": response})
        st.session_state.user_input = ""

# --- Input Area ---
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
st.text_input(
    label="Ask a question",
    value=st.session_state.user_input,
    key="user_input",
    label_visibility="collapsed",
    on_change=handle_message
)
st.button("Send", on_click=handle_message)
st.markdown("</div>", unsafe_allow_html=True)
