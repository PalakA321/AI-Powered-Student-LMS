"""
AI-Powered Student Learning Management System
Professional Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Student LMS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────
st.markdown("""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background: #0F1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1d2e 0%, #141625 100%);
    border-right: 1px solid #2a2d3e;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Hero header */
.hero-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d1b69 50%, #1a1d2e 100%);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 24px;
    border: 1px solid #2a3a5c;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 99px;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Metric cards */
.metric-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    transition: border-color 0.2s;
    height: 100%;
}
.metric-card:hover { border-color: #4f46e5; }
.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 4px 0;
    line-height: 1;
}
.metric-label {
    font-size: 0.8rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.metric-delta {
    font-size: 0.8rem;
    margin-top: 4px;
    font-weight: 500;
}

/* Section headers */
.section-header {
    font-family: 'Poppins', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 28px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-line {
    height: 2px;
    background: linear-gradient(90deg, #4f46e5, transparent);
    margin-bottom: 20px;
    border-radius: 2px;
}

/* Risk badges */
.risk-high   { background:#ff4d4d; color:#ff6b6b; border:1px solid #ff4d4d; border-radius:6px; padding:3px 10px; font-size:0.78rem; font-weight:600; }
.risk-medium { background:#ffa500; color:#ffa500; border:1px solid #ffa500; border-radius:6px; padding:3px 10px; font-size:0.78rem; font-weight:600; }
.risk-low    { background:#00c851; color:#00c851; border:1px solid #00c851; border-radius:6px; padding:3px 10px; font-size:0.78rem; font-weight:600; }

/* Info box */
.info-box {
    background: linear-gradient(135deg, #1e3a5f, #2d1b69);
    border: 1px solid #2a3a5c;
    border-left: 3px solid #6366f1;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    color: #cbd5e1;
    font-size: 0.88rem;
    line-height: 1.6;
}

/* Study plan card */
.plan-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}
.plan-day {
    font-weight: 600;
    color: #a5b4fc;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.plan-task {
    color: #e2e8f0;
    font-size: 0.9rem;
}

/* Student table */
.student-table {
    background: #1a1d2e;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #2a2d3e;
}

/* Sidebar nav buttons */
div[data-testid="stSidebar"] .stButton button {
    width: 100%;
    background: transparent;
    border: 1px solid #2a2d3e;
    color: #94a3b8 !important;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 4px;
    text-align: left;
    font-size: 0.88rem;
    transition: all 0.2s;
}
div[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(99,102,241,0.15);
    border-color: #6366f1;
    color: #a5b4fc !important;
}

/* Chart container */
.chart-container {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 16px;
}

/* Selectbox & inputs dark */
.stSelectbox > div > div {
    background: #1a1d2e !important;
    border-color: #2a2d3e !important;
    color: #e2e8f0 !important;
}
.stSlider > div { color: #e2e8f0 !important; }
label { color: #94a3b8 !important; font-size: 0.85rem !important; }

/* Alert box */
.alert-danger  { background:#ff4d4d; border:1px solid #ff4d4d; border-radius:8px; padding:12px 16px; color:#ff6b6b; font-size:0.88rem; margin:8px 0; }
.alert-warning { background:#ffa500; border:1px solid #ffa500; border-radius:8px; padding:12px 16px; color:#ffa500; font-size:0.88rem; margin:8px 0; }
.alert-success { background:#00c851; border:1px solid #00c851; border-radius:8px; padding:12px 16px; color:#00c851; font-size:0.88rem; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── PATHS ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(BASE, "models")
DATA = os.path.join(BASE, "data", "raw", "data.csv")

# ── LOAD MODELS ───────────────────────────────────────────────
@st.cache_resource
def load_models():
    models = {}
    try:
        models['iso']        = joblib.load(os.path.join(MODELS, 'isolation_forest.pkl'))
        models['iso_scaler'] = joblib.load(os.path.join(MODELS, 'anomaly_scaler.pkl'))
        models['iso_feats']  = joblib.load(os.path.join(MODELS, 'anomaly_features.pkl'))
        models['rf']         = joblib.load(os.path.join(MODELS, 'random_forest.pkl'))
        models['xgb']        = joblib.load(os.path.join(MODELS, 'xgboost.pkl'))
        models['feat_names'] = joblib.load(os.path.join(MODELS, 'feature_names.pkl'))
        models['le']         = joblib.load(os.path.join(MODELS, 'label_encoder.pkl'))
        models['score_mdl']  = joblib.load(os.path.join(MODELS, 'score_predictor.pkl'))
        models['score_sc']   = joblib.load(os.path.join(MODELS, 'score_scaler.pkl'))
        models['score_ft']   = joblib.load(os.path.join(MODELS, 'score_features.pkl'))
        models['kmeans']     = joblib.load(os.path.join(MODELS, 'kmeans.pkl'))
        models['cl_scaler']  = joblib.load(os.path.join(MODELS, 'cluster_scaler.pkl'))
        models['cl_feats']   = joblib.load(os.path.join(MODELS, 'cluster_features.pkl'))
        models['cl_labels']  = joblib.load(os.path.join(MODELS, 'cluster_labels.pkl'))
        models['plans']      = joblib.load(os.path.join(MODELS, 'study_plans.pkl'))
    except Exception as e:
        st.error(f"Model load error: {e}")
    return models

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, sep=';')
    return df

models = load_models()
df     = load_data()

# Pre-compute anomaly scores on full dataset
iso_feats = models.get('iso_feats', [])
iso_feats = [f for f in iso_feats if f in df.columns]
if iso_feats:
    X_iso = models['iso_scaler'].transform(df[iso_feats])
    df['anomaly_score'] = models['iso'].decision_function(X_iso)
    df['anomaly_flag']  = models['iso'].predict(X_iso)
    df['risk_label']    = df['anomaly_flag'].map({-1: 'AT-RISK', 1: 'Normal'})

# Dropout risk probability
feat_names = models.get('feat_names', [])
feat_names = [f for f in feat_names if f in df.columns]
if feat_names:
    X_clf = df[feat_names].values
    proba = models['rf'].predict_proba(X_clf)
    le    = models['le']
    classes = list(le.classes_)
    if 'Dropout' in classes:
        di = classes.index('Dropout')
        df['dropout_prob'] = proba[:, di]
    else:
        df['dropout_prob'] = proba[:, 0]

# Cluster / learning style
cl_feats = models.get('cl_feats', [])
cl_feats = [f for f in cl_feats if f in df.columns]
if cl_feats:
    X_cl = models['cl_scaler'].transform(df[cl_feats])
    df['cluster']       = models['kmeans'].predict(X_cl)
    cl_labels           = models['cl_labels']
    df['learning_style']= df['cluster'].map(cl_labels)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px 0;'>
        <div style='font-size:2.5rem;'>🎓</div>
        <div style='font-family:Poppins; font-weight:700; font-size:1.1rem; color:#e2e8f0;'>AI Student LMS</div>
        <div style='font-size:0.75rem; color:#475569; margin-top:4px;'>Powered by Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='color:#475569; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; font-weight:600;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        label="page",
        options=["🏠  Overview", "⚠️  Early Warning", "👤  Student Profile", "📚  Study Plans", "📊  Analytics"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1e2130; margin:20px 0;'>", unsafe_allow_html=True)

    # Dataset summary
    total  = len(df)
    dropout_n = (df['Target'] == 'Dropout').sum()
    atrisk_n  = (df['anomaly_flag'] == -1).sum() if 'anomaly_flag' in df.columns else 0

    st.markdown(f"""
    <div style='background:#12141f; border-radius:10px; padding:14px 16px; border:1px solid #1e2130;'>
        <div style='color:#475569; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:10px; font-weight:600;'>Dataset Overview</div>
        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
            <span style='color:#94a3b8; font-size:0.82rem;'>Total Students</span>
            <span style='color:#e2e8f0; font-weight:600; font-size:0.82rem;'>{total:,}</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
            <span style='color:#94a3b8; font-size:0.82rem;'>AT-RISK Flagged</span>
            <span style='color:#ff6b6b; font-weight:600; font-size:0.82rem;'>{atrisk_n:,}</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
            <span style='color:#94a3b8; font-size:0.82rem;'>Dropout Count</span>
            <span style='color:#ffa500; font-weight:600; font-size:0.82rem;'>{dropout_n:,}</span>
        </div>
        <div style='display:flex; justify-content:space-between;'>
            <span style='color:#94a3b8; font-size:0.82rem;'>Features Used</span>
            <span style='color:#a5b4fc; font-weight:600; font-size:0.82rem;'>37</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e2130; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#475569; font-size:0.72rem; text-align:center;'>4th Year Major Project • 2025–26</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════
if "Overview" in page:

    st.markdown("""
    <div class='hero-header'>
        <div class='hero-badge'>AI-Powered Educational Analytics</div>
        <div class='hero-title'>Student Learning Management System</div>
        <div class='hero-subtitle'>Real-time dropout risk detection, exam score prediction & personalized study plans — all in one dashboard.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI CARDS ─────────────────────────────────────────────
    total        = len(df)
    graduate_n   = (df['Target'] == 'Graduate').sum()
    enrolled_n   = (df['Target'] == 'Enrolled').sum()
    dropout_pct  = dropout_n / total * 100
    atrisk_pct   = atrisk_n  / total * 100
    avg_dropout_prob = df['dropout_prob'].mean() * 100 if 'dropout_prob' in df.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Total Students</div>
            <div class='metric-value' style='color:#a5b4fc;'>{total:,}</div>
            <div class='metric-delta' style='color:#64748b;'>Dataset records</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Graduates</div>
            <div class='metric-value' style='color:#34d399;'>{graduate_n:,}</div>
            <div class='metric-delta' style='color:#34d399;'>▲ {graduate_n/total*100:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Dropouts</div>
            <div class='metric-value' style='color:#f87171;'>{dropout_n:,}</div>
            <div class='metric-delta' style='color:#f87171;'>▲ {dropout_pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>AT-RISK Flagged</div>
            <div class='metric-value' style='color:#fbbf24;'>{atrisk_n:,}</div>
            <div class='metric-delta' style='color:#fbbf24;'>⚠ {atrisk_pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Avg Dropout Risk</div>
            <div class='metric-value' style='color:#fb923c;'>{avg_dropout_prob:.1f}%</div>
            <div class='metric-delta' style='color:#64748b;'>Across all students</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    # ── CHARTS ROW 1 ──────────────────────────────────────────
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("<div class='section-header'>📊 Student Status Distribution</div>", unsafe_allow_html=True)
        status_counts = df['Target'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        colors_map = {'Graduate': '#34d399', 'Enrolled': '#60a5fa', 'Dropout': '#f87171'}
        fig = px.bar(
            status_counts, x='Status', y='Count', color='Status',
            color_discrete_map=colors_map,
            text='Count',
        )
        fig.update_traces(textposition='outside', textfont_size=13, marker_line_width=0)
        fig.update_layout(
            plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
            font_color='#94a3b8', showlegend=False,
            margin=dict(t=20, b=20, l=10, r=10),
            xaxis=dict(gridcolor='#2a2d3e', title=''),
            yaxis=dict(gridcolor='#2a2d3e', title='Number of Students'),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>🧩 Learning Style Groups</div>", unsafe_allow_html=True)
        if 'learning_style' in df.columns:
            ls_counts = df['learning_style'].value_counts().reset_index()
            ls_counts.columns = ['Style', 'Count']
            ls_colors = ['#f87171','#fbbf24','#60a5fa','#34d399']
            fig2 = px.pie(
                ls_counts, values='Count', names='Style',
                color_discrete_sequence=ls_colors,
                hole=0.5,
            )
            fig2.update_traces(textposition='outside', textinfo='percent+label',
                               textfont_size=10)
            fig2.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', showlegend=False,
                margin=dict(t=20, b=20, l=10, r=10),
                height=280,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ── CHARTS ROW 2 ──────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-header'>🔴 Dropout Risk Score Distribution</div>", unsafe_allow_html=True)
        if 'dropout_prob' in df.columns:
            fig3 = go.Figure()
            for status, color in zip(['Graduate','Enrolled','Dropout'],
                                     ['#34d399','#60a5fa','#f87171']):
                subset = df[df['Target'] == status]['dropout_prob']
                fig3.add_trace(go.Histogram(
                    x=subset, name=status, opacity=0.75,
                    marker_color=color, nbinsx=30,
                ))
            fig3.update_layout(
                barmode='overlay',
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8',
                legend=dict(bgcolor='#1a1d2e', bordercolor='#2a2d3e'),
                margin=dict(t=20, b=20, l=10, r=10),
                xaxis=dict(gridcolor='#2a2d3e', title='Dropout Probability'),
                yaxis=dict(gridcolor='#2a2d3e', title='Count'),
                height=280,
            )
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-header'>📈 Anomaly Score vs Dropout Risk</div>", unsafe_allow_html=True)
        if 'anomaly_score' in df.columns and 'dropout_prob' in df.columns:
            sample = df.sample(min(1000, len(df)), random_state=42)
            color_col = sample['Target'].map({'Dropout':'#f87171','Enrolled':'#fbbf24','Graduate':'#34d399'})
            fig4 = go.Figure()
            for status, color in zip(['Graduate','Enrolled','Dropout'],['#34d399','#fbbf24','#f87171']):
                sub = sample[sample['Target'] == status]
                fig4.add_trace(go.Scatter(
                    x=sub['anomaly_score'], y=sub['dropout_prob'],
                    mode='markers', name=status,
                    marker=dict(color=color, size=5, opacity=0.6),
                ))
            fig4.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8',
                legend=dict(bgcolor='#1a1d2e', bordercolor='#2a2d3e'),
                margin=dict(t=20, b=20, l=10, r=10),
                xaxis=dict(gridcolor='#2a2d3e', title='Anomaly Score'),
                yaxis=dict(gridcolor='#2a2d3e', title='Dropout Probability'),
                height=280,
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ── ML MODEL RESULTS ──────────────────────────────────────
    st.markdown("<div class='section-header'>🤖 ML Model Performance Summary</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    models_info = [
        ("Isolation Forest", "Anomaly Detection", "15%", "Contamination", "#a5b4fc"),
        ("Random Forest", "Dropout Classifier", "77.06%", "Accuracy", "#34d399"),
        ("XGBoost Regressor", "Score Predictor", "0.9690", "RMSE", "#fbbf24"),
        ("K-Means (K=4)", "Study Plan Cluster", "0.1978", "Silhouette", "#f87171"),
    ]
    for col, (name, task, val, metric, color) in zip([m1,m2,m3,m4], models_info):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;'>{task}</div>
                <div style='font-size:0.88rem;font-weight:600;color:#e2e8f0;margin-bottom:10px;'>{name}</div>
                <div style='font-size:1.6rem;font-weight:700;color:{color};font-family:Poppins;'>{val}</div>
                <div style='font-size:0.75rem;color:#64748b;margin-top:2px;'>{metric}</div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — EARLY WARNING SYSTEM
# ════════════════════════════════════════════════════════════════
elif "Warning" in page:

    st.markdown("""
    <div class='hero-header'>
        <div class='hero-badge'>Module 1 + 2 — Isolation Forest & Random Forest</div>
        <div class='hero-title'>⚠️ Early Warning System</div>
        <div class='hero-subtitle'>Detect students with abnormal academic patterns before it's too late.</div>
    </div>
    """, unsafe_allow_html=True)

    # Top stats
    if 'anomaly_flag' in df.columns:
        atrisk_df   = df[df['anomaly_flag'] == -1].copy()
        normal_df   = df[df['anomaly_flag'] == 1].copy()

        c1, c2, c3, c4 = st.columns(4)
        actual_dropout_in_atrisk = (atrisk_df['Target'] == 'Dropout').sum()
        catch_rate = actual_dropout_in_atrisk / atrisk_df.shape[0] * 100 if len(atrisk_df) > 0 else 0

        with c1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>AT-RISK Students</div><div class='metric-value' style='color:#f87171;'>{len(atrisk_df)}</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Normal Students</div><div class='metric-value' style='color:#34d399;'>{len(normal_df)}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Actual Dropouts Caught</div><div class='metric-value' style='color:#fbbf24;'>{actual_dropout_in_atrisk}</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Detection Rate</div><div class='metric-value' style='color:#a5b4fc;'>{catch_rate:.1f}%</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown("<div class='section-header'>🔴 Top At-Risk Students</div>", unsafe_allow_html=True)

            # Risk level based on dropout_prob
            display_cols = ['anomaly_score', 'dropout_prob', 'Target']
            grade_col    = 'Curricular units 2nd sem (grade)'
            approved_col = 'Curricular units 2nd sem (approved)'

            show_cols = [c for c in [grade_col, approved_col] if c in atrisk_df.columns]
            table_df  = atrisk_df[show_cols + display_cols].copy()
            table_df  = table_df.sort_values('anomaly_score').head(15).reset_index()
            table_df.rename(columns={'index': 'Student ID'}, inplace=True)
            table_df['anomaly_score'] = table_df['anomaly_score'].round(4)
            table_df['dropout_prob']  = (table_df['dropout_prob'] * 100).round(1).astype(str) + '%'

            def color_risk(val):
                if 'Dropout' in str(val):
                    return 'color: #f87171'
                return ''

            st.dataframe(
                table_df,
                use_container_width=True,
                height=350,
            )

        with col2:
            st.markdown("<div class='section-header'>📊 AT-RISK by Actual Status</div>", unsafe_allow_html=True)
            atrisk_status = atrisk_df['Target'].value_counts().reset_index()
            atrisk_status.columns = ['Status', 'Count']
            fig5 = px.pie(
                atrisk_status, values='Count', names='Status',
                color='Status',
                color_discrete_map={'Dropout':'#f87171','Enrolled':'#fbbf24','Graduate':'#34d399'},
                hole=0.45,
            )
            fig5.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', height=320,
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(bgcolor='#1a1d2e'),
            )
            st.plotly_chart(fig5, use_container_width=True)

        # Anomaly score scatter
        st.markdown("<div class='section-header'>📈 Anomaly Score — All Students</div>", unsafe_allow_html=True)
        df_sorted = df.sort_values('anomaly_score').reset_index(drop=True)
        fig6 = go.Figure()
        for status, color in zip(['Graduate','Enrolled','Dropout'],['#34d399','#60a5fa','#f87171']):
            sub = df_sorted[df_sorted['Target'] == status]
            fig6.add_trace(go.Scatter(
                x=sub.index, y=sub['anomaly_score'],
                mode='markers', name=status,
                marker=dict(color=color, size=4, opacity=0.5),
            ))
        fig6.add_hline(y=0, line_dash='dash', line_color='white',
                       annotation_text='Decision boundary (below = AT-RISK)',
                       annotation_font_color='#94a3b8')
        fig6.update_layout(
            plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
            font_color='#94a3b8', height=300,
            margin=dict(t=20, b=20, l=10, r=10),
            xaxis=dict(gridcolor='#2a2d3e', title='Student Index (sorted by score)'),
            yaxis=dict(gridcolor='#2a2d3e', title='Anomaly Score'),
            legend=dict(bgcolor='#1a1d2e', bordercolor='#2a2d3e'),
        )
        st.plotly_chart(fig6, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — STUDENT PROFILE
# ════════════════════════════════════════════════════════════════
elif "Student Profile" in page:

    st.markdown("""
    <div class='hero-header'>
        <div class='hero-badge'>Module 2 + 3 — Dropout Classifier & Score Predictor</div>
        <div class='hero-title'>👤 Student Profile Analysis</div>
        <div class='hero-subtitle'>Select a student to view dropout risk, predicted exam score, and SHAP explanation.</div>
    </div>
    """, unsafe_allow_html=True)

    # Student selector
    student_idx = st.selectbox(
        "Select Student ID",
        options=list(range(len(df))),
format_func=lambda x: f"Student #{x:04d} — {['Rahul','Priya','Amit','Neha','Rohan','Anjali','Vikram','Sneha','Arjun','Kavya'][x%10]}  |  Actual: {df.iloc[x]['Target']}"
    )

    student = df.iloc[student_idx]

    col1, col2 = st.columns([1, 1.5])

    with col1:
        # Risk card
        dropout_risk = student.get('dropout_prob', 0) * 100
        anomaly_sc   = student.get('anomaly_score', 0)
        risk_flag    = student.get('risk_label', 'Unknown')
        style        = student.get('learning_style', 'Unknown')

        risk_color = '#f87171' if dropout_risk > 60 else '#fbbf24' if dropout_risk > 35 else '#34d399'
        risk_text  = 'HIGH RISK' if dropout_risk > 60 else 'MEDIUM RISK' if dropout_risk > 35 else 'LOW RISK'

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1a1d2e,#12141f);border:1px solid #2a2d3e;
                    border-left:4px solid {risk_color};border-radius:12px;padding:24px;margin-bottom:16px;'>
            <div style='font-size:0.75rem;color:#475569;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px;'>Student #{student_idx:04d}</div>
            <div style='font-size:2.8rem;font-weight:800;font-family:Poppins;color:{risk_color};line-height:1;'>{dropout_risk:.1f}%</div>
            <div style='color:#64748b;font-size:0.82rem;margin:4px 0 12px;'>Dropout Probability</div>
            <div style='display:inline-block;background:{risk_color}22;border:1px solid {risk_color}44;
                        color:{risk_color};font-size:0.78rem;font-weight:700;padding:4px 14px;border-radius:99px;
                        letter-spacing:.5px;'>{risk_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # Score prediction
        score_feats = models.get('score_ft', [])
        score_feats = [f for f in score_feats if f in df.columns]
        if score_feats:
            X_score = models['score_sc'].transform(student[score_feats].values.reshape(1, -1))
            pred_score = models['score_mdl'].predict(X_score)[0]
            pred_score = max(0, min(20, pred_score))

            grade_band = ('🟢 Excellent' if pred_score >= 16
                          else '🔵 Good' if pred_score >= 13
                          else '🟡 Average' if pred_score >= 10
                          else '🔴 At Risk')
            band_color = ('#34d399' if pred_score >= 16
                          else '#60a5fa' if pred_score >= 13
                          else '#fbbf24' if pred_score >= 10
                          else '#f87171')

            st.markdown(f"""
            <div style='background:#1a1d2e;border:1px solid #2a2d3e;border-radius:12px;padding:20px;margin-bottom:16px;'>
                <div style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px;'>Predicted Exam Score</div>
                <div style='display:flex;align-items:baseline;gap:8px;'>
                    <span style='font-size:2.4rem;font-weight:700;font-family:Poppins;color:{band_color};'>{pred_score:.1f}</span>
                    <span style='color:#475569;font-size:1rem;'>/ 20</span>
                </div>
                <div style='margin-top:8px;color:{band_color};font-size:0.85rem;font-weight:600;'>{grade_band}</div>
                <div style='margin-top:12px;background:#12141f;border-radius:8px;height:8px;overflow:hidden;'>
                    <div style='height:100%;width:{pred_score/20*100:.0f}%;background:linear-gradient(90deg,{band_color},{band_color}88);border-radius:8px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Info grid
        actual = student['Target']
        anomaly_status = '⚠️ AT-RISK' if risk_flag == 'AT-RISK' else '✅ Normal'
        st.markdown(f"""
        <div style='background:#1a1d2e;border:1px solid #2a2d3e;border-radius:12px;padding:18px;'>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>
                <div><div style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.5px;'>Actual Status</div>
                     <div style='color:#e2e8f0;font-weight:600;font-size:0.9rem;margin-top:2px;'>{actual}</div></div>
                <div><div style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.5px;'>Anomaly Flag</div>
                     <div style='color:#e2e8f0;font-weight:600;font-size:0.9rem;margin-top:2px;'>{anomaly_status}</div></div>
                <div><div style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.5px;'>Learning Style</div>
                     <div style='color:#e2e8f0;font-weight:600;font-size:0.9rem;margin-top:2px;'>{style}</div></div>
                <div><div style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.5px;'>Anomaly Score</div>
                     <div style='color:#e2e8f0;font-weight:600;font-size:0.9rem;margin-top:2px;'>{anomaly_sc:.4f}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-header'>📊 Student Academic Features</div>", unsafe_allow_html=True)

        feature_display = {
            'Curricular units 1st sem (grade)': '1st Sem Grade',
            'Curricular units 2nd sem (grade)': '2nd Sem Grade',
            'Curricular units 1st sem (approved)': '1st Sem Approved',
            'Curricular units 2nd sem (approved)': '2nd Sem Approved',
            'Curricular units 1st sem (enrolled)': '1st Sem Enrolled',
            'Admission grade': 'Admission Grade',
            'Previous qualification (grade)': 'Prev Qualification',
            'Age at enrollment': 'Age at Enrollment',
        }

        feat_vals, feat_labels, feat_maxes = [], [], []
        for col_name, label in feature_display.items():
            if col_name in df.columns:
                val = student[col_name]
                max_val = df[col_name].max()
                feat_vals.append(float(val))
                feat_labels.append(label)
                feat_maxes.append(float(max_val))

        if feat_vals:
            norm_vals = [v / m if m > 0 else 0 for v, m in zip(feat_vals, feat_maxes)]
            bar_colors = ['#f87171' if v < 0.4 else '#fbbf24' if v < 0.7 else '#34d399'
                          for v in norm_vals]

            fig7 = go.Figure(go.Bar(
                x=norm_vals, y=feat_labels,
                orientation='h',
                marker_color=bar_colors,
                text=[f'{v:.1f}' for v in feat_vals],
                textposition='outside',
                textfont=dict(color='#94a3b8', size=11),
            ))
            fig7.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', height=400,
                margin=dict(t=10, b=10, l=10, r=60),
                xaxis=dict(gridcolor='#2a2d3e', title='Normalized Value (0–1)',
                           range=[0, 1.2]),
                yaxis=dict(gridcolor='#2a2d3e'),
            )
            st.plotly_chart(fig7, use_container_width=True)

        # Dropout gauge
        st.markdown("<div class='section-header'>🎯 Dropout Risk Gauge</div>", unsafe_allow_html=True)
        fig8 = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=dropout_risk,
            number={'suffix': '%', 'font': {'size': 36, 'color': '#e2e8f0'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#475569'},
                'bar': {'color': risk_color, 'thickness': 0.25},
                'bgcolor': '#12141f',
                'bordercolor': '#2a2d3e',
                'steps': [
                    {'range': [0, 33],  'color': '#34d399'},
                    {'range': [33, 66], 'color': '#f59e0b'},
                    {'range': [66, 100],'color': '#ef4444'},
                ],
                'threshold': {
                    'line': {'color': 'white', 'width': 2},
                    'thickness': 0.75,
                    'value': dropout_risk
                }
            },
        ))
        fig8.update_layout(
            paper_bgcolor='#1a1d2e', font_color='#94a3b8',
            height=220, margin=dict(t=20, b=10, l=30, r=30),
        )
        st.plotly_chart(fig8, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — STUDY PLANS
# ════════════════════════════════════════════════════════════════
elif "Study" in page:

    st.markdown("""
    <div class='hero-header'>
        <div class='hero-badge'>Module 4 — K-Means Clustering</div>
        <div class='hero-title'>📚 Personalized Study Plans</div>
        <div class='hero-subtitle'>AI-generated weekly study schedules based on each student's learning style cluster.</div>
    </div>
    """, unsafe_allow_html=True)

    student_idx = st.selectbox(
        "Select Student",
        options=list(range(len(df))),
        format_func=lambda x: f"Student #{x:04d}  |  Style: {df.iloc[x].get('learning_style', 'Unknown')}"
    )

    student = df.iloc[student_idx]
    style   = student.get('learning_style', None)

    if style and style in models.get('plans', {}):
        plan = models['plans'][style]

        style_colors = {
            '🔴 Struggling Learner': '#f87171',
            '🟡 Average Performer':  '#fbbf24',
            '🔵 Late Bloomer':       '#60a5fa',
            '🟢 High Achiever':      '#34d399',
        }
        sc = style_colors.get(style, '#a5b4fc')

        col1, col2 = st.columns([1, 1.5])

        with col1:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#1a1d2e,#12141f);
                        border:1px solid {sc}44;border-left:4px solid {sc};
                        border-radius:12px;padding:24px;margin-bottom:16px;'>
                <div style='font-size:0.72rem;color:#475569;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;'>Learning Style</div>
                <div style='font-size:1.4rem;font-weight:700;color:{sc};margin-bottom:8px;'>{style}</div>
                <div style='font-size:0.85rem;color:#94a3b8;line-height:1.6;margin-bottom:16px;'>{plan['description']}</div>
                <div style='display:flex;gap:16px;flex-wrap:wrap;'>
                    <div style='background:#12141f;border-radius:8px;padding:10px 16px;text-align:center;'>
                        <div style='font-size:1.6rem;font-weight:700;color:{sc};font-family:Poppins;'>{plan['weekly_hours']}h</div>
                        <div style='font-size:0.72rem;color:#475569;text-transform:uppercase;letter-spacing:.5px;'>Weekly</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Alert
            alert_text = plan.get('alert', '')
            alert_class = 'alert-danger' if 'HIGH' in alert_text else 'alert-warning' if 'MEDIUM' in alert_text else 'alert-success'
            st.markdown(f"<div class='{alert_class}'>{alert_text}</div>", unsafe_allow_html=True)

            # Priority
            st.markdown(f"""
            <div class='info-box'>
                <strong>🎯 Priority Focus:</strong><br>{plan['priority']}
            </div>
            """, unsafe_allow_html=True)

            # Resources
            st.markdown("<div class='section-header'>📖 Recommended Resources</div>", unsafe_allow_html=True)
            for res in plan['resources']:
                st.markdown(f"<div style='background:#12141f;border:1px solid #1e2130;border-radius:6px;padding:8px 14px;margin-bottom:6px;color:#94a3b8;font-size:0.85rem;'>📌 {res}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-header'>📅 Weekly Study Schedule</div>", unsafe_allow_html=True)
            day_colors = {
                'Monday':'#6366f1','Tuesday':'#8b5cf6','Wednesday':'#ec4899',
                'Thursday':'#f59e0b','Friday':'#10b981','Saturday':'#3b82f6','Sunday':'#64748b'
            }
            for day, task in plan['schedule'].items():
                dc = day_colors.get(day, '#475569')
                st.markdown(f"""
                <div style='background:#1a1d2e;border:1px solid #2a2d3e;border-left:3px solid {dc};
                            border-radius:8px;padding:12px 16px;margin-bottom:8px;display:flex;gap:16px;align-items:flex-start;'>
                    <div style='min-width:90px;font-size:0.75rem;font-weight:700;color:{dc};
                                text-transform:uppercase;letter-spacing:.5px;padding-top:2px;'>{day}</div>
                    <div style='color:#cbd5e1;font-size:0.88rem;line-height:1.5;'>{task}</div>
                </div>
                """, unsafe_allow_html=True)

    # Cluster distribution chart
    st.markdown("<div class='section-header'>🧩 Learning Style Distribution</div>", unsafe_allow_html=True)
    if 'learning_style' in df.columns:
        ls_df = df['learning_style'].value_counts().reset_index()
        ls_df.columns = ['Style', 'Count']
        ls_colors_map = {
            '🔴 Struggling Learner': '#f87171',
            '🟡 Average Performer':  '#fbbf24',
            '🔵 Late Bloomer':       '#60a5fa',
            '🟢 High Achiever':      '#34d399',
        }
        ls_df['color'] = ls_df['Style'].map(ls_colors_map)
        fig9 = px.bar(ls_df, x='Style', y='Count', color='Style',
                      color_discrete_map=ls_colors_map, text='Count')
        fig9.update_traces(textposition='outside', marker_line_width=0)
        fig9.update_layout(
            plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
            font_color='#94a3b8', showlegend=False,
            margin=dict(t=20, b=20, l=10, r=10),
            xaxis=dict(gridcolor='#2a2d3e', title=''),
            yaxis=dict(gridcolor='#2a2d3e', title='Number of Students'),
            height=300,
        )
        st.plotly_chart(fig9, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — ANALYTICS
# ════════════════════════════════════════════════════════════════
elif "Analytics" in page:

    st.markdown("""
    <div class='hero-header'>
        <div class='hero-badge'>Deep Dive Analytics</div>
        <div class='hero-title'>📊 Academic Analytics Dashboard</div>
        <div class='hero-subtitle'>Course-level insights, feature correlations, and dropout pattern analysis.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Dropout by course
        if 'Course' in df.columns:
            st.markdown("<div class='section-header'>📚 Dropout Rate by Course</div>", unsafe_allow_html=True)
            dr_course = df.groupby('Course').apply(
                lambda x: (x['Target'] == 'Dropout').sum() / len(x) * 100
            ).reset_index()
            dr_course.columns = ['Course', 'Dropout Rate (%)']
            dr_course = dr_course.sort_values('Dropout Rate (%)', ascending=False)
            dr_course['color'] = dr_course['Dropout Rate (%)'].apply(
                lambda x: '#f87171' if x > 30 else '#fbbf24' if x > 15 else '#34d399'
            )
            fig10 = px.bar(
                dr_course, x='Course', y='Dropout Rate (%)',
                color='Dropout Rate (%)',
                color_continuous_scale=['#34d399','#fbbf24','#f87171'],
                text=dr_course['Dropout Rate (%)'].round(1).astype(str) + '%'
            )
            fig10.update_traces(textposition='outside', marker_line_width=0)
            fig10.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', coloraxis_showscale=False,
                margin=dict(t=20, b=20, l=10, r=10), height=320,
                xaxis=dict(gridcolor='#2a2d3e'),
                yaxis=dict(gridcolor='#2a2d3e'),
            )
            st.plotly_chart(fig10, use_container_width=True)

    with col2:
        # Grade distribution by status
        grade_col = 'Curricular units 2nd sem (grade)'
        if grade_col in df.columns:
            st.markdown("<div class='section-header'>📈 Grade Distribution by Status</div>", unsafe_allow_html=True)
            fig11 = go.Figure()
            for status, color in zip(['Graduate','Enrolled','Dropout'],['#34d399','#60a5fa','#f87171']):
                subset = df[(df['Target'] == status) & (df[grade_col] > 0)][grade_col]
                fig11.add_trace(go.Box(
                    y=subset, name=status,
                    marker_color=color, line_color=color,
                    fillcolor=color,
                ))
            fig11.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', height=320,
                margin=dict(t=20, b=20, l=10, r=10),
                yaxis=dict(gridcolor='#2a2d3e', title='2nd Sem Grade'),
                xaxis=dict(gridcolor='#2a2d3e'),
                legend=dict(bgcolor='#1a1d2e'),
            )
            st.plotly_chart(fig11, use_container_width=True)

    # Correlation heatmap
    st.markdown("<div class='section-header'>🔥 Feature Correlation Heatmap</div>", unsafe_allow_html=True)
    corr_cols = [c for c in [
        'Curricular units 1st sem (grade)',
        'Curricular units 2nd sem (grade)',
        'Curricular units 1st sem (approved)',
        'Curricular units 2nd sem (approved)',
        'Admission grade',
        'Age at enrollment',
        'dropout_prob',
        'anomaly_score',
    ] if c in df.columns]

    if len(corr_cols) > 3:
        corr_matrix = df[corr_cols].corr().round(2)
        fig12 = px.imshow(
            corr_matrix,
            color_continuous_scale='RdBu_r',
            text_auto=True, aspect='auto',
            zmin=-1, zmax=1,
        )
        fig12.update_layout(
            plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
            font_color='#94a3b8', height=380,
            margin=dict(t=20, b=20, l=10, r=10),
        )
        st.plotly_chart(fig12, use_container_width=True)

    # Scholarship vs dropout
    col3, col4 = st.columns(2)
    with col3:
        if 'Scholarship holder' in df.columns:
            st.markdown("<div class='section-header'>🎓 Scholarship vs Dropout Rate</div>", unsafe_allow_html=True)
            sch = df.groupby('Scholarship holder').apply(
                lambda x: (x['Target'] == 'Dropout').sum() / len(x) * 100
            ).reset_index()
            sch.columns = ['Scholarship', 'Dropout Rate (%)']
            sch['Scholarship'] = sch['Scholarship'].map({0: 'No Scholarship', 1: 'Has Scholarship'})
            fig13 = px.bar(sch, x='Scholarship', y='Dropout Rate (%)',
                           color='Scholarship',
                           color_discrete_sequence=['#f87171', '#34d399'],
                           text=sch['Dropout Rate (%)'].round(1).astype(str) + '%')
            fig13.update_traces(textposition='outside', marker_line_width=0)
            fig13.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', showlegend=False, height=280,
                margin=dict(t=20, b=10, l=10, r=10),
                xaxis=dict(gridcolor='#2a2d3e'),
                yaxis=dict(gridcolor='#2a2d3e'),
            )
            st.plotly_chart(fig13, use_container_width=True)

    with col4:
        if 'Gender' in df.columns:
            st.markdown("<div class='section-header'>👥 Gender vs Dropout Rate</div>", unsafe_allow_html=True)
            gen = df.groupby('Gender').apply(
                lambda x: (x['Target'] == 'Dropout').sum() / len(x) * 100
            ).reset_index()
            gen.columns = ['Gender', 'Dropout Rate (%)']
            gen['Gender'] = gen['Gender'].map({0: 'Female', 1: 'Male'})
            fig14 = px.bar(gen, x='Gender', y='Dropout Rate (%)',
                           color='Gender',
                           color_discrete_sequence=['#c084fc', '#60a5fa'],
                           text=gen['Dropout Rate (%)'].round(1).astype(str) + '%')
            fig14.update_traces(textposition='outside', marker_line_width=0)
            fig14.update_layout(
                plot_bgcolor='#1a1d2e', paper_bgcolor='#1a1d2e',
                font_color='#94a3b8', showlegend=False, height=280,
                margin=dict(t=20, b=10, l=10, r=10),
                xaxis=dict(gridcolor='#2a2d3e'),
                yaxis=dict(gridcolor='#2a2d3e'),
            )
            st.plotly_chart(fig14, use_container_width=True)
