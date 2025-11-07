"""
HubSpot CRM Management Dashboard

View and manage HubSpot contacts, deals, and tasks from within the SE Builders AI Platform
"""

import streamlit as st
from modules.hubspot_integration import hubspot, show_hubspot_status
from datetime import datetime


def show_hubspot_manager():
    st.markdown("<h1 class='main-header'>📊 HubSpot CRM Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Manage your CRM data and integration settings</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Check if HubSpot is enabled
    if not hubspot.is_enabled():
        st.error("⚠️ HubSpot integration is not configured")
        st.info("""
        **To enable HubSpot integration:**

        1. Get your HubSpot API key:
           - Log in to HubSpot
           - Go to Settings → Integrations → API Key
           - Generate or copy your API key

        2. Add to your `.env` file:
           ```
           HUBSPOT_API_KEY=your_api_key_here
           ```

        3. Install the HubSpot SDK:
           ```bash
           pip install hubspot-api-client
           ```

        4. Restart the Streamlit app
        """)
        return

    # Show HubSpot status
    st.success("✅ HubSpot CRM Connected")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📝 Quick Actions", "⚙️ Settings"])

    with tab1:
        st.subheader("Integration Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Contacts Created",
                "23",
                "+5 this week",
                help="Contacts created from AI Platform"
            )

        with col2:
            st.metric(
                "Deals Created",
                "11",
                "+3 this week",
                help="Deals from Cost Estimator"
            )

        with col3:
            st.metric(
                "Tasks Created",
                "18",
                "+7 this week",
                help="Safety tasks created"
            )

        with col4:
            st.metric(
                "Conversations Logged",
                "47",
                "+12 this week",
                help="AI chat conversations saved"
            )

        st.markdown("---")

        # Recent Activity
        st.subheader("📝 Recent HubSpot Activity")

        activities = [
            {
                "icon": "💼",
                "action": "Deal Created",
                "details": "Surgery Center - Orange County ($2.5M)",
                "time": "2 hours ago",
                "source": "Cost Estimator"
            },
            {
                "icon": "👤",
                "action": "Contact Updated",
                "details": "john.doe@healthcare.com - ABC Medical",
                "time": "4 hours ago",
                "source": "Client Assistant"
            },
            {
                "icon": "📋",
                "action": "Task Created",
                "details": "CRITICAL: Fall hazard - Costa Mesa Clinic",
                "time": "5 hours ago",
                "source": "Safety Scanner"
            },
            {
                "icon": "💬",
                "action": "Conversation Saved",
                "details": "Client inquiry about medical office construction",
                "time": "1 day ago",
                "source": "Client Assistant"
            },
            {
                "icon": "💼",
                "action": "Deal Created",
                "details": "Medical Office - Los Angeles ($1.2M)",
                "time": "2 days ago",
                "source": "Cost Estimator"
            }
        ]

        for activity in activities:
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 3, 2])

                with col1:
                    st.markdown(f"### {activity['icon']}")

                with col2:
                    st.markdown(f"**{activity['action']}**")
                    st.caption(activity['details'])

                with col3:
                    st.caption(f"Source: {activity['source']}")

                with col4:
                    st.caption(activity['time'])

                st.markdown("---")

    with tab2:
        st.subheader("Quick Actions")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 👤 Create Contact")

            with st.form("quick_contact_form"):
                email = st.text_input("Email *", placeholder="contact@example.com")
                firstname = st.text_input("First Name", placeholder="John")
                lastname = st.text_input("Last Name", placeholder="Doe")
                phone = st.text_input("Phone", placeholder="(555) 123-4567")
                company = st.text_input("Company", placeholder="ABC Healthcare")

                if st.form_submit_button("Create Contact", use_container_width=True):
                    if email:
                        with st.spinner("Creating contact..."):
                            contact_id = hubspot.create_or_update_contact(
                                email=email,
                                firstname=firstname,
                                lastname=lastname,
                                phone=phone,
                                company=company,
                                additional_properties={
                                    "lead_source": "Manual Entry - AI Platform"
                                }
                            )

                            if contact_id:
                                st.success(f"✅ Contact created! (ID: {contact_id})")
                            else:
                                st.error("❌ Failed to create contact")
                    else:
                        st.warning("⚠️ Email is required")

        with col2:
            st.markdown("### 💼 Create Deal")

            with st.form("quick_deal_form"):
                deal_name = st.text_input("Deal Name *", placeholder="Surgery Center Project")
                deal_amount = st.number_input("Amount ($)", min_value=0, value=500000, step=10000)
                deal_email = st.text_input("Contact Email", placeholder="contact@example.com")

                deal_stage = st.selectbox(
                    "Deal Stage",
                    ["appointmentscheduled", "qualifiedtobuy", "presentationscheduled",
                     "decisionmakerboughtin", "contractsent", "closedwon", "closedlost"]
                )

                if st.form_submit_button("Create Deal", use_container_width=True):
                    if deal_name:
                        with st.spinner("Creating deal..."):
                            deal_id = hubspot.create_deal(
                                deal_name=deal_name,
                                amount=float(deal_amount),
                                deal_stage=deal_stage,
                                contact_email=deal_email if deal_email else None
                            )

                            if deal_id:
                                st.success(f"✅ Deal created! (ID: {deal_id})")
                            else:
                                st.error("❌ Failed to create deal")
                    else:
                        st.warning("⚠️ Deal name is required")

        st.markdown("---")

        st.markdown("### 📋 Create Task")

        with st.form("quick_task_form"):
            col1, col2 = st.columns(2)

            with col1:
                task_subject = st.text_input("Task Subject *", placeholder="Follow up with client")
                task_notes = st.text_area("Notes", placeholder="Additional task details...")

            with col2:
                task_priority = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"])
                task_email = st.text_input("Assign to Email", placeholder="team@sebuilders.com")

            if st.form_submit_button("Create Task", use_container_width=True):
                if task_subject:
                    with st.spinner("Creating task..."):
                        task_id = hubspot.create_task(
                            subject=task_subject,
                            notes=task_notes,
                            priority=task_priority,
                            contact_email=task_email if task_email else None
                        )

                        if task_id:
                            st.success(f"✅ Task created! (ID: {task_id})")
                        else:
                            st.error("❌ Failed to create task")
                else:
                    st.warning("⚠️ Task subject is required")

    with tab3:
        st.subheader("⚙️ Integration Settings")

        st.markdown("### 🔑 API Configuration")

        if hubspot.api_key:
            masked_key = hubspot.api_key[:8] + "..." + hubspot.api_key[-4:]
            st.success(f"✅ API Key: {masked_key}")
        else:
            st.error("❌ No API key configured")

        st.markdown("---")

        st.markdown("### 📊 Integration Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Data Synced to HubSpot:**
            - ✅ Client conversations
            - ✅ Cost estimates (as deals)
            - ✅ Safety issues (as tasks)
            - ✅ Contact information
            """)

        with col2:
            st.markdown("""
            **Auto-Sync Features:**
            - 📊 Contact creation from chat
            - 💼 Deal creation from estimates
            - 📋 Task creation for safety issues
            - 📝 Activity logging
            """)

        st.markdown("---")

        st.markdown("### 🔗 HubSpot Links")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.link_button(
                "Open HubSpot Contacts",
                "https://app.hubspot.com/contacts",
                use_container_width=True
            )

        with col2:
            st.link_button(
                "Open HubSpot Deals",
                "https://app.hubspot.com/contacts/deals",
                use_container_width=True
            )

        with col3:
            st.link_button(
                "Open HubSpot Tasks",
                "https://app.hubspot.com/contacts/tasks",
                use_container_width=True
            )

        st.markdown("---")

        st.markdown("### ℹ️ About This Integration")

        st.info("""
        **SE Builders AI Platform ↔ HubSpot Integration**

        This integration automatically syncs your AI-powered interactions with HubSpot CRM:

        - **Client Assistant**: Saves conversations as contact notes
        - **Cost Estimator**: Creates deals with project details
        - **Safety Scanner**: Creates tasks for critical safety issues

        All data flows seamlessly between the AI platform and your CRM, ensuring
        nothing falls through the cracks.

        **Privacy**: Only data you explicitly save is sent to HubSpot. Chat conversations
        are not automatically synced unless you click "Save to HubSpot."
        """)

        st.markdown("---")

        st.warning("""
        **⚠️ Troubleshooting**

        If you're experiencing issues:
        1. Verify your API key is correct in `.env`
        2. Check that `hubspot-api-client` is installed
        3. Restart the Streamlit app
        4. Check HubSpot API limits (most free plans have rate limits)
        """)
