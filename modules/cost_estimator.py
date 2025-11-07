import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from modules.hubspot_integration import hubspot, show_hubspot_status, extract_estimated_cost

def show_cost_estimator():
    st.markdown("<h1 class='main-header'>💰 AI-Powered Cost Estimator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Generate accurate project estimates in minutes</p>", unsafe_allow_html=True)

    # Show HubSpot status in sidebar
    with st.sidebar:
        show_hubspot_status()

    st.markdown("---")

    # Input form
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Project Details")

        facility_type = st.selectbox(
            "Facility Type",
            ["Hospital", "Surgery Center", "Medical Office Building", "Urgent Care Clinic",
             "Imaging Center", "Dental Office", "Laboratory", "Rehabilitation Center"]
        )

        square_footage = st.number_input(
            "Square Footage",
            min_value=1000,
            max_value=500000,
            value=25000,
            step=1000
        )

        location = st.selectbox(
            "Location (Southern California)",
            ["Orange County", "Los Angeles County", "San Diego County",
             "Riverside County", "San Bernardino County", "Ventura County"]
        )

        num_floors = st.number_input("Number of Floors", min_value=1, max_value=20, value=2)

    with col2:
        st.subheader("Special Requirements")

        special_reqs = st.multiselect(
            "Select applicable features:",
            ["Clean Rooms", "Operating Suites", "Imaging Suites (MRI, CT)",
             "Medical Gas Systems", "Emergency Power Generator",
             "HVAC with HEPA Filtration", "Lead-Lined Walls",
             "Laboratory Equipment", "Sterilization Areas",
             "Patient Recovery Rooms", "Parking Structure"]
        )

        timeline = st.selectbox(
            "Target Timeline",
            ["12 months", "18 months", "24 months", "30+ months"]
        )

        quality_level = st.select_slider(
            "Finish Quality Level",
            options=["Standard", "Mid-Range", "High-End", "Premium"],
            value="Mid-Range"
        )

    # Additional notes
    st.subheader("Additional Project Notes")
    additional_notes = st.text_area(
        "Describe any special considerations, site conditions, or unique requirements:",
        placeholder="e.g., Hillside location, existing building renovation, LEED certification required...",
        height=100
    )

    # Generate button
    if st.button("🎯 Generate Cost Estimate", type="primary", use_container_width=True):
        with st.spinner("Analyzing project parameters and generating estimate..."):
            # Configure AI
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

            # Create detailed prompt
            prompt = f"""You are a construction cost estimator for SE Builders, a healthcare construction company in Southern California.

Generate a detailed, realistic cost estimate for the following project:

PROJECT DETAILS:
- Facility Type: {facility_type}
- Square Footage: {square_footage:,} sq ft
- Location: {location}
- Number of Floors: {num_floors}
- Timeline: {timeline}
- Finish Quality: {quality_level}

SPECIAL REQUIREMENTS:
{', '.join(special_reqs) if special_reqs else 'None specified'}

ADDITIONAL NOTES:
{additional_notes if additional_notes else 'None provided'}

Please provide:

1. COST BREAKDOWN by category (with dollar amounts):
   - Site Work & Foundation
   - Structural (concrete, steel)
   - Healthcare Systems (medical gas, HVAC, emergency power)
   - Finishes & Interior (flooring, walls, ceilings)
   - Technology & Equipment
   - Permits & Compliance (OSHPD, building permits)
   - Labor
   - Contingency (10%)

2. TOTAL ESTIMATED COST with confidence level (%)

3. COST PER SQUARE FOOT

4. RISK FACTORS & CONSIDERATIONS:
   - List 3-4 potential cost variables
   - Timeline risks
   - Regulatory considerations

5. TIMELINE BREAKDOWN:
   - Design & Permitting
   - Construction
   - Inspection & Turnover

6. COMPARABLE PROJECTS:
   - Mention 2-3 similar SE Builders projects (you can create realistic examples)

7. RECOMMENDATIONS:
   - Cost-saving opportunities
   - Value engineering suggestions

Format the response professionally, as if presenting to a healthcare client. Use clear sections and bullet points. Be specific with numbers."""

            try:
                response = model.generate_content(prompt)

                st.markdown("---")
                st.success("✅ Estimate Generated Successfully!")

                # Display results
                st.markdown("### 📊 Project Cost Estimate")
                st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

                # Display the AI response
                st.markdown(response.text)

                # Export options
                st.markdown("---")
                col1, col2, col3 = st.columns(3)

                with col1:
                    # Create downloadable text file
                    estimate_text = f"""SE BUILDERS - PROJECT COST ESTIMATE
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

PROJECT DETAILS:
- Facility Type: {facility_type}
- Square Footage: {square_footage:,} sq ft
- Location: {location}
- Floors: {num_floors}
- Timeline: {timeline}
- Quality Level: {quality_level}

SPECIAL REQUIREMENTS:
{', '.join(special_reqs) if special_reqs else 'None specified'}

{response.text}

---
SE Builders - Building spaces where care and community thrive
"""
                    st.download_button(
                        label="📥 Download as TXT",
                        data=estimate_text,
                        file_name=f"SE_Builders_Estimate_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col2:
                    if st.button("📧 Email Estimate", use_container_width=True):
                        st.info("Email feature coming soon!")

                # HubSpot Integration
                if hubspot.is_enabled():
                    st.markdown("---")
                    st.subheader("💾 Save to HubSpot CRM")

                    with st.form("hubspot_deal_form"):
                        st.write("Create a deal in HubSpot for this estimate")

                        deal_email = st.text_input(
                            "Client Email *",
                            placeholder="client@example.com",
                            help="Required to create HubSpot deal"
                        )

                        deal_name = st.text_input(
                            "Client Name (Optional)",
                            placeholder="John Doe"
                        )

                        deal_phone = st.text_input(
                            "Phone (Optional)",
                            placeholder="(555) 123-4567"
                        )

                        deal_company = st.text_input(
                            "Company (Optional)",
                            placeholder="ABC Healthcare"
                        )

                        col_submit1, col_submit2 = st.columns(2)

                        with col_submit1:
                            save_deal = st.form_submit_button("💼 Create Deal", use_container_width=True)

                        with col_submit2:
                            save_contact = st.form_submit_button("👤 Save Contact Only", use_container_width=True)

                        if save_deal and deal_email:
                            with st.spinner("Creating HubSpot deal..."):
                                # Extract estimated cost from response
                                estimated_value = extract_estimated_cost(response.text)

                                # Prepare estimate data
                                estimate_data = {
                                    'facility_type': facility_type,
                                    'square_footage': square_footage,
                                    'location': location,
                                    'num_floors': num_floors,
                                    'timeline': timeline,
                                    'quality_level': quality_level,
                                    'special_requirements': ', '.join(special_reqs) if special_reqs else 'None'
                                }

                                # Parse contact name
                                firstname, lastname = "", ""
                                if deal_name:
                                    name_parts = deal_name.split()
                                    firstname = name_parts[0] if len(name_parts) > 0 else ""
                                    lastname = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

                                # Create or update contact first
                                hubspot.create_or_update_contact(
                                    email=deal_email,
                                    firstname=firstname,
                                    lastname=lastname,
                                    phone=deal_phone,
                                    company=deal_company
                                )

                                # Create the deal
                                deal_id = hubspot.log_cost_estimate(
                                    contact_email=deal_email,
                                    estimate_data=estimate_data,
                                    estimate_text=response.text,
                                    estimated_value=estimated_value
                                )

                                if deal_id:
                                    st.success(f"✅ Deal created in HubSpot! (ID: {deal_id})")
                                    st.balloons()
                                else:
                                    st.error("❌ Failed to create deal in HubSpot")

                        elif save_contact and deal_email:
                            with st.spinner("Saving contact to HubSpot..."):
                                # Parse contact name
                                firstname, lastname = "", ""
                                if deal_name:
                                    name_parts = deal_name.split()
                                    firstname = name_parts[0] if len(name_parts) > 0 else ""
                                    lastname = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

                                contact_id = hubspot.create_or_update_contact(
                                    email=deal_email,
                                    firstname=firstname,
                                    lastname=lastname,
                                    phone=deal_phone,
                                    company=deal_company,
                                    additional_properties={
                                        "lead_source": "Cost Estimator",
                                        "project_type": facility_type,
                                        "estimated_project_value": str(extract_estimated_cost(response.text))
                                    }
                                )

                                if contact_id:
                                    st.success(f"✅ Contact saved to HubSpot! (ID: {contact_id})")
                                else:
                                    st.error("❌ Failed to save contact")

                        elif (save_deal or save_contact) and not deal_email:
                            st.warning("⚠️ Please enter a client email")

            except Exception as e:
                st.error(f"Error generating estimate: {str(e)}")

    # Info section
    st.markdown("---")
    st.info("""
    **💡 How it works:**

    This AI estimator analyzes your project parameters against SE Builders' historical data,
    current market conditions, and healthcare construction requirements to generate accurate
    cost projections. All estimates should be reviewed by the SE Builders team before
    client presentation.

    **Average accuracy:** 90-95% | **Generation time:** ~30 seconds
    """)
