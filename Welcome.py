import logging
import os

import streamlit as st

from src.utils import setup_logging

# Initialize logger
setup_logging()  # Set up logging configuration
logger = logging.getLogger(__name__)

# Set page config with title, icon, and layout
st.set_page_config(
    page_title="Jam with AI - Your Conversational Platform", page_icon="🤖"
)


# Custom CSS to style the page and sidebar
def apply_custom_css() -> None:
    """Applies custom CSS styling to the Streamlit page and sidebar."""
    st.markdown(
        """
        <style>
        /* Main background and text colors */
        body {
            background-color: #f0f8ff;  /* Light cyan background */
            color: #002B5B;  /* Dark blue text for readability */
        }
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] label {
            color: #002B5B;
        }
        [data-testid="stSidebar"] {
            background-color: #006d77;
        }
        [data-testid="stSidebar"] * {
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #006d77;  /* Dark cyan sidebar background */
            color: white;
            padding: 20px;
            border-right: 2px solid #003d5c;  /* Darker border */
        }
        .sidebar h2, .sidebar h4 {
            color: white;  /* White text for sidebar headings */
        }
        .block-container {
            background-color: white;  /* White content background */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);  /* Subtle shadow for modern look */
        }
        /* Center content inside columns */
        .stColumn {
            text-align: center;
        }
        /* Style for the centered and bold footer text */
        .footer-text {
            font-size: 1.1rem;
            font-weight: bold;
            color: black;
            text-align: center;
            margin-top: 10px;
        }
        /* Style buttons to look modern and attractive */
        .stButton button {
            background-color: #118ab2;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        }
        .stButton button:hover {
            background-color: #07a6c2;
            color: white;
        }
        /* Headings inside the main page */
        h1, h2, h3, h4 {
            color: #006d77;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Applied custom CSS styling.")


# Function to display logo or placeholder
def display_logo(logo_path: str) -> None:
    """Displays the logo in the sidebar or a placeholder if the logo is not found.

    Args:
        logo_path (str): The file path for the logo image.
    """
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        logger.info("Logo displayed.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo not found, displaying placeholder.")


# Function to display main content
def display_main_content() -> None:
    """Displays the main welcome content on the page."""
    st.title("Personal Document Assistant 📄🤖")
    st.markdown(
        """
        Welcome to the AI-Powered Document Retrieval Assistant 👋
                
        This app allows you to interact with an AI-powered assistant and upload documents for processing and retrieval.
        
        **Features:**
        - **Chatbot**: Have a conversation with the AI using the latest LLM model.
        - **Document Upload**: Upload PDFs and retrieve data from them using OpenSearch as a Hybrid RAG System.
        
        **Choose a page from the sidebar to begin!**
        """
    )
    logger.info("Displayed main welcome content.")


# Function to display sidebar content
def display_sidebar_content() -> None:
    """Displays headers and footer content in the sidebar."""
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>Jam with AI</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Your Conversational Platform</h4>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2024 Jam with AI
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Displayed sidebar content.")


# Main execution
if __name__ == "__main__":
    apply_custom_css()
    display_logo("images/jamwithai_logo.png")
    display_sidebar_content()
    display_main_content()
