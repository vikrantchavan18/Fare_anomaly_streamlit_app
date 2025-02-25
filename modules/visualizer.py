import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_fare_distribution(df):
    """
    Create a histogram of fare distribution with anomalies highlighted
    """
    fig = go.Figure()

    # Add normal fares
    fig.add_trace(go.Histogram(
        x=df[~df['is_anomaly']]['fare'],
        name='Normal',
        opacity=0.75
    ))

    # Add anomalous fares
    fig.add_trace(go.Histogram(
        x=df[df['is_anomaly']]['fare'],
        name='Anomaly',
        opacity=0.75
    ))

    fig.update_layout(
        title="Fare Distribution",
        xaxis_title="Fare Amount ($)",
        yaxis_title="Count",
        barmode='overlay'
    )

    return fig

def plot_anomalies_scatter(df):
    """
    Create a line chart of fares vs distance with anomalies highlighted
    """
    # Calculate max distance and create bins in 5km intervals
    max_distance = df['distance'].max()
    bin_edges = np.arange(0, max_distance + 5, 5)

    # Create distance ranges using 5km intervals
    df['distance_range'] = pd.cut(
        df['distance'], 
        bins=bin_edges,
        labels=[f'{int(i)}-{int(i+5)}km' for i in bin_edges[:-1]]
    )

    # Calculate average fares for different distance ranges
    normal_avg = df[~df['is_anomaly']].groupby('distance_range')['fare'].mean()
    anomaly_avg = df[df['is_anomaly']].groupby('distance_range')['fare'].mean()

    fig = go.Figure()

    # Add normal fares as a line
    fig.add_trace(go.Scatter(
        x=normal_avg.index.astype(str),
        y=normal_avg.values,
        name='Normal',
        line=dict(color='blue', width=2),
        mode='lines+markers'
    ))

    # Add anomalous fares as a line
    fig.add_trace(go.Scatter(
        x=anomaly_avg.index.astype(str),
        y=anomaly_avg.values,
        name='Anomaly',
        line=dict(color='red', width=2),
        mode='lines+markers'
    ))

    fig.update_layout(
        title="Average Fare by Distance Range",
        xaxis_title="Distance Range (km)",
        yaxis_title="Average Fare ($)",
        hovermode='x unified'
    )

    return fig

def plot_anomaly_timeline(df):
    """
    Create area charts (layered and stacked) view of fares with anomalies highlighted
    """
    if 'timestamp' not in df.columns:
        return None

    # Create two subplots for layered and stacked area charts
    fig = go.Figure()

    # Resample data to hourly intervals for smoother visualization
    df_resampled = df.set_index('timestamp').resample('1H').agg({
        'fare': 'mean',
        'is_anomaly': 'any'
    }).reset_index()

    # Split data into normal and anomaly
    normal_data = df_resampled[~df_resampled['is_anomaly']]
    anomaly_data = df_resampled[df_resampled['is_anomaly']]

    # Add layered area chart
    fig.add_trace(go.Scatter(
        x=normal_data['timestamp'],
        y=normal_data['fare'],
        fill='tozeroy',
        name='Normal Fares',
        line=dict(color='blue'),
        fillcolor='rgba(0, 0, 255, 0.2)'
    ))

    fig.add_trace(go.Scatter(
        x=anomaly_data['timestamp'],
        y=anomaly_data['fare'],
        fill='tonexty',
        name='Anomalous Fares',
        line=dict(color='red'),
        fillcolor='rgba(255, 0, 0, 0.2)'
    ))

    fig.update_layout(
        title="Fare Timeline (Area Chart)",
        xaxis_title="Time",
        yaxis_title="Fare Amount ($)",
        showlegend=True,
        hovermode='x unified'
    )

    return fig