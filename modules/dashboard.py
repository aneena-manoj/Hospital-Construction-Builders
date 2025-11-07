import streamlit as st
from datetime import datetime, timedelta
import random

def show_dashboard():
    st.markdown("<h1 class='main-header'>SE Builders AI Platform</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Welcome to your intelligent construction management system</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3>🏗️ Active Projects</h3>
            <h1>12</h1>
            <p>+2 from last month</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3>👷 Team Members</h3>
            <h1>64</h1>
            <p>Across all sites</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3>💰 Estimates</h3>
            <h1>23</h1>
            <p>Generated this month</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='metric-card'>
            <h3>🛡️ Safety Score</h3>
            <h1>94/100</h1>
            <p>↑ 6% improvement</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Actions
    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💰 Generate Estimate", use_container_width=True):
            st.switch_page = "Cost Estimator"

    with col2:
        if st.button("📱 Create Post", use_container_width=True):
            st.switch_page = "Social Media"

    with col3:
        if st.button("🛡️ Safety Scan", use_container_width=True):
            st.switch_page = "Safety Scanner"

    with col4:
        if st.button("💬 Chat Assist", use_container_width=True):
            st.switch_page = "Client Assistant"

    st.markdown("---")

    # Recent Activity
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 Recent Activity")

        activities = [
            {"icon": "💰", "text": "New estimate: Riverside Medical Office ($3.2M)", "time": "2 hours ago"},
            {"icon": "🛡️", "text": "Safety scan: 2 moderate hazards detected", "time": "4 hours ago"},
            {"icon": "📱", "text": "Social post scheduled: Instagram (Jan 16, 10am)", "time": "5 hours ago"},
            {"icon": "💬", "text": "Client inquiry: Dr. Martinez (consultation)", "time": "6 hours ago"},
            {"icon": "✅", "text": "Project complete: Irvine Surgery Center", "time": "Yesterday"},
            {"icon": "📊", "text": "Monthly report generated", "time": "2 days ago"},
        ]

        for activity in activities:
            st.markdown(f"""
            <div style='background-color: #f8fafc; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 3px solid #f97316;'>
                <span style='font-size: 1.2rem;'>{activity['icon']}</span>
                <strong>{activity['text']}</strong>
                <br><small style='color: #64748b;'>{activity['time']}</small>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.subheader("🔔 Alerts & Notifications")

        st.error("🔴 **Critical safety hazard**\nCosta Mesa project - Immediate action required")
        st.warning("🟡 **Client waiting**\nDr. Chen inquiry - 2 hours pending")
        st.success("🟢 **Estimate approved**\nNewport Beach Surgery Center")
        st.info("ℹ️ **New lead**\nOrange County Medical Group")

    st.markdown("---")

    # AI Platform Performance
    st.subheader("📊 AI Platform Performance - This Month")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cost Estimator", "23 estimates", "+44%")
        st.caption("Avg time: 8.4 minutes")

    with col2:
        st.metric("Social Media", "47 posts", "+67%")
        st.caption("18 hours saved")

    with col3:
        st.metric("Client AI", "147 chats", "+32%")
        st.caption("23 leads generated")

    with col4:
        st.metric("Safety Scanner", "12 scans", "+15%")
        st.caption("96% resolution rate")
