"""
YouTube Script Generator Page
"""
import streamlit as st
import markdown
from utils.groq_client import GroqGenerator, AVAILABLE_MODELS
from utils.prompting import YOUTUBE_SCRIPT_TEMPLATE, CONVERSATION_SYSTEM_PROMPT

def show():
    """Display the YouTube script generator page."""
    st.header("YouTube Script Generator")
    st.markdown("""
    Generate a complete YouTube script based on your topic and genre. 
    Enter the details below and click "Generate Script" to create your content.
    """)
    
    # Initialize session state for chat history
    if "script_messages" not in st.session_state:
        st.session_state.script_messages = []
    
    if "script_generated" not in st.session_state:
        st.session_state.script_generated = False
    
    # Input form
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_area("Topic or Synopsis", 
                                placeholder="E.g., 'The rise of Generative AI and its impact on creative industries'",
                                help="Provide a brief description of what your video will be about")
        
        with col2:
            genre = st.selectbox("Video Genre", 
                                ["Educational", "Tutorial", "Entertainment", "Commentary", 
                                 "Review", "Vlog", "Documentary", "News"],
                                help="Select the genre that best fits your video concept")
        
        # Model settings
        st.subheader("Generation Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            model = st.selectbox("Model", AVAILABLE_MODELS, 
                                help="Select the AI model to use for generation")
        
        with col2:
            temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1,
                                  help="Lower values for more predictable outputs, higher for more creative")
    
    # Generate button
    generate_pressed = st.button("Generate Script", use_container_width=True)
    
    # Display chat history
    st.subheader("Conversation")
    for message in st.session_state.script_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "thinking" in message and message["thinking"]:
                with st.expander("View thinking process"):
                    st.markdown(message["thinking"])
            st.markdown(message["content"])
    
    # Handle script generation
    if generate_pressed and topic and genre:
        with st.spinner("Generating your YouTube script..."):
            try:
                # Create generator instance
                generator = GroqGenerator(model_name=model, temperature=temperature)
                
                # Generate the script
                response = generator.generate_content(
                    YOUTUBE_SCRIPT_TEMPLATE,
                    topic=topic,
                    genre=genre
                )
                
                # Check if we need to extract thinking for DeepSeek model
                thinking = ""
                if model == "deepseek-r1-distill-llama-70b":
                    thinking, response = generator.parse_deepseek_thinking(response)
                
                # Store the user query and response in session state
                st.session_state.script_messages.append({"role": "user", "content": f"Please create a YouTube script about '{topic}' in the {genre} genre."})
                st.session_state.script_messages.append({"role": "assistant", "content": response, "thinking": thinking})
                st.session_state.script_generated = True
                
                # Force refresh to show new messages
                st.rerun()
            
            except Exception as e:
                st.error(f"Error generating script: {str(e)}")
    
    # Chat input for conversation after script generation
    if st.session_state.script_generated:
        user_input = st.chat_input("Ask about your script or request changes...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.script_messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Thinking..."):
                try:
                    # Create generator instance with current settings
                    generator = GroqGenerator(model_name=model, temperature=temperature)
                    
                    # Convert session state messages to format needed for the API
                    api_messages = [{"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}]
                    for msg in st.session_state.script_messages[:-1]:  # Exclude latest user message
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Add the latest user message
                    api_messages.append({"role": "user", "content": user_input})
                    
                    # Get response
                    response = generator.chat_with_history(api_messages[1:], system_prompt=CONVERSATION_SYSTEM_PROMPT)
                    
                    # Check if we need to extract thinking for DeepSeek model
                    thinking = ""
                    if model == "deepseek-r1-distill-llama-70b":
                        thinking, response = generator.parse_deepseek_thinking(response)
                    
                    # Add response to chat history
                    st.session_state.script_messages.append({"role": "assistant", "content": response, "thinking": thinking})
                    
                    # Force refresh to show new messages
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")