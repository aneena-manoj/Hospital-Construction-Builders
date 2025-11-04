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

# Logo (to be composited into output)
if logo_image_path:
    logo_mime = "image/png" if str(logo_image_path).lower().endswith(".png") else "image/jpeg"
    parts.append(image_to_part(logo_image_path, mime=logo_mime))

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
    out = Image.open(io.BytesIO(image_parts[0]))
    out.save("se_builders_christmas_instagram.png")
    out.show()  # Opens the image for preview
    print("Saved: se_builders_christmas_instagram.png")
else:
    print("No image data found in response.")
