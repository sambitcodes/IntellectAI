"""
Short Story Generator Page
"""
import streamlit as st
from utils.groq_client import GroqGenerator, AVAILABLE_MODELS
from utils.prompting import SHORT_STORY_TEMPLATE, CONVERSATION_SYSTEM_PROMPT

# List of famous authors for style selection
FAMOUS_AUTHORS = [
    "Charles Dickens", 
    "William Shakespeare", 
    "Jane Austen", 
    "Ernest Hemingway", 
    "Fyodor Dostoevsky", 
    "Virginia Woolf",
    "Gabriel García Márquez", 
    "Franz Kafka", 
    "Toni Morrison", 
    "George Orwell",
    "Edgar Allan Poe",
    "J.K. Rowling",
    "Stephen King",
    "Neil Gaiman",
    "Agatha Christie"
]

def show():
    """Display the Short Story Generator page."""
    st.header("Short Story Generator")
    st.markdown("""
    Generate a well-crafted short story based on your chosen topic, genre, and author style. 
    Enter the details below and click "Generate Story" to create your narrative.
    """)
    
    # Initialize session state for chat history
    if "story_messages" not in st.session_state:
        st.session_state.story_messages = []
    
    if "story_generated" not in st.session_state:
        st.session_state.story_generated = False
    
    # Input form
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_area("Topic or Premise", 
                                placeholder="E.g., 'A forgotten letter discovered 50 years too late'",
                                help="Provide a brief description of your story idea")
        
        with col2:
            genre = st.selectbox("Story Genre", 
                               ["Fantasy", "Science Fiction", "Mystery", "Romance", 
                                "Horror", "Historical Fiction", "Literary Fiction", 
                                "Adventure", "Thriller", "Comedy"],
                               help="Select the genre that best fits your story concept")
        
        # Author style selection
        style = st.selectbox("Writing Style (Author)", 
                           FAMOUS_AUTHORS,
                           help="Select the author whose writing style you want to emulate")
        
        # Model settings
        st.subheader("Generation Settings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            model = st.selectbox("Model", AVAILABLE_MODELS, 
                               help="Select the AI model to use for generation",
                               key="story_model")
        
        with col2:
            temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1,
                                  help="Lower values for more predictable outputs, higher for more creative",
                                  key="story_temp")
        
        with col3:
            word_count = st.select_slider("Word Count", 
                                        options=[300, 500, 750, 1000, 1500, 2000],
                                        value=750,
                                        help="Select the approximate length of the story")
    
    # Generate button
    generate_pressed = st.button("Generate Story", use_container_width=True)
    
    # Display chat history
    st.subheader("Conversation")
    for message in st.session_state.story_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "thinking" in message and message["thinking"]:
                with st.expander("View thinking process"):
                    st.markdown(message["thinking"])
            st.markdown(message["content"])
    
    # Handle story generation
    if generate_pressed and topic and genre and style:
        with st.spinner("Generating your short story..."):
            try:
                # Create generator instance
                generator = GroqGenerator(model_name=model, temperature=temperature)
                
                # Generate the story
                response = generator.generate_content(
                    SHORT_STORY_TEMPLATE,
                    topic=topic,
                    genre=genre,
                    style=style,
                    word_count=word_count
                )
                
                # Check if we need to extract thinking for DeepSeek model
                thinking = ""
                if model == "deepseek-r1-distill-llama-70b":
                    thinking, response = generator.parse_deepseek_thinking(response)
                
                # Store the user query and response in session state
                st.session_state.story_messages.append({
                    "role": "user", 
                    "content": f"Please write a {word_count}-word {genre} short story about '{topic}' in the style of {style}."
                })
                st.session_state.story_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "thinking": thinking
                })
                st.session_state.story_generated = True
                
                # Force refresh to show new messages
                st.rerun()
            
            except Exception as e:
                st.error(f"Error generating story: {str(e)}")
    
    # Chat input for conversation after story generation
    if st.session_state.story_generated:
        user_input = st.chat_input("Ask about your story or request changes...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.story_messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Thinking..."):
                try:
                    # Create generator instance with current settings
                    generator = GroqGenerator(model_name=model, temperature=temperature)
                    
                    # Convert session state messages to format needed for the API
                    api_messages = [{"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}]
                    for msg in st.session_state.story_messages[:-1]:  # Exclude latest user message
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
                    st.session_state.story_messages.append({
                        "role": "assistant", 
                        "content": response,
                        "thinking": thinking
                    })
                    
                    # Force refresh to show new messages
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")