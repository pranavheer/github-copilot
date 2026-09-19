import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Career Coach", page_icon="🎓", layout="centered")

# --- SYSTEM PROMPTS (The 'Brain' of our Agents) ---
PROMPTS = {
    "Primary School (Ages 5-11)": """You are an enthusiastic, fun, and encouraging Career Explorer for young children. 
Your goal is to help them discover their interests. 
Rules:
1. Use simple language and lots of emojis.
2. Ask fun 'Would you rather' questions (e.g., 'Would you rather talk to animals or build a robot?').
3. Relate their answers to broad, exciting job categories (like Science, Art, Helping people, Building things).
4. Keep your responses short (2-3 sentences max).""",

    "Secondary/High School (Ages 12-17)": """You are a supportive and knowledgeable Career Navigator for high school students. 
Your goal is to help them map their current interests and subjects to potential careers.
Rules:
1. Be encouraging and structured.
2. Ask about their favorite subjects in school, hobbies, or what they care about in the world.
3. Suggest 2-3 potential career paths that match their interests and explain briefly what those jobs actually do.
4. Suggest high school clubs, easy extracurriculars, or simple online skills they could learn to explore these paths.""",

    "Higher Education (Ages 18+)": """You are a professional, strategic, and direct Career Coach for college students and recent graduates.
Your goal is to help them land internships or entry-level jobs and build their professional profile.
Rules:
1. Maintain a professional, actionable tone.
2. Offer to do mock interview questions, review their resume structure, or help them write cold networking emails.
3. If they state a career goal, perform a quick skill-gap analysis (what skills they likely need vs what they have).
4. Give concrete, industry-standard advice."""
}

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Input for API Key so you don't need a .env file for the hackathon
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")
    st.markdown("Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    
    # Dropdown to select the target audience
    education_level = st.selectbox(
        "Select Education Level",
        options=list(PROMPTS.keys()),
        index=1
    )
    
    # Clear chat history if the education level changes (to swap personas cleanly)
    if "current_level" not in st.session_state:
        st.session_state.current_level = education_level
        
    if st.session_state.current_level != education_level:
        st.session_state.messages = []
        st.session_state.current_level = education_level
        
    st.divider()
    st.markdown("Built for the Hackathon 🚀")

# --- MAIN APP UI ---
st.title("🎓 AI Career Coach")
st.markdown(f"**Current Mode:** {education_level}")

# Initialize chat history array in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User chat input at the bottom
if prompt := st.chat_input("Ask your career coach a question..."):
    
    # Check if API key is provided
    if not api_key:
        st.warning("Please enter your Google Gemini API key in the sidebar to start chatting.")
        st.stop()
        
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # We use Gemini 1.5 Flash as it is fast and perfect for this use case
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PROMPTS[education_level])

    # Display user's prompt in the chat UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the AI's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Format history for Gemini API
            formatted_history = []
            for msg in st.session_state.messages[:-1]: # Exclude the current prompt we just added
                role = "model" if msg["role"] == "assistant" else "user"
                formatted_history.append({"role": role, "parts": [msg["content"]]})
                
            # Start a chat session with history
            chat = model.start_chat(history=formatted_history)
            
            # Send message and stream response
            response = chat.send_message(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌") # Show typing effect
            
            # Finalize message text
            message_placeholder.markdown(full_response)
            
            # Save AI response to session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred with the AI API: {e}")
