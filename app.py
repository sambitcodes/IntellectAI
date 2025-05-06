"""
AI Storytelling App - Main Application
"""
import os
import streamlit as st
from dotenv import load_dotenv
import pages.script_generator as script_page
import pages.story_generator as story_page
import pages.poem_generator as poem_page

# Load environment variables from .env file if present
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="IntellectAI",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main .block-container {padding-top: 2rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 5px;}
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
        border-bottom: 2px solid #4e8cff;
    }
    .stButton button {
        background-color: #4e8cff;
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 4px;
    }
    .stButton button:hover {
        background-color: #3a7de0;
    }
    .thinking-box {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        background-color: #f8f9fa;
        margin-bottom: 15px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #f0f3f9;
        border-left: 4px solid #4e8cff;
    }
    .chat-message.assistant {
        background-color: #f9f9f9;
        border-left: 4px solid #10a37f;
    }
    .chat-message .message-content {
        flex: 1;
        padding-left: 0.75rem;
    }
    .chat-message .avatar {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }
    .chat-message .avatar.user {
        background-color: #4e8cff;
    }
    .chat-message .avatar.assistant {
        background-color: #10a37f;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    st.title(":blue[Intellect]:red[AI] 🖋️🤖")
    st.markdown("***:violet[Content Creator, Story Writer, Poet  powered by AI]***")
    
    # Check if GROQ_API_KEY is set
    if not os.environ.get("GROQ_API_KEY"):
        st.error("⚠️ GROQ_API_KEY environment variable is not set. Please set it before using this application.")
        st.info("You can set it by creating a .env file with GROQ_API_KEY=your_api_key or by setting it in your environment.")
        return
    
    # Create tabs for different content types
    tabs = st.tabs(["YouTube Script Generator", "Short Story Generator", "Poetry Generator"])
    
    # YouTube Script Generator tab
    with tabs[0]:
        script_page.show()
    
    # Short Story Generator tab
    with tabs[1]:
        story_page.show()
    
    # Poetry Generator tab
    with tabs[2]:
        poem_page.show()

if __name__ == "__main__":
    main()