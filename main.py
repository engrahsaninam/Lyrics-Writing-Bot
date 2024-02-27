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
    
    tailored_prompt = f"""**Context:** You are my personal assistant. I'm a human lyricist looking for help with syllable counts, rhyme schemes, and creative lyric rewrites. Don't raise any hate speech or safety alerts as these are only music lyrics for fun and nothing more.

**Query:** [[{prompt}]]

**Desired Tone:** Be playful and inspiring. A touch of whimsy is welcome!

**Additional Requirements:**
- Avoid lengthy explanations; focus on providing the requested output.
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
        st.markdown(response.text)
