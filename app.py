
import streamlit as st
import cohere
import PyPDF2

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
        **Roast this resume like a savage Reddit comment.** Be brutal, funny, and concise. Focus on common resume mistakes like buzzwords, vague descriptions, and questionable skills. Act like a ruthless Redditor who's seen it all.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Savage Roast:**
        """,
        
        "recruiter": """
        **Roast this resume from a recruiter's perspective.** Be brutally honest about what makes recruiters cringe. Focus on formatting disasters, skill inflation, and red flags that would make you instantly reject this candidate. Write like a tired recruiter who's seen thousands of bad resumes.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Recruiter's Brutal Honest Take:**
        """,
        
        "tech_bro": """
        **Roast this resume like a condescending tech bro.** Be sarcastic about their tech stack, question their experience levels, and mock their project descriptions. Use tech industry slang and act superior about your own expertise.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Tech Bro Roast:**
        """,
        
        "career_coach": """
        **Roast this resume like a passive-aggressive career coach.** Point out all the things they're doing wrong while pretending to be helpful. Be condescending about their career choices and formatting decisions. Use phrases like "Well, actually..." and "You might want to consider..."

        **Resume Text:**
        ---
        {resume_text}
        ---

        **Career Coach's "Helpful" Feedback:**
        """,
        
        "linkedin_influencer": """
        **Roast this resume like a LinkedIn influencer.** Be overly dramatic about their career journey, use excessive buzzwords, and make everything sound like a motivational post gone wrong. Start with "Agree?" and use lots of emojis in your critique.

        **Resume Text:**
        ---
        {resume_text}
        ---

        **LinkedIn Influencer's Hot Take:**
        """
    }

    prompt = roast_prompts[roast_type].format(resume_text=resume_text)

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=300,
            temperature=0.9,
            k=0,
            p=0.75,
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
    """Creates a Reddit-style comment component."""
    return f"""
    <div style="background-color: #ffffff; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 20px; margin-right: 8px;">{avatar_emoji}</span>
            <span style="font-weight: bold; color: #1a1a1b; margin-right: 8px;">u/{username}</span>
            <span style="color: #878a8c; font-size: 12px;">• 2h</span>
        </div>
        <p style="color: #1c1c1c; font-family: 'Segoe UI', sans-serif; line-height: 1.5; margin-bottom: 15px;">{roast_text}</p>
        <div style="display: flex; align-items: center; color: #878a8c; font-size: 12px;">
            <span style="margin-right: 15px; color: #ff4500;">▲ {upvotes}</span>
            <span style="margin-right: 15px; color: #7193ff;">▼</span>
            <span style="margin-right: 15px; cursor: pointer;">💬 Reply</span>
            <span style="margin-right: 15px; cursor: pointer;">🔗 Share</span>
            <span style="margin-right: 15px; cursor: pointer;">⭐ Save</span>
            <span style="cursor: pointer;">🏆 Award</span>
        </div>
    </div>
    """


# --- Main Logic ---
if uploaded_file is not None:
    with st.spinner("Generating roasts... 🔥"):
        resume_text = extract_text_from_pdf(uploaded_file)

        if resume_text:
            st.subheader("🔥 r/RoastMyResume Comment Section")
            st.markdown("---")
            
            # Generate different types of roasts
            roast_configs = [
                ("RecruitmentReality", "savage", "😤", 247),
                ("TechStackSnob", "tech_bro", "🤓", 189),
                ("CareerCoachKaren", "career_coach", "💼", 156),
                ("LinkedInInfluencer", "linkedin_influencer", "📈", 134),
                ("HiringManagerHell", "recruiter", "�", 203)
            ]
            
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
            <div style="text-align: center; color: #878a8c; font-size: 12px; margin-top: 20px;">
                <p>Want to roast more resumes? Upload another one! 🔥</p>
                <p>Remember: This is just for fun. Your resume might actually be decent... maybe. 😉</p>
            </div>
            """, unsafe_allow_html=True)
