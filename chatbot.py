import streamlit as st
import os
import random
import time
import google.generativeai as genai
from utils import process_uploaded_file

# Function to render Chatbot page
def render_chatbot_page():
    st.title("💬 Chat with Gemini")
    st.caption("🤖 Your AI Assistant Powered by Google Gemini 2.0 Flash")
    
    # API Configuration (only for chatbot page)
    try:
        api_key = st.secrets.get['secrets']['key'] or os.getenv('API_KEY') or st.session_state.get("API_KEY")
        if not api_key or api_key == "your-gemini-api-key-here" or not api_key.strip():
            #st.error("❌ API_KEY not found in secrets.toml")
            st.info("You can add your Gemini API key below for this session")
            user_key = st.text_input("Enter your Gemini API key:", type="password", key="api_key_input")
            if user_key:
                st.session_state["API_KEY"] = user_key
                st.success("API key set for this session! Please rerun the page.")
                st.stop()
            st.info("Get your API key from: https://aistudio.google.com/app/apikey")
            st.stop()
        genai.configure(api_key=api_key)
        st.session_state.app_key = True
    except Exception as e:
        st.error(f"❌ Error configuring API: {str(e)}")
        st.info("Please check your API key in .streamlit/secrets.toml or enter it above.")
        st.stop()

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        chat = model.start_chat(history=st.session_state.history)
    except Exception as e:
        st.error(f"❌ Error initializing model: {str(e)}")
        if "API_KEY" in str(e) or "authentication" in str(e).lower():
            st.info("Please check your API key configuration")
        st.stop()

    # Display chat history
    try:
        for message in chat.history:
            role = "assistant" if message.role == 'model' else message.role
            with st.chat_message(role):
                st.markdown(message.parts[0].text)
    except Exception as e:
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
                    if any(f['is_image'] for f in file_contents):
                        # For image files, use Gemini Pro Vision model
                        vision_model = genai.GenerativeModel("gemini-2.0-flash")
                        
                        # Prepare image data
                        image_parts = []
                        for file_info in file_contents:
                            if file_info['is_image']:
                                image_parts.append(file_info['content'])
                        
                        if image_parts:
                            # Create a message with both text and images
                            message_parts = [complete_message] + image_parts
                            response = vision_model.generate_content(message_parts, stream=True)
                        else:
                            response = chat.send_message(complete_message, stream=True)
                    else:
                        # Regular text-based processing
                        response = chat.send_message(complete_message, stream=True)
                    
                    # Stream the response
                    for chunk in response:
                        word_count = 0
                        random_int = random.randint(5, 10)
                        for word in chunk.text:
                            full_response += word
                            word_count += 1
                            if word_count == random_int:
                                time.sleep(0.05)
                                message_placeholder.markdown(full_response + "▋")
                                word_count = 0
                                random_int = random.randint(5, 10)
                    
                    message_placeholder.markdown(full_response)
                    st.session_state.history = chat.history
                    
                    # Add file processing summary if files were used
                    if file_contents:
                        st.caption(f"✅ Response generated using context from {len(file_contents)} file(s)")
                        
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
