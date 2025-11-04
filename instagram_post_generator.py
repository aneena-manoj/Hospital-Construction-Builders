import io
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path

# ========= Auth =========
load_dotenv()  # Load environment variables from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
assert GOOGLE_API_KEY, "Set your GOOGLE_API_KEY in the .env file"
genai.configure(api_key=GOOGLE_API_KEY)

# ========= Inputs (update these paths) =========
# Get the directory where this script is located
script_dir = Path(__file__).parent

# CEO reference face
ceo_image_path = script_dir / "images" / "1761862936473.jpeg"
# Company logo (PNG with transparency preferred)
logo_image_path = script_dir / "images" / "logo.png"

# Optional: a background reference you like (e.g., your Thanksgiving poster or a facility shot)
# If you don't want to send it, set background_image_path = None
background_image_path = None  # <- or set to a valid path

# ========= Helper: load image file → bytes part =========
def image_to_part(path, mime="image/png"):
    path = str(path)  # Convert Path object to string
    with Image.open(path) as im:
        buf = io.BytesIO()
        # Preserve PNG for transparency if file is PNG; otherwise fallback to PNG
        fmt = "PNG" if (mime.endswith("png") or path.lower().endswith(".png")) else "PNG"
        im.save(buf, format=fmt)
        return {"mime_type": mime, "data": buf.getvalue()}

parts = []

# CEO (reference) – use JPEG/PNG mime depending on file
if ceo_image_path:
    ceo_mime = "image/png" if str(ceo_image_path).lower().endswith(".png") else "image/jpeg"
    parts.append(image_to_part(ceo_image_path, mime=ceo_mime))

# Logo will be added after generation, not sent to AI model

# Optional background/scene reference
if background_image_path:
    bg_mime = "image/png" if str(background_image_path).lower().endswith(".png") else "image/jpeg"
    parts.append(image_to_part(background_image_path, mime=bg_mime))

# ========= Prompt =========
text_input = """
Create a SQUARE Instagram post (1:1 aspect ratio - equal width and height)
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

3) Brand: Leave space in the top-right corner for logo placement (we'll add it separately).

4) Scene: Modern healthcare facility under construction with tower cranes in the background.
   Add subtle festive touches: light snow, string lights, small ornaments, evergreen accents.
   Keep it professional and corporate.

5) Text Overlay:
   Headline: "Merry Christmas & Happy Holidays from SE Builders!"
   Subtext: "Building spaces where care and community can thrive."

   CRITICAL: Spell these texts EXACTLY as written above. Double check spelling before rendering.

6) Style: Cinematic, premium, professional. Navy + white base colors with red/green/gold
   holiday accents. Clean layout, balanced composition, and legible typography optimized
   for Instagram marketing.
"""

# ========= Generate =========
model = genai.GenerativeModel(model_name="gemini-2.5-flash-image")
response = model.generate_content(contents=parts + [text_input])

# ========= Extract & Save =========
image_parts = []
if response and response.candidates:
    for p in response.candidates[0].content.parts:
        if hasattr(p, "inline_data") and p.inline_data and getattr(p.inline_data, "data", None):
            image_parts.append(p.inline_data.data)

if image_parts:
    # Load the generated image
    out = Image.open(io.BytesIO(image_parts[0]))

    # Overlay the logo in the top-right corner
    if logo_image_path.exists():
        logo = Image.open(logo_image_path)

        # Calculate logo size (make it about 15% of image width)
        img_width, img_height = out.size
        logo_width = int(img_width * 0.15)
        logo_aspect = logo.height / logo.width
        logo_height = int(logo_width * logo_aspect)

        # Resize logo
        logo_resized = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        # Position in top-right with padding
        padding = int(img_width * 0.03)  # 3% padding
        x = img_width - logo_width - padding
        y = padding

        # Paste with transparency if logo has alpha channel
        if logo_resized.mode == 'RGBA':
            out.paste(logo_resized, (x, y), logo_resized)
        else:
            out.paste(logo_resized, (x, y))

    out.save("se_builders_christmas_instagram.png")
    out.show()  # Opens the image for preview
    print("Saved: se_builders_christmas_instagram.png")
else:
    print("No image data found in response.")
