import streamlit as st
import time
import pandas as pd

# --- 1. CONFIGURATION & ASSETS ---
GAMES = [
    {"url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b", "targets": ["mountains", "peaks", "nature", "clouds", "landscape"]},
    {"url": "https://images.unsplash.com/photo-1514565131-fce0801e5785", "targets": ["city", "skyline", "buildings", "urban", "night"]},
    {"url": "https://images.unsplash.com/photo-1500622764614-be358d8d80c3", "targets": ["forest", "trees", "green", "woods", "sunlight"]}
]

st.set_page_config(page_title="Prompt Master: Elite", layout="centered")

# --- 2. ADVANCED GLASS DESIGN ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 3.5em; 
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border: none; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 20px rgba(0, 210, 255, 0.5); }
    .leaderboard-table { width: 100%; border-radius: 15px; overflow: hidden; background: rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (The Lobby Logic) ---
if "room_players" not in st.session_state:
    st.session_state.room_players = []
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "turn_idx" not in st.session_state:
    st.session_state.turn_idx = 0
if "all_time_record" not in st.session_state:
    st.session_state.all_time_record = [] # Global Record

# --- 4. NAVIGATION LOGIC ---
def start_game():
    st.session_state.game_active = True

# --- 5. LOBBY SCREEN (Waiting for 5) ---
if not st.session_state.game_active:
    st.title("🛡️ Prompt Master: Elite Room")
    st.markdown(f"### Lobby Status: `{len(st.session_state.room_players)} / 5 Players`")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        new_player = st.text_input("Enter your codename:", placeholder="e.g. ShadowWriter")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Join Room"):
                if new_player and len(st.session_state.room_players) < 5:
                    if new_player not in [p['name'] for p in st.session_state.room_players]:
                        st.session_state.room_players.append({"name": new_player, "score": 0})
                        st.rerun()
        with col2:
            if st.button("Reset Room"):
                st.session_state.room_players = []
                st.rerun()
        
        # Display Joined Players
        if st.session_state.room_players:
            st.write("---")
            for p in st.session_state.room_players:
                st.markdown(f"✅ **{p['name']}** joined the room.")
        st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.room_players) >= 5:
        st.success("Room Full! Initializing Game...")
        time.sleep(1)
        st.session_state.game_active = True
        st.rerun()

# --- 6. GAMEPLAY SCREEN ---
else:
    r_idx = st.session_state.current_round
    p_idx = st.session_state.turn_idx
    
    if r_idx < 3: # 3 Rounds Total
        player = st.session_state.room_players[p_idx]
        
        st.markdown(f"#### Round {r_idx + 1} • {player['name']}'s Turn")
        st.progress((r_idx * 5 + p_idx + 1) / 15)
        
        st.image(GAMES[r_idx]["url"], use_container_width=True)
        
        user_input = st.text_area("Analyze the image and provide your prompt:", key=f"input_{r_idx}_{p_idx}")
        
        if st.button("Submit to Leaderboard"):
            # Scoring
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input.lower()]
            score = int((len(matches) / len(targets)) * 100)
            
            # Update internal score
            st.session_state.room_players[p_idx]["score"] += score
            
            # Turn Logic
            if p_idx < 4:
                st.session_state.turn_idx += 1
            else:
                st.session_state.turn_idx = 0
                st.session_state.current_round += 1
            st.rerun()

    # --- 7. FINAL RECORD & LEADERBOARD ---
    else:
        st.balloons()
        st.title("🏆 Room Results")
        
        final_players = sorted(st.session_state.room_players, key=lambda x: x['score'], reverse=True)
        
        # Add to All-Time Record
        for p in final_players:
            st.session_state.all_time_record.append({"Player": p['name'], "Total Score": p['score'], "Date": time.strftime("%Y-%m-%d")})
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Current Room Rankings")
        for i, p in enumerate(final_players):
            st.write(f"#{i+1} **{p['name']}** — {p['score']} pts")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("📜 All-Time Hall of Fame")
        df = pd.DataFrame(st.session_state.all_time_record)
        if not df.empty:
            df = df.sort_values(by="Total Score", ascending=False).head(10)
            st.table(df)

        if st.button("New Room"):
            st.session_state.game_active = False
            st.session_state.room_players = []
            st.session_state.current_round = 0
            st.rerun()
