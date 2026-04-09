import streamlit as st

# ------------------ CONFIG (8 PROMPTS) ------------------
PROMPTS = [
    {"title": "Abstract Vision", "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe", "answers": ["abstract", "geometry", "lines"]},
    {"title": "Nature Guess", "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470", "answers": ["mountain", "nature", "sky"]},
    {"title": "Tech Puzzle", "image": "https://images.unsplash.com/photo-1518770660439-4636190af475", "answers": ["technology", "chip", "electronics"]},
    {"title": "Art Mystery", "image": "https://images.unsplash.com/photo-1504198458649-3128b932f49b", "answers": ["art", "painting", "creative"]},
    {"title": "City Life", "image": "https://images.unsplash.com/photo-1494526585095-c41746248156", "answers": ["city", "buildings", "urban"]},
    {"title": "Ocean World", "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", "answers": ["ocean", "sea", "water"]},
    {"title": "Space Theme", "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa", "answers": ["space", "stars", "galaxy"]},
    {"title": "Food Fun", "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836", "answers": ["food", "meal", "dish"]}
]

# ------------------ SESSION INIT ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# ------------------ HOME ------------------
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
    st.subheader("Choose ONE Prompt Challenge")

    for i, prompt in enumerate(PROMPTS):
        if st.button(prompt["title"]):
            st.session_state.selected_prompt = i
            st.session_state.page = "game"

# ------------------ GAME (ONLY 1 ROUND) ------------------
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]

    st.title(f"🎯 {prompt['title']}")

    st.image(prompt["image"], use_container_width=True)

    guess = st.text_input("Enter your guess")

    if st.button("Submit"):
        if guess.lower() in prompt["answers"]:
            st.success("✅ Correct!")
            st.session_state.score = 10
        else:
            st.error("❌ Wrong!")
            st.session_state.score = 0

        # Save to leaderboard
        st.session_state.leaderboard.append({
            "name": st.session_state.user,
            "score": st.session_state.score
        })

        st.session_state.page = "leaderboard"

# ------------------ LEADERBOARD ------------------
def leaderboard():
    st.title("🏆 Leaderboard")

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
