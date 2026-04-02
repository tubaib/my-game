import streamlit as st

# --- GAME CONFIG ---
GAMES = [
    {"url": "https://tinyurl.com/starry-night-img", "targets": ["starry", "night", "painting", "blue", "yellow"]},
    {"url": "https://tinyurl.com/cyberpunk-city-img", "targets": ["cyberpunk", "neon", "city", "future", "rain"]},
    {"url": "https://tinyurl.com/spaceman-art", "targets": ["astronaut", "space", "galaxy", "floating"]}
]

st.set_page_config(page_title="Prompt Master", layout="centered")

# --- SESSION STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "setup" # setup, playing, results
    st.session_state.players = []
    st.session_state.round = 0
    st.session_state.current_p_idx = 0
    st.session_state.round_scores = {0: [], 1: [], 2: []}

# --- STEP 1: SETUP ---
if st.session_state.step == "setup":
    st.title("🎨 Prompt Master")
    st.subheader("Mobile 3-Player Edition")
    
    p1 = st.text_input("Player 1 Name", "Player 1")
    p2 = st.text_input("Player 2 Name", "Player 2")
    p3 = st.text_input("Player 3 Name", "Player 3")
    
    if st.button("🚀 START GAME", use_container_width=True):
        st.session_state.players = [
            {"name": p1, "total": 0},
            {"name": p2, "total": 0},
            {"name": p3, "total": 0}
        ]
        st.session_state.step = "playing"
        st.rerun()

# --- STEP 2: PLAYING ---
elif st.session_state.step == "playing":
    round_idx = st.session_state.round
    p_idx = st.session_state.current_p_idx
    player = st.session_state.players[p_idx]
    
    st.header(f"Round {round_idx + 1}")
    st.progress((round_idx * 3 + p_idx + 1) / 9)
    
    st.image(GAMES[round_idx]["url"], use_container_width=True)
    st.info(f"📱 **Pass the phone to: {player['name']}**")
    
    user_input = st.text_input("Describe the image...", key=f"input_{round_idx}_{p_idx}").lower()
    
    if st.button("SUBMIT GUESS", use_container_width=True):
        # Scoring
        targets = GAMES[round_idx]["targets"]
        matches = [w for w in targets if w in user_input]
        score = int((len(matches) / len(targets)) * 100)
        
        # Save Score
        st.session_state.players[p_idx]["total"] += score
        st.session_state.round_scores[round_idx].append({"name": player['name'], "score": score})
        
        # Logic to move to next player or next round
        if p_idx < 2:
            st.session_state.current_p_idx += 1
        else:
            st.session_state.current_p_idx = 0
            st.session_state.round += 1
            
        if st.session_state.round > 2:
            st.session_state.step = "results"
        
        st.rerun()

# --- STEP 3: FINAL RESULTS ---
elif st.session_state.step == "results":
    st.balloons()
    st.title("🏆 Final Standings")
    
    # Show Final Leaderboard
    final_sorted = sorted(st.session_state.players, key=lambda x: x['total'], reverse=True)
    for i, p in enumerate(final_sorted):
        st.subheader(f"{i+1}. {p['name']} — {p['total']} pts")
    
    st.divider()
    if st.button("🔄 Play Again", use_container_width=True):
        st.session_state.clear()
        st.rerun()
