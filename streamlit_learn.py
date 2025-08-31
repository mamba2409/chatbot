import streamlit as st
from groq import Groq

st.set_page_config(page_icon="💬", layout="wide",
                   page_title="JainBOT")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🤖")

st.write("# Your Jain bot")
x = st.chat_input("What is on your mind?")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# st.write(st.session_state)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if x:
    st.session_state["messages"].append({"role": "user", "content" : x})

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=st.session_state["messages"],
        temperature=1,
        max_completion_tokens=8000,
        top_p=1,
        stream=True
    )

    response = ""
    response_container = st.empty()
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response+=chunk.choices[0].delta.content
            response_container.write(response)

    st.session_state["messages"].append({"role": "assistant", "content" : response})

