import streamlit as st
import time
import pandas as pd

# --- 1. CARNIVAL CONFIGURATION (8 ELITE ROUNDS) ---
GAMES = [
    {"url": "https://images.unsplash.com/photo-1579310964728-441f2000c1be", "targets": ["forest", "sunlight", "magic", "trees", "ethereal"], "title": "The Enchanted Grove"},
    {"url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe", "targets": ["abstract", "geometry", "lines", "blue", "minimal"], "title": "Digital Dreamscape"},
    {"url": "https://images.unsplash.com/photo-1605142859862-978be7eba909", "targets": ["architecture", "modern", "stairs", "white", "symmetry"], "title": "The Infinite Staircase"},
    {"url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853", "targets": ["neon", "cyberpunk", "robot", "future", "glow"], "title": "Android Awakening"},
    {"url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa", "targets": ["earth", "space", "satellite", "network", "global"], "title": "Orbital Network"},
    {"url": "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e", "targets": ["moon", "surreal", "floating", "night", "clouds"], "title": "Lunar Gravity"},
    {"url": "https://images.unsplash.com/photo-1547891299-bc7837090333", "targets": ["water", "splash", "liquid", "macro", "crystal"], "title": "Liquid Motion"},
    {"url": "https://images.unsplash.com/photo-1614728263952-84ea206f99b6", "targets": ["fire", "embers", "smoke", "hot", "particles"], "title": "Inferno Dust"}
]

st.set_page_config(page_title="Prompt Picasso | Carnival Booth", layout="centered")

# --- 2. CARNIVAL UI DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Space+Grotesk:wght@300;700&display=swap');
    .stApp { background: radial-gradient(circle at center, #1a1a2e 0%, #020205 100%); color: #e0e0e0; font-family: 'Space Grotesk', sans-serif; }
    .carnival-header { font-family: 'Bungee Spice', cursive; font-size: 3rem; text-align: center; margin-bottom: 0px; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border: 2px solid rgba(0, 210, 255, 0.3); border-radius: 20px; padding: 25px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(45deg, #ff00ff, #00d2ff); color: white; border: none; border-radius: 50px; font-weight: bold; height: 3.5rem; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 210, 255, 0.4); }
    .player-chip { background: rgba(255, 0, 255, 0.1); border: 1px solid #ff00ff; padding: 5px 12px; border-radius: 12px; margin: 4px; display: inline-block; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "round_setup" # round_setup, playing, leaderboard, final
    st.session_state.round = 0
    st.session_state.round_players = []
    st.session_state.p_turn = 0
    st.session_state.master_leaderboard = {} # Persistent scores: {Name: TotalScore}
    st.session_state.round_history = []

# --- 4. STEP 1: PER-ROUND REGISTRATION ---
if st.session_state.step == "round_setup":
    st.markdown('<h1 class="carnival-header">PROMPT PICASSO</h1>', unsafe_allow_html=True)
    st.subheader(f"🎪 Step 1: Register Artists for Round {st.session_state.round + 1}")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Target Masterpiece:** {GAMES[st.session_state.round]['title']}")
    p_name = st.text_input("Enter Artist Name", placeholder="Who's playing this round?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ADD ARTIST"):
            if p_name and len(st.session_state.round_players) < 5:
                if p_name not in st.session_state.round_players:
                    st.session_state.round_players.append(p_name)
                    st.rerun()
    with col2:
        if st.button("CLEAR ROUND"):
            st.session_state.round_players = []
            st.rerun()

    if st.session_state.round_players:
        st.write("---")
        st.write("**Artists for this Round:**")
        for p in st.session_state.round_players:
            st.markdown(f'<span class="player-chip">🎨 {p}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if 1 <= len(st.session_state.round_players) <= 5:
        if st.button(f"🔥 START ROUND {st.session_state.round + 1}"):
            st.session_state.p_turn = 0
            st.session_state.step = "playing"
            st.rerun()

# --- 5. STEP 2: GAMEPLAY ---
elif st.session_state.step == "playing":
    r_idx = st.session_state.round
    p_name = st.session_state.round_players[st.session_state.p_turn]
    
    st.title("🖌️ Performance Stage")
    st.progress((st.session_state.p_turn + 1) / len(st.session_state.round_players))
    
    st.markdown(f"#### Round {r_idx + 1}: {GAMES[r_idx]['title']}")
    st.info(f"🎨 Current Picasso: **{p_name}**")

    st.image(GAMES[r_idx]["url"], use_container_width=True)
    user_input = st.text_area("Describe the masterpiece (1-2 lines):", key=f"in_{r_idx}_{p_name}").lower()
    
    if st.button("🎨 SUBMIT PROMPT"):
        if len(user_input) < 10:
            st.error("Too short! Picasso needs more detail.")
        else:
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
            # Update Master Leaderboard
            st.session_state.master_leaderboard[p_name] = st.session_state.master_leaderboard.get(p_name, 0) + score
            st.session_state.round_history.append({"Round": r_idx + 1, "Artist": p_name, "Score": score})
            
            if st.session_state.p_turn < len(st.session_state.round_players) - 1:
                st.session_state.p_turn += 1
            else:
                st.session_state.step = "leaderboard"
            st.rerun()

# --- 6. STEP 3: ROUND LEADERBOARD ---
elif st.session_state.step == "leaderboard":
    r_idx = st.session_state.round
    st.title(f"📊 Round {r_idx + 1} Standings")
    
    # Filter only this round's scores
    current_round_data = [h for h in st.session_state.round_history if h['Round'] == r_idx + 1]
    df = pd.DataFrame(current_round_data).sort_values(by="Score", ascending=False)
    
    st.table(df[["Artist", "Score"]])
    
    btn_label = "NEXT ROUND: REGISTER NEW ARTISTS 🎡" if r_idx < 7 else "GRAND FINALE 🏆"
    if st.button(btn_label):
        if r_idx < 7:
            st.session_state.round += 1
            st.session_state.round_players = []
            st.session_state.step = "round_setup"
        else:
            st.session_state.step = "final"
        st.rerun()

# --- 7. STEP 4: FINAL HALL OF FAME ---
elif st.session_state.step == "final":
    st.balloons()
    st.markdown('<h1 class="carnival-header">HALL OF FAME</h1>', unsafe_allow_html=True)
    
    master_df = pd.DataFrame(st.session_state.master_leaderboard.items(), columns=['Artist', 'Total Score'])
    master_df = master_df.sort_values(by="Total Score", ascending=False)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Top Overall Artists")
    st.table(master_df.head(10))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("RESTART CARNIVAL"):
        st.session_state.clear()
        st.rerun()
