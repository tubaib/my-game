import streamlit as st

# --- 1. GAME CONFIGURATION ---
# Using high-quality, direct Unsplash links for reliability
GAMES = [
    {
        "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b", 
        "targets": ["mountains", "peaks", "nature", "clouds", "landscape"],
        "title": "The High Peaks"
    },
    {
        "url": "https://images.unsplash.com/photo-1514565131-fce0801e5785", 
        "targets": ["city", "skyline", "buildings", "urban", "night"],
        "title": "Neon Metropolis"
    },
    {
        "url": "https://images.unsplash.com/photo-1500622764614-be358d8d80c3", 
        "targets": ["forest", "trees", "green", "woods", "sunlight"],
        "title": "Sunlit Woodland"
    }
]

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Prompt Master Pro", page_icon="🎨", layout="centered")

# Custom CSS for a professional "App" feel
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0e1117 0%, #161b22 100%); }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3333; border: none; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .stTextArea>div>div>textarea { border-radius: 15px; }
    img { border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "setup"
    st.session_state.players = []
    st.session_state.round = 0
    st.session_state.p_turn = 0  # We will use p_turn consistently
    st.session_state.history = []

# --- 4. SETUP SCREEN ---
if st.session_state.step == "setup":
    st.title("🎨 Prompt Master Pro")
    st.markdown("#### 3 Players • 3 Rounds • 1 Champion")
    
    with st.container():
        p1 = st.text_input("Player 1 Name", "Player 1")
        p2 = st.text_input("Player 2 Name", "Player 2")
        p3 = st.text_input("Player 3 Name", "Player 3")
        
        if st.button("🚀 START TOURNAMENT", use_container_width=True):
            st.session_state.players = [{"name": n, "total": 0} for n in [p1, p2, p3]]
            st.session_state.step = "playing"
            st.rerun()

# --- 5. GAMEPLAY SCREEN ---
elif st.session_state.step == "playing":
    r_idx = st.session_state.round
    p_idx = st.session_state.p_turn
    player = st.session_state.players[p_idx]
    
    st.subheader(f"Round {r_idx + 1} of 3")
    # Total game progress (out of 9 turns)
    st.progress((r_idx * 3 + p_idx + 1) / 9)
    
    st.image(GAMES[r_idx]["url"], use_container_width=True)
    st.info(f"👤 **{player['name']}**, it is your turn to describe!")
    
    user_input = st.text_area("What do you see? (1-2 lines)", placeholder="Describe the scene...", key=f"input_{r_idx}_{p_idx}").lower()
    
    if st.button("SUBMIT PROMPT", use_container_width=True):
        if len(user_input) < 15:
            st.error("Your description is too short! Add more detail.")
        else:
            # Scoring Logic
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
            # Update Score and History
            st.session_state.players[p_idx]["total"] += score
            st.session_state.history.append({"round": r_idx, "name": player['name'], "score": score})
            
            # Rotation Logic (The Fix)
            if p_idx < 2:
                st.session_state.p_turn += 1  # Corrected variable name
            else:
                st.session_state.step = "round_review"
            st.rerun()

# --- 6. ROUND REVIEW ---
elif st.session_state.step == "round_review":
    r_idx = st.session_state.round
    st.title(f"📊 Round {r_idx + 1} Standings")
    st.image(GAMES[r_idx]["url"], use_container_width=True)
    
    # Sort scores for this specific round
    round_data = [h for h in st.session_state.history if h['round'] == r_idx]
    round_data = sorted(round_data, key=lambda x: x['score'], reverse=True)
    
    for i, res in enumerate(round_data):
        st.write(f"**{i+1}. {res['name']}** — `{res['score']} pts`")
    
    btn_text = "NEXT ROUND ➡️" if r_idx < 2 else "FINAL RESULTS 🏆"
    if st.button(btn_text, use_container_width=True):
        if st.session_state.round < 2:
            st.session_state.round += 1
            st.session_state.p_turn = 0
            st.session_state.step = "playing"
        else:
            st.session_state.step = "final"
        st.rerun()

# --- 7. FINAL STANDINGS ---
elif st.session_state.step == "final":
    st.balloons()
    st.title("🏆 Final Tournament Standings")
    
    # Sort players by total score
    final_sorted = sorted(st.session_state.players, key=lambda x: x['total'], reverse=True)
    for i, p in enumerate(final_sorted):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        st.subheader(f"{medal} {p['name']}: {p['total']} total pts")
        
    st.divider()
    if st.button("🔄 START NEW GAME", use_container_width=True):
        st.session_state.clear()
        st.rerun()
