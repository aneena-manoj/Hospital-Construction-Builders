import io
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the page
st.set_page_config(page_title="SE Builders Instagram Post Generator", layout="wide")
st.title("🎄 Instagram Post Generator")
st.subheader("Generate custom Instagram posts with AI")

# Check for API key
if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found in .env file. Please add it to continue.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Helper function to convert image to bytes
def image_to_part(image, mime="image/png"):
    buf = io.BytesIO()
    fmt = "PNG" if mime.endswith("png") else "JPEG"
    image.save(buf, format=fmt)
    return {"mime_type": mime, "data": buf.getvalue()}

# Layout with two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Inputs")

    # Prompt selection dropdown (moved to top)
    st.subheader("Select Prompt Template")
    prompt_type = st.selectbox(
        "Choose a template:",
        ["Holiday Poster", "Building Launch"],
        index=0
    )

    # File uploaders with dynamic labels based on prompt type
    if prompt_type == "Holiday Poster":
        ceo_file = st.file_uploader("Upload CEO Image (Required)", type=["png", "jpg", "jpeg"], key="ceo", help="CEO's face will be used for Santa")
        logo_file = st.file_uploader("Upload Company Logo (Required)", type=["png", "jpg", "jpeg"], key="logo")
    else:
        ceo_file = st.file_uploader("Upload CEO Image (Optional)", type=["png", "jpg", "jpeg"], key="ceo")
        logo_file = st.file_uploader("Upload Company Logo (Optional)", type=["png", "jpg", "jpeg"], key="logo")

    # Optional background
    background_file = st.file_uploader("Upload Background (Optional)", type=["png", "jpg", "jpeg"], key="bg")

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
completion and launch of a new commercial healthcare facility built by
SE Builders.

Main visual: A beautifully finished, state-of-the-art medical building with
modern architecture — glass façade, clean lines, and well-lit interior spaces
visible through the windows. Add subtle details that show the building is now
open and operational, such as welcoming exterior lighting, fresh landscaping,
and a grand entrance.

Branding: Place the SE Builders logo clearly at the top right corner with
proper spacing and correct proportions. Include tagline in clean typography.

Text layout:
Headline (bold, professional): "Project Complete!"
Sub-headline: "Proudly Delivered by SE Builders"
Footer text (smaller): "Building spaces where care and community thrive"
Include location label (optional): "Southern California Healthcare Facility"

Design style: sleek and premium with a focus on quality craftsmanship and
innovation. Use a color palette of navy blue, white, and subtle metallic accents
(silver or gold) to convey professionalism and prestige. Soft sunset or golden
hour lighting preferred for a warm, welcoming feel. Clean margins, balanced
visual hierarchy, high resolution.

Tone: Confident, innovative, and celebratory — conveying that this finished
project enhances community wellbeing and represents excellence in healthcare
construction.
"""

    # Select the appropriate prompt based on dropdown
    if prompt_type == "Holiday Poster":
        base_prompt = holiday_prompt
    else:
        base_prompt = building_launch_prompt

    # Display the base prompt (read-only)
    st.text_area("Base Prompt Template", value=base_prompt, height=300, disabled=True, key=f"base_prompt_{prompt_type}")

    # Additional custom prompt
    additional_prompt = st.text_area(
        "Additional Custom Instructions (Optional)",
        value="",
        height=150,
        placeholder="Add any extra instructions here to customize the prompt further..."
    )

    # Combine prompts
    if additional_prompt.strip():
        prompt = base_prompt + "\n\nADDITIONAL INSTRUCTIONS:\n" + additional_prompt
    else:
        prompt = base_prompt

    # Generate button
    generate_button = st.button("🎨 Generate Instagram Post", type="primary", use_container_width=True)

with col2:
    st.header("Output")

    if generate_button:
        # Validate required files based on prompt type
        if prompt_type == "Holiday Poster" and (not ceo_file or not logo_file):
            st.error("⚠️ For Holiday Poster, please upload both CEO image and logo.")
        else:
            with st.spinner("Generating your Instagram post... This may take a moment."):
                try:
                    # Prepare image parts
                    parts = []

                    # CEO image (if uploaded)
                    if ceo_file:
                        ceo_image = Image.open(ceo_file)
                        ceo_mime = "image/png" if ceo_file.name.lower().endswith(".png") else "image/jpeg"
                        parts.append(image_to_part(ceo_image, mime=ceo_mime))

                    # Logo image (if uploaded)
                    if logo_file:
                        logo_image = Image.open(logo_file)
                        logo_mime = "image/png" if logo_file.name.lower().endswith(".png") else "image/jpeg"
                        parts.append(image_to_part(logo_image, mime=logo_mime))

                    # Background (optional)
                    if background_file:
                        bg_image = Image.open(background_file)
                        bg_mime = "image/png" if background_file.name.lower().endswith(".png") else "image/jpeg"
                        parts.append(image_to_part(bg_image, mime=bg_mime))

                    # Generate with Gemini
                    model = genai.GenerativeModel(model_name="gemini-2.5-flash-image")
                    response = model.generate_content(contents=parts + [prompt])

                    # Extract image
                    image_parts = []
                    if response and response.candidates:
                        for p in response.candidates[0].content.parts:
                            if hasattr(p, "inline_data") and p.inline_data and getattr(p.inline_data, "data", None):
                                image_parts.append(p.inline_data.data)

                    if image_parts:
                        output_image = Image.open(io.BytesIO(image_parts[0]))

                        # Display the generated image
                        st.image(output_image, caption="Generated Instagram Post", use_column_width=True)

                        # Download button
                        buf = io.BytesIO()
                        output_image.save(buf, format="PNG")
                        st.download_button(
                            label="📥 Download Image",
                            data=buf.getvalue(),
                            file_name="instagram_post.png",
                            mime="image/png",
                            use_container_width=True
                        )

                        st.success("✅ Image generated successfully!")
                    else:
                        st.error("❌ No image data found in response. Please try again.")

                except Exception as e:
                    st.error(f"❌ Error generating image: {str(e)}")
    else:
        st.info("👈 Upload images and click 'Generate' to create your Instagram post")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google Gemini AI")
