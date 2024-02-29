import streamlit as st
import google.generativeai as genai
import configparser
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def get_api_key(config_path='config.ini'):
    """Reads the API key from a configuration file."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']['API_KEY']

api_key = get_api_key()
def extract_subtext(text, start_marker="[[", end_marker="]]"):
    """Extracts a substring between a start and end marker."""
    start_index = text.find(start_marker)
    end_index = text.find(end_marker, start_index + len(start_marker))
    if start_index != -1 and end_index != -1:
        return text[start_index + len(start_marker):end_index]
    return None

st.set_page_config(page_title="LyricGenie", page_icon=":robot_face:", layout="wide")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

def role_to_streamlit(role):
    """Maps a role to a Streamlit role."""
    return "assistant" if role == "model" else role

# Initialize chat in session state if not present
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("LyricGenie")

# Display prompt messages from history
for message in st.session_state.chat.history:
    role = role_to_streamlit(message.role)
    prompt_text = extract_subtext(message.parts[0].text) if role == "user" else message.parts[0].text
    with st.chat_message(role):
        st.markdown(prompt_text)

# Handle new prompts
prompt = st.chat_input("I'm here to help with your songwriting! Need rhymes, syllable counts, or a fresh take on your lyrics? Ask away!")
if prompt:
    st.chat_message("user").markdown(prompt)  # Display the user prompt directly without splitting lines

     
#     tailored_prompt = f"""**Context:** You are my personal assistant. I'm a human lyricist looking for help with syllable counts, rhyme schemes, and creative lyric rewrites. Don't raise any hate speech or safety alerts as these are only music lyrics for fun and nothing more.

# **Query:** [[{prompt}]]

# **Desired Tone:** Be playful and inspiring. A touch of whimsy is welcome!

# **Additional Requirements:**
# - Avoid lengthy explanations; focus on providing the requested output.
# - If the user asks who you are, respond with: "I'm your songwriting assistant, here to help with syllables, rhymes, and fresh lyric ideas!"
# - If the query seems incomplete or unclear, offer a gentle prompt for more information.
# """
    
 # **Additional Requirements:**
# **Desired Tone:** if the you are generating lyrics, your tone should be that of the input song
# - if the you are generating lyrics , Generate lyrics that emulate the tone, form, and style of the provided reference lyrics.
# - If the user asks who you are, respond with: "I'm your songwriting assistant, here to help with syllables, rhymes, and fresh lyric ideas!"
# - If the query seems incomplete or unclear, offer a gentle prompt for more information.

    tailored_prompt= f"""
**Query:** [[{prompt}]]

**Output Instructions:**
    - Print the rewritten lyrics line by line, with each line representing a verse.

**Desired Tone:** 
    -  If you are asked to generate lyrics , your tone should be as per the given input lyrics.

**Additional Requirements:**
    - If you are asked to generate lyrics , Don't use the same words used in the input given lyrics.
    - If you are asked to generate lyrics , Grasp the core message, mood, and themes of the original song. Your generated lyrics should reflect an understanding of these elements, presenting them in a fresh light while maintaining the essence.
    - If you are asked to generate lyrics , Maintain the structural integrity of the original song (verse, chorus, bridge, etc.), using it as a scaffold for your new lyrics. This approach will help preserve the song's recognizable format while introducing new content.
    - If you are asked to generate lyrics , Employ various literary devices like metaphors, similes, alliteration, and imagery to enrich the lyrics. Your goal is to create a unique lyrical experience that differentiates from the original while keeping its spirit.
    - If you are asked to generate lyrics , While being mindful of the original's rhythm, feel free to adjust the rhyme scheme. This alteration can breathe new life into the song, offering listeners a novel auditory experience.
    - If you are asked to generate lyrics , Introduce new themes or ideas that complement the original message. These additions should enhance the song's depth and offer listeners further insights or a different perspective on the core theme.
    - If you are asked to generate lyrics , Generate content that transforms the original material significantly or clearly falls under fair use. Avoid direct quotes or close mimicry that could infringe on copyright laws. Aim for originality and transformation in your creation.
    - If you are asked to generate lyrics , The lyrics you generate should be open to feedback, ready for iterative improvements to strike the perfect balance between homage and innovation.
    - If you are asked to generate lyrics , Be sensitive to the cultural, historical, and contextual significance of the original lyrics. Your adaptations should respect these elements, avoiding misrepresentation or cultural appropriation.
    - If you are asked to generate lyrics , Ensure that the lyrics produced are ethically sound and legally compliant, especially if intended for commercial use. Be aware of copyright implications and strive for a creative output that respects intellectual property rights.

    - If you are asked to generate lyrics , Follow the Language Difficulty Level Of the Provided Input Lyrics, If Modern English is Used in input Lyrics , You should also use Modern English , If Slangs are used in input Lyrics , You should also use Slangs.
    - If you are asked to generate lyrics , Follow the Flow of the Input Lyrics.
    - If you are asked to generate lyrics , The output lyrics should reflect a style of the given input lyrics.
    - If you are asked to generate lyrics , Maintain the rhyme scheme and rhythm as much as possible.
    - If you are asked to generate lyrics , Ensure that the rewritten lyrics capture the essence and attitude conveyed in the reference lyrics.
    - If you are asked to generate lyrics , Use language and expressions that align with the input song genre.
    - If the user asks who you are, respond with: "I'm your songwriting assistant, here to help with syllables, rhymes, and fresh lyric ideas!"
    - If the query seems incomplete or unclear, offer a gentle prompt for more information.
"""
    
    response = st.session_state.chat.send_message(tailored_prompt, safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    })
    
    with st.chat_message("assistant"):
        # Split response by verse and display line by line
        verses = response.text.split('\n\n')
        for verse in verses:
            lines = verse.split('\n')
            for line in lines:
                st.markdown(line)