# AI Content Creator

A Streamlit-based conversational AI application that uses LangChain and Groq to generate creative content.

## Features

- **YouTube Script Generator**: Create full scripts for YouTube videos based on topic and genre
- **Short Story Generator**: Craft short stories in the style of famous authors
- **Poetry Generator**: Produce poems and haikus in various poetic styles
- **Conversational Interface**: Chat with the AI to refine and customize your content
- **Multiple Models**: Choose from different Groq models for content generation
- **DeepSeek Thinking Mode**: When using DeepSeek models, see the AI's thinking process

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-content-creator.git
   cd ai-content-creator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

Run the Streamlit app:
```
streamlit run app.py
```

Then navigate to the provided URL (typically http://localhost:8501) in your web browser.

### YouTube Script Generator
- Enter a topic and select the genre of your video
- Adjust parameters like length, tone, model, and temperature
- Ask the AI to generate a script or chat conversationally about your video

### Short Story Generator
- Provide a topic and select a genre
- Choose an author's style to emulate (Dickens, Austen, Hemingway, etc.)
- Customize length, mood, and generation parameters
- Receive a well-crafted short story

### Poetry Generator
- Input a topic and select a genre
- Choose a poet's style to emulate (Shakespeare, Dickinson, Frost, etc.)
- Select poem type, length, and emotional tone
- Generate poetry that matches your specifications

## Models

The application supports the following Groq models:
- llama3-70b-8192
- llama-3.3-70b-versatile
- gemma2-9b-it
- deepseek-r1-distill-llama-70b
- qwen-qwq-32b

## Project Structure

```
creative_ai_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables (Groq API key)
├── pages/
│   ├── youtube_script.py       # YouTube script generator page
│   ├── short_story.py          # Short story generator page
│   ├── poetry.py               # Poetry generator page
├── utils/
│   ├── __init__.py
│   ├── groq_client.py          # Groq API client
│   ├── prompts.py              # Prompt templates
│   ├── chain_factory.py        # Chain factory for different generation types
│   └── ui_components.py        # Reusable UI components
├── styles/
│   └── main.css                # CSS for styling the app
└── README.md                   # Project documentation
```

## Advanced Features

- **Conversation History**: Maintain context throughout your conversation
- **Temperature Control**: Adjust randomness in the generated content
- **Thinking Process Visibility**: See the model's reasoning (with DeepSeek models)
- **Custom Styling**: Enhanced UI with custom CSS

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
