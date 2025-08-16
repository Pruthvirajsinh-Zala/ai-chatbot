import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(
    page_title="Chat with Gemini",
    page_icon="🔥"
)

st.title("Chat with Gemini")
st.caption("A Chatbot Powered by Google Gemini")


if "history" not in st.session_state:
    st.session_state.history = []

try:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
    st.session_state.app_key = True  # Set flag to enable chat input
except KeyError:
    st.error("❌ API_KEY not found in secrets.toml")
    st.info("Please add your Gemini API key to .streamlit/secrets.toml")
    st.info("Get your API key from: https://aistudio.google.com/app/apikey")
    st.stop()
except Exception as e:
    st.error(f"❌ Error configuring API: {str(e)}")
    st.info("Please check your API key in .streamlit/secrets.toml")
    st.stop()

try:
    model = genai.GenerativeModel("gemini-2.0-flash")
    chat = model.start_chat(history = st.session_state.history)
except Exception as e:
    st.error(f"❌ Error initializing model: {str(e)}")
    if "API_KEY" in str(e) or "authentication" in str(e).lower():
        st.info("Please check your API key configuration")
    st.stop()

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()

try:
    for message in chat.history:
        role ="assistant" if message.role == 'model' else message.role
        with st.chat_message(role):
            st.markdown(message.parts[0].text)
except Exception as e:
    # If there's an error displaying history, just continue
    pass

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', ' \n')
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True):
                    word_count = 0
                    random_int = random.randint(5,10)
                    for word in chunk.text:
                        full_response+=word
                        word_count+=1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5,10)
                message_placeholder.markdown(full_response)
                st.session_state.history = chat.history
            except genai.types.generation_types.BlockedPromptException as e:
                message_placeholder.markdown("❌ **Content Blocked**: The prompt was blocked due to safety filters.")
                st.error("Your message was blocked by content safety filters. Please try rephrasing your question.")
            except Exception as e:
                message_placeholder.markdown("❌ **Error**: Failed to get response")
                error_msg = str(e)
                if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    st.error("Rate limit or quota exceeded. Please wait a moment and try again.")
                elif "key" in error_msg.lower():
                    st.error("API key issue. Please check your configuration.")
                else:
                    st.error(f"Unexpected error: {error_msg}")
                st.info("Please try again or check your internet connection.")
