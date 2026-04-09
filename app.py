import streamlit as st
import pandas as pd

# --- 1. STABLE CARNIVAL CONFIGURATION ---
# Using specific Unsplash Source IDs for higher reliability
GAMES = [
    {"url": "https://images.unsplash.com/photo-1579310964728-441f2000c1be?auto=format&fit=crop&q=80&w=800", "targets": ["forest", "sunlight", "magic", "trees", "ethereal"], "title": "The Enchanted Grove"},
    {"url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&q=80&w=800", "targets": ["abstract", "geometry", "lines", "blue", "minimal"], "title": "Digital Dreamscape"},
    {"url": "https://images.unsplash.com/photo-1605142859862-978be7eba909?auto=format&fit=crop&q=80&w=800", "targets": ["architecture", "modern", "stairs", "white", "symmetry"], "title": "The Infinite Staircase"},
    {"url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?auto=format&fit=crop&q=80&w=800", "targets": ["neon", "cyberpunk", "robot", "future", "glow"], "title": "Android Awakening"},
    {"url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800", "targets": ["earth", "space", "satellite", "network", "global"], "title": "Orbital Network"},
    {"url": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&q=80&w=800", "targets": ["gradient", "colors", "mesh", "soft", "vibrant"], "title": "Chromatic Flow"},
    {"url": "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?auto=format&fit=crop&q=80&w=800", "targets": ["moon", "surreal", "floating", "night", "clouds"], "title": "Lunar Gravity"},
    {"url": "https://images.unsplash.com/photo-1547891299-bc7837090333?auto=format&fit=crop&q=80&w=800", "targets": ["water", "splash", "liquid", "macro", "crystal"], "title": "Liquid Motion"}
]

st.set_page_config(page_title="Prompt Picasso | Carnival", layout="centered")

# --- 2. PREMIUM UI DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Spice&family=Space+Grotesk:wght@700&display=swap');
    
    .stApp { background: #05050a; color: #e0e0e0; font-family: 'Space Grotesk', sans-serif; }
    .carnival-header { font-family: 'Bungee Spice', cursive; font-size: 3.2rem; text-align: center; margin-top: -40px; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 25px; border-radius: 20px; 
        border: 1px solid #00d2ff; margin-bottom: 20px; 
    }
    .stButton>button { 
        background: linear-gradient(90deg, #FF4B4B, #FF8000); 
        color: white; border-radius: 12px; font-weight: 700; height: 3.5rem; width: 100%; 
    }
    .player-tag { 
        background: rgba(255, 0, 255, 0.2); border: 1px solid #ff00ff; 
        padding: 5px 12px; border-radius: 8px; margin: 5px; display: inline-block; 
    }
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

# --- 4. STEP 1: ROUND REGISTRATION ---
if st.session_state.step == "round_setup":
    st.markdown('<h1 class="carnival-header">PROMPT PICASSO</h1>', unsafe_allow_html=True)
    st.markdown(f"### 🎟️ Round {st.session_state.round + 1} Artist Signup")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write(f"🏷️ **Challenge Name:** {GAMES[st.session_state.round]['title']}")
        p_name = st.text_input("Enter Player Name", placeholder="Type here...", key=f"reg_{st.session_state.round}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ ADD PLAYER"):
                if p_name and len(st.session_state.round_players) < 5:
                    if p_name not in st.session_state.round_players:
                        st.session_state.round_players.append(p_name)
                        st.rerun()
        with col2:
            if st.button("🗑️ RESET LIST"):
                st.session_state.round_players = []
                st.rerun()

        if st.session_state.round_players:
            st.divider()
            for p in st.session_state.round_players:
                st.markdown(f'<span class="player-tag">👤 {p}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if 1 <= len(st.session_state.round_players) <= 5:
        if st.button(f"🚀 START ROUND {st.session_state.round + 1}"):
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
    st.markdown(f"<h2 style='color: #00d2ff;'>Artist: {p_name}</h2>", unsafe_allow_html=True)

    # use_container_width ensures the image fits the screen properly
    st.image(GAMES[r_idx]["url"], use_container_width=True)
    
    user_input = st.text_area("Your Description (1-2 lines):", key=f"play_{r_idx}_{p_name}").lower()
    
    if st.button("✨ SUBMIT TO JUDGES"):
        if len(user_input) < 10:
            st.error("Too short! Add more detail.")
        else:
            targets = GAMES[r_idx]["targets"]
            matches = [w for w in targets if w in user_input]
            score = int((len(matches) / len(targets)) * 100)
            
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
    st.title(f"📊 Round {r_idx + 1} Scores")
    
    round_data = [h for h in st.session_state.round_history if h['Round'] == r_idx + 1]
    df = pd.DataFrame(round_data).sort_values(by="Score", ascending=False)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.table(df[["Player", "Score"]])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("NEXT ROUND 🎡" if r_idx < 7 else "GRAND FINALE 🏆"):
        if r_idx < 7:
            st.session_state.round += 1
            st.session_state.round_players = []
            st.session_state.step = "round_setup"
        else:
            st.session_state.step = "final"
        st.rerun()

# --- 7. STEP 4: FINAL STANDINGS ---
elif st.session_state.step == "final":
    st.balloons()
    st.markdown('<h1 class="carnival-header">HALL OF FAME</h1>', unsafe_allow_html=True)
    
    master_df = pd.DataFrame(st.session_state.master_leaderboard.items(), columns=['Player', 'Total Points'])
    master_df = master_df.sort_values(by="Total Points", ascending=False)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.table(master_df.head(10))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 RESTART GAME"):
        st.session_state.clear()
        st.rerun()
