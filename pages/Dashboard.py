import streamlit as st
import pandas as pd
import plotly.express as px

# 🔒 Redirect to login page if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login_signup.py")

st.set_page_config(page_title="Dashboard", layout="wide")
st.markdown("## 📊 Prediction Dashboard")

# Load predictions
recent_predictions = st.session_state.get("recent_predictions", [])

if not recent_predictions:
    st.info("📂 No predictions in this session yet. Upload an image to begin.")
else:
    df = pd.DataFrame(recent_predictions)
    df = df[df["Label"].str.lower() != "none"]  # Exclude 'None' predictions

    if df.empty:
        st.warning("⚠️ No valid steel strip defect data to display.")
    else:
        # Prepare numeric column
        df['Confidence (%)'] = df['Confidence'].str.replace('%', '').astype(float)

        ### 1️⃣ LINE CHART - Confidence per Predicted Class
        st.subheader("📈 Model Confidence Trend per Defect Category")
        fig_line = px.line(
            df,
            x="Label",
            y="Confidence (%)",
            markers=True,
            text="Confidence (%)",
            labels={"Label": "Prediction Class"},
        )
        fig_line.update_traces(textposition="top center")
        fig_line.update_layout(
            height=300,
            margin=dict(l=30, r=30, t=30, b=30),
        )
        st.plotly_chart(fig_line, use_container_width=True)

        ### 2️⃣ BOX CHART - Confidence Range by Class
        st.subheader("📉 Confidence Distribution Across Defect Classes")
        fig_box = px.box(
            df,
            x="Label",
            y="Confidence (%)",
            color="Label",
            title="Confidence by Prediction Class",
            template="plotly_dark"
        )
        fig_box.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=30, r=30, t=30, b=30),
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig_box, use_container_width=True)

        ### 3️⃣ BAR CHART - Average Confidence per Class
        st.subheader("📏 Average Confidence per Class")
        avg_conf = df.groupby("Label")["Confidence (%)"].mean().reset_index()
        fig_bar = px.bar(
            avg_conf,
            x="Label",
            y="Confidence (%)",
            color="Label",
            text="Confidence (%)",
            labels={"Label": "Prediction Class"},
            template="plotly_dark"
        )
        fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_bar.update_layout(
            showlegend=False,
            yaxis_range=[0, 105],
            height=350,
            margin=dict(l=30, r=30, t=30, b=30),
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig_bar, use_container_width=True)

      