import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Institutional Memory Agent 💬",
    page_icon="💼",
    layout="wide" # Using wide layout
)

# --- Session State Initialization ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "Hi there! I'm your Institutional Memory Agent. Ask me anything about our ML platform."}
    ]

# --- Knowledge Base (Your simplified mock data) ---
knowledge_base = {
    "What is our MLOps strategy?": "We focus on automated CI/CD, monitoring, and scalable infrastructure using GCP.",
    "How do we ensure data quality?": "We use Great Expectations to validate data contracts at multiple pipeline stages.",
    "Where is the churn model deployed?": "It's on Vertex AI in us-east1, managed via Terraform and Cloud Build.",
    "Do we use a feature store?": "Yes, we leverage a managed feature store for consistent training and inference features.",
    "Why did we move away from LangChain?": "LangChain was opaque. We switched to LlamaIndex for clearer agent debugging.",
}

# --- Suggestions Data ---
SUGGESTIONS = [
    "What is our MLOps strategy?",
    "Do we use a feature store?",
    "Where is the churn model deployed?",
    "How do we ensure data quality?",
]

# --- CSS Styling (Revised) ---
st.markdown("""
    <style>
        /* Hide Streamlit's default header and toolbar */
        [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Ensure the main app content is a flex column and fills space */
        .stApp {
            display: flex;
            flex-direction: column;
            height: 100vh; /* Make the app take full viewport height */
            overflow: hidden; /* Hide main scrollbar */
        }
        /* Important for the main content area which now handles padding */
        .stApp > div:first-child {
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            overflow: hidden; /* Keep this hidden */
            padding: 0 !important;
        }
        /* Additional styling for the block that wraps the main content */
        .stApp > div:first-child > div:first-child {
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            overflow: hidden;
            padding: 0 !important;
        }

        /* --- Header (Fixed Top Ribbon) --- */
        .header-container {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            font-size: 1.8rem;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            flex-shrink: 0; /* Prevent from shrinking */
            color: white; /* Ensure text is visible */
            z-index: 1000;
        }

        /* --- Chat History Area (Scrollable Middle Section) --- */
        /* IMPORTANT: This needs a defined height or max-height to scroll */
        .chat-history-container {
            flex-grow: 1; /* Allows it to take up available space */
            overflow-y: auto; /* THIS MAKES IT SCROLLABLE */
            padding: 1rem; /* Padding inside the scrollable area */
            max-width: 700px; /* Max width for chat content */
            margin-left: auto;
            margin-right: auto;
            /* No direct padding-top/bottom here if parent handles it */
            box-sizing: border-box; /* Include padding in height calculation */
            /* Ensure it has a min-height for flexbox to work properly */
            min-height: 0;
            /* Add some background to visually separate from scrollbar area */
            background-color: #f0f2f6; /* Lighter background for chat area */
        }
        
        div.stChatMessage {
            margin-bottom: 0.5rem;
        }
        /* Your chat message styling (unchanged) */
        .stChatMessage.st-chat-message-user .stChatMessageContent {
            background-color: #2e7d32 !important;
            color: white !important;
            border-bottom-right-radius: 4px !important;
            border-top-left-radius: 12px !important;
            border-top-right-radius: 12px !important;
            border-bottom-left-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            max-width: 85%;
            margin-left: auto;
        }
        .stChatMessage.st-chat-message-assistant .stChatMessageContent {
            background-color: #333 !important;
            color: white !important;
            border-top-left-radius: 4px !important;
            border-top-right-radius: 12px !important;
            border-bottom-right-radius: 12px !important;
            border-bottom-left-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            max-width: 85%;
            margin-right: auto;
        }

        /* --- Fixed Bottom Section (Suggestions + Chat Input) --- */
        .bottom-fixed-container {
            flex-shrink: 0; /* Prevent from shrinking */
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            border-top: 1px solid #333;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4);
            z-index: 1000;
            display: flex;
            flex-direction: column; /* Stack suggestions and input */
            align-items: center; /* Center horizontally */
            gap: 1rem;
        }

        /* Suggestions Styling (unchanged) */
        .suggestions-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            width: 100%;
            max-width: 700px;
            padding-bottom: 0.5rem;
        }
        .suggestion-button button {
            background-color: #444 !important;
            color: white !important;
            border: 1px solid #555 !important;
            border-radius: 15px !important;
            padding: 0.4rem 1rem !important;
            font-size: 0.85rem !important;
            cursor: pointer;
            transition: background-color 0.2s ease-in-out;
            white-space: nowrap;
            flex-shrink: 0;
            height: auto !important;
            line-height: 1.2 !important;
        }
        .suggestion-button button:hover {
            background-color: #555 !important;
        }
        .stColumns {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            gap: 0.5rem !important;
            justify-content: center;
        }
        .stColumn {
            padding: 0 !important;
            margin: 0 !important;
            flex-grow: 0 !important;
            flex-basis: auto !important;
            min-width: 0 !important;
        }

        /* Chat Input Styling (unchanged) */
        .stChatInputContainer {
            width: 100% !important;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            background-color: transparent !important;
            padding: 0 !important;
        }
        .stChatInputContainer .stTextInput {
            flex-grow: 1;
            margin-bottom: 0 !important;
        }
        .stChatInputContainer .stTextInput div[data-baseweb="input"] input {
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
        .stChatInputContainer .stTextInput label {
            display: none !important;
        }
        .stChatInputContainer .stButton button {
            background-color: #3e8e41 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.6rem 1.5rem !important;
            min-width: 80px !important;
            height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: background-color 0.2s ease-in-out;
        }
        .stChatInputContainer .stButton button:hover {
            background-color: #4CAF50 !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header-container'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)


# --- Define the function to handle suggestion clicks ---
def handle_suggestion_click(suggestion_text):
    st.session_state['messages'].append({"role": "user", "content": suggestion_text})
    with st.spinner("Thinking..."):
        response = knowledge_base.get(suggestion_text, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.rerun() # Rerun the app to update chat history and clear input


# --- Main Chat History Area (Scrollable) ---
# Create an empty placeholder for the chat history container
# This is crucial for Streamlit to handle the fixed scrolling behavior
chat_history_placeholder = st.empty()

# This is where the chat messages will be rendered.
# We create a div with a specific ID that we can target with JavaScript
with chat_history_placeholder.container():
    st.markdown('<div class="chat-history-container" id="chat-history-scroll-area">', unsafe_allow_html=True)
    for msg in st.session_state['messages']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)


# --- Suggestions and Chat Input (Fixed at Bottom) ---
st.markdown("<div class='bottom-fixed-container'>", unsafe_allow_html=True)

# Suggestions Area
st.markdown("<div class='suggestions-row'>", unsafe_allow_html=True)
for i, suggestion in enumerate(SUGGESTIONS):
    col = st.columns(1)[0]
    with col:
        st.button(
            suggestion,
            on_click=handle_suggestion_click,
            args=(suggestion,),
            key=f"suggestion_btn_{i}",
            help=suggestion,
            use_container_width=False
        )
st.markdown("</div>", unsafe_allow_html=True)


# Chat Input (Streamlit Native)
user_query = st.chat_input("Ask a question...")

st.markdown("</div>", unsafe_allow_html=True) # Close bottom-fixed-container

# --- JavaScript for Auto-Scrolling to Latest Message ---
# This script will run every time the app re-runs.
# It targets the 'chat-history-scroll-area' ID.
st.markdown("""
    <script>
        var chatHistory = document.getElementById("chat-history-scroll-area");
        if (chatHistory) {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    </script>
""", unsafe_allow_html=True)


if user_query:
    st.session_state['messages'].append({"role": "user", "content": user_query})

    with st.spinner("Thinking..."):
        response = knowledge_base.get(user_query, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")

    st.session_state['messages'].append({"role": "assistant", "content": response})

    st.rerun()
