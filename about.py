import streamlit as st

# Function to render About page
def render_about_page():
    st.title("ℹ️ About This App")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 What is AI Chatbot Hub?
        
        AI Chatbot Hub is an intelligent conversational AI application built with **Streamlit** and powered by 
        **Google's Gemini 3 Pro** model. It provides users with a seamless chat experience featuring 
        real-time streaming responses and an intuitive web interface.
        
        ## 🚀 Key Features
        
        - **🤖 Advanced AI**: Powered by Google Gemini 3 Pro
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
        - **AI Model**: Google Gemini 3 Pro with Vision
        - **File Processing**: PyPDF2, python-docx, pandas, Pillow
        - **Language**: Python 3.8+
        - **Deployment**: Streamlit Cloud / Local hosting
        
        ## 📊 Model Capabilities
        
        The Gemini 3 Pro model can help with:
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
        st.info("🤖 **AI Model**: Gemini 3 Pro")
        
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