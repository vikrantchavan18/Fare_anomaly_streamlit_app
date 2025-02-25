import streamlit as st
import pandas as pd
import numpy as np
from modules.data_processor import process_data
from modules.anomaly_detector import detect_anomalies
from modules.visualizer import (
    plot_fare_distribution,
    plot_anomalies_scatter,
    plot_anomaly_timeline
)

# Set page config
st.set_page_config(
    page_title="Fare Anomaly Detection System",
    page_icon="🚗",
    layout="wide"
)

# Main title
st.title("🚗 Fare Anomaly Detection System")

# Sidebar
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Model parameters
    st.header("Model Parameters")
    contamination = st.slider(
        "Contamination Factor",
        min_value=0.01,
        max_value=0.5,
        value=0.1,
        help="Expected proportion of anomalies in the dataset"
    )

    # Alert settings
    st.header("Alert Settings")
    alert_threshold = st.slider(
        "Alert Threshold Score",
        min_value=-1.0,
        max_value=0.0,
        value=-0.5,
        help="Anomaly score threshold for generating alerts"
    )

if uploaded_file is not None:
    try:
        # Load and process data
        df = pd.read_csv(uploaded_file)
        processed_df = process_data(df)

        # Detect anomalies
        df_with_anomalies = detect_anomalies(processed_df, contamination)

        # Dashboard Layout
        st.header("📊 Real-time Monitoring Dashboard")

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rides", len(df))
        with col2:
            anomaly_count = sum(df_with_anomalies['is_anomaly'])
            st.metric("Anomalies Detected", anomaly_count)
        with col3:
            avg_fare = f"${df_with_anomalies['fare'].mean():.2f}"
            st.metric("Average Fare", avg_fare)
        with col4:
            anomaly_rate = f"{(anomaly_count/len(df)*100):.1f}%"
            st.metric("Anomaly Rate", anomaly_rate)

        # Alert Section
        st.header("⚠️ Active Alerts")
        high_risk_anomalies = df_with_anomalies[
            (df_with_anomalies['is_anomaly']) & 
            (df_with_anomalies['anomaly_score'] < alert_threshold)
        ]

        if not high_risk_anomalies.empty:
            st.error(f"🚨 {len(high_risk_anomalies)} high-risk anomalies detected!")

            # Display detailed alerts
            with st.expander("View Alert Details"):
                for _, row in high_risk_anomalies.iterrows():
                    st.warning(
                        f"Suspicious fare detected:\n"
                        f"- Fare Amount: ${row['fare']:.2f}\n"
                        f"- Distance: {row['distance']:.1f} km\n"
                        f"- Fare per km: ${row['fare_per_km']:.2f}\n"
                        f"- Anomaly Score: {row['anomaly_score']:.3f}"
                    )
        else:
            st.success("✅ No high-risk anomalies detected")

        # Visualizations
        st.header("📈 Anomaly Analysis")

        # Fare Distribution
        st.subheader("Fare Distribution")
        fig_dist = plot_fare_distribution(df_with_anomalies)
        st.plotly_chart(fig_dist, use_container_width=True)

        # Anomalies by Distance
        st.subheader("Anomaly Detection Results")
        fig_scatter = plot_anomalies_scatter(df_with_anomalies)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Timeline View
        if 'timestamp' in df_with_anomalies.columns:
            st.subheader("Anomalies Timeline")
            fig_timeline = plot_anomaly_timeline(df_with_anomalies)
            st.plotly_chart(fig_timeline, use_container_width=True)

        # Export functionality
        st.header("📥 Export Results")

        col1, col2 = st.columns(2)
        with col1:
            # Export all anomalies
            anomalies_df = df_with_anomalies[df_with_anomalies['is_anomaly']]
            if not anomalies_df.empty:
                csv = anomalies_df.to_csv(index=False)
                st.download_button(
                    label="Download All Anomalies",
                    data=csv,
                    file_name="all_anomalies.csv",
                    mime="text/csv"
                )

        with col2:
            # Export high-risk anomalies
            if not high_risk_anomalies.empty:
                high_risk_csv = high_risk_anomalies.to_csv(index=False)
                st.download_button(
                    label="Download High-risk Anomalies",
                    data=high_risk_csv,
                    file_name="high_risk_anomalies.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload a CSV file to begin analysis")

    # Sample format
    st.header("Expected Data Format")
    sample_data = pd.DataFrame({
        'timestamp': ['2023-01-01 10:00:00'],
        'fare': [25.50],
        'distance': [5.2],
        'duration': [15]
    })
    st.dataframe(sample_data)