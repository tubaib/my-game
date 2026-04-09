import streamlit as st
import time
import streamlit.components.v1 as components

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Gen AI Carnival", layout="wide", initial_sidebar_state="collapsed")

# ------------------ PREMIUM CSS ------------------
st.markdown("""
<style>
@import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap)');

/* Hide Streamlit defaults */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background with animated gradient */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating particles effect */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #eee, transparent),
        radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
        radial-gradient(1px 1px at 90px 40px, #fff, transparent),
        radial-gradient(2px 2px at 130px 80px, rgba(255,255,255,0.6), transparent),
        radial-gradient(1px 1px at 160px 120px, #ddd, transparent);
    background-size: 200px 200px;
    animation: sparkle 4s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes sparkle {
    from { transform: translateY(0); }
    to { transform: translateY(-200px); }
}

/* Main Title */
.main-title {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 72px;
    font-weight: 900;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 25%, #4facfe 50%, #00f2fe 75%, #43e97b 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: textGradient 5s ease infinite;
    text-shadow: 0 0 80px rgba(79, 172, 254, 0.5);
    margin-bottom: 0;
    letter-spacing: 4px;
}

@keyframes textGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 24px;
    color: #a78bfa;
    margin-bottom: 50px;
    letter-spacing: 8px;
    text-transform: uppercase;
    opacity: 0.9;
}

/* Welcome text */
.welcome-text {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 42px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 10px;
    text-shadow: 0 0 30px rgba(167, 139, 250, 0.8);
}

/* Glass Card */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 20px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
}

.glass-card:hover::before {
    left: 100%;
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 
        0 25px 50px rgba(79, 172, 254, 0.3),
        0 0 100px rgba(167, 139, 250, 0.2),
        inset 0 0 60px rgba(255, 255, 255, 0.05);
    border-color: rgba(167, 139, 250, 0.5);
}

/* Neon Button */
.stButton > button {
    width: 100%;
    border-radius: 16px;
    height: 55px;
    font-size: 18px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-size: 200% 200%;
    color: white;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    animation: buttonPulse 2s ease-in-out infinite;
}

@keyframes buttonPulse {
    0%, 100% { box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4); }
    50% { box-shadow: 0 10px 60px rgba(102, 126, 234, 0.6), 0 0 30px rgba(240, 147, 251, 0.3); }
}

.stButton > button:hover {
    background-position: 100% 50%;
    transform: translateY(-3px);
    box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6), 0 0 40px rgba(240, 147, 251, 0.4);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Input Field */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px solid rgba(167, 139, 250, 0.3) !important;
    border-radius: 16px !important;
    color: #fff !important;
    font-size: 18px !important;
    padding: 15px 20px !important;
    font-family: 'Poppins', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 30px rgba(167, 139, 250, 0.4) !important;
    background: rgba(255, 255, 255, 0.08) !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.4) !important;
}

/* Leaderboard Entry */
.leaderboard-entry {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 20px 30px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.leaderboard-entry:hover {
    transform: translateX(10px);
    border-color: rgba(167, 139, 250, 0.5);
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
}

.leaderboard-rank {
    font-family: 'Orbitron', monospace;
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffd700, #ffaa00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    min-width: 60px;
}

.leaderboard-name {
    font-family: 'Poppins', sans-serif;
    font-size: 22px;
    color: #fff;
    flex-grow: 1;
    margin-left: 20px;
}

.leaderboard-score {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #4facfe;
    text-shadow: 0 0 20px rgba(79, 172, 254, 0.5);
}

/* Timer */
.timer-container {
    text-align: center;
    margin: 30px 0;
}

.timer {
    font-family: 'Orbitron', monospace;
    font-size: 64px;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 40px rgba(255, 255, 255, 0.5);
    animation: timerPulse 1s ease-in-out infinite;
}

.timer.warning {
    color: #f5576c;
    text-shadow: 0 0 40px rgba(245, 87, 108, 0.8);
}

@keyframes timerPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Game Image */
.game-image-container {
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 100px rgba(102, 126, 234, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 30px;
}

/* Section Title */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    color: #fff;
    margin-bottom: 40px;
    text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
}

/* Card Title */
.card-title {
    font-family: 'Poppins', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #fff;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 10px;
}

/* Trophy Icon */
.trophy-section {
    text-align: center;
    font-size: 80px;
    margin-bottom: 20px;
    animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

/* Success/Error Messages */
.stSuccess, .stError {
    border-radius: 16px !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Hide default label */
.stTextInput label {
    color: rgba(255, 255, 255, 0.7) !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px !important;
}

/* Decorative elements */
.decoration-circle {
    position: fixed;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.3;
    z-index: -1;
}

.circle-1 {
    width: 400px;
    height: 400px;
    background: #667eea;
    top: -100px;
    right: -100px;
}

.circle-2 {
    width: 300px;
    height: 300px;
    background: #f093fb;
    bottom: -50px;
    left: -50px;
}

/* Image styling */
.stImage {
    border-radius: 20px;
    overflow: hidden;
}

.stImage img {
    border-radius: 20px;
}
</style>

<!-- Decorative circles -->
<div class="decoration-circle circle-1"></div>
<div class="decoration-circle circle-2"></div>
""", unsafe_allow_html=True)

# ------------------ SOUND EFFECT ------------------
def play_sound(url):
    components.html(f"""
    <audio autoplay>
        <source src="{url}" type="audio/mp3">
    </audio>
    """, height=0)

# ------------------ CONFETTI ------------------
def show_confetti():
    components.html("""
    <script src="[cdn.jsdelivr.net](https://cdn.jsdelivr.net/npm/)[email protected]/dist/canvas-confetti.browser.min.js"></script>
    <script>
    confetti({
        particleCount: 150,
        spread: 180,
        origin: { y: 0.6 },
        colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
    });
    </script>
    """, height=0)

# ------------------ PROMPTS ------------------
PROMPTS = [
    {"title": "🏔️ Mountain", "emoji": "🏔️", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800)", "answers": ["mountain", "mountains"]},
    {"title": "🌊 Ocean", "emoji": "🌊", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800)", "answers": ["ocean", "sea", "beach"]},
    {"title": "🌃 City", "emoji": "🌃", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1494526585095-c41746248156?w=800)", "answers": ["city", "urban", "skyline"]},
    {"title": "🚀 Space", "emoji": "🚀", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800)", "answers": ["space", "galaxy", "stars"]},
    {"title": "🍔 Food", "emoji": "🍔", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800)", "answers": ["food", "meal", "dish"]},
    {"title": "🐕 Dog", "emoji": "🐕", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1517849845537-4d257902454a?w=800)", "answers": ["dog", "puppy", "canine"]},
    {"title": "🌲 Forest", "emoji": "🌲", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800)", "answers": ["tree", "forest", "nature", "trees"]},
    {"title": "🏎️ Car", "emoji": "🏎️", "image": "[images.unsplash.com](https://images.unsplash.com/photo-1502877338535-766e1452684a?w=800)", "answers": ["car", "vehicle", "automobile"]}
]

# ------------------ SESSION ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = ""
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# ------------------ HOME ------------------
def home():
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="main-title">🎡 GEN AI CARNIVAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">✨ From Prompts to Possibilities ✨</div>', unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("")
        
        # Glass card for login
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#a78bfa; font-size:20px; font-family:Poppins; margin-bottom:20px;">Enter the Arena</p>', unsafe_allow_html=True)
        
        name = st.text_input("", placeholder="Your Name...", label_visibility="collapsed")
        
        st.markdown("")
        
        if st.button("🚀 ENTER CARNIVAL"):
            if name:
                st.session_state.user = name
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.warning("⚠️ Please enter your name to continue!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ DASHBOARD ------------------
def dashboard():
    st.markdown(f'<div class="welcome-text">Welcome, {st.session_state.user}! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Choose Your Challenge</div>', unsafe_allow_html=True)
    
    # Create 2 rows of 4 cards
    for row in range(2):
        cols = st.columns(4)
        for col_idx in range(4):
            prompt_idx = row * 4 + col_idx
            if prompt_idx < len(PROMPTS):
                prompt = PROMPTS[prompt_idx]
                with cols[col_idx]:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.image(prompt["image"], use_container_width=True)
                    st.markdown(f'<div class="card-title">{prompt["title"]}</div>', unsafe_allow_html=True)
                    
                    if st.button(f"PLAY", key=f"btn_{prompt_idx}"):
                        st.session_state.selected_prompt = prompt_idx
                        st.session_state.start_time = time.time()
                        st.session_state.game_over = False
                        st.session_state.page = "game"
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ GAME ------------------
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f'<div class="main-title">{prompt["emoji"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">What do you see?</div>', unsafe_allow_html=True)
        
        # Timer
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(15 - elapsed, 0)
        
        timer_class = "timer warning" if remaining <= 5 else "timer"
        st.markdown(f'''
        <div class="timer-container">
            <div class="{timer_class}">{remaining:02d}</div>
            <p style="color:#a78bfa; font-family:Poppins;">seconds remaining</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Image
        st.markdown('<div class="game-image-container">', unsafe_allow_html=True)
        st.image(prompt["image"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check if time is up
        if remaining == 0 and not st.session_state.game_over:
            st.session_state.game_over = True
            st.error("⏰ Time's up!")
            play_sound("[soundjay.com](https://www.soundjay.com/button/beep-10.mp3)")
            
            st.session_state.leaderboard.append({
                "name": st.session_state.user,
                "score": 0,
                "challenge": prompt["title"]
            })
            
            time.sleep(1)
            st.session_state.page = "leaderboard"
            st.rerun()
        
        # Input
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        guess = st.text_input("", placeholder="Type your answer...", label_visibility="collapsed")
        
        st.markdown("")
        
        if st.button("⚡ SUBMIT ANSWER"):
            if guess.lower().strip() in prompt["answers"]:
                st.success("🎉 CORRECT! Amazing!")
                show_confetti()
                play_sound("[soundjay.com](https://www.soundjay.com/human/sounds/applause-01.mp3)")
                score = max(10, remaining * 2)  # Bonus for speed
            else:
                st.error("❌ Not quite right!")
                play_sound("[soundjay.com](https://www.soundjay.com/button/beep-10.mp3)")
                score = 0
            
            st.session_state.leaderboard.append({
                "name": st.session_state.user,
                "score": score,
                "challenge": prompt["title"]
            })
            
            time.sleep(1.5)
            st.session_state.page = "leaderboard"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ LEADERBOARD ------------------
def leaderboard():
    st.markdown('<div class="trophy-section">🏆</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">LEADERBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Hall of Fame</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
        
        if not sorted_board:
            st.markdown('<p style="text-align:center; color:#a78bfa; font-size:20px;">No scores yet. Be the first!</p>', unsafe_allow_html=True)
        
        for i, entry in enumerate(sorted_board[:10]):  # Top 10
            rank_emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎯"
            
            st.markdown(f'''
            <div class="leaderboard-entry">
                <div class="leaderboard-rank">{rank_emoji}</div>
                <div class="leaderboard-name">{entry['name']}</div>
                <div class="leaderboard-score">{entry['score']} pts</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("")
        
        if st.button("🔥 PLAY AGAIN"):
            st.session_state.page = "dashboard"
            st.rerun()
        
        st.markdown("")
        
        if st.button("🏠 HOME"):
            st.session_state.page = "home"
            st.rerun()

# ------------------ ROUTER ------------------
if st.session_state.page == "home":
    home()
elif st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "game":
    game()
elif st.session_state.page == "leaderboard":
    leaderboard()
