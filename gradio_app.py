import gradio as gr
import requests
import json

SYSTEM_PROMPT = """You are the official "CGC Career Coach", an AI-powered, highly specialized career mentor exclusively for students of CGC University (Chandigarh Group of Colleges, Mohali).

Your mission is to provide deeply contextualized, highly specific career guidance that leverages actual CGC infrastructure, culture, and placement processes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. CGC-SPECIFIC KNOWLEDGE BASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You must actively integrate these CGC Mohali facts into your advice naturally:
- PLACEMENTS (TPP): CGC's Training and Placement Program (TPP) is rigorous. Remind students to actively participate in TPP mock interviews and aptitude tests.
- RECRUITERS: Reference CGC's major mass and premium recruiters (e.g., Wipro, Infosys, Cognizant, TCS, Amazon, Microsoft, Capgemini, Deloitte, IBM). Mention the legacy of 1 Crore+ premium packages for motivation.
- CAMPUS LIFE & CLUBS: Advise students to build their resume by joining active CGC clubs like 'CodeBoom' or 'Kerberos' (for tech/coding), and 'Virasat' or 'Rangmanch' (for cultural/soft skills). 
- EVENTS: Mention participating in major CGC events and hackathons like the annual 'Parivartan' fest to build networking and leadership skills.
- COURSES: You are aware that CGC is renowned for B.Tech (CSE, AI/ML, IT), BCA, MCA, Pharmacy, and Management (BBA/MBA).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. CORE AI TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- INTERVIEWS: Give mock interview questions specifically tailored to the companies that visit the CGC Mohali campus.
- SKILL GAP: Do not give generic advice (like "learn Python"). Give specific, project-based advice (e.g., "Build a full-stack React app for your 6th-semester major project to impress Capgemini recruiters").
- ROADMAP: Create semester-appropriate learning plans aligned with standard Indian university curriculums.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. STRICT TONE & GUARDRAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- BREVITY: Keep all responses extremely concise and brief. Use short bullet points. Do not write long essays or paragraphs. Get straight to the point.
- NO EMOJIS: Do NOT use emojis. Maintain a professional, academic, and highly focused tone. You are a serious career mentor, not a social media bot.
- NO GENERIC FILLER: Avoid generic motivational fluff. Be direct, actionable, and specific.
- PERSONALIZATION: Always ask for the student's current semester and specific branch (e.g., "Are you in B.Tech CSE or BCA?") before giving detailed roadmaps.
- GUARDRAIL: Do not guarantee jobs or salaries.
"""

def chat_func(message, history):
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            for h in history:
                if isinstance(h, dict):
                    role = h.get("role", "user")
                    messages.append({"role": role, "content": h.get("content", "")})
                elif isinstance(h, (list, tuple)) and len(h) >= 2:
                    messages.append({"role": "user", "content": h[0]})
                    messages.append({"role": "assistant", "content": h[1]})
                    
        messages.append({"role": "user", "content": message})
        
        # 🚀 KEYLESS HACKATHON MAGIC v2! 
        # Using Pollinations.ai which acts as a completely free, unlimited OpenAI proxy.
        response = requests.post(
            "https://text.pollinations.ai/",
            json={"messages": messages, "model": "openai"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.text
        else:
            return f"API Error: Server returned {response.status_code}"
                    
    except Exception as e:
        return f"Network Error: {str(e)} - Please check your university wifi."

# Jet Black and Emerald Green Theme
custom_theme = gr.themes.Monochrome(
    font=[gr.themes.GoogleFont('Inter'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
    radius_size=gr.themes.sizes.radius_sm,
).set(
    body_background_fill="#000000",
    block_background_fill="#0a0a0a",
    block_border_width="1px",
    block_border_color="#27272a",
    button_primary_background_fill="#10b981",
    button_primary_background_fill_hover="#059669",
    button_primary_text_color="#000000",
    block_title_text_color="#10b981",
    block_label_text_color="#10b981",
    input_background_fill="#000000",
)

# Minimalist Jet Black CSS
css = """
body { font-family: 'Inter', sans-serif; background-color: #000000 !important; color: #e4e4e7; }
.header-container { text-align: center; padding: 2rem 2rem 1rem 2rem; background: transparent; margin-bottom: 0.5rem; }
.header-container h1 { margin: 0; font-weight: 800; font-size: 2.5rem; letter-spacing: -0.05em; color: #ffffff; }
.header-container p { font-size: 1rem; color: #10b981; margin-top: 0.75rem; font-weight: 500; }
.gradio-container { max-width: 1200px !important; margin: auto; }
.chat-container { border: 1px solid #27272a !important; box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.8); border-radius: 12px; overflow: hidden; background: #0a0a0a !important; margin-top: 1rem; }
input[type="text"], textarea { background-color: #000000 !important; color: #ffffff !important; box-shadow: none !important; border: 1px solid #27272a !important; border-radius: 6px !important; transition: all 0.2s ease; }
input:focus, textarea:focus { border-color: #10b981 !important; box-shadow: 0 0 0 1px #10b981 !important; }
button.primary { font-weight: 600 !important; letter-spacing: -0.02em !important; color: #000000 !important; }
"""

with gr.Blocks(theme=custom_theme, css=css) as demo:
    gr.HTML("""
    <div class="header-container">
        <h1>CGC AI Career Coach</h1>
        <p>⚡ Powered by Keyless GPT-4o-Mini Architecture</p>
    </div>
    """)
    
    with gr.Column(elem_classes="chat-container"):
        gr.ChatInterface(
            fn=chat_func,
            chatbot=gr.Chatbot(height=650, show_label=False)
        )

if __name__ == "__main__":
    demo.launch(inbrowser=True, theme=custom_theme, css=css)
