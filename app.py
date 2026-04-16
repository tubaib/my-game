import streamlit as st
import streamlit.components.v1 as components
from difflib import SequenceMatcher
import re

# CONFIG
st.set_page_config(page_title="Gen AI Carnival", page_icon="🎡", layout="wide")

# -------------------- SCORING FUNCTIONS --------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

def calculate_score(user_input, correct_answers):
    user_input = clean_text(user_input)

    max_similarity = 0

    for ans in correct_answers:
        ans = clean_text(ans)
        similarity = SequenceMatcher(None, user_input, ans).ratio()
        max_similarity = max(max_similarity, similarity)

    score = round(max_similarity * 10)
    return score, max_similarity

# -------------------- SOUND --------------------
def play_sound(url):
    components.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# -------------------- PROMPTS --------------------
PROMPTS = [
    {"title":"Sunset Beach","emoji":"🌅","image":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
     "answers":["sunset beach","sunset over ocean","beach at sunset"]},

    {"title":"Snow Mountains","emoji":"🏔️","image":"https://images.unsplash.com/photo-1519681393784-d120267933ba?w=600&q=80",
     "answers":["snow mountains","snowy mountain","mountains covered with snow"]},

    {"title":"City Night","emoji":"🌃","image":"https://images.unsplash.com/photo-1494526585095-c41746248156?w=600&q=80",
     "answers":["city at night","night city","city skyline night"]},

    {"title":"Galaxy Space","emoji":"🌌","image":"https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&q=80",
     "answers":["galaxy","space stars","galaxy in space"]},

    {"title":"Delicious Food","emoji":"🍕","image":"https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80",
     "answers":["delicious food","tasty food","meal on table"]},

    {"title":"Cute Dog","emoji":"🐶","image":"https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600&q=80",
     "answers":["cute dog","puppy","small dog"]},

    {"title":"Green Forest","emoji":"🌳","image":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=600&q=80",
     "answers":["green forest","forest trees","dense forest"]},

    {"title":"Sports Car","emoji":"🚗","image":"https://images.unsplash.com/photo-1493238792000-8113da705763?w=600&q=80",
     "answers":["sports car","fast car","luxury car"]}
]

# -------------------- SESSION --------------------
for k, v in {
    "page": "home",
    "user": "",
    "selected_prompt": None,
    "leaderboard": []
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------- HOME --------------------
def home():
    st.markdown("<h1 style='text-align:center;'>Gen AI Carnival 🎡</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>From Prompts to Possibilities</p>", unsafe_allow_html=True)

    name = st.text_input("Enter your name")

    if st.button("Start Game"):
        if name.strip():
            st.session_state.user = name
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.warning("Enter name first")

# -------------------- DASHBOARD --------------------
def dashboard():
    st.subheader(f"Welcome {st.session_state.user}")

    cols = st.columns(4)

    for i, prompt in enumerate(PROMPTS):
        with cols[i % 4]:
            st.image(prompt["image"])
            if st.button(f"Play {prompt['emoji']}", key=i):
                st.session_state.selected_prompt = i
                st.session_state.page = "game"
                st.rerun()

# -------------------- GAME --------------------
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]

    st.image(prompt["image"])
    st.write("### What do you see?")

    guess = st.text_input("Enter your prompt")

    if st.button("Submit Answer"):
        score, similarity = calculate_score(guess, prompt["answers"])

        if score >= 8:
            st.success(f"🔥 Excellent! +{score} points")
            st.balloons()
            play_sound("https://www.soundjay.com/human/cheering-01.mp3")

        elif score >= 5:
            st.info(f"👍 Close! +{score} points")

        elif score >= 3:
            st.warning(f"🙂 Not bad! +{score} points")

        else:
            st.error(f"❌ Too far! +{score} points\nCorrect: {prompt['answers'][0]}")
            play_sound("https://www.soundjay.com/button/beep-10.mp3")

        st.session_state.leaderboard.append({
            "name": st.session_state.user,
            "score": score
        })

        st.session_state.page = "leaderboard"
        st.rerun()

# -------------------- LEADERBOARD --------------------
def leaderboard():
    st.title("🏆 Leaderboard")

    sorted_board = sorted(st.session_state.leaderboard,
                          key=lambda x: x["score"],
                          reverse=True)

    for i, entry in enumerate(sorted_board):
        st.write(f"{i+1}. {entry['name']} — {entry['score']} pts")

    if st.button("Play Again"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button("Home"):
        st.session_state.page = "home"
        st.rerun()

# -------------------- ROUTER --------------------
pages = {
    "home": home,
    "dashboard": dashboard,
    "game": game,
    "leaderboard": leaderboard
}

pages[st.session_state.page]()
