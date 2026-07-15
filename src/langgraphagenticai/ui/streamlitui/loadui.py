import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config

CUSTOM_CSS = """
<style>
    /* ---- App background & typography ---- */
    .stApp {
        background: linear-gradient(180deg, #0F1117 0%, #14172352 100%);
    }

    /* ---- Header banner ---- */
    .app-header {
        padding: 1.1rem 1.4rem;
        border-radius: 14px;
        background: linear-gradient(120deg, #8B5CF6 0%, #6366F1 55%, #4F46E5 100%);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
        margin-bottom: 1.4rem;
    }
    .app-header h1 {
        color: #FFFFFF !important;
        font-size: 1.6rem;
        margin: 0;
        font-weight: 700;
    }
    .app-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.2rem 0 0 0;
        font-size: 0.92rem;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: #151823;
        border-right: 1px solid rgba(139, 92, 246, 0.18);
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #C4B5FD !important;
    }

    /* ---- Buttons ---- */
    .stButton>button {
        background: linear-gradient(120deg, #8B5CF6, #6366F1);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.45);
        color: white;
    }

    /* ---- Chat bubbles ---- */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.4rem 0.2rem;
        margin-bottom: 0.4rem;
    }

    /* ---- Inputs ---- */
    .stTextInput>div>div>input, .stSelectbox>div>div {
        border-radius: 8px !important;
    }
</style>
"""


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        page_title = self.config.get_page_title()
        st.set_page_config(page_title="🔮 " + page_title, page_icon="🔮", layout="wide")

        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="app-header">
                <h1>🔮 {page_title}</h1>
                <p>Multi-agent workflows powered by LangGraph — chat, browse the web, or get an AI news digest.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.IsFetchButtonClicked = False
        st.session_state.timeframe = ""

        with st.sidebar:
            st.markdown("### ⚙️ Configuration")
            st.caption("Set up your model and pick a use case to get started.")
            st.divider()

            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            st.markdown("#### 🧠 LLM")
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                groq_model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Groq Model", groq_model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your Groq API Key to proceed. Don't have one? Get it from https://platform.groq.ai/signup", icon="🔑")

            st.divider()
            st.markdown("#### 🧩 Use Case")
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase", usecase_options)

            if self.user_controls["selected_usecase"] == 'Chatbot with Web' or self.user_controls["selected_usecase"] == 'AI News':
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key", type="password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your Tavily API Key to proceed. Don't have one? Get it from https://tavily.com/", icon="🔑")

            if self.user_controls["selected_usecase"] == 'AI News':
                st.divider()
                st.markdown("#### 📰 AI News Options")

                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select time frame",
                        ["daily", "weekly", "monthly"],
                        index=0
                    )
                    topic = st.selectbox(
                        "🗂️ Select Topic",
                        ["all", "healthcare", "finance", "technology", "education", "entertainment", "politics", "environment", "business"],
                        index=0
                    )

                if st.button("🚀 Fetch AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame
                    st.session_state.topic = topic

        return self.user_controls
