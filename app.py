import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# EDUTRACK AI — Academic Risk & Learning Drift Dashboard
# Prototype / Simulation Version
# ============================================================

st.set_page_config(
    page_title="EduTrack AI | Student Risk Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- THEME --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f7fb;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1f3a 0%, #102f56 100%);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.hero {
    background: linear-gradient(135deg, #0b1f3a 0%, #145da0 55%, #1f8dd6 100%);
    padding: 28px 32px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 12px 35px rgba(11,31,58,.18);
    margin-bottom: 20px;
}

.hero h1 {
    margin: 0;
    font-size: 2.25rem;
    font-weight: 800;
}

.hero p {
    margin: 7px 0 0;
    opacity: .88;
    font-size: 1rem;
}

.badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 20px;
    background: rgba(255,255,255,.16);
    margin-top: 14px;
    font-size: .78rem;
    font-weight: 600;
}

.kpi {
    background: white;
    border: 1px solid #e4eaf2;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 5px 18px rgba(16,47,86,.06);
    min-height: 115px;
}

.kpi-title {
    color: #718096;
    font-size: .78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.kpi-value {
    color: #102f56;
    font-size: 1.85rem;
    font-weight: 800;
    margin-top: 5px;
}

.kpi-sub {
    color: #718096;
    font-size: .78rem;
    margin-top: 3px;
}

.panel {
    background: white;
    border: 1px solid #e4eaf2;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 5px 18px rgba(16,47,86,.05);
    margin-bottom: 16px;
}

.section-title {
    color: #102f56;
    font-size: 1.08rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.risk-critical {
    background: #fff1f2;
    border-left: 5px solid #e11d48;
    padding: 14px 16px;
    border-radius: 10px;
}

.risk-medium {
    background: #fff8e7;
    border-left: 5px solid #f59e0b;
    padding: 14px 16px;
    border-radius: 10px;
}

.risk-low {
    background: #ecfdf5;
    border-left: 5px solid #10b981;
    padding: 14px 16px;
    border-radius: 10px;
}

.intervention {
    background: #f8fbff;
    border: 1px solid #dbe8f5;
    border-radius: 14px;
    padding: 17px;
    min-height: 170px;
}

.intervention h4 {
    color: #123d68;
    margin: 0 0 8px;
}

.intervention p {
    color: #5d6b7a;
    font-size: .86rem;
    line-height: 1.55;
}

.footer {
    text-align: center;
    color: #8a98a8;
    font-size: .75rem;
    padding: 20px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e4eaf2;
    padding: 10px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DEMO DATA --------------------
students = {
    "Rahul Kumar": {
        "id": "ET-4021", "attendance": 72, "quiz": 58, "assignment": 61,
        "forum": 18, "late": 4, "risk": 74.5, "trend": "Declining"
    },
    "Sneha R": {
        "id": "ET-4022", "attendance": 91, "quiz": 84, "assignment": 88,
        "forum": 67, "late": 1, "risk": 32.0, "trend": "Stable"
    },
    "Aditya Verma": {
        "id": "ET-4023", "attendance": 64, "quiz": 49, "assignment": 52,
        "forum": 11, "late": 6, "risk": 88.2, "trend": "Declining"
    },
    "Meena S": {
        "id": "ET-4024", "attendance": 86, "quiz": 73, "assignment": 79,
        "forum": 49, "late": 2, "risk": 43.8, "trend": "Fluctuating"
    },
    "Arjun K": {
        "id": "ET-4025", "attendance": 95, "quiz": 92, "assignment": 94,
        "forum": 81, "late": 0, "risk": 18.6, "trend": "Improving"
    }
}

selected_name = st.sidebar.selectbox("👤 Student Profile", list(students.keys()))
profile = students[selected_name]

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ System Controls")
system_online = st.sidebar.toggle("AI Monitoring Gateway", value=True)
simulation_mode = st.sidebar.toggle("Intervention Simulation", value=True)

if system_online:
    st.sidebar.success("● SYSTEM ONLINE")
else:
    st.sidebar.error("● SYSTEM OFFLINE")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 Data Sources")
st.sidebar.checkbox("LMS Activity Logs", value=True, disabled=True)
st.sidebar.checkbox("Quiz / Assignment Scores", value=True, disabled=True)
st.sidebar.checkbox("Attendance Data", value=True, disabled=True)
st.sidebar.checkbox("Forum Activity", value=True, disabled=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="hero">
    <h1>🎓 EduTrack AI</h1>
    <p>Real-Time Student Learning Drift & Academic Risk Prediction System</p>
    <span class="badge">AI / ML • Learning Analytics • Explainable AI • Early Intervention</span>
</div>
""", unsafe_allow_html=True)

# -------------------- TOP STATUS --------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Selected Student</div>
        <div class="kpi-value" style="font-size:1.35rem;">{selected_name}</div>
        <div class="kpi-sub">{profile['id']}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Academic Risk</div>
        <div class="kpi-value">{profile['risk']:.1f}%</div>
        <div class="kpi-sub">{profile['trend']} learning pattern</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Attendance</div>
        <div class="kpi-value">{profile['attendance']}%</div>
        <div class="kpi-sub">Recent attendance indicator</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Quiz Performance</div>
        <div class="kpi-value">{profile['quiz']}%</div>
        <div class="kpi-sub">Latest assessment trend</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# -------------------- TABS --------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Student Analytics",
    "🧠 Drift & Explainability",
    "🚨 Intervention Center"
])

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================
with tab1:
    left, right = st.columns([1.05, 1.5])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Academic Risk Assessment</div>',
                    unsafe_allow_html=True)

        risk = profile["risk"]

        if risk >= 70:
            label = "CRITICAL RISK"
            color = "#e11d48"
            css = "risk-critical"
            message = "Multiple behavioural and academic indicators require early intervention."
        elif risk >= 40:
            label = "MODERATE RISK"
            color = "#f59e0b"
            css = "risk-medium"
            message = "Learning behaviour is fluctuating. Preventive support is recommended."
        else:
            label = "LOW RISK"
            color = "#10b981"
            css = "risk-low"
            message = "Current learning indicators are within a comparatively stable range."

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            number={"suffix": "%", "font": {"size": 34}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 35], "color": "#ecfdf5"},
                    {"range": [35, 70], "color": "#fff8e7"},
                    {"range": [70, 100], "color": "#fff1f2"}
                ],
                "threshold": {
                    "line": {"color": "#102f56", "width": 3},
                    "thickness": .75,
                    "value": risk
                }
            }
        ))
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="{css}">
            <strong>{label}</strong><br>
            <span style="font-size:.85rem;">{message}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Learning Performance Snapshot</div>',
                    unsafe_allow_html=True)

        metrics = pd.DataFrame({
            "Metric": ["Attendance", "Quiz Score", "Assignments", "Forum Activity"],
            "Score": [
                profile["attendance"],
                profile["quiz"],
                profile["assignment"],
                profile["forum"]
            ]
        })

        fig = px.bar(
            metrics,
            x="Score",
            y="Metric",
            orientation="h",
            text="Score",
            range_x=[0, 100]
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(
            height=290,
            margin=dict(l=10, r=35, t=10, b=10),
            xaxis_title="Performance / Activity (%)",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔎 Key Signals Detected</div>',
                unsafe_allow_html=True)

    signal_cols = st.columns(4)
    signals = [
        ("Attendance", profile["attendance"], "Attendance level"),
        ("Quiz Score", profile["quiz"], "Assessment performance"),
        ("Forum Activity", profile["forum"], "Learning engagement"),
        ("Late Submissions", profile["late"], "Recent delayed tasks")
    ]

    for col, (name, value, desc) in zip(signal_cols, signals):
        with col:
            st.metric(name, f"{value}%" if name != "Late Submissions" else str(value),
                      help=desc)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 2 — ANALYTICS
# ============================================================
with tab2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 8-Week Learning Performance Trend</div>',
                unsafe_allow_html=True)

    weeks = [f"Week {i}" for i in range(1, 9)]
    base = profile["quiz"]
    trend_adjust = np.linspace(-10, 6, 8) if profile["trend"] == "Improving" else (
        np.linspace(7, -8, 8) if profile["trend"] == "Declining" else np.array([0, 3, -2, 4, 1, -1, 2, 0])
    )
    np.random.seed(42 + list(students.keys()).index(selected_name))
    scores = np.clip(base + trend_adjust + np.random.normal(0, 3, 8), 20, 100)

    trend_df = pd.DataFrame({"Week": weeks, "Performance": scores.round(1)})

    fig = px.line(
        trend_df,
        x="Week",
        y="Performance",
        markers=True,
        range_y=[0, 100]
    )
    fig.update_traces(line_width=4, marker_size=8)
    fig.update_layout(height=340, margin=dict(l=10, r=20, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📚 Activity Distribution</div>',
                    unsafe_allow_html=True)

        activity = pd.DataFrame({
            "Activity": ["LMS Login", "Quiz", "Assignment", "Forum", "Video Learning"],
            "Engagement": [
                min(100, profile["attendance"] + 5),
                profile["quiz"],
                profile["assignment"],
                profile["forum"],
                min(100, profile["forum"] + 12)
            ]
        })
        fig = px.bar(activity, x="Activity", y="Engagement", range_y=[0, 100])
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with b:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧾 Student Profile Summary</div>',
                    unsafe_allow_html=True)

        summary = pd.DataFrame({
            "Indicator": [
                "Attendance",
                "Quiz performance",
                "Assignment performance",
                "Forum engagement",
                "Late submissions"
            ],
            "Value": [
                f"{profile['attendance']}%",
                f"{profile['quiz']}%",
                f"{profile['assignment']}%",
                f"{profile['forum']}%",
                profile["late"]
            ]
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)
        st.info("These values are prototype inputs for demonstrating the EduTrack AI dashboard workflow.")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 3 — DRIFT & EXPLAINABILITY
# ============================================================
with tab3:
    left, right = st.columns([1.25, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧠 Learning Drift Detection</div>',
                    unsafe_allow_html=True)

        factors = pd.DataFrame({
            "Risk Factor": [
                "Low Quiz Performance",
                "Attendance Reduction",
                "Forum Inactivity",
                "Late Assignments"
            ],
            "Impact": [
                max(0.1, (100 - profile["quiz"]) / 100),
                max(0.1, (100 - profile["attendance"]) / 100),
                max(0.1, (100 - profile["forum"]) / 100),
                min(1.0, profile["late"] / 6)
            ]
        }).sort_values("Impact")

        fig = px.bar(
            factors,
            x="Impact",
            y="Risk Factor",
            orientation="h",
            text="Impact"
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            height=340,
            xaxis_title="Relative Impact",
            yaxis_title="",
            margin=dict(l=10, r=40, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Explainability view: the chart represents prototype feature contributions "
            "that would be replaced by actual SHAP values after model integration."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔬 AI/ML Processing Pipeline</div>',
                    unsafe_allow_html=True)

        pipeline = [
            ("1", "Data Ingestion", "LMS • Quiz • Attendance • Forum"),
            ("2", "Anomaly Detection", "Autoencoder / Drift Detection"),
            ("3", "Forecasting", "LSTM / Transformer"),
            ("4", "Risk Scoring", "XGBoost / Classical ML"),
            ("5", "Explainability", "SHAP Feature Contributions"),
            ("6", "Intervention", "Teacher • Student • Parent")
        ]

        for num, title, desc in pipeline:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:center;
                        padding:10px 0;border-bottom:1px solid #edf1f5;">
                <div style="width:30px;height:30px;border-radius:50%;
                            background:#e8f2fb;color:#145da0;display:flex;
                            align-items:center;justify-content:center;font-weight:800;">
                    {num}
                </div>
                <div>
                    <b style="color:#123d68;">{title}</b><br>
                    <span style="font-size:.78rem;color:#718096;">{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 4 — INTERVENTIONS
# ============================================================
with tab4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎛️ Counterfactual Intervention Simulator</div>',
                unsafe_allow_html=True)

    st.write("Test how supportive actions could change the prototype risk score.")

    x, y = st.columns(2)
    with x:
        mentor = st.slider("Teacher Mentorship Sessions", 0, 5, 1)
    with y:
        peer = st.slider("Peer Support Hours", 0, 5, 1)

    with x:
        study = st.slider("Personalized Study Modules", 0, 5, 1)
    with y:
        reminders = st.slider("Assignment Reminder Support", 0, 5, 1)

    reduction = (
        mentor * 4.0 +
        peer * 3.0 +
        study * 2.5 +
        reminders * 1.5
    )

    simulated_risk = max(5.0, profile["risk"] - reduction)

    st.markdown(f"""
    <div style="background:#f7fbff;border:1px solid #d7e7f5;border-radius:14px;
                padding:18px;margin-top:12px;">
        <div style="color:#718096;font-size:.78rem;font-weight:700;text-transform:uppercase;">
            Simulated Post-Intervention Risk
        </div>
        <div style="font-size:2.4rem;font-weight:800;color:#145da0;">
            {simulated_risk:.1f}%
        </div>
        <div style="color:#718096;font-size:.82rem;">
            Prototype counterfactual calculation — not a clinical or academic decision.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🚨 Recommended Support Actions")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.markdown("""
        <div class="intervention">
            <h4>🎯 Student Support</h4>
            <p><b>Personalized learning nudge</b><br>
            Generate a short study plan based on recent low-performing topics
            and encourage consistent LMS engagement.</p>
        </div>
        """, unsafe_allow_html=True)

    with i2:
        st.markdown("""
        <div class="intervention">
            <h4>👩‍🏫 Teacher Action</h4>
            <p><b>Early check-in</b><br>
            Schedule a brief teacher-student interaction to understand learning
            barriers and provide targeted academic support.</p>
        </div>
        """, unsafe_allow_html=True)

    with i3:
        st.markdown("""
        <div class="intervention">
            <h4>👪 Parent / Guardian</h4>
            <p><b>Progress notification</b><br>
            Share an appropriate progress summary when institutional policy
            permits, while keeping the student data protected.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    if system_online:
        st.success("✅ Intervention engine is ready in prototype mode.")
    else:
        st.warning("⚠️ AI Monitoring Gateway is offline. Intervention automation is disabled.")

# -------------------- FOOTER --------------------
st.markdown("""
<div class="footer">
    EduTrack AI • Real-Time Student Learning Drift & Academic Risk Prediction System<br>
    Prototype dashboard for academic project demonstration
</div>
""", unsafe_allow_html=True)
