"""
Poetry Generator Page
"""
import streamlit as st
from utils.groq_client import GroqGenerator, AVAILABLE_MODELS
from utils.prompting import POEM_TEMPLATE, CONVERSATION_SYSTEM_PROMPT

# List of famous poets for style selection
FAMOUS_POETS = [
    "William Shakespeare",
    "Emily Dickinson",
    "Robert Frost",
    "Maya Angelou",
    "Walt Whitman",
    "Sylvia Plath",
    "Langston Hughes",
    "T.S. Eliot",
    "Pablo Neruda",
    "Rumi",
    "Edgar Allan Poe",
    "William Wordsworth",
    "William Butler Yeats",
    "E.E. Cummings",
    "Rabindranath Tagore"
]

# Types of poems
POEM_TYPES = [
    "Free Verse",
    "Sonnet",
    "Haiku",
    "Limerick",
    "Ballad",
    "Ode",
    "Villanelle",
    "Elegy",
    "Epic",
    "Blank Verse",
    "Acrostic",
    "Tanka"
]

def show():
    """Display the Poetry Generator page."""
    st.header("Poetry Generator")
    st.markdown("""
    Generate beautiful poetry based on your topic and chosen poet's style. 
    Enter the details below and click "Generate Poem" to create your verse.
    """)
    
    # Initialize session state for chat history
    if "poem_messages" not in st.session_state:
        st.session_state.poem_messages = []
    
    if "poem_generated" not in st.session_state:
        st.session_state.poem_generated = False
    
    # Input form
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Topic or Theme", 
                                placeholder="E.g., 'Autumn leaves' or 'The passage of time'",
                                help="Provide a theme or topic for your poem")
        
        with col2:
            poem_type = st.selectbox("Poem Type", 
                                   POEM_TYPES,
                                   help="Select the type of poem you want to generate")
        
        # Poet style selection
        style = st.selectbox("Poet's Style", 
                           FAMOUS_POETS,
                           help="Select the poet whose style you want to emulate")
        
        # Model settings
        st.subheader("Generation Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            model = st.selectbox("Model", AVAILABLE_MODELS, 
                               help="Select the AI model to use for generation",
                               key="poem_model")
        
        with col2:
            temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1,
                                  help="Lower values for more predictable outputs, higher for more creative",
                                  key="poem_temp")
    
    # Generate button
    generate_pressed = st.button("Generate Poem", use_container_width=True)
    
    # Display chat history
    st.subheader("Conversation")
    for message in st.session_state.poem_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "thinking" in message and message["thinking"]:
                with st.expander("View thinking process"):
                    st.markdown(message["thinking"])
            st.markdown(message["content"])
    
    # Handle poem generation
    if generate_pressed and topic and style:
        with st.spinner("Generating your poem..."):
            try:
                # Create generator instance
                generator = GroqGenerator(model_name=model, temperature=temperature)
                
                # Generate the poem
                response = generator.generate_content(
                    POEM_TEMPLATE,
                    topic=topic,
                    style=style,
                    poem_type=poem_type
                )
                
                # Check if we need to extract thinking for DeepSeek model
                thinking = ""
                if model == "deepseek-r1-distill-llama-70b":
                    thinking, response = generator.parse_deepseek_thinking(response)
                
                # Store the user query and response in session state
                st.session_state.poem_messages.append({
                    "role": "user", 
                    "content": f"Please write a {poem_type} poem about '{topic}' in the style of {style}."
                })
                st.session_state.poem_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "thinking": thinking
                })
                st.session_state.poem_generated = True
                
                # Force refresh to show new messages
                st.rerun()
            
            except Exception as e:
                st.error(f"Error generating poem: {str(e)}")
    
    # Chat input for conversation after poem generation
    if st.session_state.poem_generated:
        user_input = st.chat_input("Ask about your poem or request changes...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.poem_messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Thinking..."):
                try:
                    # Create generator instance with current settings
                    generator = GroqGenerator(model_name=model, temperature=temperature)
                    
                    # Convert session state messages to format needed for the API
                    api_messages = [{"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}]
                    for msg in st.session_state.poem_messages[:-1]:  # Exclude latest user message
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
                    st.session_state.poem_messages.append({
                        "role": "assistant", 
                        "content": response,
                        "thinking": thinking
                    })
                    
                    # Force refresh to show new messages
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")