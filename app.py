import streamlit as st

# --- GAME CONFIG ---
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

# --- UI ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(10,10,20,0.9), rgba(10,10,20,0.9)),
    url("https://images.unsplash.com/photo-1519681393784-d120267933ba");
    background-size: cover;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if "step" not in st.session_state:
    st.session_state.step = "register"
    st.session_state.players = []
    st.session_state.current_player = 0
    st.session_state.round = 0

# --- REGISTER ---
if st.session_state.step == "register":

    st.title("🎨 Prompt Picasso")

    name = st.text_input("Enter Your Name")

    if st.button("Join Game"):
        if name:
            if len(st.session_state.players) >= 5:
                st.error("Max 5 players allowed")
            elif name in [p["name"] for p in st.session_state.players]:
                st.warning("Name already exists")
            else:
                st.session_state.players.append({
                    "name": name,
                    "scores": [0]*8,
                    "total": 0
                })
                st.rerun()

    if st.session_state.players:
        st.write("### Players Joined:")
        for p in st.session_state.players:
            st.success(p["name"])

        if st.button("🚀 Start Game"):
            st.session_state.step = "game"
            st.rerun()

# --- GAME ---
elif st.session_state.step == "game":

    r = st.session_state.round
    p = st.session_state.current_player
    player = st.session_state.players[p]

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

            player["scores"][r] = score
            player["total"] += score

            # next player
            if p < len(st.session_state.players) - 1:
                st.session_state.current_player += 1
            else:
                st.session_state.current_player = 0
                st.session_state.round += 1

            # finish all rounds
            if st.session_state.round >= 8:
                st.session_state.step = "final"

            st.rerun()

# --- FINAL ---
elif st.session_state.step == "final":

    st.title("🏆 Final Leaderboard")

    sorted_players = sorted(st.session_state.players, key=lambda x: x["total"], reverse=True)

    for i, p in enumerate(sorted_players):
        medal = ["🥇", "🥈", "🥉"]
        icon = medal[i] if i < 3 else "🏅"
        st.write(f"{icon} {p['name']} → {p['total']} pts")

    st.divider()

    st.subheader("🔗 Revisit Prompts")

    for i, game in enumerate(GAMES):
        st.markdown(f"[👉 Go to Round {i+1} - {game['title']}]({game['url']})")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
