import streamlit as st
import pandas as pd

from fetch_data import fetch_students
from duplicate_detection import detect_duplicates
from save_results import save_duplicates

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Duplicate Record Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Typography & base */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Page background */
.stApp { background: #0f1117; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #16213e 60%, #0f3460 100%);
    border: 1px solid rgba(99, 179, 237, 0.15);
    border-radius: 16px;
    padding: 48px 56px 44px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #63b3ed;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #f0f4f8;
    line-height: 1.2;
    margin: 0 0 14px;
    letter-spacing: -0.03em;
}
.hero-sub {
    font-size: 1.05rem;
    color: #8a9bb5;
    line-height: 1.6;
    max-width: 560px;
    margin: 0;
}

/* ── Stat cards ── */
.stat-row {
    display: flex;
    gap: 16px;
    margin-top: 36px;
}
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 16px 22px;
    min-width: 120px;
}
.stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #63b3ed;
    line-height: 1;
    margin-bottom: 4px;
}
.stat-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #5d7291;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* ── Action cards ── */
.action-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 28px;
}
.action-card {
    background: #161b27;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 28px 28px 24px;
    transition: border-color 0.2s;
}
.action-card:hover { border-color: rgba(99,179,237,0.3); }
.action-icon {
    font-size: 1.5rem;
    margin-bottom: 12px;
    display: block;
}
.action-title {
    font-size: 1rem;
    font-weight: 600;
    color: #d6e4f0;
    margin-bottom: 6px;
}
.action-desc {
    font-size: 0.82rem;
    color: #5d7291;
    line-height: 1.5;
    margin-bottom: 18px;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 32px 0 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #c8d8e8;
    margin: 0;
}
.section-count {
    background: rgba(99,179,237,0.15);
    color: #63b3ed;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
}

/* ── Similarity badge ── */
.sim-high   { color: #fc8181; font-weight: 600; }
.sim-medium { color: #f6ad55; font-weight: 600; }
.sim-low    { color: #68d391; font-weight: 600; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 56px 24px;
    color: #4a5568;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 12px; }
.empty-title { font-size: 1rem; font-weight: 600; color: #718096; margin-bottom: 6px; }
.empty-sub { font-size: 0.84rem; color: #4a5568; }

/* ── Dataframe tweaks ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Button overrides ── */
.stButton > button {
    background: #2b6cb0;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 10px 20px;
    width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover { background: #2c7be5; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.25); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🔍 &nbsp;DBMS Project</div>
  <h1 class="hero-title">Duplicate Record Detection</h1>
  <p class="hero-sub">
    Detect near-duplicate student entries using fuzzy matching across
    name, email, and phone — then save flagged pairs for review.
  </p>
  <div class="stat-row">
    <div class="stat-card">
      <div class="stat-value">3</div>
      <div class="stat-label">Match Fields</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">75%</div>
      <div class="stat-label">Score Threshold</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">O(n²)</div>
      <div class="stat-label">Comparison Strategy</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Action cards ───────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="action-card">
      <span class="action-icon">🗂️</span>
      <div class="action-title">Student Records</div>
      <div class="action-desc">
        Browse all students in the database — ID, name, email, phone,
        department, and city.
      </div>
    </div>
    """, unsafe_allow_html=True)
    view_clicked = st.button("Load Records", key="view_btn")

with col2:
    st.markdown("""
    <div class="action-card">
      <span class="action-icon">⚡</span>
      <div class="action-title">Detect Duplicates</div>
      <div class="action-desc">
        Run pairwise fuzzy matching and surface all pairs
        with a combined similarity score ≥ 75.
      </div>
    </div>
    """, unsafe_allow_html=True)
    detect_clicked = st.button("Run Detection", key="detect_btn")

# ── Save to DB (full width) ────────────────────────────────────────────────────
save_clicked = st.button("💾  Save Results to Database", key="save_btn")

# ── Results ────────────────────────────────────────────────────────────────────
if view_clicked:
    with st.spinner("Connecting to Oracle DB…"):
        df = fetch_students()

    st.markdown(f"""
    <div class="section-header">
      <span class="section-title">Student Records</span>
      <span class="section-count">{len(df)} rows</span>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

if detect_clicked:
    with st.spinner("Running fuzzy matching — this may take a moment…"):
        results = detect_duplicates()

    if results:
        result_df = pd.DataFrame(results)

        # Colour-code similarity column
        def colour_sim(val):
            if val >= 90:
                return "color:#fc8181; font-weight:600"
            elif val >= 80:
                return "color:#f6ad55; font-weight:600"
            return "color:#68d391; font-weight:600"

        st.markdown(f"""
        <div class="section-header">
          <span class="section-title">Detected Duplicate Pairs</span>
          <span class="section-count">{len(results)} pairs</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Duplicate Pairs Found", len(results))
        high = sum(1 for r in results if r["Similarity"] >= 90)
        c2.metric("High Confidence (≥ 90)", high)
        c3.metric("Medium Confidence (75–89)", len(results) - high)

        st.dataframe(
            result_df.style.map(colour_sim, subset=["Similarity"]),
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">✅</div>
          <div class="empty-title">No duplicates found</div>
          <div class="empty-sub">Every student record appears unique above the 75-point threshold.</div>
        </div>
        """, unsafe_allow_html=True)

if save_clicked:
    with st.spinner("Saving flagged pairs to DUPLICATE_RECORDS…"):
        try:
            save_duplicates()
            st.success("✅ Results saved to the database successfully.")
        except Exception as e:
            st.error(f"Save failed: {e}")