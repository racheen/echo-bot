import logging
import os

import streamlit as st

from src.chat import (  # type: ignore
    ensure_model_pulled,
    generate_response_streaming,
    get_embedding_model,
)
from src.ingestion import create_index, get_opensearch_client
from src.constants import OLLAMA_MODEL_NAME, OPENSEARCH_INDEX
from src.utils import setup_logging

# Initialize logger
setup_logging()  # Configures logging for the application
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(page_title="Jam with AI - Chatbot", page_icon="🤖")

# Apply custom CSS
st.markdown(
    """
    <style>
    /* Main background and text colors */
    body { background-color: #f0f8ff; color: #002B5B; }
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] label { color: #002B5B; }
    [data-testid="stSidebar"] { background-color: #006d77; }
    [data-testid="stSidebar"] * { color: white; }
    .sidebar .sidebar-content { background-color: #006d77; color: white; padding: 20px; border-right: 2px solid #003d5c; }
    .sidebar h2, .sidebar h4 { color: white; }
    .block-container { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); }
    .footer-text { font-size: 1.1rem; font-weight: bold; color: black; text-align: center; margin-top: 10px; }
    .stButton button { background-color: #118ab2; color: white; border-radius: 5px; padding: 10px 20px; font-size: 16px; }
    .stButton button:hover { background-color: #07a6c2; color: white; }
    h1, h2, h3, h4 { color: #006d77; }
    [data-testid="stChatMessage"] { background-color: #e0f7fa; color: #002B5B; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    [data-testid="stChatMessage"] * { color: #002B5B; }
    [data-testid="stChatInput"] textarea { color: #002B5B; background-color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)
logger.info("Custom CSS applied.")


# Main chatbot page rendering function
def render_chatbot_page() -> None:
    # Set up a placeholder at the very top of the main content area
    st.title("Jam with AI - Chatbot 🤖")
    model_loading_placeholder = st.empty()

    # Initialize session state variables for chatbot settings
    if "use_hybrid_search" not in st.session_state:
        st.session_state["use_hybrid_search"] = True
    if "num_results" not in st.session_state:
        st.session_state["num_results"] = 5
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = 0.7

    # Initialize OpenSearch client
    with st.spinner("Connecting to OpenSearch..."):
        client = get_opensearch_client()
    index_name = OPENSEARCH_INDEX

    # Ensure the index exists
    create_index(client)

    # Sidebar settings for hybrid search toggle, result count, and temperature
    st.session_state["use_hybrid_search"] = st.sidebar.checkbox(
        "Enable RAG mode", value=st.session_state["use_hybrid_search"]
    )
    st.session_state["num_results"] = st.sidebar.number_input(
        "Number of Results in Context Window",
        min_value=1,
        max_value=10,
        value=st.session_state["num_results"],
        step=1,
    )
    st.session_state["temperature"] = st.sidebar.slider(
        "Response Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state["temperature"],
        step=0.1,
    )

    # Display logo or placeholder
    logo_path = "images/jamwithai_logo.png"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        logger.info("Logo displayed.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo not found, displaying placeholder.")

    # Sidebar headers and footer
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>Jam with AI</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Your Conversational Platform</h4>",
        unsafe_allow_html=True,
    )

    # Footer text
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2025 Jam with AI
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Sidebar configured with headers and footer.")

    # Display loading spinner at the top of the main content area
    with model_loading_placeholder.container():
        st.spinner("Loading models for chat...")

    # Load models if not already loaded
    if "embedding_models_loaded" not in st.session_state:
        with model_loading_placeholder:
            with st.spinner("Loading Embedding and Ollama models for Hybrid Search..."):
                get_embedding_model()
                ensure_model_pulled(OLLAMA_MODEL_NAME)
                st.session_state["embedding_models_loaded"] = True
        logger.info("Embedding model loaded.")
        model_loading_placeholder.empty()

    # Initialize chat history in session state if not already present
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display chat history
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process user input and generate response
    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        logger.info("User input received.")

        # Generate response from assistant
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response_placeholder = st.empty()
                response_text = ""

                response_stream = generate_response_streaming(
                    prompt,
                    use_hybrid_search=st.session_state["use_hybrid_search"],
                    num_results=st.session_state["num_results"],
                    temperature=st.session_state["temperature"],
                    chat_history=st.session_state["chat_history"],
                )

            # Stream response content if response_stream is valid
            if response_stream is not None:
                for chunk in response_stream:
                    if (
                        isinstance(chunk, dict)
                        and "message" in chunk
                        and "content" in chunk["message"]
                    ):
                        response_text += chunk["message"]["content"]
                        response_placeholder.markdown(response_text + "▌")
                    else:
                        logger.error("Unexpected chunk format in response stream.")

            response_placeholder.markdown(response_text)
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": response_text}
            )
            logger.info("Response generated and displayed.")


# Main execution
if __name__ == "__main__":
    render_chatbot_page()
