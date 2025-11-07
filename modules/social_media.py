import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

def image_to_part(image, mime="image/png"):
    buf = io.BytesIO()
    fmt = "PNG" if mime.endswith("png") else "JPEG"
    image.save(buf, format=fmt)
    return {"mime_type": mime, "data": buf.getvalue()}

def show_social_media():
    st.markdown("<h1 class='main-header'>📱 Multi-Platform Social Media Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Create platform-optimized content in one click</p>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Campaign Setup")

        # Prompt selection dropdown
        prompt_type = st.selectbox(
            "Select Campaign Template:",
            ["Holiday Poster", "Building Launch", "Project Completion", "Team Spotlight",
             "Behind the Scenes", "Industry News", "Awards & Achievements"],
            index=0
        )

        # File uploaders with dynamic labels
        if prompt_type == "Holiday Poster":
            ceo_file = st.file_uploader(
                "Upload CEO Image (Required)",
                type=["png", "jpg", "jpeg"],
                key="ceo",
                help="CEO's face will be used for Santa"
            )
            logo_file = st.file_uploader(
                "Upload Company Logo (Required)",
                type=["png", "jpg", "jpeg"],
                key="logo"
            )
        else:
            ceo_file = st.file_uploader(
                "Upload CEO Image (Optional)",
                type=["png", "jpg", "jpeg"],
                key="ceo"
            )
            logo_file = st.file_uploader(
                "Upload Company Logo (Optional)",
                type=["png", "jpg", "jpeg"],
                key="logo"
            )

        background_file = st.file_uploader(
            "Upload Background (Optional)",
            type=["png", "jpg", "jpeg"],
            key="bg"
        )

        # Define prompt templates
        holiday_prompt = """Create a SQUARE Instagram post (1:1 aspect ratio - equal width and height)
for a Christmas greeting campaign for a commercial healthcare construction company named SE Builders.

IMPORTANT: The image MUST be perfectly square, not rectangular.

CRITICAL REQUIREMENTS:

1) Character - CEO as Santa (MOST IMPORTANT):
   - Study the uploaded CEO reference photo carefully
   - Create Santa Claus but with the CEO's EXACT facial features:
     * Match his face shape, jawline, and facial structure precisely
     * Copy his eye shape, eye color, and gaze direction
     * Replicate his smile, mouth shape, and teeth
     * Match his nose shape and size
     * Preserve his skin tone and facial proportions
     * Keep his distinctive facial characteristics recognizable
   - Dress as Santa: classic red suit, white fur trim, and red Santa hat
   - NO BEARD - keep the CEO's face clean and fully visible
   - The face should be clearly visible and prominent in the composition
   - People should be able to recognize the CEO in Santa's outfit

2) Format: The output image MUST be perfectly SQUARE (1:1 ratio). Same width and height.
   Not portrait, not landscape - SQUARE only.

3) Brand: Place the uploaded SE Builders logo cleanly in the top-right corner with ample padding.
   Keep the logo crisp, undistorted, and clearly visible.

4) Scene: Modern healthcare facility under construction with tower cranes in the background.
   Add subtle festive touches: light snow, string lights, small ornaments, evergreen accents.
   Keep it professional and corporate.

5) Text Overlay:
   Headline: "Merry Christmas & Happy Holidays from SE Builders!"
   Subtext: "Building spaces where care and community can thrive."

6) Style: Cinematic, premium, professional. Navy + white base colors with red/green/gold
   holiday accents. Clean layout, balanced composition, and legible typography optimized
   for Instagram marketing.
"""

        building_launch_prompt = """Create a professional Instagram portrait poster (1080x1350) announcing the
completion and launch of a new commercial healthcare facility built by SE Builders.

Main visual: A beautifully finished, state-of-the-art medical building with
modern architecture — glass façade, clean lines, and well-lit interior spaces
visible through the windows. Add subtle details that show the building is now
open and operational, such as welcoming exterior lighting, fresh landscaping,
and a grand entrance.

Branding: Place the SE Builders logo clearly at the top right corner with
proper spacing and correct proportions.

Text layout:
Headline (bold, professional): "Project Complete!"
Sub-headline: "Proudly Delivered by SE Builders"
Footer text (smaller): "Building spaces where care and community thrive"

Design style: sleek and premium with a focus on quality craftsmanship and
innovation. Use a color palette of navy blue, white, and subtle metallic accents
(silver or gold) to convey professionalism and prestige. Soft sunset or golden
hour lighting preferred for a warm, welcoming feel. Clean margins, balanced
visual hierarchy, high resolution.

Tone: Confident, innovative, and celebratory — conveying that this finished
project enhances community wellbeing and represents excellence in healthcare
construction.
"""

        project_completion_prompt = """Create a professional Instagram post celebrating the successful completion of a healthcare construction project by SE Builders.

Show a stunning exterior shot of the completed building with:
- Modern healthcare architecture
- Golden hour lighting
- Landscaping and finished details
- SE Builders logo in top-right corner

Text: "Another Milestone Achieved ✅"
Subtext: "Proud to deliver excellence in healthcare construction"

Style: Professional, celebratory, premium quality. Navy and orange SE Builders brand colors."""

        team_spotlight_prompt = """Create a professional Instagram post highlighting the SE Builders construction team.

Show a diverse, professional team on a healthcare construction site:
- Team members in SE Builders gear (hard hats, safety vests)
- Modern healthcare facility in background
- Professional photography style
- SE Builders logo prominently displayed

Text: "Meet the Team Building Your Healthcare Future"
Subtext: "Excellence through craftsmanship and dedication"

Style: Human-focused, professional, inspiring. SE Builders brand colors."""

        # Select prompt based on type
        prompt_templates = {
            "Holiday Poster": holiday_prompt,
            "Building Launch": building_launch_prompt,
            "Project Completion": project_completion_prompt,
            "Team Spotlight": team_spotlight_prompt,
            "Behind the Scenes": "Create a behind-the-scenes Instagram post showing SE Builders construction process...",
            "Industry News": "Create a professional Instagram post sharing healthcare construction industry insights...",
            "Awards & Achievements": "Create a celebratory Instagram post announcing SE Builders achievement or award..."
        }

        base_prompt = prompt_templates.get(prompt_type, building_launch_prompt)

        # Display base prompt
        with st.expander("📝 View Base Prompt Template"):
            st.text_area("Base Prompt", value=base_prompt, height=200, disabled=True, key="base_prompt_view")

        # Additional instructions
        additional_prompt = st.text_area(
            "Additional Custom Instructions (Optional)",
            value="",
            height=100,
            placeholder="Add any extra instructions here to customize the prompt further..."
        )

        # Combine prompts
        if additional_prompt.strip():
            final_prompt = base_prompt + "\n\nADDITIONAL INSTRUCTIONS:\n" + additional_prompt
        else:
            final_prompt = base_prompt

        # Generate button
        generate_button = st.button("🎨 Generate Instagram Post", type="primary", use_container_width=True)

    with col2:
        st.subheader("Generated Content")

        if generate_button:
            # Validate files
            if prompt_type == "Holiday Poster" and (not ceo_file or not logo_file):
                st.error("⚠️ For Holiday Poster, please upload both CEO image and logo.")
            else:
                with st.spinner("Generating your Instagram post... This may take a moment."):
                    try:
                        # Configure AI
                        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                        model = genai.GenerativeModel(model_name="gemini-2.5-flash-image")

                        # Prepare image parts
                        parts = []

                        if ceo_file:
                            ceo_image = Image.open(ceo_file)
                            ceo_mime = "image/png" if ceo_file.name.lower().endswith(".png") else "image/jpeg"
                            parts.append(image_to_part(ceo_image, mime=ceo_mime))

                        if logo_file:
                            logo_image = Image.open(logo_file)
                            logo_mime = "image/png" if logo_file.name.lower().endswith(".png") else "image/jpeg"
                            parts.append(image_to_part(logo_image, mime=logo_mime))

                        if background_file:
                            bg_image = Image.open(background_file)
                            bg_mime = "image/png" if background_file.name.lower().endswith(".png") else "image/jpeg"
                            parts.append(image_to_part(bg_image, mime=bg_mime))

                        # Generate
                        response = model.generate_content(contents=parts + [final_prompt])

                        # Extract image
                        image_parts = []
                        if response and response.candidates:
                            for p in response.candidates[0].content.parts:
                                if hasattr(p, "inline_data") and p.inline_data and getattr(p.inline_data, "data", None):
                                    image_parts.append(p.inline_data.data)

                        if image_parts:
                            output_image = Image.open(io.BytesIO(image_parts[0]))

                            # Display
                            st.image(output_image, caption="Generated Instagram Post", use_column_width=True)

                            # Download
                            buf = io.BytesIO()
                            output_image.save(buf, format="PNG")
                            st.download_button(
                                label="📥 Download Image",
                                data=buf.getvalue(),
                                file_name=f"se_builders_{prompt_type.lower().replace(' ', '_')}.png",
                                mime="image/png",
                                use_container_width=True
                            )

                            st.success("✅ Image generated successfully!")

                            # Platform-specific copy
                            st.markdown("---")
                            st.subheader("📝 Platform-Specific Captions")

                            with st.expander("Instagram Caption"):
                                st.text_area("Instagram", value="[AI will generate caption here in future update]", height=100)

                            with st.expander("LinkedIn Post"):
                                st.text_area("LinkedIn", value="[AI will generate caption here in future update]", height=100)

                            with st.expander("Facebook Post"):
                                st.text_area("Facebook", value="[AI will generate caption here in future update]", height=100)

                        else:
                            st.error("❌ No image data found in response. Please try again.")

                    except Exception as e:
                        st.error(f"❌ Error generating image: {str(e)}")
        else:
            st.info("👈 Configure your campaign settings and click 'Generate' to create your Instagram post")

    # Info
    st.markdown("---")
    st.info("""
    **💡 How it works:**

    Select a template, upload reference images (if needed), and let AI generate platform-optimized
    content. The system maintains SE Builders brand consistency while creating engaging visuals
    for your social media campaigns.

    **Supported Platforms:** Instagram, LinkedIn, Facebook, X (Twitter), TikTok
    """)
