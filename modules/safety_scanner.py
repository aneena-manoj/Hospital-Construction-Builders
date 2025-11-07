import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
from datetime import datetime
from modules.hubspot_integration import hubspot, show_hubspot_status

def show_safety_scanner():
    st.markdown("<h1 class='main-header'>🛡️ Construction Safety AI Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Identify hazards and ensure OSHA compliance with computer vision</p>", unsafe_allow_html=True)

    # Show HubSpot status in sidebar
    with st.sidebar:
        show_hubspot_status()

    st.markdown("---")

    # Two column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Site Photos")

        # Project selection
        project_name = st.selectbox(
            "Select Project",
            ["Costa Mesa Clinic", "Irvine Surgery Center", "Orange County Medical Office",
             "Newport Beach Imaging", "Riverside Hospital Addition", "Other/New Project"]
        )

        if project_name == "Other/New Project":
            project_name = st.text_input("Enter Project Name")

        # Location/area
        location = st.text_input(
            "Specific Location/Area",
            placeholder="e.g., 2nd Floor, North Wing, Room 142..."
        )

        # File uploader
        uploaded_files = st.file_uploader(
            "Upload Construction Site Photos",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Upload one or more photos from your site walk"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} photo(s) uploaded")

            # Display thumbnails
            cols = st.columns(min(len(uploaded_files), 4))
            for idx, file in enumerate(uploaded_files):
                with cols[idx % 4]:
                    image = Image.open(file)
                    st.image(image, caption=file.name, use_column_width=True)

        # Scan button
        scan_button = st.button("🔍 Scan for Safety Hazards", type="primary", use_container_width=True)

    with col2:
        st.subheader("Safety Analysis Results")

        if scan_button:
            if not uploaded_files:
                st.error("⚠️ Please upload at least one photo to scan.")
            else:
                with st.spinner("Analyzing photos for safety hazards..."):
                    try:
                        # Configure AI
                        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                        model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

                        all_hazards = []

                        # Process each image
                        for idx, file in enumerate(uploaded_files):
                            image = Image.open(file)

                            # Convert to bytes for AI
                            buf = io.BytesIO()
                            image.save(buf, format="JPEG")
                            image_part = {
                                "mime_type": "image/jpeg",
                                "data": buf.getvalue()
                            }

                            # Create safety scanning prompt
                            prompt = f"""You are a construction safety inspector analyzing a photo from a healthcare construction site.

PROJECT: {project_name}
LOCATION: {location if location else 'Not specified'}
PHOTO: {file.name}

Analyze this construction site photo for safety hazards and OSHA violations.

Look for:

1. **PPE (Personal Protective Equipment) Violations:**
   - Missing hard hats
   - No safety vests/high-visibility clothing
   - Improper footwear
   - Missing eye protection
   - No fall protection harness when needed
   - Missing gloves

2. **Fall Hazards:**
   - Unguarded edges or openings
   - Missing guardrails
   - Unsecured ladders
   - Open holes or penetrations
   - Improper scaffolding
   - Damaged platforms

3. **Electrical Hazards:**
   - Exposed wiring
   - Uncovered electrical panels
   - Extension cords in unsafe locations
   - Water near electrical equipment

4. **Equipment & Material Safety:**
   - Improperly stored materials
   - Unstable stacks
   - Heavy equipment in unsafe positions
   - Tools left in walkways

5. **Site Housekeeping:**
   - Debris accumulation
   - Trip hazards
   - Blocked walkways or exits
   - Poor organization

6. **Healthcare-Specific Concerns:**
   - Contamination risks
   - Medical gas system hazards
   - Clean room protocol violations

For EACH hazard you identify, provide:
- Severity: CRITICAL, MODERATE, or MINOR
- Description: What is the hazard?
- OSHA Reference: Relevant OSHA standard (if applicable)
- Recommended Action: What should be done?

If NO hazards are found, state that clearly.

Format your response as:

HAZARDS FOUND: [number]

[For each hazard:]
🔴 CRITICAL / 🟡 MODERATE / 🟢 MINOR
Description: [detailed description]
OSHA Reference: [standard number if applicable]
Recommended Action: [specific corrective action]

---

If no hazards: "✅ NO SAFETY HAZARDS DETECTED - Site appears compliant"
"""

                            # Generate analysis
                            response = model.generate_content([image_part, prompt])
                            analysis = response.text

                            all_hazards.append({
                                "file": file.name,
                                "analysis": analysis
                            })

                        # Display results
                        st.markdown("---")
                        st.success(f"✅ Analyzed {len(uploaded_files)} photo(s)")

                        # Summary
                        st.markdown("### 📊 Safety Scan Report")
                        st.markdown(f"**Project:** {project_name}")
                        st.markdown(f"**Location:** {location if location else 'Not specified'}")
                        st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
                        st.markdown(f"**Photos Analyzed:** {len(uploaded_files)}")

                        st.markdown("---")

                        # Display results for each photo
                        for idx, hazard_data in enumerate(all_hazards):
                            with st.expander(f"📷 {hazard_data['file']}", expanded=(idx == 0)):
                                st.markdown(hazard_data['analysis'])

                        # Overall summary
                        st.markdown("---")
                        st.markdown("### 📋 Overall Summary")

                        # Combine all analyses for summary
                        combined_text = "\n\n".join([h['analysis'] for h in all_hazards])

                        summary_prompt = f"""Based on these safety scan results from {len(uploaded_files)} photos:

{combined_text}

Provide:
1. Overall Safety Score (0-100)
2. Total number of hazards by severity (Critical, Moderate, Minor)
3. Top 3 priority actions needed
4. Overall site safety assessment (1-2 sentences)

Format as:
SAFETY SCORE: XX/100
CRITICAL: X | MODERATE: X | MINOR: X

TOP PRIORITIES:
1. [action]
2. [action]
3. [action]

ASSESSMENT: [brief assessment]
"""

                        summary_response = model.generate_content(summary_prompt)
                        st.markdown(summary_response.text)

                        # Export options
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)

                        # Create full report text
                        report_text = f"""SE BUILDERS - SAFETY SCAN REPORT
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

PROJECT: {project_name}
LOCATION: {location if location else 'Not specified'}
PHOTOS ANALYZED: {len(uploaded_files)}

{'=' * 60}

"""
                        for hazard_data in all_hazards:
                            report_text += f"\nPHOTO: {hazard_data['file']}\n{'-' * 60}\n"
                            report_text += hazard_data['analysis'] + "\n\n"

                        report_text += f"\n{'=' * 60}\n\nOVERALL SUMMARY\n{'-' * 60}\n"
                        report_text += summary_response.text

                        with col1:
                            st.download_button(
                                label="📥 Download Report",
                                data=report_text,
                                file_name=f"Safety_Report_{project_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )

                        with col2:
                            if st.button("📧 Email Report", use_container_width=True):
                                st.info("Email feature coming soon!")

                        # HubSpot Integration
                        if hubspot.is_enabled():
                            st.markdown("---")
                            st.subheader("📋 Create HubSpot Tasks for Safety Issues")

                            # Extract critical issues from analysis
                            critical_found = any("CRITICAL" in h['analysis'] or "🔴" in h['analysis'] for h in all_hazards)

                            if critical_found:
                                st.warning("⚠️ Critical safety issues detected - Consider creating HubSpot tasks for follow-up")

                            with st.form("hubspot_task_form"):
                                st.write("Create tasks in HubSpot for safety issues requiring follow-up")

                                task_email = st.text_input(
                                    "Project Manager Email (Optional)",
                                    placeholder="pm@sebuilders.com",
                                    help="Associate tasks with a contact in HubSpot"
                                )

                                create_tasks = st.form_submit_button("📝 Create Safety Tasks", use_container_width=True)

                                if create_tasks:
                                    with st.spinner("Creating HubSpot tasks..."):
                                        tasks_created = 0

                                        # Parse each analysis for severity
                                        for hazard_data in all_hazards:
                                            analysis = hazard_data['analysis']

                                            # Detect critical issues
                                            if "CRITICAL" in analysis or "🔴" in analysis:
                                                severity = "CRITICAL"
                                            elif "MODERATE" in analysis or "🟡" in analysis:
                                                severity = "MODERATE"
                                            elif "MINOR" in analysis or "🟢" in analysis:
                                                severity = "MINOR"
                                            else:
                                                continue  # Skip if no clear severity

                                            # Skip if no hazards found
                                            if "NO SAFETY HAZARDS DETECTED" in analysis:
                                                continue

                                            # Create task for this hazard
                                            task_id = hubspot.log_safety_issue(
                                                project_name=project_name,
                                                location=f"{location} - {hazard_data['file']}",
                                                severity=severity,
                                                description=analysis[:1000],  # Limit to 1000 chars
                                                contact_email=task_email if task_email else None
                                            )

                                            if task_id:
                                                tasks_created += 1

                                        if tasks_created > 0:
                                            st.success(f"✅ Created {tasks_created} safety task(s) in HubSpot!")
                                            st.balloons()
                                        else:
                                            st.info("ℹ️ No critical safety issues found - no tasks created")
                        else:
                            with col3:
                                if st.button("💾 Save to Database", use_container_width=True):
                                    st.info("Database integration coming soon!")

                    except Exception as e:
                        st.error(f"Error analyzing photos: {str(e)}")
        else:
            st.info("👈 Upload site photos and click 'Scan' to analyze safety hazards")

    # Info section
    st.markdown("---")
    st.info("""
    **💡 How it works:**

    Upload photos from your construction site, and our AI will analyze them for common
    safety hazards, OSHA violations, and compliance issues. The system uses advanced
    computer vision to identify risks that might be missed during manual inspections.

    **Detection Categories:** PPE violations, fall hazards, electrical safety, housekeeping,
    equipment safety, and healthcare-specific concerns.

    **Note:** AI analysis should supplement, not replace, professional safety inspections.
    """)

    # Safety tips
    st.markdown("---")
    st.subheader("🎯 Common Safety Hazards to Watch For")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **PPE Requirements:**
        - Hard hats at all times
        - High-visibility vests
        - Safety glasses
        - Steel-toe boots
        - Fall protection when needed
        """)

    with col2:
        st.markdown("""
        **Fall Protection:**
        - Guardrails at 6+ feet
        - Secured ladders
        - Proper scaffolding
        - Hole covers
        - Safety harnesses
        """)

    with col3:
        st.markdown("""
        **Housekeeping:**
        - Clear walkways
        - Organized materials
        - Debris removal
        - Proper storage
        - Exit access
        """)

    # Monthly stats
    st.markdown("---")
    st.subheader("📊 Safety Performance (Last 30 Days)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Inspections", "12", "+15%")
    col2.metric("Hazards Found", "47", "-8%")
    col3.metric("Resolution Rate", "96%", "+4%")
    col4.metric("Safety Score", "94/100", "+6")
