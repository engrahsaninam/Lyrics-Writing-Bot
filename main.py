import streamlit as st
import os
import google.generativeai as genai
# from dotenv import load_dotenv

def extract_subtext(text):
    start_marker = "[["
    end_marker = "]]"
    
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index != -1 and end_index != -1 and start_index < end_index:
        subtext = text[start_index + len(start_marker):end_index]
        return subtext
    else:
        return None


# load_dotenv()
st.set_page_config(
    page_title="LyricGenie",
    page_icon=":robot_face:",
    layout="wide",
)

# Initialize Gemini-Pro
genai.configure(api_key='AIzaSyA7pwwY9mUN_XrDGihJNeA1QSgEg2lvUDc')
model = genai.GenerativeModel("gemini-pro")

def role_to_streamlit(role):
    return "assistant" if role == "model" else role

# Store only prompt messages in chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("LyricGenie")

# Display prompt messages from history
for message in st.session_state.chat.history:
    if message.role == "user":
        prompt_text = extract_subtext(message.parts[0].text)  # Extract prompt from first line
        with st.chat_message("user"):
            st.markdown(prompt_text)
    else:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

if prompt := st.chat_input("I'm here to help with your songwriting! Need rhymes, syllable counts, or a fresh take on your lyrics? Ask away!"):
    # Display only the prompt
    st.chat_message("user").markdown(prompt.splitlines()[0])

    tailored_prompt = f"""
**Context:** You are my songwriting assistant. I'm a human lyricist looking for help with syllable counts, rhyme schemes, and creative lyric rewrites. 

**Query:** [[{prompt}]]

**Desired Tone:** Be playful and inspiring. A touch of whimsy is welcome!

**Additional Requirements:**
- Start with a friendly greeting if the user says "hello" or "hey". ("Hey there, ready to write some hits?")
- Avoid lengthy explanations; focus on providing the requested output.
- If the user asks who you are, respond with: "I'm your songwriting assistant, here to help with syllables, rhymes, and fresh lyric ideas!" 
- If the query seems incomplete or unclear, offer a gentle prompt for more information. ("That's a cool start! Can you tell me a bit more about what kind of rewrite you're looking for?")
"""

    response = st.session_state.chat.send_message(tailored_prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)
