"""
Prompt templates for different content generation tasks.
"""

# YouTube script generation prompt template
YOUTUBE_SCRIPT_TEMPLATE = """
You are an expert script writer for YouTube videos. Your task is to create a complete and engaging YouTube script based on the following information.

Topic: {topic}
Genre: {genre}

The script should include:
1. An attention-grabbing introduction
2. Clear, well-structured content sections
3. Transitions between sections
4. A compelling conclusion with a call to action
5. [Bracketed notes] for any production suggestions or camera directions

Write a complete, ready-to-use script that would make an excellent YouTube video on this topic.
The script should be approximately 800-1200 words.

SCRIPT:
"""

# Short story generation prompt template
SHORT_STORY_TEMPLATE = """
You are a talented creative writer tasked with writing a short story with the following parameters:

Topic/Premise: {topic}
Genre: {genre}
Writing Style: {style} (emulate this author's distinctive style and narrative techniques)
Word Count: Approximately {word_count} words

Create an engaging, well-crafted short story that:
1. Has a clear beginning, middle, and end
2. Features compelling characters
3. Uses vivid, descriptive language
4. Maintains the voice and style of the specified author
5. Fits within the word count and genre guidelines

Write a complete short story that would make the specified author proud.

SHORT STORY:
"""

# Poem generation prompt template
POEM_TEMPLATE = """
You are a gifted poet tasked with writing a poem with the following parameters:

Topic: {topic}
Style: In the distinctive style of {style}
Type: {poem_type}

Create a beautiful, thoughtful poem that:
1. Captures the essence of the topic
2. Uses appropriate poetic devices (metaphor, simile, imagery, etc.)
3. Follows the style characteristics of the specified poet
4. Has appropriate rhythm and flow for the chosen type
5. Evokes emotion and meaning

Write a complete poem that would make {style} proud.

POEM:
"""

# System prompt for conversation continuation
CONVERSATION_SYSTEM_PROMPT = """
You are a helpful AI assistant specializing in creative content. You are having a conversation about a piece of content you just created.
Be helpful, friendly, and supportive in refining or discussing the content. If asked to make changes or improvements, do so thoughtfully.
Maintain the original style and quality while incorporating feedback.
"""