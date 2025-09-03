import streamlit as st
from home import render_home_page
from chatbot import render_chatbot_page
from about import render_about_page
from contact import render_contact_page


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
