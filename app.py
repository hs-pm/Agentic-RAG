import streamlit as st
import os

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

# --- CSS Styling (Revised for Scrollable Chat History) ---
st.markdown("""
    <style>
        /* Hide Streamlit's default header and toolbar */
        [data-testid="stHeader"] {
            display: none !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Ensure the main app content is a flex column and fills space */
        .stApp {
            display: flex;
            flex-direction: column;
            height: 100vh; /* Make the app take full viewport height */
            overflow: hidden; /* Hide main scrollbar */
        }
        /* Important for the main content area */
        .stApp > div:first-child {
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            overflow: hidden;
            padding: 0 !important; /* Remove default padding */
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
        .chat-history-container { /* This is the new container for messages */
            flex-grow: 1; /* Allows it to take up available space */
            overflow-y: auto; /* THIS MAKES IT SCROLLABLE */
            padding: 1rem; /* Padding inside the scrollable area */
            max-width: 700px; /* Max width for chat content */
            margin-left: auto;
            margin-right: auto;
            /* Add padding to account for fixed header and footer */
            padding-top: 7rem; /* Space for the header */
            padding-bottom: 11rem; /* Space for input and suggestions */
            box-sizing: border-box; /* Include padding in height calculation */
        }
        
        div.stChatMessage {
            margin-bottom: 0.5rem;
        }
        /* Your chat message styling */
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

        /* Suggestions Styling */
        .suggestions-row { /* New class for the suggestions row */
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center; /* Center suggestion buttons */
            width: 100%; /* Take full width of parent */
            max-width: 700px; /* Match chat history max-width */
            padding-bottom: 0.5rem; /* Small padding below suggestions */
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

        /* Chat Input Styling */
        .stChatInputContainer { /* This is the element Streamlit attaches st.chat_input to */
            width: 100% !important;
            max-width: 700px; /* Match chat history max-width */
            margin-left: auto;
            margin-right: auto;
            background-color: transparent !important; /* To see parent background */
            padding: 0 !important; /* Remove internal padding, parent handles it */
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
# This is now a simple container that uses the 'header-container' CSS class
st.markdown("<div class='header-container'>💼 Institutional Memory Agent</div>", unsafe_allow_html=True)


# --- Define the function to handle suggestion clicks ---
def handle_suggestion_click(suggestion_text):
    # This function will add the suggestion as a user message
    # and trigger a bot response, then rerun the app.
    st.session_state['messages'].append({"role": "user", "content": suggestion_text})
    # Simulate thinking for a moment before response
    with st.spinner("Thinking..."):
        response = knowledge_base.get(suggestion_text, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.rerun() # Rerun the app to update chat history and clear input


# --- Main Chat History Area (Scrollable) ---
# Create an empty placeholder for the chat history container
# This is crucial for Streamlit to handle the fixed scrolling behavior
chat_history_placeholder = st.empty()

with chat_history_placeholder.container():
    st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
    for msg in st.session_state['messages']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)


# --- Suggestions and Chat Input (Fixed at Bottom) ---
# Use a single container to hold both suggestions and the chat input
st.markdown("<div class='bottom-fixed-container'>", unsafe_allow_html=True)

# Suggestions Area
st.markdown("<div class='suggestions-row'>", unsafe_allow_html=True)
# Create columns to lay out the suggestion buttons horizontally
# Adjust column width as needed. Use_container_width=False
# and flex-grow: 0 !important on stColumn in CSS for better control
for i, suggestion in enumerate(SUGGESTIONS):
    # Creating a column for each button helps with layout
    # if you want them wrapped consistently, though you could also just
    # render buttons directly in the row if flex-wrap handles it well.
    col = st.columns(1)[0] # Create a single column, grab the first element
    with col:
        st.button(
            suggestion,
            on_click=handle_suggestion_click,
            args=(suggestion,),
            key=f"suggestion_btn_{i}",
            help=suggestion,
            use_container_width=False # Ensure button doesn't stretch to fill column
        )
st.markdown("</div>", unsafe_allow_html=True)


# Chat Input (Streamlit Native)
user_query = st.chat_input("Ask a question...")

st.markdown("</div>", unsafe_allow_html=True) # Close bottom-fixed-container

if user_query: # This block executes when the user types and submits a message
    # Add user message to history
    st.session_state['messages'].append({"role": "user", "content": user_query})

    # Simulate thinking for a moment before response
    with st.spinner("Thinking..."):
        # Replace this with your actual LangChain RAG call
        response = knowledge_base.get(user_query, "Sorry, I couldn’t find that. Try asking #ml-platform or check Confluence.")

    st.session_state['messages'].append({"role": "assistant", "content": response})

    st.rerun() # Rerun the app to show the new messages and clear the input
