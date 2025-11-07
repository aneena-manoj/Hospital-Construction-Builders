# SE Builders AI Platform - Technical Documentation

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Application Structure](#application-structure)
4. [AI Pipeline Implementation](#ai-pipeline-implementation)
5. [Module Deep Dives](#module-deep-dives)
6. [Data Flow Diagrams](#data-flow-diagrams)
7. [API Integration](#api-integration)
8. [Setup & Configuration](#setup--configuration)
9. [Deployment Guide](#deployment-guide)
10. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                    (Streamlit Frontend)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   MAIN APPLICATION                          │
│                      (app.py)                               │
│  - Navigation Router                                        │
│  - Session Management                                       │
│  - UI Configuration                                         │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODULE LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │  Cost    │  │  Social  │  │  Client  │   │
│  │          │  │Estimator │  │  Media   │  │ Assistant│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐                                               │
│  │  Safety  │                                               │
│  │ Scanner  │                                               │
│  └──────────┘                                               │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI LAYER                                 │
│  ┌───────────────────┐      ┌───────────────────┐          │
│  │  Gemini 2.0 Flash │      │ Gemini 2.5 Flash  │          │
│  │  (Text/Vision)    │      │  (Image Gen)      │          │
│  └───────────────────┘      └───────────────────┘          │
│           ▲                           ▲                     │
│           │                           │                     │
│    ┌──────┴──────────┐       ┌───────┴─────────┐          │
│    │ google-         │       │ google-          │          │
│    │ generativeai    │       │ generativeai     │          │
│    │ Python SDK      │       │ Python SDK       │          │
│    └─────────────────┘       └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                          │
│  - Google Gemini API                                        │
│  - Environment Config (.env)                                │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Modular Architecture** - Each feature is a self-contained module
2. **Single Responsibility** - Each module handles one specific domain
3. **Stateless AI Calls** - Each AI request is independent
4. **Session State Management** - User data persisted in Streamlit session
5. **Error Isolation** - Module failures don't crash the entire app

---

## 🔧 Technology Stack

### Core Framework
- **Streamlit** (v1.28+) - Web application framework
  - Handles UI rendering
  - Manages session state
  - Provides built-in components (chat, file upload, etc.)

### AI/ML
- **Google Gemini API** - LLM and vision models
  - `gemini-2.0-flash-exp` - Fast text generation and vision
  - `gemini-2.5-flash-image` - Image generation
- **google-generativeai** (Python SDK) - API client library

### Image Processing
- **Pillow (PIL)** - Image manipulation
  - Format conversion (PNG/JPEG)
  - Resizing and optimization
  - In-memory buffer operations

### Configuration
- **python-dotenv** - Environment variable management
  - Secure API key storage
  - Environment-specific configs

### Language & Runtime
- **Python 3.11+** - Primary language
- **Type Hints** - Code documentation and IDE support

---

## 📂 Application Structure

```
Hospital-Construction-Builders/
│
├── app.py                          # Main application entry point
│   ├── Page configuration
│   ├── Custom CSS styling
│   ├── Sidebar navigation
│   └── Module routing logic
│
├── modules/                        # Feature modules directory
│   ├── __init__.py                # Package initializer
│   │
│   ├── dashboard.py               # Dashboard module
│   │   └── show_dashboard()      # Main function
│   │
│   ├── cost_estimator.py          # Cost estimation module
│   │   └── show_cost_estimator() # Main function
│   │
│   ├── social_media.py            # Social media generator
│   │   ├── show_social_media()   # Main function
│   │   └── image_to_part()       # Helper function
│   │
│   ├── client_assistant.py        # AI chatbot module
│   │   └── show_client_assistant() # Main function
│   │
│   └── safety_scanner.py          # Safety analysis module
│       └── show_safety_scanner()  # Main function
│
├── images/                         # Static assets
│   ├── logo.png                   # SE Builders logo
│   └── 1761862936473.jpeg         # Sample CEO image
│
├── .env                           # Environment variables (create this)
│   └── GOOGLE_API_KEY=xxx         # Gemini API key
│
├── pyproject.toml                 # Python project configuration
│   └── dependencies               # Package requirements
│
├── README.md                      # User-facing documentation
├── TECHNICAL_README.md            # This file
└── SE_Builders_AI_Platform_Proposal.md  # Business proposal
```

---

## 🤖 AI Pipeline Implementation

### Pipeline Architecture Pattern

All AI modules follow this standardized pipeline:

```
┌─────────────┐
│   INPUT     │
│  Collection │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   INPUT     │
│ Validation  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   PROMPT    │
│ Engineering │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     AI      │
│   API Call  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  RESPONSE   │
│  Processing │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   OUTPUT    │
│  Rendering  │
└─────────────┘
```

### Common Pipeline Components

#### 1. API Configuration (Used by all modules)

```python
import google.generativeai as genai
import os

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize model
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
# OR for image generation:
model = genai.GenerativeModel(model_name="gemini-2.5-flash-image")
```

#### 2. Error Handling Pattern

```python
try:
    # AI API call
    response = model.generate_content(prompt)
    result = response.text

    # Process result
    st.success("✅ Success!")
    st.markdown(result)

except Exception as e:
    # Graceful error handling
    st.error(f"❌ Error: {str(e)}")
    # Provide fallback or guidance
```

#### 3. Session State Management

```python
# Initialize session state (runs once)
if "key_name" not in st.session_state:
    st.session_state.key_name = default_value

# Access session state
value = st.session_state.key_name

# Update session state
st.session_state.key_name = new_value
```

---

## 📊 Module Deep Dives

### Module 1: Dashboard (`dashboard.py`)

**Purpose:** Central hub showing metrics and quick actions

**Type:** Static display module (no AI)

**Architecture:**
```
show_dashboard()
├── Display key metrics (4 cards)
├── Quick action buttons (4 buttons)
├── Recent activity feed
├── Alerts & notifications
└── AI platform performance metrics
```

**Implementation Details:**

```python
def show_dashboard():
    # 1. HEADER
    st.markdown("<h1 class='main-header'>SE Builders AI Platform</h1>")

    # 2. METRICS ROW (4 columns)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Metric card with custom HTML/CSS
        st.markdown("""
        <div class='metric-card'>
            <h3>🏗️ Active Projects</h3>
            <h1>12</h1>
            <p>+2 from last month</p>
        </div>
        """, unsafe_allow_html=True)

    # 3. QUICK ACTIONS (4 buttons)
    if st.button("💰 Generate Estimate"):
        # Navigation would go here (not yet implemented)
        pass

    # 4. ACTIVITY FEED (loop through activities)
    activities = [
        {"icon": "💰", "text": "New estimate...", "time": "2 hours ago"}
    ]
    for activity in activities:
        st.markdown(f"... {activity['text']} ...")

    # 5. ALERTS (Streamlit built-in components)
    st.error("🔴 Critical safety hazard")
    st.warning("🟡 Client waiting")
    st.success("🟢 Estimate approved")

    # 6. PERFORMANCE METRICS (4 columns with st.metric)
    col1.metric("Cost Estimator", "23 estimates", "+44%")
```

**Data Source:** Currently hardcoded (mock data). In production, would connect to:
- Project management database
- Analytics platform
- Notification system

---

### Module 2: Cost Estimator (`cost_estimator.py`)

**Purpose:** Generate detailed project cost estimates using AI

**AI Model:** Gemini 2.0 Flash (text generation)

**Architecture:**
```
show_cost_estimator()
├── INPUT: Project form
│   ├── Facility type (dropdown)
│   ├── Square footage (number input)
│   ├── Location (dropdown)
│   ├── Floors (number input)
│   ├── Special requirements (multiselect)
│   ├── Timeline (dropdown)
│   ├── Quality level (slider)
│   └── Additional notes (text area)
│
├── PROMPT ENGINEERING
│   ├── Structure input data
│   ├── Build detailed prompt
│   ├── Include context about SE Builders
│   └── Specify output format
│
├── AI PIPELINE
│   ├── Configure Gemini API
│   ├── Create model instance
│   ├── Send prompt
│   └── Receive response
│
└── OUTPUT RENDERING
    ├── Display formatted estimate
    ├── Download options (TXT)
    └── Future: Email, CRM integration
```

**Pipeline Implementation:**

#### Step 1: Input Collection

```python
# User inputs via Streamlit widgets
facility_type = st.selectbox(
    "Facility Type",
    ["Hospital", "Surgery Center", "Medical Office", ...]
)

square_footage = st.number_input(
    "Square Footage",
    min_value=1000,
    max_value=500000,
    value=25000
)

special_reqs = st.multiselect(
    "Select applicable features:",
    ["Clean Rooms", "Operating Suites", "Medical Gas Systems", ...]
)

# ... other inputs
```

#### Step 2: Prompt Engineering

```python
# Build comprehensive prompt
prompt = f"""You are a construction cost estimator for SE Builders,
a healthcare construction company in Southern California.

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

Please provide:
1. COST BREAKDOWN by category (with dollar amounts)
2. TOTAL ESTIMATED COST with confidence level
3. COST PER SQUARE FOOT
4. RISK FACTORS & CONSIDERATIONS
5. TIMELINE BREAKDOWN
6. COMPARABLE PROJECTS
7. RECOMMENDATIONS

Format the response professionally..."""
```

**Key Prompt Engineering Techniques:**
- **Role Definition:** "You are a construction cost estimator..."
- **Context Provision:** SE Builders, Southern California, healthcare
- **Structured Output:** Numbered sections, clear formatting
- **Specific Instructions:** "with dollar amounts", "confidence level"
- **Format Requirements:** Professional, bullet points

#### Step 3: AI API Call

```python
if st.button("🎯 Generate Cost Estimate"):
    with st.spinner("Analyzing project parameters..."):
        try:
            # Configure API
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

            # Create model
            model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

            # Generate content
            response = model.generate_content(prompt)

            # Extract text
            estimate_text = response.text

        except Exception as e:
            st.error(f"Error: {str(e)}")
```

#### Step 4: Output Processing

```python
# Display results
st.success("✅ Estimate Generated Successfully!")
st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}")
st.markdown(estimate_text)

# Download functionality
estimate_report = f"""SE BUILDERS - PROJECT COST ESTIMATE
Generated: {datetime.now().strftime('%B %d, %Y')}

PROJECT DETAILS:
- Facility Type: {facility_type}
- Square Footage: {square_footage:,} sq ft
...

{estimate_text}
"""

st.download_button(
    label="📥 Download as TXT",
    data=estimate_report,
    file_name=f"SE_Builders_Estimate_{datetime.now().strftime('%Y%m%d')}.txt",
    mime="text/plain"
)
```

**Performance Characteristics:**
- **Average Response Time:** 20-40 seconds
- **Token Usage:** ~2,000-3,000 tokens per request
- **Cost per Request:** ~$0.01-0.02 (Gemini pricing)

---

### Module 3: Social Media Generator (`social_media.py`)

**Purpose:** Generate branded Instagram posts using AI image generation

**AI Model:** Gemini 2.5 Flash Image

**Architecture:**
```
show_social_media()
├── INPUT: Campaign setup
│   ├── Template selection (dropdown)
│   ├── CEO image upload (optional/required)
│   ├── Logo upload (optional/required)
│   ├── Background upload (optional)
│   └── Custom instructions (text area)
│
├── PROMPT SELECTION
│   ├── Holiday Poster prompt
│   ├── Building Launch prompt
│   ├── Project Completion prompt
│   └── ... other templates
│
├── IMAGE PROCESSING
│   ├── Load uploaded images (PIL)
│   ├── Convert to bytes (io.BytesIO)
│   ├── Create image parts for API
│   └── Determine MIME types
│
├── AI PIPELINE
│   ├── Configure Gemini API
│   ├── Combine image parts + prompt
│   ├── Call image generation model
│   └── Receive generated image
│
└── OUTPUT RENDERING
    ├── Display generated image
    ├── Download as PNG
    └── Platform captions (placeholder)
```

**Pipeline Implementation:**

#### Step 1: Template Selection

```python
# Template dropdown
prompt_type = st.selectbox(
    "Select Campaign Template:",
    ["Holiday Poster", "Building Launch", "Project Completion", ...]
)

# Conditional file upload requirements
if prompt_type == "Holiday Poster":
    ceo_file = st.file_uploader(
        "Upload CEO Image (Required)",
        type=["png", "jpg", "jpeg"],
        help="CEO's face will be used for Santa"
    )
    logo_file = st.file_uploader(
        "Upload Company Logo (Required)",
        type=["png", "jpg", "jpeg"]
    )
else:
    ceo_file = st.file_uploader(
        "Upload CEO Image (Optional)",
        type=["png", "jpg", "jpeg"]
    )
```

#### Step 2: Image Processing Helper

```python
def image_to_part(image, mime="image/png"):
    """
    Convert PIL Image to bytes format for Gemini API

    Args:
        image: PIL Image object
        mime: MIME type string ("image/png" or "image/jpeg")

    Returns:
        dict: {"mime_type": str, "data": bytes}
    """
    buf = io.BytesIO()

    # Determine format from MIME type
    fmt = "PNG" if mime.endswith("png") else "JPEG"

    # Save image to buffer
    image.save(buf, format=fmt)

    # Return API-compatible format
    return {
        "mime_type": mime,
        "data": buf.getvalue()
    }
```

#### Step 3: Prepare Image Parts

```python
# Prepare image parts array
parts = []

# Process CEO image (if uploaded)
if ceo_file:
    ceo_image = Image.open(ceo_file)
    ceo_mime = "image/png" if ceo_file.name.lower().endswith(".png") else "image/jpeg"
    parts.append(image_to_part(ceo_image, mime=ceo_mime))

# Process logo (if uploaded)
if logo_file:
    logo_image = Image.open(logo_file)
    logo_mime = "image/png" if logo_file.name.lower().endswith(".png") else "image/jpeg"
    parts.append(image_to_part(logo_image, mime=logo_mime))

# Process background (if uploaded)
if background_file:
    bg_image = Image.open(background_file)
    bg_mime = "image/png" if background_file.name.lower().endswith(".png") else "image/jpeg"
    parts.append(image_to_part(bg_image, mime=bg_mime))
```

#### Step 4: Prompt Engineering (Holiday Example)

```python
holiday_prompt = """Create a SQUARE Instagram post (1:1 aspect ratio - equal width and height)
for a Christmas greeting campaign for SE Builders.

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
   - Dress as Santa: red suit, white fur trim, red Santa hat
   - NO BEARD - keep the CEO's face clean and fully visible
   - The face should be clearly visible and prominent

2) Format: SQUARE (1:1 ratio). Same width and height.

3) Brand: Place the SE Builders logo in top-right corner with padding.

4) Scene: Modern healthcare facility under construction with tower cranes.
   Add festive touches: light snow, string lights, ornaments.

5) Text Overlay:
   Headline: "Merry Christmas & Happy Holidays from SE Builders!"
   Subtext: "Building spaces where care and community can thrive."

6) Style: Cinematic, premium, professional. Navy + white base with red/green/gold
   holiday accents. Clean layout, legible typography for Instagram."""
```

**Prompt Engineering Strategies:**
- **Explicit Constraints:** "MUST be perfectly square"
- **Priority Emphasis:** "MOST IMPORTANT"
- **Detailed Instructions:** Bullet points for facial features
- **Visual Specifications:** Colors, layout, typography
- **Brand Requirements:** Logo placement, tagline
- **Format Enforcement:** Repeated mention of square ratio

#### Step 5: AI Image Generation

```python
if generate_button:
    with st.spinner("Generating your Instagram post..."):
        try:
            # Configure API
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

            # Create image generation model
            model = genai.GenerativeModel(model_name="gemini-2.5-flash-image")

            # Combine image parts and prompt
            # parts = [ceo_image_part, logo_image_part, ...]
            # final_prompt = holiday_prompt + custom_instructions

            response = model.generate_content(contents=parts + [final_prompt])

            # Extract generated image from response
            image_parts = []
            if response and response.candidates:
                for p in response.candidates[0].content.parts:
                    if hasattr(p, "inline_data") and p.inline_data:
                        if getattr(p.inline_data, "data", None):
                            image_parts.append(p.inline_data.data)

            if image_parts:
                # Convert bytes to PIL Image
                output_image = Image.open(io.BytesIO(image_parts[0]))

                # Display
                st.image(output_image, caption="Generated Instagram Post")

            else:
                st.error("No image data found in response")

        except Exception as e:
            st.error(f"Error: {str(e)}")
```

#### Step 6: Download Functionality

```python
# Prepare image for download
buf = io.BytesIO()
output_image.save(buf, format="PNG")

st.download_button(
    label="📥 Download Image",
    data=buf.getvalue(),
    file_name=f"se_builders_{prompt_type.lower().replace(' ', '_')}.png",
    mime="image/png",
    use_container_width=True
)
```

**Performance Characteristics:**
- **Average Response Time:** 40-70 seconds
- **Image Quality:** 1024x1024 or higher
- **Cost per Request:** ~$0.05-0.10 (image generation pricing)

---

### Module 4: Client AI Assistant (`client_assistant.py`)

**Purpose:** 24/7 conversational AI for client inquiries

**AI Model:** Gemini 2.0 Flash (conversational)

**Architecture:**
```
show_client_assistant()
├── SESSION STATE MANAGEMENT
│   ├── Initialize chat history
│   └── Persist across interactions
│
├── KNOWLEDGE BASE
│   ├── Company information
│   ├── Services offered
│   ├── Typical timelines & costs
│   ├── Past projects
│   └── Escalation guidelines
│
├── CHAT INTERFACE
│   ├── Display message history
│   ├── Chat input widget
│   └── Message rendering
│
├── AI PIPELINE
│   ├── Build conversation context
│   ├── Include last N messages
│   ├── Add knowledge base
│   ├── Generate response
│   └── Update chat history
│
└── SIDEBAR FEATURES
    ├── Quick actions
    ├── Common questions
    └── Performance metrics
```

**Pipeline Implementation:**

#### Step 1: Session State Initialization

```python
# Initialize chat history (runs once per session)
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": """Hello! 👋 Welcome to SE Builders.

I'm your AI assistant, here to help answer questions about
our healthcare construction services.

I can help you with:
• Information about our services and expertise
• Project timelines and typical budgets
• Healthcare facility construction requirements
• Past projects and case studies
• Scheduling consultations

How can I assist you today?"""
    })
```

#### Step 2: Knowledge Base Definition

```python
se_builders_context = """
You are an AI assistant for SE Builders, a premier commercial
construction company specializing in healthcare facilities in
Southern California.

COMPANY INFORMATION:
- Company: SE Builders Inc.
- Specialty: Healthcare construction (hospitals, surgery centers, medical offices)
- Service Area: Southern California
- Experience: 15+ years in healthcare construction
- Team: 64+ skilled professionals
- Active Projects: 12 concurrent projects

SERVICES OFFERED:
1. Healthcare Facility Construction
   - Hospitals and hospital additions
   - Outpatient surgery centers
   - Medical office buildings
   - Urgent care facilities
   - Imaging centers
   - Dental offices
   - Laboratories

2. Specialized Healthcare Systems:
   - OSHPD compliance
   - Medical gas systems
   - HVAC with HEPA filtration
   - Emergency power systems
   - Clean rooms and sterile environments

TYPICAL PROJECT TIMELINES:
- Medical Office (10,000-20,000 sq ft): 12-18 months
- Surgery Center (15,000-30,000 sq ft): 18-24 months
- Small Hospital Addition: 24-36 months

TYPICAL INVESTMENT RANGES:
- Medical Office: $250-350 per sq ft
- Surgery Center: $350-500 per sq ft
- Hospital: $500-800+ per sq ft

CONVERSATION GUIDELINES:
1. Be professional, friendly, and helpful
2. Ask clarifying questions to understand client needs
3. Provide accurate information based on context
4. For specific pricing, encourage scheduling a consultation
5. Highlight SE Builders' healthcare expertise
6. When appropriate, suggest:
   - Schedule a consultation
   - See examples of similar projects
   - Get a preliminary cost estimate

ESCALATION TRIGGERS (suggest human contact):
- Client requests specific detailed pricing
- Complex regulatory questions
- Legal or contract discussions
- Project budget exceeds typical ranges
- RFP or formal proposal requested
- Timeline is urgent (less than 6 months)
"""
```

#### Step 3: Chat Interface Rendering

```python
# Create container for chat history
chat_container = st.container()

# Display all messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
```

#### Step 4: User Input Handling

```python
# Chat input (Streamlit built-in widget)
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
```

#### Step 5: AI Response Generation

```python
try:
    # Configure AI
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

    # Build conversation with context
    conversation = se_builders_context + "\n\nCONVERSATION HISTORY:\n"

    # Include last 6 messages for context window
    for msg in st.session_state.messages[-6:]:
        conversation += f"{msg['role'].upper()}: {msg['content']}\n"

    # Add current prompt
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
    # Error handling
    error_msg = "I apologize, but I encountered an error..."
    st.session_state.messages.append({
        "role": "assistant",
        "content": error_msg
    })
    st.rerun()
```

**Key Implementation Details:**

1. **Context Window Management:**
   - Only sends last 6 messages to AI
   - Reduces token usage
   - Maintains conversation context

2. **State Persistence:**
   - Uses `st.session_state` for chat history
   - Persists across page interactions
   - Cleared only when user explicitly clicks "Clear"

3. **Rerun Pattern:**
   - `st.rerun()` refreshes the page after new message
   - Ensures chat history displays correctly
   - Prevents duplicate message rendering

#### Step 6: Quick Actions Sidebar

```python
with col2:
    st.subheader("Quick Actions")

    if st.button("📅 Schedule Consultation"):
        st.info("Contact: (555) 123-4567")

    st.markdown("---")
    st.subheader("Common Questions")

    common_questions = [
        "What types of healthcare facilities do you build?",
        "What is your service area?",
        "How long does a typical medical office take?"
    ]

    for question in common_questions:
        if st.button(f"❓ {question}", key=question):
            # Add question to chat
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })
            st.rerun()
```

**Performance Characteristics:**
- **Average Response Time:** 2-5 seconds
- **Context Window:** Last 6 messages (~1,500 tokens)
- **Cost per Message:** ~$0.001-0.003

---

### Module 5: Safety Scanner (`safety_scanner.py`)

**Purpose:** Computer vision analysis of construction site photos for safety hazards

**AI Model:** Gemini 2.0 Flash (vision capabilities)

**Architecture:**
```
show_safety_scanner()
├── INPUT: Photo upload
│   ├── Project selection
│   ├── Location input
│   └── Multiple file upload
│
├── IMAGE PROCESSING
│   ├── Load images (PIL)
│   ├── Convert to JPEG bytes
│   └── Create image parts
│
├── AI VISION PIPELINE (per photo)
│   ├── Build safety inspection prompt
│   ├── Include image + prompt
│   ├── AI analyzes for hazards
│   └── Returns structured findings
│
├── AGGREGATION
│   ├── Collect results from all photos
│   ├── Generate overall summary
│   └── Calculate safety score
│
└── OUTPUT RENDERING
    ├── Display per-photo results
    ├── Overall summary
    ├── Download report
    └── Safety metrics
```

**Pipeline Implementation:**

#### Step 1: Photo Upload & Metadata

```python
# Project selection
project_name = st.selectbox(
    "Select Project",
    ["Costa Mesa Clinic", "Irvine Surgery Center", ...]
)

# Location input
location = st.text_input(
    "Specific Location/Area",
    placeholder="e.g., 2nd Floor, North Wing, Room 142..."
)

# Multiple file upload
uploaded_files = st.file_uploader(
    "Upload Construction Site Photos",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} photo(s) uploaded")

    # Display thumbnails
    cols = st.columns(min(len(uploaded_files), 4))
    for idx, file in enumerate(uploaded_files):
        with cols[idx % 4]:
            image = Image.open(file)
            st.image(image, caption=file.name)
```

#### Step 2: Safety Inspection Prompt Engineering

```python
# Comprehensive safety analysis prompt
prompt = f"""You are a construction safety inspector analyzing a photo
from a healthcare construction site.

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
OSHA Reference: [standard number]
Recommended Action: [specific corrective action]

---

If no hazards: "✅ NO SAFETY HAZARDS DETECTED - Site appears compliant"
"""
```

**Prompt Engineering Techniques:**
- **Role & Context:** Safety inspector analyzing healthcare construction
- **Structured Categories:** 6 main hazard types
- **Detailed Checklist:** Specific items to look for
- **Output Format:** Clear structure with severity, description, OSHA ref, action
- **Edge Case Handling:** "If NO hazards" clause

#### Step 3: Process Multiple Photos

```python
all_hazards = []

# Process each uploaded photo
for idx, file in enumerate(uploaded_files):
    # Load image
    image = Image.open(file)

    # Convert to bytes for API
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    image_part = {
        "mime_type": "image/jpeg",
        "data": buf.getvalue()
    }

    # Generate analysis for this photo
    response = model.generate_content([image_part, prompt])
    analysis = response.text

    # Store result
    all_hazards.append({
        "file": file.name,
        "analysis": analysis
    })
```

#### Step 4: Generate Overall Summary

```python
# Combine all analyses
combined_text = "\n\n".join([h['analysis'] for h in all_hazards])

# Summary prompt
summary_prompt = f"""Based on these safety scan results from
{len(uploaded_files)} photos:

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
```

#### Step 5: Display Results

```python
# Display per-photo results
for idx, hazard_data in enumerate(all_hazards):
    with st.expander(f"📷 {hazard_data['file']}", expanded=(idx == 0)):
        st.markdown(hazard_data['analysis'])

# Display overall summary
st.markdown("### 📋 Overall Summary")
st.markdown(summary_response.text)
```

#### Step 6: Report Generation & Export

```python
# Create comprehensive report
report_text = f"""SE BUILDERS - SAFETY SCAN REPORT
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

PROJECT: {project_name}
LOCATION: {location if location else 'Not specified'}
PHOTOS ANALYZED: {len(uploaded_files)}

{'=' * 60}

"""

# Add per-photo results
for hazard_data in all_hazards:
    report_text += f"\nPHOTO: {hazard_data['file']}\n"
    report_text += f"{'-' * 60}\n"
    report_text += hazard_data['analysis'] + "\n\n"

# Add summary
report_text += f"\n{'=' * 60}\n\nOVERALL SUMMARY\n{'-' * 60}\n"
report_text += summary_response.text

# Download button
st.download_button(
    label="📥 Download Report",
    data=report_text,
    file_name=f"Safety_Report_{project_name}_{datetime.now().strftime('%Y%m%d')}.txt",
    mime="text/plain"
)
```

**Performance Characteristics:**
- **Analysis Time:** 15-30 seconds per photo
- **Batch Capability:** Multiple photos processed sequentially
- **Cost per Photo:** ~$0.01-0.02 (vision model pricing)
- **Accuracy:** High detection rate for visible hazards

---

## 📈 Data Flow Diagrams

### Cost Estimator Flow

```
┌──────────────┐
│     USER     │
└──────┬───────┘
       │
       │ (1) Fills form
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  - Facility type     │
│  - Square footage    │
│  - Location          │
│  - Special reqs      │
└──────┬───────────────┘
       │
       │ (2) Click "Generate"
       ▼
┌──────────────────────┐
│  app.py              │
│  - Validate inputs   │
│  - Build prompt      │
└──────┬───────────────┘
       │
       │ (3) API Request
       ▼
┌──────────────────────┐
│  Google Gemini API   │
│  - Process prompt    │
│  - Generate estimate │
└──────┬───────────────┘
       │
       │ (4) Response (JSON/Text)
       ▼
┌──────────────────────┐
│  app.py              │
│  - Parse response    │
│  - Format display    │
└──────┬───────────────┘
       │
       │ (5) Render result
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  - Show estimate     │
│  - Download button   │
└──────────────────────┘
```

### Social Media Generator Flow

```
┌──────────────┐
│     USER     │
└──────┬───────┘
       │
       │ (1) Select template, upload images
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  - Template dropdown │
│  - File uploaders    │
└──────┬───────────────┘
       │
       │ (2) Click "Generate"
       ▼
┌──────────────────────┐
│  app.py              │
│  - Load images (PIL) │
│  - Convert to bytes  │
│  - Select prompt     │
└──────┬───────────────┘
       │
       │ (3) API Request (multipart)
       │     [image1, image2, prompt]
       ▼
┌──────────────────────┐
│  Google Gemini API   │
│  - Analyze images    │
│  - Generate new img  │
└──────┬───────────────┘
       │
       │ (4) Response (image bytes)
       ▼
┌──────────────────────┐
│  app.py              │
│  - Extract image     │
│  - Convert to PIL    │
└──────┬───────────────┘
       │
       │ (5) Display & download
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  - Show image        │
│  - Download button   │
└──────────────────────┘
```

### Client Assistant Flow

```
┌──────────────┐
│     USER     │
└──────┬───────┘
       │
       │ (1) Type message
       ▼
┌──────────────────────┐
│  Streamlit Chat UI   │
│  - Chat input        │
└──────┬───────────────┘
       │
       │ (2) Submit message
       ▼
┌──────────────────────┐
│  Session State       │
│  - Append to history │
│  - messages array    │
└──────┬───────────────┘
       │
       │ (3) Build context
       ▼
┌──────────────────────┐
│  app.py              │
│  - Knowledge base +  │
│  - Last 6 messages   │
└──────┬───────────────┘
       │
       │ (4) API Request
       ▼
┌──────────────────────┐
│  Google Gemini API   │
│  - Conversational AI │
└──────┬───────────────┘
       │
       │ (5) Response
       ▼
┌──────────────────────┐
│  Session State       │
│  - Append response   │
└──────┬───────────────┘
       │
       │ (6) Rerun app
       ▼
┌──────────────────────┐
│  Streamlit Chat UI   │
│  - Display history   │
└──────────────────────┘
```

### Safety Scanner Flow

```
┌──────────────┐
│     USER     │
└──────┬───────┘
       │
       │ (1) Upload photos
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  - File uploader     │
│  - Multiple files    │
└──────┬───────────────┘
       │
       │ (2) Click "Scan"
       ▼
┌──────────────────────┐
│  app.py              │
│  - Loop through files│
└──────┬───────────────┘
       │
       │ For each photo:
       ▼
┌──────────────────────┐
│  Image Processing    │
│  - Load with PIL     │
│  - Convert to bytes  │
└──────┬───────────────┘
       │
       │ (3) API Request (vision)
       │     [image, prompt]
       ▼
┌──────────────────────┐
│  Google Gemini API   │
│  - Analyze photo     │
│  - Detect hazards    │
└──────┬───────────────┘
       │
       │ (4) Response (text)
       ▼
┌──────────────────────┐
│  app.py              │
│  - Store result      │
│  - all_hazards[]     │
└──────┬───────────────┘
       │
       │ After all photos:
       │ (5) Generate summary
       ▼
┌──────────────────────┐
│  Google Gemini API   │
│  - Aggregate results │
└──────┬───────────────┘
       │
       │ (6) Display
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  - Per-photo results │
│  - Overall summary   │
│  - Download report   │
└──────────────────────┘
```

---

## 🔌 API Integration

### Google Gemini API Setup

#### Installation

```bash
pip install google-generativeai
```

#### Configuration

```python
import google.generativeai as genai
import os

# Load API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
```

#### Model Selection

```python
# Text generation and vision
model_text = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

# Image generation
model_image = genai.GenerativeModel(model_name="gemini-2.5-flash-image")
```

### API Request Patterns

#### Text Generation

```python
# Simple text prompt
response = model.generate_content("Your prompt here")
text_result = response.text

# With configuration
response = model.generate_content(
    "Your prompt",
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 2048
    }
)
```

#### Vision (Image Analysis)

```python
# Image + text prompt
image_part = {
    "mime_type": "image/jpeg",
    "data": image_bytes
}

response = model.generate_content([image_part, "Analyze this image"])
analysis = response.text
```

#### Image Generation

```python
# Text prompt + reference images
parts = [
    {"mime_type": "image/jpeg", "data": ref_image1},
    {"mime_type": "image/png", "data": ref_image2},
    "Generate an image based on these references..."
]

response = model.generate_content(contents=parts)

# Extract generated image
for part in response.candidates[0].content.parts:
    if hasattr(part, "inline_data"):
        generated_image_bytes = part.inline_data.data
```

### Rate Limiting & Best Practices

```python
import time

# Add retry logic
max_retries = 3
for attempt in range(max_retries):
    try:
        response = model.generate_content(prompt)
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
```

### Error Handling

```python
from google.generativeai.types import BlockedPromptException

try:
    response = model.generate_content(prompt)
except BlockedPromptException:
    st.error("Content was blocked by safety filters")
except Exception as e:
    st.error(f"API Error: {str(e)}")
```

---

## ⚙️ Setup & Configuration

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- Google Cloud account with Gemini API access

### Step-by-Step Setup

#### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Hospital-Construction-Builders.git
cd Hospital-Construction-Builders
```

#### 2. Install Dependencies

**Using pip:**
```bash
pip install python-dotenv google-generativeai pillow streamlit
```

**Using uv (faster):**
```bash
uv pip install python-dotenv google-generativeai pillow streamlit
```

**Using project file:**
```bash
pip install -e .
```

#### 3. Get Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Navigate to "Get API Key"
4. Create a new API key
5. Copy the key

#### 4. Configure Environment

Create `.env` file in project root:

```bash
# .env
GOOGLE_API_KEY=your_api_key_here
```

**Important:** Add `.env` to `.gitignore` to avoid exposing API keys

```bash
# .gitignore
.env
*.pyc
__pycache__/
.DS_Store
```

#### 5. Verify Installation

```bash
python -c "import streamlit; import google.generativeai; print('✅ All dependencies installed')"
```

#### 6. Run Application

```bash
streamlit run app.py
```

Application should open in browser at `http://localhost:8501`

### Configuration Options

#### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#f97316"  # SE Builders orange
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f9ff"
textColor = "#1e3a8a"  # Navy blue

[server]
port = 8501
enableCORS = false
```

#### Environment Variables

```bash
# .env

# Required
GOOGLE_API_KEY=your_api_key

# Optional (future enhancements)
DATABASE_URL=postgresql://...
CRM_API_KEY=...
EMAIL_API_KEY=...
```

---

## 🚀 Deployment Guide

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Add secrets in dashboard:
   ```
   GOOGLE_API_KEY = "your_api_key"
   ```
5. Deploy

**Advantages:**
- Free hosting
- Automatic SSL
- Easy updates via git push
- Built-in authentication

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build & Run:**
```bash
docker build -t se-builders-ai .
docker run -p 8501:8501 --env-file .env se-builders-ai
```

### Production Considerations

1. **Security:**
   - Use secrets management (not .env in production)
   - Implement authentication
   - Add rate limiting

2. **Performance:**
   - Enable caching with `@st.cache_data`
   - Use async API calls where possible
   - Implement request queuing

3. **Monitoring:**
   - Log all API requests
   - Track error rates
   - Monitor costs (API usage)

4. **Scalability:**
   - Consider load balancing for high traffic
   - Implement API request batching
   - Cache common responses

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError: No module named 'google.generativeai'`

**Solution:**
```bash
pip install google-generativeai
```

#### Issue: `GOOGLE_API_KEY not found`

**Solution:**
1. Create `.env` file in project root
2. Add: `GOOGLE_API_KEY=your_key_here`
3. Verify file is in same directory as `app.py`

#### Issue: Streamlit not loading modules

**Solution:**
```bash
# Ensure modules directory exists
ls modules/

# Check __init__.py exists
ls modules/__init__.py

# Restart Streamlit
streamlit run app.py
```

#### Issue: Image upload failing

**Solution:**
- Check file size (< 10MB recommended)
- Verify file format (PNG, JPEG only)
- Ensure PIL is installed: `pip install Pillow`

#### Issue: Chat messages displaying incorrectly

**Solution:**
- Clear session state: Click "Clear Conversation"
- Refresh browser page
- Check Streamlit version: `streamlit version` (should be 1.28+)

#### Issue: API rate limit exceeded

**Solution:**
```python
# Add rate limiting in code
import time

time.sleep(1)  # Wait 1 second between requests
```

#### Issue: Slow AI responses

**Possible causes:**
- Large prompt/context
- High API load
- Network latency

**Solutions:**
- Reduce context window (fewer messages)
- Use faster model (already using Flash)
- Check internet connection

### Debug Mode

Enable debug mode to see detailed logs:

```bash
streamlit run app.py --logger.level=debug
```

### Performance Profiling

```python
import time

start = time.time()
response = model.generate_content(prompt)
end = time.time()

st.write(f"Request took {end - start:.2f} seconds")
```

---

## 📊 Cost Analysis

### API Pricing (Approximate)

**Gemini 2.0 Flash:**
- Input: $0.075 per 1M tokens
- Output: $0.30 per 1M tokens

**Gemini 2.5 Flash Image:**
- Generation: ~$0.05-0.10 per image

### Cost Per Request

| Module | Avg Tokens | Estimated Cost |
|--------|------------|----------------|
| Cost Estimator | 3,000 | $0.01 |
| Social Media | N/A (image) | $0.08 |
| Client Assistant | 1,500 | $0.003 |
| Safety Scanner | 2,000/photo | $0.015 |

### Monthly Cost Estimates

**Low Usage (50 requests/month):**
- Cost Estimator: 20 requests × $0.01 = $0.20
- Social Media: 10 requests × $0.08 = $0.80
- Client Assistant: 150 messages × $0.003 = $0.45
- Safety Scanner: 20 photos × $0.015 = $0.30
- **Total: ~$2/month**

**Medium Usage (500 requests/month):**
- **Total: ~$20/month**

**High Usage (2000 requests/month):**
- **Total: ~$80/month**

---

## 🔐 Security Best Practices

### API Key Management

**✅ DO:**
- Store in `.env` file
- Use environment variables
- Never commit to git
- Rotate keys regularly

**❌ DON'T:**
- Hardcode in source code
- Share in public repositories
- Include in client-side code
- Use production keys in development

### Input Validation

```python
# Validate user inputs
if not project_name or len(project_name) < 3:
    st.error("Project name must be at least 3 characters")
    return

# Sanitize file uploads
if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
    st.error("File too large")
    return
```

### Rate Limiting

```python
# Implement simple rate limiting
if "last_request" in st.session_state:
    time_since_last = time.time() - st.session_state.last_request
    if time_since_last < 2:  # Minimum 2 seconds between requests
        st.warning("Please wait before making another request")
        return

st.session_state.last_request = time.time()
```

---

## 📝 Development Guidelines

### Code Style

**Follow PEP 8:**
- 4 spaces for indentation
- Max line length: 100 characters
- Descriptive variable names
- Type hints where applicable

**Example:**
```python
def process_image(
    image: Image.Image,
    mime_type: str = "image/png"
) -> dict[str, any]:
    """
    Convert PIL Image to API-compatible format.

    Args:
        image: PIL Image object
        mime_type: MIME type string

    Returns:
        Dictionary with mime_type and data keys
    """
    # Implementation
```

### Testing

**Manual Testing Checklist:**
- [ ] All modules load without errors
- [ ] API calls succeed with valid inputs
- [ ] Error handling works for invalid inputs
- [ ] UI renders correctly on different screen sizes
- [ ] File uploads work for various formats
- [ ] Session state persists across interactions

**Future: Automated Testing**
```python
# tests/test_cost_estimator.py
def test_cost_estimator_valid_input():
    result = generate_estimate(
        facility_type="Hospital",
        square_footage=50000,
        location="Orange County"
    )
    assert result is not None
    assert "cost" in result.lower()
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-module

# Make changes
git add .
git commit -m "Add new module for X"

# Push to remote
git push origin feature/new-module

# Create pull request on GitHub
```

---

## 🎯 Next Steps & Roadmap

### Phase 2 (Q2 2025)
- [ ] Real database integration
- [ ] User authentication
- [ ] CRM integration (Salesforce/HubSpot)
- [ ] Email notifications
- [ ] Mobile app (React Native)

### Phase 3 (Q3 2025)
- [ ] Project management integration (Procore)
- [ ] Document intelligence (RFP parsing)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

### Phase 4 (Q4 2025)
- [ ] Predictive analytics
- [ ] BIM integration
- [ ] IoT sensor data
- [ ] Drone footage analysis

---

## 📚 Additional Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [PIL/Pillow Docs](https://pillow.readthedocs.io)

### Tutorials
- [Streamlit Tutorial](https://docs.streamlit.io/get-started/tutorials)
- [Gemini API Quickstart](https://ai.google.dev/tutorials/python_quickstart)

### Community
- [Streamlit Forum](https://discuss.streamlit.io)
- [Google AI Forum](https://discuss.ai.google.dev)

---

## 👨‍💻 Support & Contact

**Developer:** [Your Name]
**Email:** your.email@example.com
**GitHub:** [@yourusername](https://github.com/yourusername)

**SE Builders:**
**Website:** [SE Builders](#)
**Location:** Southern California

---

*Last Updated: January 2025*
*Version: 1.0*
*License: Proprietary - SE Builders AI Platform Demo*
