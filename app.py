import streamlit as st

# --- 1. GAME CONFIGURATION (8 ROUNDS) ---
GAMES = [
    {"url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe", "targets": ["abstract", "geometry", "lines", "blue", "minimal"], "title": "Digital Dreamscape"},
    {"url": "https://images.unsplash.com/photo-1605142859862-978be7eba909", "targets": ["architecture", "modern", "stairs", "white", "symmetry"], "title": "The Infinite Staircase"},
    {"url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853", "targets": ["neon", "cyberpunk", "robot", "future", "glow"], "title": "Android Awakening"},
    {"url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa", "targets": ["earth", "space", "satellite", "network", "global"], "title": "Orbital Network"},
    {"url": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809", "targets": ["gradient", "colors", "mesh", "soft", "vibrant"], "title": "Chromatic Flow"},
    {"url": "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e", "targets": ["moon", "surreal", "floating", "night", "clouds"], "title": "Lunar Gravity"},
    {"url": "https://images.unsplash.com/photo-1547891299-bc7837090333", "targets": ["water", "splash", "liquid", "macro", "crystal"], "title": "Liquid Motion"},
    {"url": "https://images.unsplash.com/photo-1614728263952-84ea206f99b6", "targets": ["fire", "embers", "smoke", "hot", "particles"], "title": "Inferno Dust"}
]

st.set_page_config(page_title="Prompt Picasso", layout="centered")

# --- 2. UI DESIGN ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Space+Grotesk:wght@300;700&display=swap');

.stApp {
    background: linear-gradient(rgba(10,10,20,0.9), rgba(10,10,20,0.9)),
    url("https://images.unsplash.com/photo-1506744038136-46273834b3fb");
    background-size: cover;
    background-attachment: fixed;
    color: white;
    font-family: 'Space Grotesk', sans-serif;
}

.title {
    font-family: 'Bungee Spice';
    text-align: center;
    font-size: 3rem;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "step" not in st.session_state:
    st.session_state.step = "lobby"
    st.session_state.round = 0
    st.session_state.players = []
    st.session_state.round_players = []
    st.session_state.turn = 0

# --- 4. LOBBY ---
if st.session_state.step == "lobby":

    st.markdown('<h1 class="title">🎨 PROMPT PICASSO</h1>', unsafe_allow_html=True)
    st.subheader(f"Round {st.session_state.round + 1} Registration")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        name = st.text_input("Enter Player Name")

        if st.button("Join Room"):
            if name:
                if len(st.session_state.round_players) >= 5:
                    st.error("Max 5 players allowed!")
                elif name in [p["name"] for p in st.session_state.round_players]:
                    st.warning("Name already exists!")
                else:
                    st.session_state.round_players.append({"name": name, "score": 0})
                    st.rerun()

        # Show players
        if st.session_state.round_players:
            st.write("### Players in Room:")
            for p in st.session_state.round_players:
                st.success(p["name"])

        st.markdown('</div>', unsafe_allow_html=True)

    # --- ADMIN PANEL ---
    with st.expander("🔐 ADMIN PANEL"):
        st.write(f"Players: {len(st.session_state.round_players)} / 5")

        if len(st.session_state.round_players) < 1:
            st.error("Minimum 1 player required")
        else:
            if st.button("Start Game"):
                st.session_state.step = "game"
                st.session_state.turn = 0
                st.rerun()

        if st.button("Reset Lobby"):
            st.session_state.round_players = []
            st.rerun()

# --- 5. GAME ---
elif st.session_state.step == "game":

    r = st.session_state.round
    t = st.session_state.turn
    player = st.session_state.round_players[t]

    st.subheader(f"Round {r+1}: {GAMES[r]['title']}")
    st.write(f"🎯 Player: **{player['name']}**")

    st.image(GAMES[r]["url"], use_container_width=True)

    text = st.text_area("Describe the image").lower()

    if st.button("Submit"):

        if len(text) < 5:
            st.error("Too short!")
        else:
            targets = GAMES[r]["targets"]
            score = sum([1 for w in targets if w in text]) * 20

            st.session_state.round_players[t]["score"] = score

            # Next player
            if t < len(st.session_state.round_players) - 1:
                st.session_state.turn += 1
            else:
                st.session_state.step = "result"

            st.rerun()

# --- 6. ROUND RESULT ---
elif st.session_state.step == "result":

    st.subheader(f"🏆 Round {st.session_state.round + 1} Results")

    for p in st.session_state.round_players:
        st.write(f"{p['name']} → {p['score']} pts")

        # Add to leaderboard
        found = next((x for x in st.session_state.players if x["name"] == p["name"]), None)

        if found:
            found["total"] += p["score"]
        else:
            st.session_state.players.append({"name": p["name"], "total": p["score"]})

    if st.button("Next Round"):
        if st.session_state.round < 7:
            st.session_state.round += 1
            st.session_state.round_players = []  # 🔥 IMPORTANT: fresh registration
            st.session_state.step = "lobby"
        else:
            st.session_state.step = "final"

        st.rerun()

# --- 7. FINAL ---
elif st.session_state.step == "final":

    st.title("🏁 FINAL LEADERBOARD")

    sorted_players = sorted(st.session_state.players, key=lambda x: x["total"], reverse=True)

    for i, p in enumerate(sorted_players):
        medal = ["🥇", "🥈", "🥉"]
        icon = medal[i] if i < 3 else "🏅"
        st.write(f"{icon} {p['name']} → {p['total']} pts")

    if st.button("Restart Game"):
        st.session_state.clear()
        st.rerun()
