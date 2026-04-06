import streamlit as st
import requests
import time
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduPath AI Counsellor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000/chat"   # ← change if your API runs elsewhere

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --green-950: #052e16;
    --green-900: #14532d;
    --green-800: #166534;
    --green-700: #15803d;
    --green-600: #16a34a;
    --green-500: #22c55e;
    --green-400: #4ade80;
    --green-300: #86efac;
    --green-200: #bbf7d0;
    --green-100: #dcfce7;
    --green-50:  #f0fdf4;
    --dark:      #0a0f0d;
    --card:      #0d1a12;
    --border:    rgba(34,197,94,0.18);
    --text-main: #e8f5ec;
    --text-muted:#7fb890;
    --glow:      0 0 24px rgba(34,197,94,0.25);
}

/* ── Global reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--dark) !important;
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-main);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061a0f 0%, #0a1a12 60%, #0d2318 100%) !important;
    border-right: 1px solid var(--border);
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* ── Main content area ── */
[data-testid="stMain"] .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--dark); }
::-webkit-scrollbar-thumb { background: var(--green-800); border-radius: 4px; }

/* ── Chat input override ── */
[data-testid="stChatInput"] > div {
    background: #0d1a12 !important;
    border: 1.5px solid var(--green-700) !important;
    border-radius: 16px !important;
    box-shadow: var(--glow) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text-main) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
}
[data-testid="stChatInput"] button {
    background: var(--green-600) !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] button:hover {
    background: var(--green-500) !important;
}

/* ── Chat message bubbles ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--green-700), var(--green-600)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: all .2s !important;
    box-shadow: 0 2px 12px rgba(22,163,74,.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--green-600), var(--green-500)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(22,163,74,.45) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 16px !important;
}
[data-testid="stMetricValue"] { color: var(--green-400) !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()


# ── Helper ────────────────────────────────────────────────────────────────────
def query_api(user_message: str) -> str:
    try:
        resp = requests.post(API_URL, json={"message": user_message}, timeout=60)
        resp.raise_for_status()
        return resp.json().get("reply", "⚠️ No reply received from the server.")
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to the counsellor API. Make sure your backend is running on `localhost:8000`."
    except requests.exceptions.Timeout:
        return "⚠️ The server took too long to respond. Please try again."
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"


def stream_text(text: str):
    """Yield text word-by-word for a typewriter effect."""
    for word in text.split():
        yield word + " "
        time.sleep(0.025)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="padding:28px 20px 18px;text-align:center;border-bottom:1px solid rgba(34,197,94,.15);margin-bottom:20px;">
        <div style="font-size:52px;margin-bottom:6px;">🎓</div>
        <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;
                    background:linear-gradient(135deg,#4ade80,#22c55e,#86efac);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            EduPath AI
        </div>
        <div style="font-size:11px;color:#7fb890;letter-spacing:2px;font-weight:500;margin-top:2px;">
            ENGINEERING COUNSELLOR
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    elapsed = datetime.now() - st.session_state.session_start
    mins = int(elapsed.total_seconds() // 60)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.total_queries)
    with col2:
        st.metric("Session", f"{mins}m")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Quick-topic chips
    st.markdown("""
    <div style="font-size:11px;font-weight:600;color:#7fb890;
                letter-spacing:1.5px;margin-bottom:10px;">QUICK TOPICS</div>
    """, unsafe_allow_html=True)

    topics = [
        ("🏛️", "Top NITs for CSE"),
        ("📊", "JEE rank vs college"),
        ("💸", "Fee structure overview"),
        ("🌍", "Abroad vs India options"),
        ("📝", "JOSAA counselling steps"),
        ("🔬", "Best branches 2025"),
    ]
    for icon, label in topics:
        if st.button(f"{icon}  {label}", key=f"chip_{label}", use_container_width=True):
            st.session_state._quick_prompt = label

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""<hr style='border:none;border-top:1px solid rgba(34,197,94,.12);margin:0 0 16px;'>""",
                unsafe_allow_html=True)

    # About section
    st.markdown("""
    <div style="background:rgba(22,163,74,.08);border:1px solid rgba(34,197,94,.18);
                border-radius:12px;padding:14px 16px;font-size:13px;line-height:1.6;color:#a3d9b1;">
        <b style="color:#4ade80;">What I can help with:</b><br><br>
        ✦ JEE / MHT-CET cutoffs<br>
        ✦ College & branch selection<br>
        ✦ JOSAA / CAP counselling<br>
        ✦ Scholarships & fees<br>
        ✦ Career path guidance<br>
        ✦ Private vs Government colleges
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)

    # Clear chat
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.session_state.session_start = datetime.now()
        st.rerun()

    st.markdown("""
    <div style="text-align:center;font-size:10px;color:#3d6b4a;margin-top:16px;padding-bottom:8px;">
        Powered by EduPath AI • v2.0
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════

# ── Header bar ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,#061a0f 0%,#0a1f14 60%,#061a0f 100%);
            border-bottom:1px solid rgba(34,197,94,.18);
            padding:18px 36px;display:flex;align-items:center;gap:16px;">
    <div style="width:10px;height:10px;background:#22c55e;border-radius:50%;
                box-shadow:0 0 10px #22c55e;flex-shrink:0;"></div>
    <div>
        <div style="font-family:'Outfit',sans-serif;font-size:18px;font-weight:700;color:#e8f5ec;">
            Engineering Admission Counsellor
        </div>
        <div style="font-size:12px;color:#7fb890;margin-top:1px;">
            AI-powered guidance for post-12th engineering admissions · Online
        </div>
    </div>
    <div style="margin-left:auto;display:flex;gap:8px;align-items:center;">
        <div style="background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.25);
                    border-radius:20px;padding:4px 14px;font-size:12px;color:#4ade80;font-weight:600;">
            🔴 LIVE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Chat area wrapper ─────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:0 32px;max-width:860px;margin:0 auto;">
""", unsafe_allow_html=True)

# ── Welcome hero (shown when no messages) ────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center;padding:52px 24px 32px;">
        <div style="font-size:70px;margin-bottom:16px;
                    filter:drop-shadow(0 0 20px rgba(34,197,94,.5));">🎓</div>
        <div style="font-family:'Outfit',sans-serif;font-size:32px;font-weight:800;
                    background:linear-gradient(135deg,#86efac,#22c55e,#4ade80);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    margin-bottom:10px;">
            Your Smart Admission Counsellor
        </div>
        <div style="font-size:15px;color:#7fb890;max-width:480px;margin:0 auto;line-height:1.7;">
            Get personalised guidance on engineering colleges, JEE cutoffs,
            branch selection, JOSAA counselling, and everything in between.
        </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:36px;">
        <div style="background:rgba(22,163,74,.07);border:1px solid rgba(34,197,94,.2);
                    border-radius:14px;padding:18px 16px;text-align:center;">
            <div style="font-size:26px;margin-bottom:6px;">🏆</div>
            <div style="font-size:13px;font-weight:600;color:#4ade80;">Top Colleges</div>
            <div style="font-size:11px;color:#7fb890;margin-top:3px;">IITs · NITs · IIITs · GFTIs</div>
        </div>
        <div style="background:rgba(22,163,74,.07);border:1px solid rgba(34,197,94,.2);
                    border-radius:14px;padding:18px 16px;text-align:center;">
            <div style="font-size:26px;margin-bottom:6px;">📈</div>
            <div style="font-size:13px;font-weight:600;color:#4ade80;">Rank Analysis</div>
            <div style="font-size:11px;color:#7fb890;margin-top:3px;">Cutoff · Trends · Predictions</div>
        </div>
        <div style="background:rgba(22,163,74,.07);border:1px solid rgba(34,197,94,.2);
                    border-radius:14px;padding:18px 16px;text-align:center;">
            <div style="font-size:26px;margin-bottom:6px;">🗺️</div>
            <div style="font-size:13px;font-weight:600;color:#4ade80;">Step-by-step</div>
            <div style="font-size:11px;color:#7fb890;margin-top:3px;">JOSAA · CAP · Seat allotment</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"""
            <div style="background:rgba(22,163,74,.12);border:1px solid rgba(34,197,94,.2);
                        border-radius:14px 14px 4px 14px;padding:12px 16px;
                        font-size:14.5px;line-height:1.65;color:#e8f5ec;max-width:85%;margin-left:auto;">
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(f"""
            <div style="background:rgba(13,26,18,.9);border:1px solid rgba(34,197,94,.18);
                        border-radius:4px 14px 14px 14px;padding:14px 18px;
                        font-size:14.5px;line-height:1.75;color:#d4f0de;max-width:92%;
                        box-shadow:0 2px 16px rgba(0,0,0,.3);">
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="font-size:10px;color:#3d6b4a;margin-top:4px;padding-left:4px;">
                {msg.get("time","--:--")} · EduPath AI
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close wrapper

# ── Input bar ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# Handle quick-prompt chips
default_input = ""
if hasattr(st.session_state, "_quick_prompt") and st.session_state._quick_prompt:
    default_input = st.session_state._quick_prompt
    st.session_state._quick_prompt = ""

prompt = st.chat_input(
    placeholder="Ask about colleges, cutoffs, branches, JOSAA counselling…",
    key="chat_input",
)

# Use chip prompt if no typed input
if not prompt and default_input:
    prompt = default_input

# ── Handle submission ─────────────────────────────────────────────────────────
if prompt:
    now_str = datetime.now().strftime("%H:%M")

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_queries += 1

    with st.chat_message("user", avatar="👤"):
        st.markdown(f"""
        <div style="background:rgba(22,163,74,.12);border:1px solid rgba(34,197,94,.2);
                    border-radius:14px 14px 4px 14px;padding:12px 16px;
                    font-size:14.5px;line-height:1.65;color:#e8f5ec;max-width:85%;margin-left:auto;">
            {prompt}
        </div>
        """, unsafe_allow_html=True)

    # Typing indicator + get response
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner(""):
            st.markdown("""
            <div style="display:flex;gap:5px;align-items:center;padding:6px 0;">
                <span style="font-size:12px;color:#7fb890;">EduPath is thinking</span>
                <span style="color:#22c55e;font-size:18px;">●</span>
            </div>
            """, unsafe_allow_html=True)
            reply = query_api(prompt)

        st.markdown(f"""
        <div style="background:rgba(13,26,18,.9);border:1px solid rgba(34,197,94,.18);
                    border-radius:4px 14px 14px 14px;padding:14px 18px;
                    font-size:14.5px;line-height:1.75;color:#d4f0de;max-width:92%;
                    box-shadow:0 2px 16px rgba(0,0,0,.3);">
            {reply}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:10px;color:#3d6b4a;margin-top:4px;padding-left:4px;">
            {now_str} · EduPath AI
        </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "time": now_str,
    })
    st.rerun()