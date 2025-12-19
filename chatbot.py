import streamlit as st
import os
import random
import time
from google import genai
from google.genai import types
from utils import process_uploaded_file

# Function to render Chatbot page
def render_chatbot_page():
    st.title("💬 Chat with Gemini")
    st.caption("🤖 Your AI Assistant Powered by Google Gemini 3 Pro")
    
    # API Configuration (only for chatbot page)
    client = None
    try:
        # Try to get API key from various sources
        api_key = None
        # Check for standard Streamlit secrets keys
        if "API_KEY" in st.secrets:
            api_key = st.secrets["API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        # Check for nested secrets (as in previous version)
        elif "secrets" in st.secrets and "key" in st.secrets["secrets"]:
            api_key = st.secrets["secrets"]["key"]
            
        # Check environment variables and session state
        if not api_key:
            api_key = os.getenv('API_KEY') or os.getenv('GOOGLE_API_KEY') or st.session_state.get("API_KEY")

        if not api_key or api_key == "your-gemini-api-key-here" or not api_key.strip():
            st.info("You can add your Gemini API key below for this session")
            user_key = st.text_input("Enter your Gemini API key:", type="password", key="api_key_input")
            if user_key:
                st.session_state["API_KEY"] = user_key
                st.success("API key set for this session! Please rerun the page.")
                st.stop()
            st.info("Get your API key from: https://aistudio.google.com/app/apikey")
            st.stop()
            
        client = genai.Client(api_key=api_key)
        st.session_state.app_key = True
    except Exception as e:
        st.error(f"❌ Error configuring API: {str(e)}")
        st.info("Please check your API key in .streamlit/secrets.toml or enter it above.")
        st.stop()

    chat = None
    try:
        # Initialize chat with history
        # Note: We use gemini-2.0-flash as the model
        if "history" not in st.session_state:
            st.session_state.history = []
            
        chat = client.chats.create(model="gemini-3-flash-preview", history=st.session_state.history)
    except Exception as e:
        st.error(f"❌ Error initializing model: {str(e)}")
        if "API_KEY" in str(e) or "authentication" in str(e).lower():
            st.info("Please check your API key configuration")
        st.stop()

    # Display chat history
    try:
        # In the new SDK, history is a list of Content objects
        # We iterate through the history stored in session state or the chat object
        # If we just created the chat, chat.history should reflect st.session_state.history
        # However, for display, we might want to use the chat.history if it's populated
        
        # If st.session_state.history is empty, chat.history is empty.
        # If st.session_state.history has items, chat.history has them.
        
        # We need to handle the case where history items are dicts (from session state persistence) 
        # vs Content objects (from SDK).
        
        for message in st.session_state.history:
            # Handle both dict and object access
            role = None
            parts = []
            
            if hasattr(message, 'role'):
                role = message.role
                parts = message.parts
            elif isinstance(message, dict):
                role = message.get('role')
                parts = message.get('parts', [])
            
            if role and parts:
                # Map 'model' role to 'assistant' for Streamlit
                display_role = "assistant" if role == 'model' else role
                
                with st.chat_message(display_role):
                    # parts is a list of Part objects or dicts
                    for part in parts:
                        text = None
                        if hasattr(part, 'text'):
                            text = part.text
                        elif isinstance(part, dict):
                            text = part.get('text')
                            
                        if text:
                            st.markdown(text)
    except Exception as e:
        # st.error(f"Error displaying history: {e}")
        pass

    # File Upload Section
    st.markdown("---")
    
    # Create two columns for file upload and file info
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 File Upload")
        uploaded_files = st.file_uploader(
            "Upload files to analyze with AI",
            type=['txt', 'pdf', 'docx', 'xlsx', 'xls', 'csv', 'json', 'jpg', 'jpeg', 'png', 'gif', 'bmp'],
            accept_multiple_files=True,
            help="Supported formats: Text, PDF, Word, Excel, CSV, JSON, and Images"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
    
    with col2:
        if uploaded_files:
            st.markdown("### 📊 File Details")
            for i, file in enumerate(uploaded_files):
                with st.expander(f"📄 {file.name}", expanded=False):
                    st.write(f"**Type:** {file.type}")
                    st.write(f"**Size:** {file.size:,} bytes")

    # Process uploaded files
    file_contents = []
    if uploaded_files:
        st.markdown("---")
        st.markdown("### 🔍 File Processing")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f'Processing {uploaded_file.name}...')
            progress_bar.progress((i + 1) / len(uploaded_files))
            
            try:
                content, file_details = process_uploaded_file(uploaded_file)
                file_contents.append({
                    'name': file_details['filename'],
                    'content': content,
                    'type': file_details['filetype'],
                    'is_image': file_details['filetype'].startswith('image/')
                })
                
                # Display preview for text-based files
                if not file_details['filetype'].startswith('image/'):
                    with st.expander(f"📖 Preview: {uploaded_file.name}"):
                        if len(str(content)) > 500:
                            st.text_area("Content (first 500 characters):", str(content)[:500] + "...", height=100)
                        else:
                            st.text_area("Content:", str(content), height=100)
                else:
                    # Display image preview
                    with st.expander(f"🖼️ Image Preview: {uploaded_file.name}"):
                        st.image(content, caption=uploaded_file.name, use_column_width=True)
                        
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        
        status_text.text('✅ All files processed!')
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()

    st.markdown("---")

    # Chat input with file support
    if "app_key" in st.session_state:
        # Enhanced chat input with file context
        chat_placeholder = "💭 Ask me anything..."
        if file_contents:
            chat_placeholder = f"💭 Ask about the uploaded files or anything else... ({len(file_contents)} files uploaded)"
        
        if prompt := st.chat_input(chat_placeholder):
            prompt = prompt.replace('\n', ' \n')
            
            # Prepare the complete message with file context
            complete_message = prompt
            if file_contents:
                # Add file context to the prompt
                file_context = "\n\n📁 **Uploaded Files Context:**\n"
                for file_info in file_contents:
                    if not file_info['is_image']:
                        file_context += f"\n**File: {file_info['name']}**\n"
                        # Limit file content to avoid token limits
                        content_preview = str(file_info['content'])[:2000] + ("..." if len(str(file_info['content'])) > 2000 else "")
                        file_context += f"Content: {content_preview}\n"
                    else:
                        file_context += f"\n**Image File: {file_info['name']}** (Image analysis available)\n"
                
                complete_message = f"User question: {prompt}\n{file_context}\n\nPlease analyze the uploaded files in the context of the user's question."
            
            with st.chat_message("user"):
                st.markdown(prompt)
                if file_contents:
                    st.caption(f"📎 Context from {len(file_contents)} uploaded file(s)")
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("🤔 Thinking...")
                try:
                    full_response = ""
                    
                    # Handle images separately with Gemini Vision
                    # In the new SDK, we can just pass images in the contents list
                    
                    image_parts = []
                    for file_info in file_contents:
                        if file_info['is_image']:
                            # Assuming content is PIL Image or bytes
                            image_parts.append(file_info['content'])
                    
                    response_stream = None
                    
                    if image_parts:
                        # Use client.models.generate_content_stream for multimodal
                        # We need to construct the contents list correctly
                        # contents = [text, image1, image2, ...]
                        contents = [complete_message] + image_parts
                        response_stream = client.models.generate_content_stream(
                            model="gemini-3-pro-preview",
                            contents=contents
                        )
                    else:
                        # Regular text-based processing using the chat session
                        response_stream = chat.send_message_stream(complete_message)
                    
                    # Stream the response
                    for chunk in response_stream:
                        word_count = 0
                        random_int = random.randint(5, 10)
                        
                        # In new SDK, chunk.text gives the text part
                        if chunk.text:
                            for word in chunk.text:
                                full_response += word
                                word_count += 1
                                if word_count == random_int:
                                    time.sleep(0.05)
                                    message_placeholder.markdown(full_response + "▋")
                                    word_count = 0
                                    random_int = random.randint(5, 10)
                    
                    message_placeholder.markdown(full_response)
                    
                    # Update session state history
                    # In the new SDK, chat object might not expose history directly as a property in the same way
                    # or it might be named differently.
                    # However, we can manually append the interaction to our session state history.
                    
                    # Append user message
                    user_message_content = types.Content(
                        role="user",
                        parts=[types.Part(text=complete_message)]
                    )
                    # If we had images, we should add them to the user message parts
                    if image_parts:
                         # This is a simplification. Reconstructing the exact Content object with images 
                         # for history storage might require more detailed handling of image data types.
                         pass

                    # Append model response
                    model_message_content = types.Content(
                        role="model",
                        parts=[types.Part(text=full_response)]
                    )
                    
                    st.session_state.history.append(user_message_content)
                    st.session_state.history.append(model_message_content)
                    
                    # Add file processing summary if files were used
                    if file_contents:
                        st.caption(f"✅ Response generated using context from {len(file_contents)} file(s)")
                        
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
