import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Institutional Memory Agent 💬", page_icon="💼", layout="wide")

# --- Custom CSS for Layout ---
st.markdown("""
<style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background-color: #121212;
        color: white;
        overflow: hidden;
    }

    .stApp {
        display: flex;
        flex-direction: column;
    }

    .main, .block-container {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        padding: 0 !important;
        overflow: hidden;
    }

    /* Header */
    .header-container {
        background-color: #1a1a1a;
        padding: 1rem 2rem;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        flex-shrink: 0;
    }

    /* Scrollable Chat History */
    .chat-history-container {
        flex-grow: 1;
        overflow-y: auto;
        padding: 1rem 2rem;
        background-color: #1e1e1e;
    }

    /* Fixed Input Bar */
    .input-bar-container {
        position: sticky;
        bottom: 0;
        z-index: 10;
        background-color: #1a1a1a;
        padding: 1rem 2rem;
        border-top: 1px solid #333;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-shrink: 0;
    }

    /* Chat Bubbles */
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        max-width: 85%;
        font-size: 1rem;
        line-height: 1.5;
        word-wrap: break-word;
        animation: fadeIn 0.3s ease-out;
    }

    .chat-message.user {
        background-color: #2e7d32;
        color: white;
        margin-left: auto;
        text-align: right;
        border-bottom-right-radius: 4px;
    }

    .chat-message.bot {
        background-color: #2c2c2c;
        color: white;
        margin-right: auto;
        text-align: left;
        border-top-left-radius: 4px;
    }

    /* Input field */
    .stTextInput div[data-baseweb="input"] input {
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 20px !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 1rem;
        line-height: 1.5;
        height: auto !important;
        min-height: 40px;
    }

    .stTextInput label {
        display: none !important;
    }

    /* Button */
    .stButton button {
        background-color: #3e8e41;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        min-width: 80px;
        height: 40px;
    }

    .stButton button:hover {
        background-color: #4CAF50;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "bot", "message": "Hello! I'm your Institutional Memory Agent. How can I help you today regarding our ML platform and processes?"}]

if 'user_question_input' not in st.session_state:
    st.session_state.user_question_input = ""

# --- Knowledge Base ---
knowledge_base = {
    "How do we handle model versioning?": "We use MLflow with Git SHAs and dataset hashes to track model versions.",
    "Where is the customer churn model deployed?": "It's deployed on Vertex AI in the us-east1 region, managed via CI/CD (Cloud Build + Terraform).",
    "Why did we move away from LangChain?": "LangChain was too opaque for debugging agent chains. We migrated to LlamaIndex + tools.",
    "What is our MLOps strategy?": "Our MLOps strategy focuses on automation of CI/CD, robust model monitoring, and scalable infrastructure using Google Cloud Platform services.",
    "How do we ensure data quality?": "We implement automated data validation checks at ingestion and before model training, using tools like Great Expectations to define data contracts.",
    "Tell me about our CI/CD for ML models.": "Our CI/CD pipeline for ML models uses Cloud Build for continuous integration, automating testing and packaging, and Terraform for continuous deployment to target environments like Vertex AI.",
    "What is the process for model retraining?": "Model retraining is triggered automatically based on data drift detection or a scheduled cron job. The new model undergoes a validation phase before being promoted to production.",
    "Do we use a feature store?": "Yes, we utilize a managed feature store solution to centralize feature creation, storage, and serving, ensuring consistency between training and inference.",
}

# --- Handle Message Sending ---
def send_message_callback():
    user_input = st.session_state.user_question_input.strip()
    if user_input:
        st.session_state.messages.append({"role": "user", "message": user_input})
        answer = knowledge_base.get(user_input, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
        st.session_state.messages.append({"role": "bot", "message": answer})
        st.session_state.user_question_input = ""

# --- Header ---
st.markdown("<div class='header-container'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- Chat History ---
chat_placeholder = st.empty()
with chat_placeholder.container():
    st.markdown("<div class='chat-history-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "bot"
        st.markdown(f"<div class='chat-message {role_class}'>{msg['message']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Input Bar (Sticky) ---
st.markdown("<div class='input-bar-container'>", unsafe_allow_html=True)
st.text_input(
    "Ask a question related to ML platform or processes 👇",
    value=st.session_state.user_question_input,
    key="user_question_input",
    label_visibility="collapsed",
    on_change=send_message_callback
)
st.button("Send", on_click=send_message_callback)
st.markdown("</div>", unsafe_allow_html=True)

