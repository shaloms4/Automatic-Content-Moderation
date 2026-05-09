"""
Automatic Content Moderation System
Cognitive Science Course Project
"""

import streamlit as st
from preprocess import preprocess_text
from rule_based import rule_based_moderate
from utils import get_toxicity_label, get_color_for_score
import httpx

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Automatic Content Moderation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    .main-header {
        font-size: 2.6rem;
        background: linear-gradient(90deg, #4B9CFF, #9B6BFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subheader {
        color: #B0B8C9;
        font-size: 1.15rem;
        margin-bottom: 1.8rem;
    }
    .score-circle {
        width: 170px;
        height: 170px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0 auto;
        border: 14px solid;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("## 🛡️ Automatic Content Moderation")
    st.caption("Cognitive Science Course Project")
    st.divider()
    
    st.markdown("### 🔬 Cognitive Science Connections")
    st.markdown("""
    - **Semantic Memory** → Rule-based profanity detection  
    - **Language Processing** → Text preprocessing & lemmatization  
    - **Attention & Context** → Future BERT Transformer integration  
    - **Tool Use** → External cognitive aid for safer discussions
    """)
    
    st.divider()
    st.info("**Current Version**: Hybrid (BERT) via backend + Preprocessing")

# ====================== MAIN HEADER ======================
st.markdown('<h1 class="main-header">🛡️ Automatic Content Moderation</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Building safer online spaces through Cognitive Science & AI</p>', unsafe_allow_html=True)

# ====================== INPUT ======================
user_text = st.text_area(
    "Enter text to moderate",
    height=180,
    placeholder="Paste a comment, message, forum post, or any text here...",
    label_visibility="collapsed"
)

if st.button("Moderate Text", type="primary", use_container_width=True):
    if not user_text.strip():
        st.error("⚠️ Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text..."):
            # Try calling the FastAPI backend first
            try:
                resp = httpx.post("http://127.0.0.1:8000/moderate", json={"text": user_text}, timeout=10.0)
                if resp.status_code == 200:
                    result = resp.json()
                else:
                    raise RuntimeError(f"Bad response {resp.status_code}")
                # Backend returns structured fields: moderated_text, toxicity_score, raw_model_score, method, flagged_words
                toxicity_score = float(result.get("toxicity_score", 0.0))
            except Exception:
                # Fallback to local rule-based moderation if backend not available
                fallback = rule_based_moderate(user_text)
                result = {
                    "original_text": fallback.get("original_text", user_text),
                    "moderated_text": fallback.get("masked_text", user_text),
                    "toxicity_score": 0.92 if fallback.get("is_profane", False) else 0.12,
                    "is_toxic": fallback.get("is_profane", False),
                    "raw_model_score": 0.0,
                    "method": fallback.get("method", "rule_based"),
                    "flagged_words": fallback.get("flagged_words", [])
                }
                toxicity_score = float(result.get("toxicity_score", 0.0))
            
        st.divider()
        
        # Results Layout
        col1, col2, col3 = st.columns([1, 1, 0.9])
        
        with col1:
            st.markdown("**📝 Original Text**")
            st.info(user_text)
        
        with col2:
            st.markdown("**🛡️ Moderated Text**")
            st.success(result.get("moderated_text", result.get("masked_text", user_text)))
        
        with col3:
            st.markdown("**📊 Toxicity Score**")
            color_emoji = get_color_for_score(toxicity_score)
            st.markdown(f"""
            <div style="text-align:center; padding:15px;">
                <div class="score-circle" style="border-color: {'#e74c3c' if toxicity_score > 0.7 else '#f1c40f' if toxicity_score > 0.4 else '#2ecc71'};">
                    {int(toxicity_score * 100)}%
                </div>
                <p style="margin-top:12px; font-weight:600; font-size:1.1rem;">
                    {color_emoji} {get_toxicity_label(toxicity_score)}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Show flagged words if present
        if result.get("flagged_words"):
            st.markdown("**🚩 Flagged Words**")
            st.warning(", ".join(result["flagged_words"]))
        else:
            st.success("✅ No inappropriate language detected.")

        # Show model metadata
        st.markdown("**🧾 Model Info**")
        method = result.get("method", "unknown")
        raw_score = result.get("raw_model_score")
        st.write(f"Method: {method}")
        if raw_score is not None:
            st.write(f"Raw model score: {raw_score}")

# ====================== FOOTER ======================
st.divider()
st.markdown(
    """
    <p style="text-align: center; color: #78849E; font-size: 0.95rem;">
        🎓 <b>Automatic Content Moderation</b> — Cognitive Science Course Project<br>
        Exploring Memory, Attention, and Language Processing through AI
    </p>
    """, 
    unsafe_allow_html=True
)