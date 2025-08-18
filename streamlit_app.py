import streamlit as st
import google.generativeai as genai
import time
import random
import os
from utils import process_uploaded_file, upload_to_gemini, format_file_size, get_supported_file_types, is_supported_file_type
from home import render_home_page

# Page configuration
st.set_page_config(
    page_title="AI Chatbot Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Navigation
with st.sidebar:
    st.title("🤖 AI Chatbot Hub")
    st.markdown("---")
    
    # Navigation buttons
    pages = {
        "🏠 Home": "Home",
        "💬 Chatbot": "Chatbot", 
        "ℹ️ About App": "About",
        "📞 Contact Me": "Contact"
    }
    
    for page_label, page_key in pages.items():
        if st.button(page_label, use_container_width=True, 
                    type="primary" if st.session_state.current_page == page_key else "secondary"):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.markdown("---")
    
    # Additional sidebar content based on current page
    if st.session_state.current_page == "Chatbot":
        st.markdown("### 🔧 Chat Controls")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        
        st.markdown("### 📁 File Support")
        st.markdown("""
        **Supported formats:**
        - 📄 Text (.txt)
        - 📄 PDF (.pdf)
        - 📄 Word (.docx)
        - 📊 Excel (.xlsx, .xls)
        - 📊 CSV (.csv)
        - 🔧 JSON (.json)
        - 🖼️ Images (.jpg, .png, .gif)
        """)
        
        # Chat statistics
        if st.session_state.history:
            st.markdown("### 📊 Chat Stats")
            st.info(f"Messages: {len(st.session_state.history)}")

# Function to render Home page

# Function to render Chatbot page
def render_chatbot_page():
    st.title("💬 Chat with Gemini")
    st.caption("🤖 Your AI Assistant Powered by Google Gemini 2.0 Flash")
    
    # API Configuration (only for chatbot page)
    try:
        api_key = st.secrets["API_KEY"] or os.getenv('API_KEY')
        if api_key == "your-gemini-api-key-here" or not api_key.strip():
            st.warning("⚠️ Please add your actual Gemini API key to .streamlit/secrets.toml")
            st.info("Get your API key from: https://aistudio.google.com/app/apikey")
            st.stop()
        
        genai.configure(api_key=api_key)
        st.session_state.app_key = True
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

# Function to render About page
def render_about_page():
    st.title("ℹ️ About This App")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 What is AI Chatbot Hub?
        
        AI Chatbot Hub is an intelligent conversational AI application built with **Streamlit** and powered by 
        **Google's Gemini 2.0 Flash** model. It provides users with a seamless chat experience featuring 
        real-time streaming responses and an intuitive web interface.
        
        ## 🚀 Key Features
        
        - **🤖 Advanced AI**: Powered by Google Gemini 2.0 Flash
        - **⚡ Real-time Streaming**: See responses as they're generated
        - **📁 File Support**: Upload and analyze various file formats
        - **🖼️ Image Analysis**: AI-powered image understanding
        - **🎨 Modern UI**: Clean, responsive design with dark/light theme support
        - **📱 Mobile Friendly**: Works perfectly on all devices
        - **🔒 Secure**: Enterprise-grade security for your conversations
        - **🌐 Multi-page**: Website-like navigation structure
        
        ## 📁 File Support Features
        
        - **📄 Document Analysis**: PDF, Word, Text files
        - **📊 Data Processing**: Excel, CSV files with statistical insights
        - **🔧 Code Understanding**: JSON and various file formats
        - **🖼️ Image Intelligence**: JPEG, PNG, GIF image analysis
        - **📈 Data Visualization**: Automatic insights from spreadsheets
        - **🔍 Content Extraction**: Smart text extraction from any format
        
        ## 🛠️ Technical Stack
        
        - **Frontend**: Streamlit (Python web framework)
        - **AI Model**: Google Gemini 2.0 Flash with Vision
        - **File Processing**: PyPDF2, python-docx, pandas, Pillow
        - **Language**: Python 3.8+
        - **Deployment**: Streamlit Cloud / Local hosting
        
        ## 📊 Model Capabilities
        
        The Gemini 2.0 Flash model can help with:
        - General knowledge questions
        - Creative writing and storytelling
        - Code explanation and debugging
        - Language translation
        - Problem-solving assistance
        - Educational content
        - **File analysis and insights**
        - **Image understanding and description**
        - **Data interpretation from spreadsheets**
        """)

    with col2:
        st.markdown("### 📈 App Statistics")
        st.info("🗓️ **Version**: 3.0")
        st.info("📅 **Released**: August 2025")
        st.info("🔧 **Framework**: Streamlit")
        st.info("🤖 **AI Model**: Gemini 2.0 Flash")
        
        st.markdown("### 🌟 Features")
        features = [
            "✅ Multi-page navigation",
            "✅ Real-time streaming",
            "✅ Responsive design",
            "✅ Error handling",
            "✅ Chat statistics",
            "✅ History management"
        ]
        for feature in features:
            st.markdown(feature)

# Function to render Contact page
def render_contact_page():
    st.title("📞 Contact Me")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ## 👨‍💻 Get in Touch
        
        I'm always excited to connect with fellow developers, users, and AI enthusiasts! 
        Whether you have questions, suggestions, or just want to chat about AI technology, 
        please reach out through the channels below.
        
        ### 🌐 Connect With Me
        """)
        
        # Social media links (replace with your actual links)
        st.markdown("""
        - 🐙 **GitHub**: [Pruthvirajsinh-Zala](https://github.com/Pruthvirajsinh-Zala)
        - 💼 **LinkedIn**: [Pruthvirajsinh Zala](https://linkedin.com/in/pruthvirajsinh-zala)
        - 📧 **Email**: prithvirajsinhzala99@gmail.com
        """)
        
        st.markdown("""
        ### 💡 Project Feedback
        
        - **Found a bug?** Report it on GitHub Issues
        - **Have suggestions?** I'd love to hear your ideas!
        - **Want to contribute?** Check out the contribution guidelines
        - **Need help?** Feel free to reach out directly
        """)
    
    with col2:
        st.markdown("### � Project Information")
        
        st.markdown("""
        This AI Chatbot is built with modern technologies and designed for 
        seamless interaction. It features advanced file processing capabilities 
        and intelligent conversation management.
        
        #### 🔧 Technologies Used
        - **AI Model**: Google Gemini 2.0 Flash
        - **Framework**: Streamlit
        - **File Processing**: Multiple format support
        - **Interface**: Responsive web design
        """)
        
        st.markdown("### 📊 Project Stats")
        with st.container():
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("AI Model", "🤖 Gemini 2.0", "Latest")
                st.metric("File Types", "� 8+", "Supported")
            with col_stat2:
                st.metric("Version", "🔄 3.0", "Current")
                st.metric("Performance", "⚡ Real-time", "Optimized")

# Main app logic - render the appropriate page
if st.session_state.current_page == "Home":
    render_home_page()
elif st.session_state.current_page == "Chatbot":
    render_chatbot_page()
elif st.session_state.current_page == "About":
    render_about_page()
elif st.session_state.current_page == "Contact":
    render_contact_page()

# Footer with license information (exclude from chatbot page)
if st.session_state.current_page != "Chatbot":
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.8em; margin-top: 50px;'>
        <p><strong>AI Chatbot Hub v3.0</strong></p>
        <p>© 2025 Pruthvirajsinh-Zala. Licensed under the <a href='https://opensource.org/licenses/MIT' target='_blank'>MIT License</a>.</p>
        <p>Built with ❤️ using Streamlit and Google Gemini 2.0 Flash</p>
    </div>
    """, unsafe_allow_html=True)
