import streamlit as st
import random
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="🪨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS + JS animations ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a0a2e 0%, #0a0a0f 60%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="block-container"] { padding-top: 2rem !important; }

/* ── Typography ── */
* { font-family: 'Space Mono', monospace; color: #e8e0ff; }

.title-wrap {
    text-align: center;
    margin-bottom: 0.5rem;
}
.game-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 5.5rem);
    letter-spacing: 0.12em;
    background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
    animation: shimmer 4s ease-in-out infinite alternate;
    background-size: 200% 200%;
}
@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.subtitle {
    font-size: 0.7rem;
    letter-spacing: 0.4em;
    color: #6366f1;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* ── Score board ── */
.scoreboard {
    display: flex;
    justify-content: center;
    gap: 1.2rem;
    margin: 1.2rem 0;
}
.score-cell {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.7rem 1.6rem;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
    min-width: 80px;
}
.score-cell:hover { transform: translateY(-2px); }
.score-label {
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.2rem;
}
.score-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
}
.score-num.wins  { color: #4ade80; }
.score-num.losses{ color: #f87171; }
.score-num.ties  { color: #facc15; }

/* ── Choice buttons ── */
.btn-row {
    display: flex;
    justify-content: center;
    gap: 1.2rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.choice-btn {
    background: rgba(255,255,255,0.04);
    border: 2px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 1.2rem 1.8rem;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(.34,1.56,.64,1);
    text-align: center;
    min-width: 110px;
    position: relative;
    overflow: hidden;
}
.choice-btn::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(129,140,248,0.15), transparent 70%);
    opacity: 0;
    transition: opacity 0.3s;
}
.choice-btn:hover::before { opacity: 1; }
.choice-btn:hover {
    border-color: #818cf8;
    transform: translateY(-6px) scale(1.06);
    box-shadow: 0 16px 40px rgba(129,140,248,0.25);
}
.choice-emoji { font-size: 2.8rem; display: block; margin-bottom: 0.4rem; }
.choice-label {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #a5b4fc;
}

/* ── Battle arena ── */
.arena {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    position: relative;
}
.arena-side {
    text-align: center;
    flex: 1;
}
.arena-label {
    font-size: 0.6rem;
    letter-spacing: 0.4em;
    color: #6366f1;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
}
.arena-emoji {
    font-size: 4rem;
    display: block;
    line-height: 1.2;
    animation: popIn 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes popIn {
    0%   { transform: scale(0) rotate(-15deg); opacity: 0; }
    100% { transform: scale(1) rotate(0deg);   opacity: 1; }
}
.arena-name {
    font-size: 0.75rem;
    color: #c4b5fd;
    margin-top: 0.3rem;
    letter-spacing: 0.1em;
}
.vs-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #4f46e5;
    letter-spacing: 0.1em;
}

/* ── Result banner ── */
.result-banner {
    text-align: center;
    padding: 1rem 2rem;
    border-radius: 16px;
    margin: 1rem 0;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.15em;
    animation: slideUp 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes slideUp {
    0%   { transform: translateY(20px); opacity: 0; }
    100% { transform: translateY(0);    opacity: 1; }
}
.result-win  { background: rgba(74,222,128,0.12); border: 1px solid rgba(74,222,128,0.3);  color: #4ade80; }
.result-loss { background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.3); color: #f87171; }
.result-tie  { background: rgba(250,204,21,0.12); border: 1px solid rgba(250,204,21,0.3);  color: #facc15; }

/* ── History table ── */
.history-wrap {
    margin-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    padding-top: 1rem;
}
.history-title {
    font-size: 0.6rem;
    letter-spacing: 0.4em;
    color: #6366f1;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    text-align: center;
}
.history-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    font-size: 0.75rem;
    transition: background 0.2s;
    gap: 0.5rem;
}
.history-row:hover { background: rgba(255,255,255,0.04); }
.h-win  { border-left: 3px solid #4ade80; }
.h-loss { border-left: 3px solid #f87171; }
.h-tie  { border-left: 3px solid #facc15; }
.h-badge {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 6px;
}
.h-badge.win  { background: rgba(74,222,128,0.15);  color: #4ade80; }
.h-badge.loss { background: rgba(248,113,113,0.15); color: #f87171; }
.h-badge.tie  { background: rgba(250,204,21,0.15);  color: #facc15; }

/* ── Streamlit button override ── */
.stButton > button {
    background: rgba(99,102,241,0.15) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    color: #c4b5fd !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    border-radius: 10px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(99,102,241,0.3) !important;
    border-color: #818cf8 !important;
    color: #e8e0ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Particles canvas (decorative) ── */
#particles { position: fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; opacity:0.4; }
</style>

<canvas id="particles"></canvas>
<script>
(function(){
    const c = document.getElementById('particles');
    if(!c) return;
    const ctx = c.getContext('2d');
    let W, H, dots = [];
    function resize(){ W = c.width = window.innerWidth; H = c.height = window.innerHeight; }
    resize();
    window.addEventListener('resize', resize);
    for(let i=0;i<55;i++){
        dots.push({
            x: Math.random()*W, y: Math.random()*H,
            r: Math.random()*1.5+0.3,
            dx: (Math.random()-.5)*0.3,
            dy: (Math.random()-.5)*0.3,
            a: Math.random()
        });
    }
    function draw(){
        ctx.clearRect(0,0,W,H);
        dots.forEach(d=>{
            ctx.beginPath();
            ctx.arc(d.x, d.y, d.r, 0, Math.PI*2);
            ctx.fillStyle = `rgba(129,140,248,${d.a})`;
            ctx.fill();
            d.x += d.dx; d.y += d.dy;
            if(d.x<0||d.x>W) d.dx*=-1;
            if(d.y<0||d.y>H) d.dy*=-1;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [('wins',0),('losses',0),('ties',0),('history',[]),('last_result',None)]:
    if key not in st.session_state:
        st.session_state[key] = default

LABELS = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
EMOJIS = {'R': '🪨',   'P': '📄',   'S': '✂️'}
BEATS  = {'R': 'S', 'S': 'P', 'P': 'R'}   # key beats value

def play(user_choice: str):
    computer_choice = random.choice(['R', 'P', 'S'])
    if computer_choice == user_choice:
        result, msg = 'tie', "It's a tie!"
        st.session_state.ties += 1
    elif BEATS[user_choice] == computer_choice:
        result = 'win'
        msg = f"{LABELS[user_choice]} beats {LABELS[computer_choice]} — you win!"
        st.session_state.wins += 1
    else:
        result = 'loss'
        msg = f"{LABELS[computer_choice]} beats {LABELS[user_choice]} — computer wins!"
        st.session_state.losses += 1

    st.session_state.last_result = {
        'user': user_choice, 'cpu': computer_choice,
        'result': result, 'msg': msg
    }
    st.session_state.history.insert(0, st.session_state.last_result)
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-wrap">
  <p class="game-title">ROCK PAPER SCISSORS</p>
  <p class="subtitle">Challenge the machine</p>
</div>
""", unsafe_allow_html=True)

# Score board
w = st.session_state.wins
l = st.session_state.losses
t = st.session_state.ties
st.markdown(f"""
<div class="scoreboard">
  <div class="score-cell">
    <div class="score-label">Wins</div>
    <div class="score-num wins">{w}</div>
  </div>
  <div class="score-cell">
    <div class="score-label">Losses</div>
    <div class="score-num losses">{l}</div>
  </div>
  <div class="score-cell">
    <div class="score-label">Ties</div>
    <div class="score-num ties">{t}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Choice buttons via st.columns
st.markdown('<div style="text-align:center;font-size:0.65rem;letter-spacing:0.3em;color:#6366f1;text-transform:uppercase;margin-bottom:0.5rem;">Make your move</div>', unsafe_allow_html=True)

col1, col2, col3, col_gap = st.columns([1, 1, 1, 0.01])
with col1:
    if st.button("🪨\nRock", key="btn_rock", use_container_width=True):
        play('R')
        st.rerun()
with col2:
    if st.button("📄\nPaper", key="btn_paper", use_container_width=True):
        play('P')
        st.rerun()
with col3:
    if st.button("✂️\nScissors", key="btn_scissors", use_container_width=True):
        play('S')
        st.rerun()

# Battle arena + result
lr = st.session_state.last_result
if lr:
    user_e = EMOJIS[lr['user']]
    cpu_e  = EMOJIS[lr['cpu']]
    user_l = LABELS[lr['user']]
    cpu_l  = LABELS[lr['cpu']]
    res    = lr['result']
    msg    = lr['msg']

    st.markdown(f"""
<div class="arena">
  <div class="arena-side">
    <div class="arena-label">You</div>
    <span class="arena-emoji">{user_e}</span>
    <div class="arena-name">{user_l}</div>
  </div>
  <div class="vs-badge">VS</div>
  <div class="arena-side">
    <div class="arena-label">CPU</div>
    <span class="arena-emoji">{cpu_e}</span>
    <div class="arena-name">{cpu_l}</div>
  </div>
</div>
<div class="result-banner result-{res}">{msg}</div>
""", unsafe_allow_html=True)

# Reset button
_, mid, _ = st.columns([2, 1, 2])
with mid:
    if st.button("↺  Reset Score", key="btn_reset", use_container_width=True):
        for k in ['wins','losses','ties','history','last_result']:
            st.session_state[k] = 0 if k in ('wins','losses','ties') else ([] if k=='history' else None)
        st.rerun()

# History
if st.session_state.history:
    rows_html = ""
    for h in st.session_state.history:
        badge_cls = h['result']
        badge_txt = h['result'].upper()
        row_cls   = f"h-{h['result']}"
        rows_html += f"""
<div class="history-row {row_cls}">
  <span>{EMOJIS[h['user']]} {LABELS[h['user']]}</span>
  <span class="h-badge {badge_cls}">{badge_txt}</span>
  <span>{EMOJIS[h['cpu']]} {LABELS[h['cpu']]}</span>
</div>"""

    st.markdown(f"""
<div class="history-wrap">
  <div class="history-title">Last 10 rounds</div>
  {rows_html}
</div>
""", unsafe_allow_html=True)
