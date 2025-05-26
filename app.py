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

# --- CSS Styling (Aggressive fixes for fixed footer) ---
st.markdown("""
    <style>
        /* Hide Streamlit's default header and toolbar */
        [data-testid="stHeader"] {
            display: none !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Crucial: Ensure all core Streamlit containers are flex columns and fill space */
        /* This targets every major wrapper div that Streamlit creates */
        .stApp,
        .stAppViewContainer,
        .stMain,
        .stMainBlockContainer,
        [data-testid="stVerticalBlock"] /* This is the specific block that holds your content */
        {
            display: flex !important;
            flex-direction: column !important;
            flex-grow: 1 !important; /* Make them grow to fill available space */
            height: 100% !important; /* Ensure they take full height of parent */
            width: 100% !important; /* Ensure they take full width */
            padding: 0 !important; /* Zero out all padding */
            margin: 0 !important; /* Zero out all margin */
            overflow: hidden !important; /* Prevent scrollbars on these containers */
            min-height: 0 !important; /* Prevent minimum height from pushing content */
        }
        
        /* Override any default padding/margin on Streamlit's element containers */
        /* These wrap each st.markdown, st.text_input etc. */
        .stElementContainer {
            padding: 0 !important;
            margin: 0 !important;
            min-height: 0 !important; /* Very important to prevent extra space */
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
            padding: 1rem 2rem; /* Internal padding for chat bubbles */
            background-color: #1e1e1e;
        }

        /* Message Styling */
        .message {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            max-width: 85%;
            line-height: 1.5;
            word-wrap: break-word;
        }
        .user { 
            background-color: #2e7d32; 
            color: white; 
            margin-left: auto; 
            text-align: right; 
            border-bottom-right-radius: 4px;
        }
        .bot { 
            background-color: #333; 
            color: white; 
            margin-right: auto; 
            text-align: left; 
            border-top-left-radius: 4px;
        }

        /* Input Container (Bottom Fixed Section) */
        .input-container {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            border-top: 1px solid #333;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-shrink: 0; /* Ensures input container doesn't shrink */
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4);
        }

        /* Streamlit Text Input within the form */
        .stTextInput {
            flex-grow: 1;
            margin-bottom: 0 !important;
        }
        .stTextInput div[data-baseweb="input"] input {
            background-color: #222 !important;
            color: white !important;
            border: 1px solid #444 !important;
            border-radius: 20px !important;
            padding: 0.6rem 1rem !important;
            font-size: 1rem;
            line-height: 1.5;
            height: auto !important;
            min-height: 40px;
        }
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
            min-width: 80px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stButton button:hover {
            background-color: #4CAF50;
        }

        /* Specific fix for stForm not respecting flex alignment in some cases */
        div.stForm {
            width: 100%;
            margin: 0;
            padding: 0;
        }
        div.stForm > div {
            display: flex;
            align-items: center;
            gap: 1rem;
            width: 100%;
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
with st.container():
    st.markdown("<div class='header'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- Chat History ---
# Using st.empty() for controlled placement within the flex layout
chat_display_area = st.empty()

with chat_display_area.container():
    st.markdown("<div class='chat'>", unsafe_allow_html=True)
    for msg in st.session_state['messages']:
        css_class = "user" if msg['role'] == 'user' else "bot"
        st.markdown(f"<div class='message {css_class}'>{msg['message']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Input Area with st.form ---
# This container applies the background and padding for the fixed input area
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    # st.form ensures reliable single submission and auto-clearing
    with st.form(key="chat_form", clear_on_submit=True):
        user_question = st.text_input(
            label="Ask a question", # Label for internal use, hidden by CSS
            placeholder="Type your question here...",
            key="user_question_input",
            label_visibility="collapsed" # Hides the default label
        )
        submit_button = st.form_submit_button("Send")

        if submit_button and user_question: # Only process if button clicked and input is not empty
            st.session_state['messages'].append({"role": "user", "message": user_question})
            response = knowledge_base.get(user_question, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
            st.session_state['messages'].append({"role": "bot", "message": response})
    
    st.markdown("</div>", unsafe_allow_html=True) # Close the input-container div
