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

# --- Suggestions Data ---
SUGGESTIONS = [
    "What is our MLOps strategy?",
    "Do we use a feature store?",
    "Where is the churn model deployed?",
    "How do we ensure data quality?",
]

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
        [data-testid="stVerticalBlock"]
        {
            display: flex !important;
            flex-direction: column !important;
            flex-grow: 1 !important;
            height: 100% !important;
            width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden !important;
            min-height: 0 !important;
        }
        
        .stElementContainer {
            padding: 0 !important;
            margin: 0 !important;
            min-height: 0 !important;
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
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100%;
            z-index: 1000;
        }

        /* --- Chat History Area (Scrollable Middle Section) --- */
        .main .block-container {
            /* Adjust padding based on header and input container heights */
            padding-top: 7rem !important;    /* Space for the fixed header */
            /* Adjusted padding-bottom to accommodate both input AND suggestions */
            padding-bottom: 11rem !important; /* Approx 4.5rem for input + 3.5rem for suggestions + 3rem gap */
            overflow-y: auto !important;
            flex-grow: 1 !important;
            max-width: 700px; /* Max width for chat content */
            margin-left: auto;
            margin-right: auto;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        div.stChatMessage {
            margin-bottom: 0.5rem;
        }

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

        /* --- st.chat_input (Fixed Bottom Section) --- */
        .stChatInputContainer {
            background-color: #1a1a1a !important;
            padding: 1rem 2rem !important;
            border-top: 1px solid #333 !important;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4) !important;
            position: fixed !important;
            bottom: 0 !important; /* Anchor to bottom */
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 1rem;
            /* No bottom-padding here as suggestions are above it in the HTML flow */
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

        /* --- Suggestions Styling --- */
        .suggestions-container {
            position: fixed; /* Fix to the viewport */
            bottom: 6rem; /* Position above the input box (adjust based on input height) */
            left: 0;
            right: 0;
            width: 100%;
            display: flex;
            justify-content: center; /* Center the suggestions horizontally */
            align-items: flex-end; /* Align items to the bottom of this container */
            flex-wrap: wrap; /* Allow suggestions to wrap to the next line */
            gap: 0.5rem; /* Space between suggestion buttons */
            padding: 0.5rem 2rem; /* Padding around the suggestion area */
            background-color: #1a1a1a; /* Match input container background */
            box-shadow: 0 -2px 5px rgba(0,0,0,0.4); /* Match input container shadow */
            z-index: 999; /* Ensure it's above chat history, below fixed input */
        }
        .suggestion-button button { /* Target the actual Streamlit button element */
            background-color: #444 !important; /* Darker gray for suggestions */
            color: white !important;
            border: 1px solid #555 !important;
            border-radius: 15px !important; /* Slightly more rounded corners */
            padding: 0.4rem 1rem !important; /* Smaller padding for suggestion boxes */
            font-size: 0.85rem !important; /* Smaller font size */
            cursor: pointer;
            transition: background-color 0.2s ease-in-out;
            white-space: nowrap; /* Prevent text from wrapping within a suggestion box */
            flex-shrink: 0; /* Prevent buttons from shrinking if space is tight */
            height: auto !important; /* Allow height to adjust to content */
            line-height: 1.2 !important; /* Adjust line height for better spacing */
        }
        .suggestion-button button:hover {
            background-color: #555 !important;
        }
        /* Target the specific st.columns wrapper to remove its default padding/margin */
        .stColumns {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            gap: 0.5rem !important; /* Consistent gap between columns */
            justify-content: center; /* Center column content */
        }
        /* Target the individual columns within st.columns */
        .stColumn {
            padding: 0 !important;
            margin: 0 !important;
            flex-grow: 0 !important; /* Do not grow */
            flex-basis: auto !important; /* Auto size based on content */
            min-width: 0 !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)

# --- Define the function to handle suggestion clicks ---
def handle_suggestion_click(suggestion_text):
    # This function will add the suggestion as a user message
    # and trigger a bot response, then rerun the app.
    st.session_state['messages'].append({"role": "user", "content": suggestion_text})
    response = knowledge_base.get(suggestion_text, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.rerun() # Rerun the app to update chat history and clear input


# --- Display Chat Messages ---
# This loop displays all messages currently in session_state
for msg in st.session_state['messages']:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Suggestions Area (Rendered BEFORE st.chat_input) ---
# This container will hold the suggestions, positioned above the chat input via CSS
st.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
# Create columns to lay out the suggestion buttons horizontally
cols = st.columns(len(SUGGESTIONS))
for i, suggestion in enumerate(SUGGESTIONS):
    with cols[i]:
        # Create a button for each suggestion
        # use_container_width=False prevents button from stretching across the entire column
        # A unique key is important for each button
        st.button(
            suggestion, 
            on_click=handle_suggestion_click, 
            args=(suggestion,), 
            key=f"suggestion_btn_{i}", 
            help=suggestion, 
            use_container_width=False
        )
st.markdown("</div>", unsafe_allow_html=True)


# --- Chat Input (Fixed at Bottom - Streamlit Native) ---
# This is placed at the very end of the script to ensure it renders at the bottom.
user_query = st.chat_input("Ask a question...")

if user_query: # This block executes when the user types and submits a message
    # Add user message to history
    st.session_state['messages'].append({"role": "user", "content": user_query})
    
    # Get bot response
    response = knowledge_base.get(user_query, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    
    st.rerun() # Rerun the app to show the new messages and clear the input
