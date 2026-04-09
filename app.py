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
    {"url": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809", "targets": ["gradient", "colors", "mesh", "soft", "vibrant"], "title": "Chromatic Flow"},
    {"url": "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e", "targets": ["moon", "surreal", "floating", "night", "clouds"], "title": "Lunar Gravity"},
    {"url": "https://images.unsplash.com/photo-1547891299-bc7837090333", "targets": ["water", "splash", "liquid", "macro", "crystal"], "title": "Liquid Motion"}
]

st.set_page_config(page_title="Prompt Picasso | Gen AI Carnival", layout="centered")

# --- 2. PREMIUM CARNIVAL UI DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Space+Grotesk:wght@300;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e 0%, #020205 100%);
        color: #e0e0e0;
        font-family: 'Space Grotesk', sans-serif;
    }

    .carnival-header {
        font-family: 'Bungee Spice', cursive;
        font-size: 3.5rem;
        text-align: center;
        margin-top: -30px;
        filter: drop-shadow(0 0 10px rgba(255, 75, 75, 0.5));
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 210, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8000 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        height: 3.5rem;
        width: 100%;
        transition: 0.3s all ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.6);
        color: white !important;
    }

    .player-tag {
        background: rgba(0, 210, 255, 0.15);
        border: 1px solid #00d2ff;
        padding: 6px 14px;
        border-radius: 8px;
        margin: 5px;
        display: inline-block;
        font-weight: bold;
        color: #00d2ff;
    }
    
    h3 { color: #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "round_setup" 
    st.session_state.round = 0
    st.session_state.round_players = []
    st.session_state.p_turn = 0
    st.session_state.master_leaderboard = {} 
    st.session_state.round_history = []

# --- 4. STEP 1: PER-ROUND REGISTRATION ---
if st.session_state.step == "round_setup":
    st.markdown('<h1 class="carnival-header">PROMPT PICASSO</h1>', unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; margin-top: -10px;'>GRAND GEN AI CARNIVAL 🎪</h5>", unsafe_allow_html=True)
    
    st.markdown(f"### 🎟️ Round {st.session_state.round + 1} Registration")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write(f"**Up Next:** {GAMES[st.session_state.round]['title']}")
        
        p_name = st.text_input("Enter Player Name", placeholder="Type name here...", key="p_reg")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ JOIN ROUND"):
                if p_name and len(st.session_state.round_players) < 5:
                    if p_name not in st.session_state.round_players:
                        st.session_state.round_players.append(p_name)
                        st.rerun()
        with col2:
            if st.button("🗑️ CLEAR LIST"):
                st.session_state.round_players = []
                st.rerun()

        if st.session_state.round_players:
            st.divider()
            st.write("**Players in this Round:**")
            for p in st.session_state.round_players:
                st.markdown(f'<span class="player-tag">👤 {p}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if 1 <= len(st.session_state.round_players) <= 5:
        if st.button(f"🚀 COMMENCE ROUND {st.session_state.round + 1}"):
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
    st.markdown(f"<h2 style='color: #FF4B4B;'>Player: {p_name}</h2>", unsafe_allow_html=True)

    st.image(GAMES[r_idx]["url"], use_container_width=True)
    user_input = st.text_area("Describe the image in 1 or 2 lines:", placeholder="Be as descriptive as possible...", key=f"play_{r_idx}_{p_name}").lower()
    
    if st.button("✨ SUBMIT DESCRIPTION"):
        if len(user_input) < 10:
            st.error("Too short! Provide more detail for the AI.")
        else:
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
            # Save scores
            st.session_state.master_leaderboard[p_name] = st.session_state.master_leaderboard.get(p_name, 0) + score
            st.session_state.round_history.append({"Round": r_idx + 1, "Player": p_name, "Score": score})
            
            if st.session_state.p_turn < len(st.session_state.round_players) - 1:
                st.session_state.p_turn += 1
            else:
                st.session_state.step = "leaderboard"
            st.rerun()

# --- 6. STEP 3: ROUND LEADERBOARD ---
elif st.session_state.step == "leaderboard":
    r_idx = st.session_state.round
    st.title(f"📊 Round {r_idx + 1} Rankings")
    
    current_round_data = [h for h in st.session_state.round_history if h['Round'] == r_idx + 1]
    df = pd.DataFrame(current_round_data).sort_values(by="Score", ascending=False)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.table(df[["Player", "Score"]])
    st.markdown('</div>', unsafe_allow_html=True)
    
    btn_label = "NEXT CHALLENGE: NEW PLAYERS 🎡" if r_idx < 7 else "SHOW FINAL STANDINGS 🏆"
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
    st.markdown('<h1 class="carnival-header">THE HALL OF FAME</h1>', unsafe_allow_html=True)
    
    master_df = pd.DataFrame(st.session_state.master_leaderboard.items(), columns=['Player', 'Total Points'])
    master_df = master_df.sort_values(by="Total Points", ascending=False)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🥇 Tournament Leaders")
    st.table(master_df.head(10))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 RESTART CARNIVAL"):
        st.session_state.clear()
        st.rerun()
