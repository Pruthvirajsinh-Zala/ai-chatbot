import streamlit as st
from home import render_home_page
from chatbot import render_chatbot_page
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
