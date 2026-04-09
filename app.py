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

# --- 2. GET ROUND FROM URL ---
query_params = st.query_params
round_no = int(query_params.get("round", 1)) - 1  # 0-based

# --- 3. UI DESIGN ---
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

# --- 4. ROUND STORAGE ---
if "round_data" not in st.session_state:
    st.session_state.round_data = {}

if round_no not in st.session_state.round_data:
    st.session_state.round_data[round_no] = {
        "players": [],
        "started": False,
        "turn": 0,
        "finished": False
    }

room = st.session_state.round_data[round_no]

st.title(f"🎨 Prompt Picasso - Round {round_no + 1}")
st.subheader(GAMES[round_no]["title"])

# --- 5. LOBBY ---
if not room["started"]:

    name = st.text_input("Enter Player Name")

    if st.button("Join Round"):
        if name:
            if len(room["players"]) >= 5:
                st.error("Max 5 players allowed")
            elif name in [p["name"] for p in room["players"]]:
                st.warning("Name already exists")
            else:
                room["players"].append({"name": name, "score": 0})
                st.rerun()

    # Show players
    if room["players"]:
        st.write("### Players Joined:")
        for p in room["players"]:
            st.success(p["name"])

    # --- ADMIN CONTROL ---
    st.markdown("### 🔐 Admin Panel")

    if len(room["players"]) < 1:
        st.error("Minimum 1 player required")
    else:
        if st.button("🚀 Start Round"):
            room["started"] = True
            st.rerun()

    st.stop()

# --- 6. GAMEPLAY ---
if not room["finished"]:

    player = room["players"][room["turn"]]

    st.write(f"🎯 Turn: **{player['name']}**")
    st.image(GAMES[round_no]["url"], use_container_width=True)

    text = st.text_area("Describe the image").lower()

    if st.button("Submit"):

        if len(text) < 5:
            st.error("Too short!")
        else:
            targets = GAMES[round_no]["targets"]
            score = sum([1 for w in targets if w in text]) * 20

            room["players"][room["turn"]]["score"] = score

            if room["turn"] < len(room["players"]) - 1:
                room["turn"] += 1
            else:
                room["finished"] = True

            st.rerun()

# --- 7. RESULT ---
if room["finished"]:
    st.subheader("🏆 Round Results")

    for p in room["players"]:
        st.write(f"{p['name']} → {p['score']} pts")
