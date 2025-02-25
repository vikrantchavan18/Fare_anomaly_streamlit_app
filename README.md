# Fare Anomaly Detection System

This Streamlit-based application detects anomalies in taxi fare data using machine learning. The system processes uploaded CSV files, analyzes fare-related anomalies using Isolation Forest, and visualizes results with interactive charts.

## Features
- **Upload CSV Files**: Supports structured fare data input.
- **Data Processing**: Cleans and prepares data for analysis.
- **Anomaly Detection**: Uses Isolation Forest to identify unusual fare patterns.
- **Interactive Visualizations**: Provides histograms, scatter plots, and timeline charts for anomaly insights.
- **Downloadable Reports**: Export detected anomalies for further review.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/fare-anomaly-detection.git
   cd fare-anomaly-detection
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run app.py
   ```

## Folder Structure
- `app.py` → Main Streamlit app.
- `modules/` → Contains processing, detection, and visualization scripts.
- `requirements.txt` → Lists project dependencies.

## Deployment
To deploy on Streamlit Sharing, push the repository to GitHub and link it to Streamlit Cloud.

---
Developed for real-time anomaly detection and visualizatio
