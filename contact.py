import streamlit as st

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
