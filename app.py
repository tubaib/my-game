import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Gen AI Carnival", layout="centered")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
    <style>
    body {
        background-color: #0f172a;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #38bdf8;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #cbd5f5;
        margin-bottom: 30px;
    }
    .card button {
        width: 100%;
        height: 80px;
        border-radius: 15px;
        font-size: 18px;
        font-weight: bold;
        background-color: #1e293b;
        color: white;
        border: 1px solid #38bdf8;
        margin-bottom: 10px;
    }
    .card button:hover {
        background-color: #38bdf8;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ EASY PROMPTS ------------------
PROMPTS = [
    {"title": "🌄 Mountain View", "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470", "answers": ["mountain", "hill"]},
    {"title": "🌊 Ocean Scene", "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", "answers": ["ocean", "sea"]},
    {"title": "🌆 City Life", "image": "https://images.unsplash.com/photo-1494526585095-c41746248156", "answers": ["city", "buildings"]},
    {"title": "🌌 Space Stars", "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa", "answers": ["space", "stars"]},
    {"title": "🍕 Food Time", "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836", "answers": ["food", "pizza"]},
    {"title": "🐶 Cute Animal", "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a", "answers": ["dog", "animal"]},
    {"title": "🌳 Green Nature", "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee", "answers": ["tree", "nature"]},
    {"title": "🚗 Fast Car", "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a", "answers": ["car", "vehicle"]}
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

    if st.button("🚀 Start"):
        if name:
            st.session_state.user = name
            st.session_state.page = "dashboard"
        else:
            st.warning("Enter your name first!")

# ------------------ DASHBOARD ------------------
def dashboard():
    st.markdown(f'<div class="title">Welcome {st.session_state.user} 🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choose a Challenge</div>', unsafe_allow_html=True)

    cols = st.columns(2)

    for i, prompt in enumerate(PROMPTS):
        with cols[i % 2]:
            if st.button(prompt["title"], key=i):
                st.session_state.selected_prompt = i
                st.session_state.page = "game"

# ------------------ GAME ------------------
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]

    st.markdown(f'<div class="title">{prompt["title"]}</div>', unsafe_allow_html=True)

    st.image(prompt["image"], use_container_width=True)

    guess = st.text_input("What do you see?")

    if st.button("Submit Answer"):
        if guess.lower() in prompt["answers"]:
            score = 10
            st.success("✅ Correct!")
        else:
            score = 0
            st.error("❌ Try Again Next Time!")

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
        st.write(f"{i+1}. 🎯 {entry['name']} — {entry['score']} pts")

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
