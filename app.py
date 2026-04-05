import streamlit as st
import time
import pandas as pd

# --- 1. CARNIVAL CONFIGURATION ---
# 8 Prompts for the Grand Carnival
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

# --- 2. CARNIVAL UI DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Space+Grotesk:wght@300;700&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #020205 100%);
        color: #e0e0e0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Carnival Title Styling */
    .carnival-header {
        font-family: 'Bungee Spice', cursive;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 0px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 0, 255, 0.2);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.1);
        margin-bottom: 25px;
    }

    /* Neon Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #00d2ff);
        color: white;
        border: none;
        border-radius: 50px;
        font-weight: 800;
        letter-spacing: 2px;
        height: 3.5rem;
        transition: 0.4s;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 0, 255, 0.4);
    }

    /* Player Chips */
    .player-chip {
        background: rgba(0, 210, 255, 0.1);
        border: 1px solid #00d2ff;
        padding: 5px 15px;
        border-radius: 15px;
        margin-right: 10px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "lobby"
    st.session_state.players = []
    st.session_state.round = 0
    st.session_state.p_turn = 0
    st.session_state.history = []

# --- 4. THE LOBBY (1-5 Players) ---
if st.session_state.step == "lobby":
    st.markdown('<h1 class="carnival-header">PROMPT PICASSO</h1>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #00d2ff;'>THE GRAND GEN AI CARNIVAL</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("🎪 **Join the Booth:** Add 1 to 5 players to start.")
    
    p_name = st.text_input("Enter Artist Name", placeholder="e.g. AI_Master", key="name_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ADD PLAYER"):
            if p_name and len(st.session_state.players) < 5:
                st.session_state.players.append({"name": p_name, "total": 0})
                st.rerun()
    with col2:
        if st.button("RESET LOBBY"):
            st.session_state.players = []
            st.rerun()

    if st.session_state.players:
        st.write("---")
        for p in st.session_state.players:
            st.markdown(f'<span class="player-chip">🎨 {p["name"]}</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    if 1 <= len(st.session_state.players) <= 5:
        if st.button("🔥 START THE CARNIVAL"):
            st.session_state.step = "playing"
            st.rerun()

# --- 5. GAMEPLAY (8 Rounds) ---
elif st.session_state.step == "playing":
    r_idx = st.session_state.round
    p_idx = st.session_state.p_turn
    player = st.session_state.players[p_idx]
    
    st.title("🖌️ Performance Stage")
    st.progress((r_idx * len(st.session_state.players) + p_idx + 1) / (8 * len(st.session_state.players)))
    
    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <h3>Round {r_idx + 1} / 8</h3>
            <h4 style='color: #ff00ff;'>Current Artist: {player['name']}</h4>
        </div>
    """, unsafe_allow_html=True)

    st.image(GAMES[r_idx]["url"], caption=GAMES[r_idx]["title"], use_container_width=True)
    
    user_input = st.text_area("Describe this masterpiece to the AI...", height=100).lower()
    
    if st.button("🎨 SUBMIT PROMPT"):
        if len(user_input) < 10:
            st.error("Too short! A Picasso needs more detail.")
        else:
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
            st.session_state.players[p_idx]["total"] += score
            st.session_state.history.append({"round": r_idx, "name": player['name'], "score": score})
            
            # Switch players or rounds
            if p_idx < len(st.session_state.players) - 1:
                st.session_state.p_turn += 1
            else:
                st.session_state.p_turn = 0
                st.session_state.step = "round_review"
            st.rerun()

# --- 6. ROUND REVIEW ---
elif st.session_state.step == "round_review":
    r_idx = st.session_state.round
    st.title(f"🏆 Round {r_idx + 1} Scoreboard")
    
    round_data = [h for h in st.session_state.history if h['round'] == r_idx]
    round_data = sorted(round_data, key=lambda x: x['score'], reverse=True)
    
    for i, res in enumerate(round_data):
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #00d2ff;'>
                <strong>Rank {i+1}: {res['name']}</strong> — {res['score']} pts
            </div>
        """, unsafe_allow_html=True)

    btn_text = "NEXT CHALLENGE 🎡" if r_idx < 7 else "FINAL CARNIVAL STANDINGS 🏆"
    if st.button(btn_text):
        if r_idx < 7:
            st.session_state.round += 1
            st.session_state.step = "playing"
        else:
            st.session_state.step = "final"
        st.rerun()

# --- 7. THE HALL OF FAME ---
elif st.session_state.step == "final":
    st.balloons()
    st.markdown('<h1 class="carnival-header">GRAND FINALE</h1>', unsafe_allow_html=True)
    
    final_sorted = sorted(st.session_state.players, key=lambda x: x['total'], reverse=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for i, p in enumerate(final_sorted):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        st.subheader(f"{medal} {p['name']} — Total: {p['total']} pts")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("RESTART CARNIVAL"):
        st.session_state.clear()
        st.rerun()
