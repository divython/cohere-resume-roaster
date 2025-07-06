import streamlit as st
import cohere
import PyPDF2

# Add custom CSS for better dark theme support
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp {
        background-color: #0d1117;
    }
    
    .stSelectbox > div > div {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    .stRadio > div {
        background-color: #21262d;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    
    .stSpinner > div {
        color: #ff4500 !important;
    }
    
    /* Make comment boxes properly sized */
    div[data-testid="stMarkdownContainer"] div {
        max-width: 100% !important;
        width: fit-content !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Configuration ---
# It's recommended to use Streamlit's secrets management for API keys
# For development, you can set it as an environment variable or directly here
try:
    cohere_api_key = st.secrets["COHERE_API_KEY"]
except KeyError:
    st.error("Cohere API key not found. Please add it to your Streamlit secrets.")
    # For local development, you might use an alternative way to get the key
    # from cohere.errors.cohere_error import CohereError
    # cohere_api_key = "YOUR_FALLBACK_API_KEY" # Replace with your key if needed for local testing

co = cohere.Client(cohere_api_key)

# --- App Layout and Styling ---
st.set_page_config(page_title="Resume Roaster", page_icon="🔥", layout="centered")

st.title("🔥 Resume Roaster")
st.markdown("""
**Upload your resume and watch it get absolutely destroyed by our AI Reddit comment section!**

Get roasted by different perspectives:
- 😤 **Savage Redditors** - No mercy, just pure brutality
- 🤓 **Tech Bros** - Condescending expertise gatekeeping  
- 💼 **Career Coaches** - Passive-aggressive "helpful" advice
- 📈 **LinkedIn Influencers** - Overly dramatic hot takes
- 💀 **Recruiters** - Tired professionals who've seen it all

*Warning: Contains strong language and brutal honesty. Not for the faint of heart!*
""")

st.markdown("---")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a resume file (PDF)", type="pdf")

# --- Roast Type Selection ---
if uploaded_file is not None:
    st.markdown("### 🎯 Choose Your Roast Style")
    roast_option = st.radio(
        "Pick your poison:",
        options=["All Perspectives", "Savage Redditor", "Tech Bro", "Career Coach", "LinkedIn Influencer", "Recruiter"],
        index=0,
        help="Select how you want to get roasted!"
    )

def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def generate_roast(resume_text, roast_type):
    """Generates a roast for the resume using Cohere with different perspectives."""
    if not resume_text:
        return "Could not read any text from the resume. Is it empty or just a picture?"

    roast_prompts = {
        "savage": """
        **Roast this resume like the most savage, brutal Reddit comment ever.** Be absolutely ruthless, hilarious, and devastating. Don't hold back - tear apart every buzzword, every skill claim, every job description. Make it hurt but make it funny. Use internet slang and be merciless.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Savage Roast (be absolutely brutal):**
        """,
        
        "recruiter": """
        **Roast this resume as a recruiter who's completely fed up with terrible resumes.** Be brutally honest about formatting disasters, obvious lies, skill inflation, and red flags that scream "immediate rejection." Channel your inner rage from seeing thousands of awful resumes. Be harsh and specific.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Recruiter's Brutal Reality Check:**
        """,
        
        "tech_bro": """
        **Roast this resume like the most arrogant, condescending tech bro ever.** Be absolutely savage about their tech stack, mock their experience levels brutally, and tear apart their project descriptions. Use heavy tech industry gatekeeping and act like you're infinitely superior. Be ruthless.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Tech Bro's Savage Takedown:**
        """,
        
        "career_coach": """
        **Roast this resume as a passive-aggressive career coach who's secretly furious.** Be brutally condescending while pretending to be helpful. Savage their career choices, destroy their formatting decisions, and be ruthlessly sarcastic. Use phrases like "Well, actually..." but make it hurt.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Career Coach's Savage "Help":**
        """,
        
        "linkedin_influencer": """
        **Roast this resume like a LinkedIn influencer having a complete meltdown.** Be overly dramatic and brutal about their career journey, use excessive buzzwords sarcastically, and make everything sound like a motivational disaster. Start with "Agree?" and absolutely destroy them with fake positivity.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **LinkedIn Influencer's Savage Hot Take:**
        """
    }

    prompt = roast_prompts[roast_type].format(resume_text=resume_text)

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=400,
            temperature=0.95,
            k=0,
            p=0.8,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        roast = response.generations[0].text.strip()
        return roast
    except cohere.errors.CohereError as e:
        st.error(f"An error occurred with the Cohere API: {e}")
        return "The roast master is taking a break. Please try again later."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "Something went wrong. Could not generate a roast."


def create_reddit_comment(username, roast_text, upvotes, avatar_emoji):
    """Creates a Reddit-style comment component with dark theme support."""
    return f"""
    <div style="background-color: var(--background-color, #1a1a1b); border-radius: 8px; padding: 12px; margin-bottom: 12px; border: 1px solid var(--border-color, #343536); width: fit-content; max-width: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 18px; margin-right: 6px;">{avatar_emoji}</span>
            <span style="font-weight: bold; color: var(--text-color, #d7dadc); margin-right: 6px; font-size: 13px;">u/{username}</span>
            <span style="color: var(--secondary-text-color, #818384); font-size: 11px;">• 2h</span>
        </div>
        <p style="color: var(--text-color, #d7dadc); font-family: 'Segoe UI', sans-serif; line-height: 1.4; margin-bottom: 10px; font-size: 14px; word-wrap: break-word;">{roast_text}</p>
        <div style="display: flex; align-items: center; color: var(--secondary-text-color, #818384); font-size: 11px;">
            <span style="margin-right: 12px; color: #ff4500; font-weight: bold;">▲ {upvotes}</span>
            <span style="margin-right: 12px; color: #7193ff;">▼</span>
            <span style="margin-right: 12px; cursor: pointer;">💬 Reply</span>
            <span style="margin-right: 12px; cursor: pointer;">🔗 Share</span>
            <span style="margin-right: 12px; cursor: pointer;">⭐ Save</span>
            <span style="cursor: pointer;">🏆 Award</span>
        </div>
    </div>
    """


# --- Main Logic ---
if uploaded_file is not None and 'roast_option' in locals():
    with st.spinner("Generating roasts... 🔥"):
        resume_text = extract_text_from_pdf(uploaded_file)

        if resume_text:
            st.subheader("🔥 r/RoastMyResume Comment Section")
            st.markdown("---")
            
            # Define all roast configurations
            all_roast_configs = [
                ("SavageRedditor2024", "savage", "😤", 547),
                ("TechStackElitist", "tech_bro", "🤓", 389),
                ("CareerCoachKaren", "career_coach", "💼", 256),
                ("LinkedInInfluencer", "linkedin_influencer", "📈", 234),
                ("RecruiterFromHell", "recruiter", "💀", 403)
            ]
            
            # Filter roast configs based on selection
            if roast_option == "All Perspectives":
                roast_configs = all_roast_configs
            else:
                roast_type_map = {
                    "Savage Redditor": "savage",
                    "Tech Bro": "tech_bro", 
                    "Career Coach": "career_coach",
                    "LinkedIn Influencer": "linkedin_influencer",
                    "Recruiter": "recruiter"
                }
                selected_type = roast_type_map[roast_option]
                roast_configs = [config for config in all_roast_configs if config[1] == selected_type]
            
            # Create progress bar for generating roasts
            progress_bar = st.progress(0)
            
            for i, (username, roast_type, emoji, upvotes) in enumerate(roast_configs):
                roast_text = generate_roast(resume_text, roast_type)
                
                # Create Reddit-style comment
                comment_html = create_reddit_comment(username, roast_text, upvotes, emoji)
                st.markdown(comment_html, unsafe_allow_html=True)
                
                # Update progress bar
                progress_bar.progress((i + 1) / len(roast_configs))
            
            # Remove progress bar when done
            progress_bar.empty()
            
            # Add some Reddit-style footer
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: var(--secondary-text-color, #818384); font-size: 12px; margin-top: 20px;">
                <p>🔥 Want to get roasted differently? Try another perspective! 🔥</p>
                <p>Remember: This is just for fun. Your resume might actually be decent... probably not though. 😈</p>
            </div>
            """, unsafe_allow_html=True)