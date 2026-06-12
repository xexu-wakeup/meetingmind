import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="MeetingMind",
    page_icon="🧠",
    layout="centered"
)

# Styling
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        width: 100%;
        padding: 12px;
        font-size: 18px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🧠 MeetingMind")
st.subheader("Paste your meeting notes. Get your action plan instantly.")
st.markdown("---")

# Disclaimer
st.info(
    "⚠️ AI-generated output. "
    "Always review before acting. "
    "MeetingMind is a drafting assistant, "
    "not a decision-making tool."
)

# API Key input
api_key = st.text_input(
    "Enter your Gemini API Key",
    type="password",
    placeholder="AIzaSy...",
    help="Get your free key at aistudio.google.com"
)

# Meeting input
transcript = st.text_area(
    "📋 Paste your meeting notes or transcript here",
    height=250,
    placeholder="""Example:
John said we need to delay the launch by one week.
Sarah will redesign the landing page by Friday.
Mike needs to update all the ads by Wednesday.
We are waiting on vendor assets before we can proceed.
Budget approved at $50,000.
Next meeting is Thursday at 3pm."""
)

# Generate button
if st.button("⚡ Extract Action Plan"):

    if not api_key:
        st.warning("Please enter your Gemini API key above.")

    elif not transcript:
        st.warning("Please paste your meeting notes above.")

    else:
        with st.spinner("Extracting your action plan..."):

            try:
                # Configure Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                # The prompt
                prompt = f"""
You are an expert meeting analyst.
Analyze the following meeting notes and extract:

1. DECISIONS MADE
   List every decision that was confirmed.

2. ACTION ITEMS
   List every task with:
   - What needs to be done
   - Who is responsible
   - Deadline if mentioned

3. BLOCKERS
   List anything blocking progress.

4. FOLLOW UP EMAIL
   Write a short professional follow-up
   email summarizing the meeting outcomes
   ready to send to all attendees.

Format everything clearly with
emojis and headers.
Be specific. Use exact names and
details from the notes.

Meeting Notes:
{transcript}
"""

                # Call Gemini
                response = model.generate_content(prompt)
                result = response.text

                # Display output
                st.markdown("---")
                st.success("✅ Action Plan Ready!")
                st.markdown(result)

                # Copy hint
                st.markdown("---")
                st.info(
                    "💡 Select all text above to copy "
                    "and paste into Notion, Slack, "
                    "or your project management tool."
                )

            except Exception as e:
                st.error(
                    f"Something went wrong: {e} "
                    "Please check your API key and try again."
                )

# Footer
st.markdown("---")
st.markdown(
    "<center>🧠 MeetingMind — Free forever. "
    "Built for professionals.</center>",
    unsafe_allow_html=True
)
