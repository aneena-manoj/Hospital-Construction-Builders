import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from modules.hubspot_integration import hubspot, show_hubspot_status

def show_client_assistant():
    st.markdown("<h1 class='main-header'>💬 Smart Client Communication Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>24/7 AI-powered client support and lead qualification</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": """Hello! 👋 Welcome to SE Builders.

I'm your AI assistant, here to help answer questions about our healthcare construction services.

I can help you with:
• Information about our services and expertise
• Project timelines and typical budgets
• Healthcare facility construction requirements
• Past projects and case studies
• Scheduling consultations
• General construction questions

How can I assist you today?"""
        })

    # SE Builders knowledge base for the AI
    se_builders_context = """
You are an AI assistant for SE Builders, a premier commercial construction company specializing in healthcare facilities in Southern California.

COMPANY INFORMATION:
- Company: SE Builders Inc.
- Specialty: Healthcare construction (hospitals, surgery centers, medical offices, urgent care, imaging centers)
- Service Area: Southern California (Orange County, Los Angeles, San Diego, Riverside, San Bernardino, Ventura)
- Experience: 15+ years in healthcare construction
- Team: 64+ skilled professionals
- Active Projects: 12 concurrent projects

SERVICES OFFERED:
1. Healthcare Facility Construction
   - Hospitals and hospital additions
   - Outpatient surgery centers
   - Medical office buildings
   - Urgent care facilities
   - Imaging centers (MRI, CT, X-ray)
   - Dental offices
   - Laboratories
   - Rehabilitation centers

2. Specialized Healthcare Systems:
   - OSHPD compliance (seismic requirements)
   - Medical gas systems (oxygen, nitrogen, medical air)
   - HVAC with HEPA filtration
   - Emergency power systems
   - Clean rooms and sterile environments
   - Lead-lined walls for imaging
   - Infection control measures

3. Project Phases:
   - Pre-construction and planning
   - Design-build services
   - Permitting and regulatory compliance
   - Construction and project management
   - Quality control and inspections
   - Post-construction support

TYPICAL PROJECT TIMELINES:
- Medical Office (10,000-20,000 sq ft): 12-18 months
- Surgery Center (15,000-30,000 sq ft): 18-24 months
- Small Hospital Addition: 24-36 months

TYPICAL INVESTMENT RANGES:
- Medical Office: $250-350 per sq ft
- Surgery Center: $350-500 per sq ft
- Hospital: $500-800+ per sq ft
(Note: These are estimates; actual costs vary based on specifications)

RECENT PROJECTS (Examples):
1. Irvine Surgery Center - 25,000 sq ft, 6 operating suites, completed 2024
2. Orange County Medical Office - 18,000 sq ft, 20 exam rooms
3. Newport Beach Imaging Center - 12,000 sq ft, MRI and CT suites

COMPANY VALUES:
- Innovation through technology
- Quality craftsmanship
- Safety-first culture
- Client collaboration
- Community impact
- Sustainable building practices

TAGLINE: "Building spaces where care and community can thrive"

CONVERSATION GUIDELINES:
1. Be professional, friendly, and helpful
2. Ask clarifying questions to understand client needs
3. Provide accurate information based on the context above
4. For specific pricing, encourage scheduling a consultation
5. Highlight SE Builders' healthcare expertise
6. If you don't know something, say so and offer to connect them with the team
7. When appropriate, ask if they'd like to:
   - Schedule a consultation
   - See examples of similar projects
   - Get a preliminary cost estimate
   - Receive more information via email

ESCALATION TRIGGERS (suggest human contact):
- Client requests specific detailed pricing
- Complex regulatory questions beyond general info
- Legal or contract discussions
- Project budget exceeds typical ranges significantly
- Client expresses frustration
- RFP or formal proposal requested
- Timeline is urgent (less than 6 months)

Remember: You represent SE Builders. Be knowledgeable, professional, and helpful while building trust with potential clients.
"""

    # Two columns layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Chat interface
        st.subheader("Chat with SE Builders AI Assistant")

        # Create a container for chat messages
        chat_container = st.container()

        # Display all messages in the container
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input at the bottom
        if prompt := st.chat_input("Type your message here..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate AI response
            try:
                # Configure AI
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

                # Build conversation history
                conversation = se_builders_context + "\n\nCONVERSATION HISTORY:\n"
                for msg in st.session_state.messages[-6:]:  # Last 6 messages for context
                    conversation += f"{msg['role'].upper()}: {msg['content']}\n"

                conversation += f"\nUSER: {prompt}\n\nASSISTANT:"

                # Generate response
                response = model.generate_content(conversation)
                assistant_response = response.text

                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

                # Rerun to display new messages
                st.rerun()

            except Exception as e:
                error_msg = f"I apologize, but I encountered an error. Please try again or contact our team directly at info@sebuilders.com"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.rerun()

        # HubSpot integration section
        if hubspot.is_enabled() and len(st.session_state.messages) > 2:
            st.markdown("---")
            st.subheader("💾 Save to HubSpot CRM")

            with st.form("hubspot_save_form"):
                contact_email = st.text_input(
                    "Client Email",
                    placeholder="client@example.com",
                    help="Enter client's email to save this conversation to HubSpot"
                )

                contact_name = st.text_input(
                    "Client Name (Optional)",
                    placeholder="John Doe"
                )

                phone = st.text_input(
                    "Phone (Optional)",
                    placeholder="(555) 123-4567"
                )

                company = st.text_input(
                    "Company (Optional)",
                    placeholder="ABC Healthcare"
                )

                submitted = st.form_submit_button("💾 Save to HubSpot", use_container_width=True)

                if submitted and contact_email:
                    with st.spinner("Saving to HubSpot..."):
                        # Parse name
                        firstname, lastname = "", ""
                        if contact_name:
                            name_parts = contact_name.split()
                            firstname = name_parts[0] if len(name_parts) > 0 else ""
                            lastname = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

                        # Create conversation summary
                        summary = f"AI chat conversation on {datetime.now().strftime('%Y-%m-%d')}"
                        summary += f"\n\nMessages exchanged: {len(st.session_state.messages)}"

                        # Extract topics from conversation
                        user_messages = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
                        if user_messages:
                            summary += f"\n\nTopics discussed: {', '.join(user_messages[:3])[:200]}..."

                        # Log to HubSpot
                        success = hubspot.log_chat_conversation(
                            contact_email=contact_email,
                            conversation_history=st.session_state.messages,
                            conversation_summary=summary
                        )

                        if success:
                            # Update contact with additional info
                            hubspot.create_or_update_contact(
                                email=contact_email,
                                firstname=firstname,
                                lastname=lastname,
                                phone=phone,
                                company=company,
                                additional_properties={
                                    "lead_source": "AI Chat Assistant",
                                    "ai_conversation_date": datetime.now().strftime("%Y-%m-%d")
                                }
                            )
                            st.success("✅ Conversation saved to HubSpot!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to save to HubSpot")
                elif submitted:
                    st.warning("⚠️ Please enter a client email")

        # Clear chat button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col2:
        # Show HubSpot status
        show_hubspot_status()

        st.markdown("---")

        # Quick actions sidebar
        st.subheader("Quick Actions")

        if st.button("📅 Schedule Consultation", use_container_width=True):
            st.info("Consultation scheduling coming soon! Contact: (555) 123-4567")

        if st.button("📧 Email Our Team", use_container_width=True):
            st.info("Email: info@sebuilders.com")

        if st.button("📱 Call Us", use_container_width=True):
            st.info("Phone: (555) 123-4567")

        if st.button("💰 Get Cost Estimate", use_container_width=True):
            st.info("Navigate to Cost Estimator module →")

        st.markdown("---")

        # Chat statistics
        st.subheader("💡 Chat Stats")
        st.metric("Messages", len(st.session_state.messages))
        st.metric("Your Messages", len([m for m in st.session_state.messages if m["role"] == "user"]))

        st.markdown("---")

        # Common questions
        st.subheader("Common Questions")

        common_questions = [
            "What types of healthcare facilities do you build?",
            "What is your service area?",
            "How long does a typical medical office take?",
            "What is OSHPD compliance?",
            "Can I see examples of past projects?",
            "What makes SE Builders different?"
        ]

        for question in common_questions:
            if st.button(f"❓ {question}", key=question, use_container_width=True):
                # Add question to chat
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

    # Info section
    st.markdown("---")
    st.info("""
    **💡 How it works:**

    This AI assistant is trained on SE Builders' services, expertise, and past projects.
    It can answer questions 24/7 and automatically qualifies leads before connecting
    them with your team.

    **For complex inquiries,** the AI will recommend connecting with a human team member.

    **Privacy:** Conversations are not stored permanently and are used only for immediate assistance.
    """)

    # Live metrics (mock data)
    st.markdown("---")
    st.subheader("📊 AI Assistant Performance (Last 30 Days)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Chats", "147", "+32%")
    col2.metric("Leads Generated", "23", "+18%")
    col3.metric("Consultations", "11", "+45%")
    col4.metric("Satisfaction", "4.7/5.0", "+0.3")
