import streamlit as st
import random

# ------------------ CONFIG ------------------
PROMPTS = [
    {
        "title": "Abstract Vision",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe",
        "answers": ["abstract", "geometry", "lines", "blue"]
    },
    {
        "title": "Nature Guess",
        "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        "answers": ["mountain", "nature", "sky", "landscape"]
    },
    {
        "title": "Tech Puzzle",
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475",
        "answers": ["technology", "circuit", "chip", "electronics"]
    },
    {
        "title": "Art Mystery",
        "image": "https://images.unsplash.com/photo-1504198458649-3128b932f49b",
        "answers": ["art", "painting", "color", "creative"]
    }
]

# ------------------ SESSION INIT ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "round" not in st.session_state:
    st.session_state.round = 0

if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# ------------------ HOME PAGE ------------------
def home():
    st.title("🎡 Gen AI Carnival")
    st.subheader("From Prompts to Possibilities")

    name = st.text_input("Enter your name")

    if st.button("Start Game"):
        if name:
            st.session_state.user = name
            st.session_state.page = "dashboard"
        else:
            st.warning("Please enter your name")

# ------------------ DASHBOARD ------------------
def dashboard():
    st.title(f"Welcome {st.session_state.user} 🎉")
    st.subheader("Choose a Prompt Challenge")

    for i, prompt in enumerate(PROMPTS):
        if st.button(prompt["title"]):
            st.session_state.selected_prompt = i
            st.session_state.page = "game"
            st.session_state.round = 0
            st.session_state.score = 0

# ------------------ GAME PAGE ------------------
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]

    st.title(f"🎯 {prompt['title']}")
    st.write(f"Round: {st.session_state.round + 1}/3")

    st.image(prompt["image"], use_container_width=True)

    guess = st.text_input("Enter your guess")

    if st.button("Submit"):
        if guess.lower() in prompt["answers"]:
            st.success("✅ Correct!")
            st.session_state.score += 10
        else:
            st.error("❌ Wrong!")

        st.session_state.round += 1

        if st.session_state.round >= 3:
            # Save to leaderboard
            st.session_state.leaderboard.append({
                "name": st.session_state.user,
                "score": st.session_state.score
            })
            st.session_state.page = "leaderboard"
        else:
            st.rerun()

# ------------------ LEADERBOARD ------------------
def leaderboard():
    st.title("🏆 Leaderboard")

    # Sort leaderboard
    sorted_board = sorted(
        st.session_state.leaderboard,
        key=lambda x: x["score"],
        reverse=True
    )

    for i, entry in enumerate(sorted_board):
        st.write(f"{i+1}. {entry['name']} - {entry['score']} points")

    if st.button("Play Again"):
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
