import streamlit as st

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

# --- Knowledge Base ---
knowledge_base = {
    "What is our MLOps strategy?": "We focus on automated CI/CD, monitoring, and scalable infrastructure using GCP.",
    "How do we ensure data quality?": "We use Great Expectations to validate data contracts at multiple pipeline stages.",
    "Where is the churn model deployed?": "It's on Vertex AI in us-east1, managed via Terraform and Cloud Build.",
    "Do we use a feature store?": "Yes, we leverage a managed feature store for consistent training and inference features.",
    "Why did we move away from LangChain?": "LangChain was opaque. We switched to LlamaIndex for clearer agent debugging.",
}

# --- CSS Styling (Aggressive fixes for fixed header/footer and chat scrolling) ---
st.markdown("""
    <style>
        /* Hide Streamlit's default header and toolbar */
        [data-testid="stHeader"] {
            display: none !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Crucial: Ensure the main app and its containers are flex columns and fill space */
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
        /* These wrap each st.markdown, st.chat_message etc. */
        .stElementContainer {
            padding: 0 !important;
            margin: 0 !important;
            min-height: 0 !important; /* Very important to prevent extra space */
        }

        /* --- Header (Fixed Top Ribbon) --- */
        .header {
            background-color: #1a1a1a;
            padding: 1rem 2rem;
            font-size: 1.8rem;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            flex-shrink: 0;
            position: fixed; /* Make header fixed */
            top: 0; /* Position at the very top */
            left: 0;
            right: 0;
            width: 100%;
            z-index: 1000; /* Ensure it stays on top of other content */
        }

        /* --- Chat History Area (Scrollable Middle Section) --- */
        /* This padding ensures content doesn't go under fixed header/footer */
        .main .block-container {
            padding-top: 7rem !important; /* Space for the fixed header (adjust as needed) */
            padding-bottom: 7rem !important; /* Space for the fixed input (adjust as needed) */
            overflow-y: auto !important; /* Enable scrolling for the chat history */
            flex-grow: 1 !important; /* Allow it to take remaining space */
            /* Ensure the content is centered and has side padding */
            max-width: 700px; /* Example max width for chat content */
            margin-left: auto;
            margin-right: auto;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Specific styles for st.chat_message bubbles */
        div.stChatMessage {
            margin-bottom: 0.5rem; /* Space between messages */
        }

        /* Customize st.chat_message appearances */
        .stChatMessage.st-chat-message-user .stChatMessageContent { /* User message bubble */
            background-color: #2e7d32 !important; 
            color: white !important; 
            border-bottom-right-radius: 4px !important; 
            border-top-left-radius: 12px !important;
            border-top-right-radius: 12px !important;
            border-bottom-left-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            max-width: 85%; /* Limit width of message bubbles */
            margin-left: auto; /* Push user messages to the right */
        }
        .stChatMessage.st-chat-message-assistant .stChatMessageContent { /* Bot message bubble */
            background-color: #333 !important; 
            color: white !important; 
            border-top-left-radius: 4px !important; 
            border-top-right-radius: 12px !important;
            border-bottom-right-radius: 12px !important;
            border-bottom-left-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            max-width: 85%; /* Limit width of message bubbles */
            margin-right: auto; /* Push bot messages to the left */
        }

        /* --- st.chat_input (Fixed Bottom Section) --- */
        .stChatInputContainer {
            background-color: #1a1a1a !important; /* Match your input-container background */
            padding: 1rem 2rem !important; /* Match your desired padding */
            border-top: 1px solid #333 !important; /* Match your border */
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4) !important;
            position: fixed !important; /* Explicitly fix it */
            bottom: 0 !important; /* Anchor to bottom */
            left: 0 !important;
            right: 0 !important;
            width: 100% !important; /* Full width */
            z-index: 1000; /* Ensure it stays on top */
            display: flex; /* Make it a flex container for alignment */
            align-items: center; /* Vertically align items */
            gap: 1rem; /* Space between input and button */
        }
        
        /* Adjust the input field inside st.chat_input */
        .stChatInputContainer .stTextInput { /* Target the text input wrapper inside chat input */
            flex-grow: 1; /* Allow input to take remaining space */
            margin-bottom: 0 !important; /* Remove default margin */
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
        /* Hide the default Streamlit label for text input within chat_input if any */
        .stChatInputContainer .stTextInput label {
            display: none !important;
        }

        /* Adjust the Send button inside st.chat_input */
        .stChatInputContainer .stButton button {
            background-color: #3e8e41 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.6rem 1.5rem !important;
            min-width: 80px !important;
            height: 40px !important;
            display: flex !important; /* Ensure it's flex for centering */
            align-items: center !important;
            justify-content: center !important;
            transition: background-color 0.2s ease-in-out;
        }
        .stChatInputContainer .stButton button:hover {
            background-color: #4CAF50 !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- Header (Now placed as a custom fixed element) ---
st.markdown("<div class='header'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- Display Chat Messages ---
# Use st.container to ensure messages are rendered within a predictable block,
# which the CSS for .main .block-container controls for scrolling.
# We don't need a separate 'chat' div here because .main .block-container handles the overflow.
for msg in st.session_state['messages']:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat Input (Fixed at Bottom - Streamlit Native) ---
# This is placed at the very end of the script to ensure it renders at the bottom.
user_query = st.chat_input("Ask a question...")

if user_query:
    # Add user message to history
    st.session_state['messages'].append({"role": "user", "content": user_query})
    
    # Get bot response
    response = knowledge_base.get(user_query, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    
    # Rerun the app to show the new messages. st.chat_input handles input clearing.
    st.rerun()
