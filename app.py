import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Institutional Memory Agent 💬",
    page_icon="💼",
    layout="wide"
)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "Hi there! I'm your Institutional Memory Agent. Ask me anything about our ML platform."}
    ]

knowledge_base = {
    "What is our MLOps strategy?": "We focus on automated CI/CD, monitoring, and scalable infrastructure using GCP.",
    "How do we ensure data quality?": "We use Great Expectations to validate data contracts at multiple pipeline stages.",
    "Where is the churn model deployed?": "It's on Vertex AI in us-east1, managed via Terraform and Cloud Build.",
    "Do we use a feature store?": "Yes, we leverage a managed feature store for consistent training and inference features.",
    "Why did we move away from LangChain?": "LangChain was opaque. We switched to LlamaIndex for clearer agent debugging.",
}

SUGGESTIONS = [
    "What is our MLOps strategy?",
    "Do we use a feature store?",
    "Where is the churn model deployed?",
    "How do we ensure data quality?",
]

# --- Custom CSS for Layout ---
st.markdown("""
    <style>
        /* Hide Streamlit's default header and toolbar */
        [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Make the main app container take full height and be a flex column */
        .stApp {
            min-height: 100vh; /* Ensure it takes full viewport height */
            display: flex;
            flex-direction: column;
            overflow: hidden; /* Hide main scrollbar */
        }

        /* Ensure the main content block fills available space */
        section.main {
            flex-grow: 1; /* Allow it to grow */
            display: flex;
            flex-direction: column;
            overflow: hidden; /* Hide its scrollbar */
            padding-bottom: 0 !important; /* Remove default padding from this section */
        }
        
        div.block-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            padding-top: 0 !important; /* Remove default padding */
            padding-bottom: 0 !important; /* Remove default padding */
        }


        /* Fixed Header */
        .header-container {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            font-size: 1.8rem;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            color: white;
            flex-shrink: 0;
            z-index: 1000;
            width: 100%;
            box-sizing: border-box;
        }

        /* Fixed Footer (Suggestions + Input) */
        .footer-container {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            border-top: 1px solid #333;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4);
            flex-shrink: 0; /* Prevent from shrinking */
            z-index: 1000;
            width: 100%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }
        
        /* The NEW SCROLLABLE CHAT AREA */
        .scrollable-chat-area {
            flex-grow: 1; /* Take up all available space */
            overflow-y: auto; /* THIS IS THE KEY FOR SCROLLING */
            padding: 1rem; /* Internal padding */
            max-width: 700px; /* Optional: limit chat width */
            margin: 0 auto; /* Center the chat area */
            box-sizing: border-box; /* Include padding in height calc */
            background-color: #f0f2f6; /* Lighter background for chat area */
            min-height: 0; /* Critical for flex items to prevent overflow */
        }

        /* Chat Message Styling (as before) */
        div.stChatMessage { margin-bottom: 0.5rem; }
        .stChatMessage.st-chat-message-user .stChatMessageContent { /* ... your user message styles ... */ }
        .stChatMessage.st-chat-message-assistant .stChatMessageContent { /* ... your assistant message styles ... */ }

        /* Suggestions Styling (as before) */
        .suggestions-row { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; width: 100%; max-width: 700px; padding-bottom: 0.5rem;}
        .suggestion-button button { /* ... your button styles ... */ }
        .stColumns { width: 100% !important; margin: 0 !important; padding: 0 !important; gap: 0.5rem !important; justify-content: center; }
        .stColumn { padding: 0 !important; margin: 0 !important; flex-grow: 0 !important; flex-basis: auto !important; min-width: 0 !important; }

        /* Chat Input Styling (as before) */
        .stChatInputContainer { /* ... your chat input container styles ... */ }
        .stChatInputContainer .stTextInput { flex-grow: 1; margin-bottom: 0 !important; }
        .stChatInputContainer .stTextInput div[data-baseweb="input"] input { /* ... input field styles ... */ }
        .stChatInputContainer .stTextInput label { display: none !important; }
        .stChatInputContainer .stButton button { /* ... send button styles ... */ }
        .stChatInputContainer .stButton button:hover { background-color: #4CAF50 !important; }
    </style>
""", unsafe_allow_html=True)

# --- Define the function to handle suggestion clicks ---
def handle_suggestion_click(suggestion_text):
    st.session_state['messages'].append({"role": "user", "content": suggestion_text})
    with st.spinner("Thinking..."):
        response = knowledge_base.get(suggestion_text, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.rerun()

# --- HEADER ---
# We put the header content directly in the main app flow,
# and let the CSS position and style it as fixed.
st.markdown("<div class='header-container'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- MAIN CHAT HISTORY AREA (Scrollable) ---
# This is the actual scrollable content area.
# It MUST be placed directly inside a flex container that has space to fill.
# The 'main' section of Streamlit already acts as a flex container,
# and we're ensuring 'block-container' within it is also flex.
chat_history_placeholder = st.container() # Use a plain st.container() here

with chat_history_placeholder:
    # Wrap the messages in a div that will become scrollable
    st.markdown('<div class="scrollable-chat-area" id="chat-history-scroll-area">', unsafe_allow_html=True)
    for msg in st.session_state['messages']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)


# --- FOOTER (Suggestions + Chat Input) ---
# We put the footer content directly in the main app flow,
# and let the CSS position and style it as fixed.
st.markdown("<div class='footer-container'>", unsafe_allow_html=True)

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

# Chat Input
user_query = st.chat_input("Ask a question...")

st.markdown("</div>", unsafe_allow_html=True) # Close footer-container

# --- JavaScript for Auto-Scrolling to Latest Message ---
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
