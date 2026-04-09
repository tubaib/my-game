import streamlit as st
import time

# --- 1. CARNIVAL CONFIGURATION (8 ELITE ROUNDS) ---
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

st.set_page_config(page_title="Prompt Picasso | Gen AI Carnival", layout="centered")

# --- 2. CARNIVAL UI DESIGN & BACKGROUND ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Space+Grotesk:wght@300;700&display=swap');
    
    .stApp {
        background-image: linear-gradient(rgba(2, 2, 5, 0.8), rgba(2, 2, 5, 0.8)), 
        url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986");
        background-size: cover;
        background-attachment: fixed;
        color: #e0e0e0;
        font-family: 'Space Grotesk', sans-serif;
    }
    .carnival-header { font-family: 'Bungee Spice', cursive; font-size: 3.5rem; text-align: center; margin-bottom: 0px; text-shadow: 2px 2px 10px rgba(255,0,255,0.5); }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(45deg, #7000ff, #00d2ff); color: white; border: none; border-radius: 12px; font-weight: 700; transition: 0.3s; width: 100%; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00d2ff; }
    .admin-box { border: 1px dashed #ff00ff; padding: 10px; border-radius: 10px; background: rgba(255,0,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "lobby"
    st.session_state.players = [] # Persistent leaderboard
    st.session_state.round_players = [] # Players registered for the current round
    st.session_state.round = 0
    st.session_state.p_turn = 0
    st.session_state.history = []

# --- 4. LOBBY / REGISTRATION (Runs before every round) ---
if st.session_state.step == "lobby":
    st.markdown('<h1 class="carnival-header">PROMPT PICASSO</h1>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #ff00ff;'>ROUND {st.session_state.round + 1} REGISTRATION</h3>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            new_player = st.text_input("Enter Artist Name", key=f"reg_{st.session_state.round}", placeholder="e.g. PixelWizard")
        with col2:
            st.write("##")
            if st.button("JOIN"):
                if new_player and len(st.session_state.round_players) < 5:
                    if not any(p['name'] == new_player for p in st.session_state.round_players):
                        st.session_state.round_players.append({"name": new_player, "round_score": 0})
                        st.rerun()
                    else:
                        st.warning("Name taken!")
        
        if st.session_state.round_players:
            st.write("**Artists Ready for this Round:**")
            cols = st.columns(len(st.session_state.round_players))
            for i, p in enumerate(st.session_state.round_players):
                cols[i].info(f"🎨 {p['name']}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ADMIN ACCESS SECTION ---
    with st.expander("🔐 ADMIN CONTROL PANEL"):
        st.write(f"Current Player Count: **{len(st.session_state.round_players)} / 5**")
        if len(st.session_state.round_players) < 1:
            st.error("Waiting for at least 1 player...")
        else:
            if st.button("🚀 START ROUND NOW"):
                st.session_state.step = "playing"
                st.rerun()
        
        if st.button("Reset Current Lobby"):
            st.session_state.round_players = []
            st.rerun()

# --- 5. GAMEPLAY ---
elif st.session_state.step == "playing":
    r_idx = st.session_state.round
    p_idx = st.session_state.p_turn
    player = st.session_state.round_players[p_idx]
    
    st.title("🖌️ Performance Stage")
    st.subheader(f"Round {r_idx + 1}: {GAMES[r_idx]['title']}")
    st.write(f"**Artist's Turn:** :blue[{player['name']}]")

    st.image(GAMES[r_idx]["url"], use_container_width=True)
    user_input = st.text_area("Describe the image elements...", placeholder="Be descriptive!", key=f"play_{r_idx}_{p_idx}").lower()
    
    if st.button("🎨 SUBMIT TO JUDGE"):
        if len(user_input) < 5:
            st.error("Too short!")
        else:
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
            # Update Score
            st.session_state.round_players[p_idx]["round_score"] = score
            
            # Move to next player or review
            if p_idx < len(st.session_state.round_players) - 1:
                st.session_state.p_turn += 1
            else:
                st.session_state.p_turn = 0
                st.session_state.step = "round_review"
            st.rerun()

# --- 6. ROUND REVIEW & SCORE MERGING ---
elif st.session_state.step == "round_review":
    st.title(f"🏆 Round {st.session_state.round + 1} Results")
    
    for p in st.session_state.round_players:
        st.write(f"**{p['name']}** scored `{p['round_score']} pts`")
        
        # Merge into global leaderboard
        existing = next((item for item in st.session_state.players if item["name"] == p["name"]), None)
        if existing:
            existing["total"] += p["round_score"]
        else:
            st.session_state.players.append({"name": p["name"], "total": p["round_score"]})

    st.divider()
    if st.button("PROCEED"):
        if st.session_state.round < 7:
            st.session_state.round += 1
            st.session_state.round_players = [] # Clear for new registration
            st.session_state.step = "lobby"
        else:
            st.session_state.step = "final"
        st.rerun()

# --- 7. GRAND FINALE ---
elif st.session_state.step == "final":
    st.balloons()
    st.markdown('<h1 class="carnival-header">GRAND FINALE</h1>', unsafe_allow_html=True)
    final_sorted = sorted(st.session_state.players, key=lambda x: x['total'], reverse=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for i, p in enumerate(final_sorted):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        st.subheader(f"{medal} {p['name']} — Total: {p['total']} pts")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("NEW CARNIVAL"):
        st.session_state.clear()
        st.rerun()
