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
        /* Hide Streamlit's default header and toolbar */
        [data-testid="stHeader"] {
            display: none !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Ensure the main app container starts from the very top and covers full height */
        .stApp {
            background-color: #121212;
            color: white;
            height: 100vh;
            overflow: hidden; /* Important: Prevents browser scrollbar */
            display: flex;
            flex-direction: column; /* Stack header, chat, input vertically */
            padding-top: 0 !important; /* Ensure no top padding on the root app element */
        }
        
        /* Ensure the main content view container starts from the very top */
        .stAppViewContainer {
            padding-top: 0 !important;
            margin-top: 0 !important;
            flex-grow: 1; /* Allow it to take vertical space */
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Ensure Streamlit's main content area and block containers have no unwanted padding */
        .main, .block-container {
            padding: 0 !important; /* Remove default Streamlit padding */
            flex-grow: 1; /* Allow content to take available space */
            display: flex;
            flex-direction: column;
            overflow: hidden; /* Crucial to prevent extra scrollbars */
        }

        /* Header (Top Ribbon) */
        .header {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            font-size: 1.8rem;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            flex-shrink: 0; /* Ensures header doesn't shrink */
        }

        /* Chat History Area (Scrollable Middle Section) */
        .chat {
            flex-grow: 1; /* Takes all available space between header and input */
            overflow-y: auto; /* Enables vertical scrolling for messages */
            padding: 1rem 2rem;
            background-color: #1e1e1e;
        }

        /* Message Styling */
        .message {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            max-width: 85%;
            line-height: 1.5;
            word-wrap: break-word; /* Ensure long words break */
        }
        .user { 
            background-color: #2e7d32; 
            color: white; 
            margin-left: auto; 
            text-align: right; 
            border-bottom-right-radius: 4px; /* Gemini-like tail */
        }
        .bot { 
            background-color: #333; 
            color: white; 
            margin-right: auto; 
            text-align: left; 
            border-top-left-radius: 4px; /* Gemini-like tail */
        }

        /* Input Container (Bottom Fixed Section) */
        .input-container {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            border-top: 1px solid #333;
            display: flex; /* Use flexbox for input and button alignment */
            align-items: center; /* Vertically align items */
            gap: 1rem; /* Space between input and button */
            flex-shrink: 0; /* Ensures input container doesn't shrink */
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4);
        }

        /* Streamlit Text Input within the form */
        .stTextInput {
            flex-grow: 1; /* Input takes most of the space */
            margin-bottom: 0 !important; /* Remove default margin */
        }
        .stTextInput div[data-baseweb="input"] input {
            background-color: #222 !important;
            color: white !important;
            border: 1px solid #444 !important;
            border-radius: 20px !important;
            padding: 0.6rem 1rem !important;
            font-size: 1rem;
            line-height: 1.5;
            height: auto !important; /* Allow height to adjust if multiline */
            min-height: 40px; /* Minimum height */
        }
        /* Hide the default Streamlit label for text input */
        .stTextInput label {
            display: none !important;
        }

        /* Streamlit Button within the form */
        .stButton button {
            background-color: #3e8e41;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 0.6rem 1.5rem;
            cursor: pointer;
            transition: background-color 0.2s ease-in-out;
            min-width: 80px; /* Ensure button has a decent width */
            height: 40px; /* Match input min-height */
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stButton button:hover {
            background-color: #4CAF50;
        }

        /* Specific fix for stForm not respecting padding if it's the main content */
        div.stForm {
            width: 100%;
            margin: 0;
            padding: 0;
        }
        div.stForm > div { /* This is the internal flex container for form elements */
            display: flex;
            align-items: center;
            gap: 1rem;
            width: 100%; /* Ensure it spans full width */
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
with st.container():
    st.markdown("<div class='header'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- Chat History ---
chat_display_area = st.empty()

with chat_display_area.container():
    st.markdown("<div class='chat'>", unsafe_allow_html=True)
    for msg in st.session_state['messages']:
        css_class = "user" if msg['role'] == 'user' else "bot"
        st.markdown(f"<div class='message {css_class}'>{msg['message']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Input Area with st.form ---
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        user_question = st.text_input(
            label="Ask a question",
            placeholder="Type your question here...",
            key="user_question_input",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("Send")

        if submit_button and user_question:
            st.session_state['messages'].append({"role": "user", "message": user_question})
            response = knowledge_base.get(user_question, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
            st.session_state['messages'].append({"role": "bot", "message": response})
    
    st.markdown("</div>", unsafe_allow_html=True)
