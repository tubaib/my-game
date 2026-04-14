import streamlit as st
import streamlit.components.v1 as components

# CONFIG
st.set_page_config(page_title="Gen AI Carnival", page_icon="🎡", layout="wide")

# GLOBAL CSS
st.markdown("""
<style>
/* ── Reset & base ── */
* { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background: #0a0a12;
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

/* ── Typography ── */

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ── Animated starfield background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,102,241,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(56,189,248,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 50% 50%, rgba(168,85,247,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── Page content sits above bg ── */
[data-testid="block-container"] {
    position: relative;
    z-index: 1;
    padding-top: 2rem !important;
    max-width: 1200px !important;
    margin: 0 auto;
}

/* ── HERO title ── */
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 13px;
    font-weight: 500;
    color: #a5b4fc;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.hero-title {
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 700;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 40%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 16px;
}
.hero-sub {
    font-size: 18px;
    color: #64748b;
    font-weight: 400;
    margin-bottom: 40px;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 28px;
    backdrop-filter: blur(16px);
    transition: all 0.3s ease;
}
.glass-card:hover {
    background: rgba(255,255,255,0.07);
    border-color: rgba(99,102,241,0.4);
    transform: translateY(-4px);
    box-shadow: 0 24px 48px rgba(0,0,0,0.4), 0 0 0 1px rgba(99,102,241,0.2);
}

/* ── Challenge card ── */
.challenge-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}
.challenge-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(99,102,241,0.5);
    box-shadow: 0 20px 60px rgba(99,102,241,0.25);
}
.challenge-card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    display: block;
    filter: brightness(0.85) saturate(1.1);
}
.challenge-card-body {
    padding: 16px;
}
.challenge-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 4px;
}
.challenge-card-sub {
    font-size: 12px;
    color: #475569;
    font-weight: 400;
}

/* ── Avatar ── */
.avatar {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #38bdf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0,0,0,0.4);
    margin: 0 auto 16px;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.25);
}

/* ── Timer ring ── */
.timer-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}
.timer-ring {
    font-size: 48px;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1;
    font-variant-numeric: tabular-nums;
    text-shadow: 0 0 30px rgba(56,189,248,0.5);
}
.timer-label {
    font-size: 12px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.timer-ring.danger { color: #f87171; text-shadow: 0 0 30px rgba(248,113,113,0.6); }

/* ── Score pill ── */
.score-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 999px;
    padding: 8px 20px;
    font-size: 15px;
    font-weight: 600;
    color: #a5b4fc;
}

/* ── Leaderboard row ── */
.lb-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    border-radius: 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 10px;
    transition: all 0.2s;
}
.lb-row:hover {
    background: rgba(255,255,255,0.06);
    border-color: rgba(99,102,241,0.25);
}
.lb-rank {
    font-size: 20px;
    font-weight: 700;
    min-width: 40px;
    text-align: center;
}
.lb-rank.gold   { color: #fbbf24; }
.lb-rank.silver { color: #94a3b8; }
.lb-rank.bronze { color: #92400e; }
.lb-rank.other  { color: #475569; }
.lb-name {
    flex: 1;
    font-size: 16px;
    font-weight: 500;
    color: #e2e8f0;
}
.lb-score {
    font-size: 15px;
    font-weight: 600;
    color: #38bdf8;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 8px;
    padding: 4px 14px;
}

/* ── Input overrides ── */
[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 12px !important;
    color: #111111 !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
    height: 50px !important;
    transition: all 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
    background: #ffffff !important;
}
[data-testid="stTextInput"] label {
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
}

/* ── Button overrides ── */
.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    height: 50px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    background: linear-gradient(135deg, #6366f1 0%, #38bdf8 100%) !important;
    color: #fff !important;
    border: none !important;
    transition: all 0.25s ease !important;
    text-transform: none !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
    filter: brightness(1.08) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Success / Error override ── */
[data-testid="stSuccess"] {
    background: rgba(52,211,153,0.1) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    border-radius: 12px !important;
    color: #6ee7b7 !important;
}
[data-testid="stError"] {
    background: rgba(248,113,113,0.1) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    border-radius: 12px !important;
    color: #fca5a5 !important;
}
[data-testid="stWarning"] {
    background: rgba(251,191,36,0.1) !important;
    border: 1px solid rgba(251,191,36,0.3) !important;
    border-radius: 12px !important;
    color: #fde68a !important;
}

/* ── Image ── */
[data-testid="stImage"] img {
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}

/* ── Divider ── */
hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 24px 0 !important;
}

/* ── Section heading ── */
.section-heading {
    font-size: 13px;
    font-weight: 500;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 20px;
}

/* ── Stat row ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}
.stat-chip {
    flex: 1;
    min-width: 100px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
}
.stat-chip-val {
    font-size: 24px;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1;
    margin-bottom: 4px;
}
.stat-chip-lbl {
    font-size: 12px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# SOUND
def play_sound(url):
    components.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# DATA
PROMPTS = [
   PROMPTS = [
    {
        "title": "Sunset Beach", "emoji": "🌅",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
        "answers": [
            "a beautiful sunset over the ocean",
            "sun setting on a beach with waves"
        ]
    },
    {
        "title": "Snow Mountains", "emoji": "🏔️",
        "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=600&q=80",
        "answers": [
            "snow covered mountains under blue sky",
            "a mountain range filled with snow"
        ]
    },
    {
        "title": "City Night", "emoji": "🌃",
        "image": "https://images.unsplash.com/photo-1494526585095-c41746248156?w=600&q=80",
        "answers": [
            "a city skyline at night with lights",
            "bright city buildings glowing in the dark"
        ]
    },
    {
        "title": "Galaxy Space", "emoji": "🌌",
        "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&q=80",
        "answers": [
            "a galaxy with stars and space",
            "deep space filled with stars and nebula"
        ]
    },
    {
        "title": "Delicious Food", "emoji": "🍕",
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80",
        "answers": [
            "a plate of delicious food",
            "tasty meal served on a table"
        ]
    },
    {
        "title": "Cute Dog", "emoji": "🐶",
        "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600&q=80",
        "answers": [
            "a cute dog looking at the camera",
            "a small puppy sitting and staring"
        ]
    },
    {
        "title": "Green Forest", "emoji": "🌳",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=600&q=80",
        "answers": [
            "a dense green forest with trees",
            "sunlight passing through forest trees"
        ]
    },
    {
        "title": "Sports Car", "emoji": "🚗",
        "image": "https://images.unsplash.com/photo-1493238792000-8113da705763?w=600&q=80",
        "answers": [
            "a fast sports car on the road",
            "a luxury car driving on highway"
        ]
    }
]


# SESSION
for k, v in {
    "page": "home", "user": "", "selected_prompt": None,
    "leaderboard": []
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# HOME
def home():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="text-align:center; padding: 60px 0 40px;">
            <div class="hero-title">Gen AI<br>Carnival</div>
            <div class="hero-sub">From Prompts to Possibilities</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stat-row">
            <div class="stat-chip"><div class="stat-chip-val">8</div><div class="stat-chip-lbl">Challenges</div></div>
            <div class="stat-chip"><div class="stat-chip-val">10</div><div class="stat-chip-lbl">Max Points</div></div>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("", placeholder="Enter your name to begin…", label_visibility="collapsed")

        if st.button("Enter the Carnival  →"):
            if name.strip():
                st.session_state.user = name.strip()
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.warning("Please enter your name first.")

# DASHBOARD
def dashboard():
    initials = "".join(w[0].upper() for w in st.session_state.user.split()[:2])
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:20px; margin-bottom:40px; padding:24px 28px;
                background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:20px;">
        <div class="avatar" style="margin:0; flex-shrink:0;">{initials}</div>
        <div>
            <div style="font-size:22px; font-weight:700; color:#e2e8f0; line-height:1.2;">
                Hey, {st.session_state.user}!
            </div>
            <div style="font-size:14px; color:#475569; margin-top:4px;">
                Pick a challenge below — you've got 10 seconds to nail it.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Choose your challenge</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, prompt in enumerate(PROMPTS):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="challenge-card">
                <img src="{prompt['image']}" alt="{prompt['title']}">
                <div class="challenge-card-body">
                    <div class="challenge-card-title">{prompt['emoji']} {prompt['title']}</div>
                    <div class="challenge-card-sub">Guess the image</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Play →", key=f"btn_{i}"):
                st.session_state.selected_prompt = i
                st.session_state.page = "game"
                st.rerun()

# GAME
def game():
    prompt = PROMPTS[st.session_state.selected_prompt]

    col_img, col_ctrl = st.columns([3, 2], gap="large")

    with col_img:
        st.markdown(f"""
        <div style="margin-bottom:12px;">
            <span class="score-pill">🎯 {prompt['emoji']} Round {st.session_state.selected_prompt + 1}</span>
        </div>
        """, unsafe_allow_html=True)
        st.image(prompt["image"], use_container_width=True)

    with col_ctrl:
        st.markdown("""
        <div style="margin-bottom:8px; font-size:13px; color:#64748b; font-weight:500;">
            WHAT DO YOU SEE?
        </div>
        """, unsafe_allow_html=True)

        guess = st.text_input("", placeholder="Type your answer…", label_visibility="collapsed", key="guess_input")

        if st.button("Submit Answer  ✓"):
            if guess.lower() in prompt["answers"]:
                st.success("✅ Nailed it! +10 points")
                st.balloons()
                play_sound("https://www.soundjay.com/human/cheering-01.mp3")
                score = 10
            else:
                st.error(f"❌ Wrong! The answer was: {prompt['answers'][0].title()}")
                play_sound("https://www.soundjay.com/button/beep-10.mp3")
                score = 0

            st.session_state.leaderboard.append({"name": st.session_state.user, "score": score})
            st.session_state.page = "leaderboard"
            st.rerun()

        st.markdown("""
        <div style="margin-top:20px; padding:14px 16px; background:rgba(255,255,255,0.03);
                    border:1px solid rgba(255,255,255,0.06); border-radius:12px;">
            <div style="font-size:12px; color:#475569; text-transform:uppercase; letter-spacing:0.08em;
                        margin-bottom:8px;">Hints</div>
            <div style="font-size:13px; color:#64748b; line-height:1.7;">
                • Look at the overall scene<br>
                • One-word answers work best<br>
                • Synonyms are accepted
            </div>
        </div>
        """, unsafe_allow_html=True)

# LEADERBOARD
def leaderboard():
    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown("""
        <div style="text-align:center; margin-bottom:40px;">
            <div class="hero-badge">✦ Results</div>
            <div class="hero-title" style="font-size:clamp(32px,5vw,56px);">Leaderboard</div>
        </div>
        """, unsafe_allow_html=True)

        sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
        rank_classes = ["gold", "silver", "bronze"]
        rank_icons = ["🥇", "🥈", "🥉"]

        for i, entry in enumerate(sorted_board):
            rc = rank_classes[i] if i < 3 else "other"
            icon = rank_icons[i] if i < 3 else f"#{i+1}"
            initials = "".join(w[0].upper() for w in entry["name"].split()[:2])
            st.markdown(f"""
            <div class="lb-row">
                <div class="lb-rank {rc}">{icon}</div>
                <div class="avatar" style="width:38px;height:38px;font-size:14px;margin:0;flex-shrink:0;
                                            box-shadow:0 0 0 3px rgba(99,102,241,0.2);">{initials}</div>
                <div class="lb-name">{entry['name']}</div>
                <div class="lb-score">{entry['score']} pts</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔁  Play Again"):
                st.session_state.page = "dashboard"
                st.rerun()
        with c2:
            if st.button("🏠  Back to Home"):
                st.session_state.page = "home"
                st.rerun()

# ROUTER
pages = {"home": home, "dashboard": dashboard, "game": game, "leaderboard": leaderboard}
pages[st.session_state.page]()
