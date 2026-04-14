import streamlit as st
import streamlit.components.v1 as components

# CONFIG
st.set_page_config(page_title="Gen AI Carnival", page_icon="🎡", layout="wide")

# GLOBAL CSS
st.markdown("""
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
[data-testid="stAppViewContainer"] { background: #0a0a12; min-height: 100vh; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,102,241,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(56,189,248,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 50% 50%, rgba(168,85,247,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="block-container"] {
    position: relative;
    z-index: 1;
    padding-top: 2rem !important;
    max-width: 1200px !important;
    margin: 0 auto;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 13px;
    font-weight: 500;
    color: #a5b4fc;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.hero-title {
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 700;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 40%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 16px;
}
.hero-sub {
    font-size: 18px;
    color: #64748b;
    font-weight: 400;
    margin-bottom: 40px;
}
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 28px;
    backdrop-filter: blur(16px);
}
.challenge-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    overflow: hidden;
    cursor: pointer;
}
.challenge-card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
}
.challenge-card-body { padding: 16px; }
.challenge-card-title { font-size: 15px; font-weight: 600; color: #e2e8f0; }
.challenge-card-sub { font-size: 12px; color: #475569; }
.avatar {
    width: 56px; height: 56px; border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #38bdf8);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 700; color: #fff;
}
.score-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99,102,241,0.15);
    border-radius: 999px;
    padding: 8px 20px;
    color: #a5b4fc;
}
</style>
""", unsafe_allow_html=True)

def play_sound(url):
    components.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ✅ UPDATED PROMPTS ONLY
PROMPTS = [
    {
        "title": "Sunset Beach", "emoji": "🌅",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
        "answers": ["a beautiful sunset over the ocean","sun setting on a beach with waves"]
    },
    {
        "title": "Snow Mountains", "emoji": "🏔️",
        "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=600&q=80",
        "answers": ["snow covered mountains under blue sky","a mountain range filled with snow"]
    },
    {
        "title": "City Night", "emoji": "🌃",
        "image": "https://images.unsplash.com/photo-1494526585095-c41746248156?w=600&q=80",
        "answers": ["a city skyline at night with lights","bright city buildings glowing in the dark"]
    },
    {
        "title": "Galaxy Space", "emoji": "🌌",
        "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&q=80",
        "answers": ["a galaxy with stars and space","deep space filled with stars and nebula"]
    },
    {
        "title": "Delicious Food", "emoji": "🍕",
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80",
        "answers": ["a plate of delicious food","tasty meal served on a table"]
    },
    {
        "title": "Cute Dog", "emoji": "🐶",
        "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600&q=80",
        "answers": ["a cute dog looking at the camera","a small puppy sitting and staring"]
    },
    {
        "title": "Green Forest", "emoji": "🌳",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=600&q=80",
        "answers": ["a dense green forest with trees","sunlight passing through forest trees"]
    },
    {
        "title": "Sports Car", "emoji": "🚗",
        "image": "https://images.unsplash.com/photo-1493238792000-8113da705763?w=600&q=80",
        "answers": ["a fast sports car on the road","a luxury car driving on highway"]
    }
]

# SESSION
for k, v in {"page": "home", "user": "", "selected_prompt": None, "leaderboard": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# HOME
def home():
    name = st.text_input("Enter your name")
    if st.button("Start"):
        if name:
            st.session_state.user = name
            st.session_state.page = "dashboard"
            st.rerun()

# DASHBOARD
def dashboard():
    cols = st.columns(4)
    for i, prompt in enumerate(PROMPTS):
        with cols[i % 4]:
            st.image(prompt["image"])
            if st.button(f"Play {prompt['title']}", key=i):
                st.session_state.selected_prompt = i
                st.session_state.page = "game"
                st.rerun()

# GAME
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]
    st.image(prompt["image"])
    guess = st.text_input("Your answer")

    if st.button("Submit"):
        if guess.lower() in prompt["answers"]:
            st.success("Correct!")
            score = 10
        else:
            st.error(f"Wrong! Answer: {prompt['answers'][0]}")
            score = 0

        st.session_state.leaderboard.append({"name": st.session_state.user, "score": score})
        st.session_state.page = "leaderboard"
        st.rerun()

# LEADERBOARD
def leaderboard():
    for entry in st.session_state.leaderboard:
        st.write(entry)

    if st.button("Play Again"):
        st.session_state.page = "dashboard"
        st.rerun()

# ROUTER
{"home": home, "dashboard": dashboard, "game": game, "leaderboard": leaderboard}[st.session_state.page]()
