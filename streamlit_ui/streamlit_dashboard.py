from typing import Dict, List
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
BASE_URL = "http://127.0.0.1:8000"
CHART_HEIGHT = 400
CHART_MARGIN = dict(l=20, r=20, t=40, b=20)
COLOR_PALETTE = px.colors.sequential.RdBu

# API Endpoints
CANDIDATES_ENDPOINT = "candidates/"
METRICS_ENDPOINT = "metrics/"


@st.cache_data
def fetch_data(endpoint: str) -> List[Dict]:
    """
    Fetch data from the FastAPI endpoint.
    """
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint}: {e}")
        return []


def flatten_data(data: List[Dict]) -> pd.DataFrame:
    """
    Flatten nested dictionaries in the data.
    """
    flattened_data = []
    for item in data:
        flattened_item = {
            **item,
            **{
                f"daily_metrics_{k}": v
                for k, v in item.get("daily_metrics", {}).items()
            },
            **{
                f"optional_metrics_{k}": v
                for k, v in item.get("optional_metrics", {}).items()
            },
        }
        flattened_data.append(flattened_item)
    return pd.DataFrame(flattened_data)


def plot_histogram(df: pd.DataFrame, x: str, title: str, color: str = "#636EFA"):
    """
    Plot a histogram for a given column.
    """
    if x in df.columns:
        fig = px.histogram(df, x=x, title=title, color_discrete_sequence=[color])
        fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
        st.plotly_chart(fig, use_container_width=True)


def plot_bar_chart(df: pd.DataFrame, x: str, title: str, color: str = "#636EFA"):
    """
    Plot a bar chart for a given column (useful for categorical data like mood).
    """
    if x in df.columns:
        fig = px.bar(df, x=x, title=title, color_discrete_sequence=[color])
        fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
        st.plotly_chart(fig, use_container_width=True)


def plot_pie_chart(df: pd.DataFrame, column: str, title: str):
    """
    Plot a pie chart for a given column.
    """
    if column in df.columns:
        status = df[column].apply(
            lambda x: "Available" if pd.notna(x) else "Not Available"
        )
        status_counts = status.value_counts().reset_index(name="count")
        status_counts.columns = ["status", "count"]
        fig = px.pie(
            status_counts,
            names="status",
            values="count",
            title=title,
            color_discrete_sequence=COLOR_PALETTE,
        )
        fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
        st.plotly_chart(fig, use_container_width=True)


def plot_line_chart(
    df: pd.DataFrame, x: str, y: str, title: str, color: str = "#00CC96"
):
    """
    Plot a line chart for a given x and y column.
    """
    if x in df.columns and y in df.columns:
        fig = px.line(df, x=x, y=y, title=title, color_discrete_sequence=[color])
        fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
        st.plotly_chart(fig, use_container_width=True)


def display_candidates():
    """
    Display candidates data and visualizations.
    """
    st.subheader("Candidates")
    data = fetch_data(CANDIDATES_ENDPOINT)

    if data:
        df = pd.DataFrame(data)
        if not df.empty:
            plot_histogram(df, "age", "Age Distribution of Candidates")
            plot_pie_chart(df, "email", "Email Availability")
        else:
            st.error("No candidates data available.")
    else:
        st.error("No candidates data available.")


def display_health_metrics():
    """
    Display health metrics data and visualizations.
    """
    st.subheader("Health Metrics")
    data = fetch_data(METRICS_ENDPOINT)

    if data:
        df = flatten_data(data)
        if not df.empty:
            plot_pie_chart(df, "daily_metrics_flow", "Daily Metrics Availability")
            plot_pie_chart(
                df, "optional_metrics_height", "Optional Metrics Availability"
            )
            if "date" in df.columns and "daily_metrics_steps" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                plot_line_chart(df, "date", "daily_metrics_steps", "Steps Over Time")

                # Mood Distribution (Bar Chart)
            if "daily_metrics_mood" in df.columns:
                plot_bar_chart(
                    df, "daily_metrics_mood", "Mood Distribution of Candidates"
                )
        else:
            st.error("No health metrics data available.")
    else:
        st.error("No health metrics data available.")


def main_app():
    """
    Main Streamlit app logic.
    """
    st.set_page_config(
        page_title="Health Metrics and Candidates Dashboard", layout="wide"
    )
    st.title("Health Metrics and Candidates Dashboard")

    # Sidebar navigation
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox(
        "Choose data to view:", ["Candidates", "Health Metrics"]
    )

    if option == "Candidates":
        display_candidates()
    elif option == "Health Metrics":
        display_health_metrics()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Contact Information**")
    st.sidebar.markdown(
        "For more information, please contact us at [email@gmail.com](mailto:email@gmail.com)."
    )


if __name__ == "__main__":
    main_app()
