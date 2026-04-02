import streamlit as st

# --- GAME CONFIGURATION ---
GAMES = [
    {
        "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b", 
        "targets": ["mountains", "peaks", "nature", "clouds", "landscape"],
        "hint": "Think about high altitudes and the natural horizon."
    },
    {
        "url": "https://images.unsplash.com/photo-1514565131-fce0801e5785", 
        "targets": ["city", "skyline", "buildings", "urban", "night"],
        "hint": "Focus on the architecture and the city atmosphere."
    },
    {
        "url": "https://images.unsplash.com/photo-1500622764614-be358d8d80c3", 
        "targets": ["forest", "trees", "green", "woods", "sunlight"],
        "hint": "Look at the density of the foliage and the lighting."
    }
]

# --- PAGE SETUP ---
st.set_page_config(page_title="Prompt Master Pro", page_icon="🎨", layout="centered")

# Custom CSS for a beautiful "App" look
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0e1117 0%, #161b22 100%); }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .stTextArea>div>div>textarea { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (The Game's Memory) ---
if "step" not in st.session_state:
    st.session_state.step = "setup"  # setup, playing, round_review, final
    st.session_state.players = []
    st.session_state.round = 0
    st.session_state.p_turn = 0
    st.session_state.history = []

# --- 1. SETUP SCREEN ---
if st.session_state.step == "setup":
    st.title("🎨 Prompt Master Pro")
    st.markdown("#### The 3-Player AI Writing Challenge")
    
    with st.container():
        p1 = st.text_input("Player 1 Name", "Player 1")
        p2 = st.text_input("Player 2 Name", "Player 2")
        p3 = st.text_input("Player 3 Name", "Player 3")
        
        if st.button("🚀 START TOURNAMENT"):
            st.session_state.players = [{"name": n, "total": 0} for n in [p1, p2, p3]]
            st.session_state.step = "playing"
            st.rerun()

# --- 2. GAMEPLAY SCREEN ---
elif st.session_state.step == "playing":
    r_idx = st.session_state.round
    p_idx = st.session_state.p_turn
    player = st.session_state.players[p_idx]
    
    st.subheader(f"Round {r_idx + 1} of 3")
    st.progress((r_idx * 3 + p_idx + 1) / 9)
    
    st.image(GAMES[r_idx]["url"], use_container_width=True)
    st.info(f"👤 **{player['name']}**, it's your turn!")
    
    user_input = st.text_area("Describe this image in 1-2 lines:", placeholder="Be descriptive...", key=f"input_{r_idx}_{p_idx}").lower()
    
    if st.button("SUBMIT PROMPT"):
        if len(user_input) < 15:
            st.error("Too short! Write a bit more to earn points.")
        else:
            # Scoring
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
            # Update scores and history
            st.session_state.players[p_idx]["total"] += score
            st.session_state.history.append({"round": r_idx, "name": player['name'], "score": score})
            
            # Rotation Logic
            if p_idx < 2:
                st.session_state.p_idx += 1
            else:
                st.session_state.step = "round_review"
            st.rerun()

# --- 3. ROUND REVIEW ---
elif st.session_state.step == "round_review":
    r_idx = st.session_state.round
    st.title(f"📊 Round {r_idx + 1} Results")
    st.image(GAMES[r_idx]["url"], use_container_width=True)
    
    # Show how each player did this round
    round_data = [h for h in st.session_state.history if h['round'] == r_idx]
    round_data = sorted(round_data, key=lambda x: x['score'], reverse=True)
    
    for i, res in enumerate(round_data):
        st.write(f"**{i+1}. {res['name']}** — `{res['score']} pts`")
    
    if st.button("NEXT ROUND ➡️"):
        if st.session_state.round < 2:
            st.session_state.round += 1
            st.session_state.p_turn = 0
            st.session_state.step = "playing"
        else:
            st.session_state.step = "final"
        st.rerun()

# --- 4. FINAL STANDINGS ---
elif st.session_state.step == "final":
    st.balloons()
    st.title("🏆 Final Standings")
    
    final_sorted = sorted(st.session_state.players, key=lambda x: x['total'], reverse=True)
    for i, p in enumerate(final_sorted):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        st.subheader(f"{medal} {p['name']}: {p['total']} total pts")
        
    if st.button("🔄 PLAY AGAIN"):
        st.session_state.clear()
        st.rerun()
