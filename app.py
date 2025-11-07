import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SE Builders AI Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for SE Builders branding
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #f97316;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f9ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #f97316;
    }
    .stButton>button {
        background-color: #f97316;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ea580c;
    }
    </style>
""", unsafe_allow_html=True)

# Check for API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found in .env file. Please add it to continue.")
    st.stop()

# Sidebar navigation
with st.sidebar:
    st.markdown("# 🏗️ SE Builders")
    st.markdown("### AI Platform")
    st.markdown("---")

    page = st.radio(
        "Navigate to:",
        ["🏠 Dashboard", "💰 Cost Estimator", "📱 Social Media", "💬 Client Assistant", "🛡️ Safety Scanner", "📊 HubSpot CRM"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Active Projects", "12")
    st.metric("This Month Estimates", "23")
    st.metric("Safety Score", "94/100")

    st.markdown("---")
    st.markdown("**AI Platform v1.0**")
    st.markdown("*Building smarter, together*")

# Main content area
if page == "🏠 Dashboard":
    from modules.dashboard import show_dashboard
    show_dashboard()

elif page == "💰 Cost Estimator":
    from modules.cost_estimator import show_cost_estimator
    show_cost_estimator()

elif page == "📱 Social Media":
    from modules.social_media import show_social_media
    show_social_media()

elif page == "💬 Client Assistant":
    from modules.client_assistant import show_client_assistant
    show_client_assistant()

elif page == "🛡️ Safety Scanner":
    from modules.safety_scanner import show_safety_scanner
    show_safety_scanner()

elif page == "📊 HubSpot CRM":
    from modules.hubspot_manager import show_hubspot_manager
    show_hubspot_manager()
