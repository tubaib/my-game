import streamlit as st
import streamlit.components.v1 as components

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Gen AI Carnival", layout="wide")

# ------------------ PREMIUM CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 10px;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.05);
    border: 1px solid #38bdf8;
}

/* Title */
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #38bdf8;
}
.subtitle {
    text-align: center;
    color: #cbd5f5;
    margin-bottom: 30px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-size: 16px;
    background: linear-gradient(90deg,#38bdf8,#6366f1);
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ------------------ PROMPTS (EASY + FUN) ------------------
PROMPTS = [
    {"title": "🌄 Mountain", "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470", "answers": ["mountain"]},
    {"title": "🌊 Ocean", "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", "answers": ["ocean","sea"]},
    {"title": "🌆 City", "image": "https://images.unsplash.com/photo-1494526585095-c41746248156", "answers": ["city"]},
    {"title": "🌌 Space", "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa", "answers": ["space"]},
    {"title": "🍕 Food", "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836", "answers": ["food","pizza"]},
    {"title": "🐶 Dog", "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a", "answers": ["dog"]},
    {"title": "🌳 Tree", "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee", "answers": ["tree"]},
    {"title": "🚗 Car", "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a", "answers": ["car"]}
]

# ------------------ SESSION ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = ""

if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# ------------------ HOME ------------------
def home():
    st.markdown('<div class="title">🎡 Gen AI Carnival</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">From Prompts to Possibilities</div>', unsafe_allow_html=True)

    name = st.text_input("Enter your name")

    if st.button("🚀 Enter Carnival"):
        if name:
            st.session_state.user = name
            st.session_state.page = "dashboard"
        else:
            st.warning("Enter your name!")

# ------------------ DASHBOARD (IMAGE CARDS) ------------------
def dashboard():
    st.markdown(f'<div class="title">Welcome {st.session_state.user}</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choose Your Challenge 🎯</div>', unsafe_allow_html=True)

    cols = st.columns(4)

    for i, prompt in enumerate(PROMPTS):
        with cols[i % 4]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(prompt["image"], use_container_width=True)

            if st.button(prompt["title"], key=i):
                st.session_state.selected_prompt = i
                st.session_state.page = "game"

            st.markdown('</div>', unsafe_allow_html=True)

# ------------------ GAME ------------------
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]

    st.markdown(f'<div class="title">{prompt["title"]}</div>', unsafe_allow_html=True)

    st.image(prompt["image"], use_container_width=True)

    guess = st.text_input("What do you see?")

    if st.button("Submit Answer"):
        if guess.lower() in prompt["answers"]:
            st.success("✅ Correct!")
            st.balloons()  # 🎉 confetti
            score = 10
        else:
            st.error("❌ Wrong!")
            score = 0

        st.session_state.leaderboard.append({
            "name": st.session_state.user,
            "score": score
        })

        st.session_state.page = "leaderboard"

# ------------------ LEADERBOARD ------------------
def leaderboard():
    st.markdown('<div class="title">🏆 Leaderboard</div>', unsafe_allow_html=True)

    sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)

    for i, entry in enumerate(sorted_board):
        st.markdown(f"""
        <div class="card">
            <h3>#{i+1} 🎯 {entry['name']}</h3>
            <p>{entry['score']} points</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔁 Play Again"):
        st.session_state.page = "dashboard"

# ------------------ ROUTER ------------------
if st.session_state.page == "home":
    home()
elif st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "game":
    game()
elif st.session_state.page == "leaderboard":
    leaderboard()
