import streamlit as st
import random

st.set_page_config(
    page_title="Rock · Paper · Scissors",
    page_icon="🪨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #06060a !important;
}
[data-testid="stAppViewContainer"] {
    background: #06060a !important;
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; display: none; }
[data-testid="block-container"] {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 680px !important;
}
* { box-sizing: border-box; }

/* ─── TITLE ─── */
.rps-header {
    text-align: center;
    padding: 2rem 0 1rem;
    position: relative;
}
.rps-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.45em;
    color: #5b5b7a;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.rps-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.6rem, 7vw, 4.2rem);
    line-height: 0.95;
    letter-spacing: -0.02em;
    margin: 0;
    color: #f0ecff;
}
.rps-title span { color: #7c6ff7; }
.rps-title span.g2 { color: #b06cf5; }
.rps-title span.g3 { color: #e87cdb; }

/* ─── SCOREBOARD ─── */
.score-outer {
    display: flex;
    gap: 0;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    overflow: hidden;
    margin: 1.5rem 0;
    background: #0d0d17;
}
.score-seg {
    flex: 1;
    padding: 1rem 0;
    text-align: center;
    border-right: 1px solid #1e1e2e;
    transition: background 0.3s;
}
.score-seg:last-child { border-right: none; }
.score-seg.active-win   { background: rgba(74,222,128,0.06); }
.score-seg.active-loss  { background: rgba(248,113,113,0.06); }
.score-seg.active-tie   { background: rgba(250,204,21,0.06); }
.score-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.35em;
    color: #3d3d55;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.score-val {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    line-height: 1;
}
.score-val.w { color: #4ade80; }
.score-val.l { color: #f87171; }
.score-val.t { color: #facc15; }
.score-streak {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: #3d3d55;
    margin-top: 0.25rem;
    letter-spacing: 0.1em;
    min-height: 1em;
}

/* ─── MOVE BUTTONS ─── */
.move-section {
    margin: 1rem 0 0.5rem;
}
.move-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.4em;
    color: #3d3d55;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 1rem;
}
.stButton > button {
    background: #0d0d17 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 20px !important;
    color: #e8e0ff !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.2em !important;
    padding: 1.4rem 0 !important;
    width: 100% !important;
    transition: all 0.22s cubic-bezier(.34,1.56,.64,1) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: #13132a !important;
    border-color: #7c6ff7 !important;
    transform: translateY(-5px) scale(1.03) !important;
    box-shadow: 0 12px 30px rgba(124,111,247,0.2) !important;
    color: #fff !important;
}
.stButton > button:active {
    transform: translateY(-1px) scale(0.98) !important;
}
button[data-testid="baseButton-secondary"]:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px #7c6ff7 !important;
}

/* ─── ARENA ─── */
.arena-wrap {
    margin: 1.2rem 0;
    border-radius: 24px;
    overflow: hidden;
    background: #0d0d17;
    border: 1px solid #1e1e2e;
}
.arena-bar {
    display: flex;
    align-items: stretch;
}
.arena-player {
    flex: 1;
    padding: 1.8rem 1rem;
    text-align: center;
    transition: background 0.4s;
}
.arena-player.result-win  { background: rgba(74,222,128,0.05); }
.arena-player.result-loss { background: rgba(248,113,113,0.05); }
.arena-player.result-tie  { background: rgba(250,204,21,0.05); }
.arena-who {
    font-family: 'DM Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.4em;
    color: #3d3d55;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.arena-icon {
    font-size: 3.8rem;
    line-height: 1;
    display: block;
    margin: 0 auto 0.5rem;
    animation: boomIn 0.55s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes boomIn {
    0%   { transform: scale(0.3) rotate(-20deg); opacity: 0; }
    60%  { transform: scale(1.15) rotate(4deg); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}
.arena-name {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7070a0;
    letter-spacing: 0.08em;
}
.arena-divider {
    width: 1px;
    background: #1e1e2e;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 1rem;
    position: relative;
}
.vs-text {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1rem;
    color: #2a2a3e;
    letter-spacing: 0.1em;
    writing-mode: horizontal-tb;
    background: #0d0d17;
    padding: 0.3rem 0;
    position: relative;
    z-index: 1;
}

/* ─── RESULT PILL ─── */
.result-pill-wrap { padding: 1rem 1.5rem 1.5rem; border-top: 1px solid #1e1e2e; }
.result-pill {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    padding: 0.85rem 1.5rem;
    border-radius: 12px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.04em;
    animation: slideUp 0.45s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes slideUp {
    0%   { transform: translateY(16px); opacity: 0; }
    100% { transform: translateY(0);    opacity: 1; }
}
.result-pill.win  { background: rgba(74,222,128,0.1);  border: 1px solid rgba(74,222,128,0.25);  color: #4ade80; }
.result-pill.loss { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.25); color: #f87171; }
.result-pill.tie  { background: rgba(250,204,21,0.1);  border: 1px solid rgba(250,204,21,0.25);  color: #facc15; }
.result-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; flex-shrink: 0; }

/* ─── STATS BAR ─── */
.stats-bar {
    display: flex;
    gap: 0.5rem;
    margin: 0.5rem 0 1.2rem;
    align-items: center;
}
.bar-track {
    flex: 1;
    height: 5px;
    background: #1e1e2e;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
}
.bar-seg { height: 100%; transition: width 0.5s ease; }
.bar-seg.w { background: #4ade80; }
.bar-seg.l { background: #f87171; }
.bar-seg.t { background: #facc15; }
.bar-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: #3d3d55;
    letter-spacing: 0.1em;
    white-space: nowrap;
}

/* ─── HISTORY ─── */
.hist-section { margin-top: 1.2rem; }
.hist-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}
.hist-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.38em;
    color: #3d3d55;
    text-transform: uppercase;
}
.hist-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
}
.hist-row {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    padding: 0.55rem 1rem;
    border-radius: 10px;
    background: #0d0d17;
    border: 1px solid #1a1a28;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    transition: border-color 0.2s;
    gap: 0.5rem;
}
.hist-row:hover { border-color: #2e2e48; }
.hist-row.win  { border-left: 3px solid rgba(74,222,128,0.5); }
.hist-row.loss { border-left: 3px solid rgba(248,113,113,0.5); }
.hist-row.tie  { border-left: 3px solid rgba(250,204,21,0.5); }
.hist-you  { color: #a0a0cc; }
.hist-cpu  { color: #a0a0cc; text-align: right; }
.hist-mid  { text-align: center; }
.hist-badge {
    font-size: 0.55rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    padding: 3px 9px;
    border-radius: 20px;
    white-space: nowrap;
}
.hist-badge.win  { background: rgba(74,222,128,0.12);  color: #4ade80; }
.hist-badge.loss { background: rgba(248,113,113,0.12); color: #f87171; }
.hist-badge.tie  { background: rgba(250,204,21,0.12);  color: #facc15; }

/* ─── RESET BTN special ─── */
.reset-row { margin-top: 1rem; }

/* ─── IDLE PROMPT ─── */
.idle-arena {
    padding: 2.5rem 1rem;
    text-align: center;
    border-radius: 24px;
    background: #0d0d17;
    border: 1px dashed #1e1e2e;
    margin: 1.2rem 0;
}
.idle-icons { font-size: 2.4rem; letter-spacing: 0.2em; opacity: 0.35; }
.idle-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #3d3d55;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.8rem;
}

/* hide streamlit chrome */
footer, #MainMenu { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
DEFAULTS = {
    'wins': 0, 'losses': 0, 'ties': 0,
    'history': [], 'last_result': None,
    'streak': 0, 'streak_type': None,   # positive=wins, negative=losses
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

LABELS = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
EMOJIS = {'R': '🪨', 'P': '📄', 'S': '✂️'}
BEATS  = {'R': 'S', 'S': 'P', 'P': 'R'}

def play(user_choice: str):
    cpu = random.choice(['R', 'P', 'S'])
    if cpu == user_choice:
        result = 'tie'
        msg = "Dead even."
        st.session_state.ties += 1
        st.session_state.streak = 0
        st.session_state.streak_type = None
    elif BEATS[user_choice] == cpu:
        result = 'win'
        msg = f"{LABELS[user_choice]} crushes {LABELS[cpu]}"
        st.session_state.wins += 1
        if st.session_state.streak_type == 'win':
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
            st.session_state.streak_type = 'win'
    else:
        result = 'loss'
        msg = f"{LABELS[cpu]} crushes {LABELS[user_choice]}"
        st.session_state.losses += 1
        if st.session_state.streak_type == 'loss':
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
            st.session_state.streak_type = 'loss'

    st.session_state.last_result = {
        'user': user_choice, 'cpu': cpu, 'result': result, 'msg': msg
    }
    st.session_state.history.insert(0, st.session_state.last_result.copy())
    if len(st.session_state.history) > 12:
        st.session_state.history = st.session_state.history[:12]

def reset():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v if not isinstance(v, list) else []

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rps-header">
  <div class="rps-eyebrow">Best of ∞</div>
  <p class="rps-title">
    <span>ROCK</span><br>
    <span class="g2">PAPER</span><br>
    <span class="g3">SCISSORS</span>
  </p>
</div>
""", unsafe_allow_html=True)

# ── Score board ────────────────────────────────────────────────────────────────
w = st.session_state.wins
l = st.session_state.losses
t = st.session_state.ties
total = w + l + t

lr = st.session_state.last_result
active_w = 'active-win'  if (lr and lr['result'] == 'win')  else ''
active_l = 'active-loss' if (lr and lr['result'] == 'loss') else ''
active_t = 'active-tie'  if (lr and lr['result'] == 'tie')  else ''

streak = st.session_state.streak
stype  = st.session_state.streak_type
streak_html_w = f'{"🔥 " + str(streak) + " streak" if stype=="win" and streak>=2 else "&nbsp;"}' 
streak_html_l = f'{"💀 " + str(streak) + " streak" if stype=="loss" and streak>=2 else "&nbsp;"}'

st.markdown(f"""
<div class="score-outer">
  <div class="score-seg {active_w}">
    <div class="score-lbl">Wins</div>
    <div class="score-val w">{w}</div>
    <div class="score-streak">{streak_html_w}</div>
  </div>
  <div class="score-seg {active_t}">
    <div class="score-lbl">Ties</div>
    <div class="score-val t">{t}</div>
    <div class="score-streak">&nbsp;</div>
  </div>
  <div class="score-seg {active_l}">
    <div class="score-lbl">Losses</div>
    <div class="score-val l">{l}</div>
    <div class="score-streak">{streak_html_l}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Win-rate bar
if total > 0:
    wp = round(w / total * 100)
    lp = round(l / total * 100)
    tp = max(0, 100 - wp - lp)
    st.markdown(f"""
<div class="stats-bar">
  <span class="bar-lbl">{wp}% win</span>
  <div class="bar-track">
    <div class="bar-seg w" style="width:{wp}%"></div>
    <div class="bar-seg t" style="width:{tp}%"></div>
    <div class="bar-seg l" style="width:{lp}%"></div>
  </div>
  <span class="bar-lbl">{total} played</span>
</div>
""", unsafe_allow_html=True)

# ── Move buttons ───────────────────────────────────────────────────────────────
st.markdown('<div class="move-label">Choose your weapon</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="small")
choice_made = None
with col1:
    if st.button("🪨\n\nROCK", key="r", use_container_width=True):
        choice_made = 'R'
with col2:
    if st.button("📄\n\nPAPER", key="p", use_container_width=True):
        choice_made = 'P'
with col3:
    if st.button("✂️\n\nSCISSORS", key="s", use_container_width=True):
        choice_made = 'S'

if choice_made:
    play(choice_made)
    st.rerun()

# ── Battle arena ───────────────────────────────────────────────────────────────
if lr:
    ue = EMOJIS[lr['user']];  ul = LABELS[lr['user']]
    ce = EMOJIS[lr['cpu']];   cl = LABELS[lr['cpu']]
    res = lr['result']
    player_cls = f"result-{res}"
    cpu_cls    = f"result-{'loss' if res=='win' else ('win' if res=='loss' else 'tie')}"

    st.markdown(f"""
<div class="arena-wrap">
  <div class="arena-bar">
    <div class="arena-player {player_cls}">
      <div class="arena-who">You</div>
      <span class="arena-icon">{ue}</span>
      <div class="arena-name">{ul}</div>
    </div>
    <div class="arena-divider"><span class="vs-text">VS</span></div>
    <div class="arena-player {cpu_cls}">
      <div class="arena-who">CPU</div>
      <span class="arena-icon">{ce}</span>
      <div class="arena-name">{cl}</div>
    </div>
  </div>
  <div class="result-pill-wrap">
    <div class="result-pill {res}">
      <span class="result-dot"></span>
      {lr['msg']}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="idle-arena">
  <div class="idle-icons">🪨 📄 ✂️</div>
  <div class="idle-text">Pick a move to start</div>
</div>
""", unsafe_allow_html=True)

# ── Reset ──────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([2, 1.2, 2])
with c2:
    if st.button("↺  Reset", key="reset_btn", use_container_width=True):
        reset()
        st.rerun()

# ── History ────────────────────────────────────────────────────────────────────
if st.session_state.history:
    rows = ""
    for h in st.session_state.history:
        badge_map = {'win': 'WIN', 'loss': 'LOSS', 'tie': 'TIE'}
        rows += f"""
<div class="hist-row {h['result']}">
  <span class="hist-you">{EMOJIS[h['user']]} {LABELS[h['user']]}</span>
  <span class="hist-mid"><span class="hist-badge {h['result']}">{badge_map[h['result']]}</span></span>
  <span class="hist-cpu">{LABELS[h['cpu']]} {EMOJIS[h['cpu']]}</span>
</div>"""

    st.markdown(f"""
<div class="hist-section">
  <div class="hist-header">
    <span class="hist-title">Recent rounds</span>
    <span class="hist-title">{len(st.session_state.history)} / 12</span>
  </div>
  <div class="hist-list">{rows}</div>
</div>
""", unsafe_allow_html=True)
