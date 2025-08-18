import streamlit as st

def render_home_page():
    st.title("🏠 Welcome to AI Chatbot Hub")
    st.caption("🎉 **Version 3.0** - Now with Advanced File Support & AI Vision!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("assets/ai_chatbot.png", 
                    caption="Your AI Assistant Powered by Google Gemini")
        except:
            # If image doesn't exist, show a placeholder
            st.markdown("""
            <div style='text-align: center; padding: 50px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;'>
                <h2>🤖 AI Chatbot Hub</h2>
                <p>Your Intelligent Assistant</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Version 3.0 Highlights
    st.markdown("## ✨ What's New in Version 3.0")
    
    # Create tabs for different feature categories
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 New Features", "📁 File Support", "🎨 UI/UX", "🔧 Technical"])
    
    with tab1:
        st.markdown("""
        ### 🎯 Major New Features
        - **📁 Multi-Format File Upload**: Support for 8+ file types
        - **🖼️ AI-Powered Image Analysis**: Advanced computer vision with Gemini
        - **📊 Data Intelligence**: Smart insights from spreadsheets and CSV files
        - **📄 Document Processing**: Extract and analyze PDF, Word documents
        - **💬 Contextual Conversations**: Chat about your uploaded files
        - **📈 Progress Tracking**: Real-time file processing indicators
        """)
    
    with tab2:
        st.markdown("""
        ### 📁 Supported File Types
        
        | File Type | Extension | AI Capabilities |
        |-----------|-----------|----------------|
        | 📄 Text Files | `.txt` | Content analysis, summarization |
        | 📄 PDF Documents | `.pdf` | Text extraction, Q&A |
        | 📄 Word Documents | `.docx` | Content review, insights |
        | 📊 Excel Files | `.xlsx, .xls` | Data analysis, statistics |
        | 📊 CSV Files | `.csv` | Pattern recognition, trends |
        | 🔧 JSON Files | `.json` | Structure analysis, validation |
        | 🖼️ Images | `.jpg, .png, .gif` | Visual understanding, description |
        """)
    
    with tab3:
        st.markdown("""
        ### 🎨 Enhanced User Experience
        - **📱 Responsive Design**: Perfect on all devices
        - **⚡ Smooth Animations**: Enhanced loading states
        - **📊 File Previews**: Smart content previews
        - **🔍 Progress Indicators**: Visual processing feedback
        - **💫 Interactive Elements**: Improved buttons and controls
        - **🎯 Contextual Help**: Better user guidance
        """)
    
    with tab4:
        st.markdown("""
        ### 🔧 Technical Improvements
        - **🧠 Gemini 2.0 Flash**: Latest AI model integration
        - **🔍 Computer Vision**: Advanced image processing
        - **📊 Data Processing**: Pandas integration for analytics
        - **🛡️ Error Handling**: Robust error management
        - **⚡ Performance**: Optimized file processing
        - **🔐 Security**: Enhanced data protection
        """)
    
    st.markdown("---")
    
    # Feature cards
    st.markdown("## 🎯 Core Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 Smart AI Assistant
        Powered by Google's latest Gemini 2.0 Flash model for intelligent conversations and file analysis.
        """)
        
    with col2:
        st.markdown("""
        ### ⚡ Real-time Streaming
        Experience smooth, real-time responses with advanced streaming capabilities and file processing.
        """)
        
    with col3:
        st.markdown("""
        ### 🔒 Secure & Private
        Your conversations and files are processed securely with Google's enterprise-grade security.
        """)
    
    st.markdown("---")
    
    # Getting started section
    st.markdown("## 🚀 Getting Started")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💬 Basic Chat
        1. **Click on the Chatbot tab** in the sidebar
        2. **Ask any question** - the AI can help with various topics
        3. **Enjoy real-time responses** with streaming text generation
        4. **Clear chat history** anytime using sidebar controls
        """)
    
    with col2:
        st.markdown("""
        ### 📁 File Analysis
        1. **Navigate to the Chatbot page**
        2. **Upload your files** using the file uploader
        3. **Review file previews** to ensure correct processing
        4. **Ask questions** about your files or any topic
        5. **Get AI insights** based on your uploaded content
        """)
    
    # Version history dropdown
    st.markdown("## 📈 Version History")
    
    with st.expander("🎉 **Version 3.0** - Advanced File Support & AI Vision (Current)", expanded=True):
        st.markdown("""
        **🗓️ Released:** August 2025
        
        **🚀 Major Features:**
        - ✅ Multi-format file upload (8+ file types)
        - ✅ AI-powered image analysis with Gemini Vision
        - ✅ Smart document processing (PDF, Word, Excel)
        - ✅ Real-time file processing with progress indicators
        - ✅ Contextual conversations about uploaded files
        - ✅ Enhanced UI/UX with tabbed interfaces
        - ✅ Robust error handling for all file types
        - ✅ Mobile-optimized file upload interface
        """)
    
    with st.expander("📱 Version 2.0 - Multi-Page Navigation"):
        st.markdown("""
        **🗓️ Released:** August 2025
        
        **📋 Features:**
        - ✅ Multi-page navigation system
        - ✅ Improved error handling
        - ✅ Real-time chat statistics
        - ✅ Enhanced UI/UX design
        - ✅ Better mobile responsiveness
        - ✅ Sidebar navigation controls
        """)
    
    with st.expander("🎯 Version 1.0 - Core Chatbot"):
        st.markdown("""
        **🗓️ Released:** August 2025
        
        **🔧 Features:**
        - ✅ Basic Gemini AI integration
        - ✅ Real-time streaming responses
        - ✅ Simple chat interface
        - ✅ Error handling and API management
        - ✅ Basic session state management
        """)

    st.markdown("---")
    
    # App Statistics
    st.markdown("## 📊 App Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🤖 AI Model",
            value="Gemini 2.0",
            delta="Flash"
        )
    
    with col2:
        st.metric(
            label="📁 File Types",
            value="8+",
            delta="Supported"
        )
    
    with col3:
        st.metric(
            label="🎯 Version",
            value="3.0",
            delta="Latest"
        )
    
    with col4:
        st.metric(
            label="⚡ Performance",
            value="Real-time",
            delta="Streaming"
        )
    
    st.markdown("---")
    st.markdown("### 🎊 Ready to explore? Click on **💬 Chatbot** in the sidebar to get started!")
