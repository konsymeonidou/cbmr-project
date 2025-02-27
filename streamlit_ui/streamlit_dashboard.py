from typing import Dict, List
import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# FastAPI Base URL
BASE_URL = "http://127.0.0.1:8000"
# Constants
CHART_HEIGHT = 400
CHART_MARGIN = dict(l=20, r=20, t=40, b=20)


def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint}: {e}")
        return []


def plot_age_distribution(df: pd.DataFrame):
    """
    Plot a histogram for age distribution.
    """
    if "age" in df.columns:
        fig = px.histogram(
            df,
            x="age",
            title="Age Distribution of Candidates",
            color_discrete_sequence=["#636EFA"],
        )
        fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
        st.plotly_chart(fig, use_container_width=True)


def plot_email_availability(df: pd.DataFrame):
    """
    Plot a pie chart for email availability.
    """
    if "email" in df.columns:
        email_status = df["email"].apply(
            lambda x: "Available" if pd.notna(x) else "Not Available"
        )
        email_status_counts = email_status.value_counts().reset_index(name="count")
        email_status_counts.columns = ["status", "count"]
        fig = px.pie(
            email_status_counts,
            names="status",
            values="count",
            title="Email Availability",
            color_discrete_sequence=px.colors.sequential.RdBu,
        )
        fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
        st.plotly_chart(fig, use_container_width=True)


def display_candidates():
    """
    Display candidates data and visualizations.
    """
    st.subheader("Candidates")
    data = fetch_data("candidates/")  # Fetch data from FastAPI

    if data:
        df = pd.DataFrame(data)
        if not df.empty:
            # Display visualizations
            plot_age_distribution(df)
            plot_email_availability(df)
        else:
            st.error("No candidates data available.")
    else:
        st.error("No candidates data available.")


def flatten_data(data: List[Dict]) -> pd.DataFrame:
    """
    Flatten nested dictionaries in the data.
    """
    flattened_data = []
    for item in data:
        flattened_item = {
            **item,
            **{f"daily_metrics_{k}": v for k, v in item["daily_metrics"].items()},
            **{f"optional_metrics_{k}": v for k, v in item["optional_metrics"].items()},
        }
        del flattened_item["daily_metrics"]
        del flattened_item["optional_metrics"]
        flattened_data.append(flattened_item)
    return pd.DataFrame(flattened_data)


def plot_pie_chart(df: pd.DataFrame, column: str, title: str):
    """
    Plot a pie chart for a given column.
    """
    status = df[column].apply(lambda x: "Available" if pd.notna(x) else "Not Available")
    status_counts = status.value_counts().reset_index(name="count")
    status_counts.columns = ["status", "count"]
    fig = px.pie(
        status_counts,
        names="status",
        values="count",
        title=title,
        color_discrete_sequence=px.colors.sequential.RdBu,
    )
    fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
    st.plotly_chart(fig, use_container_width=True)


def plot_line_chart(df: pd.DataFrame, x: str, y: str, title: str):
    """
    Plot a line chart for a given x and y column.
    """
    fig = px.line(df, x=x, y=y, title=title, color_discrete_sequence=["#00CC96"])
    fig.update_layout(height=CHART_HEIGHT, margin=CHART_MARGIN)
    st.plotly_chart(fig, use_container_width=True)


def display_health_metrics():
    """
    Display health metrics data and visualizations.
    """
    st.subheader("Health Metrics")
    data = fetch_data("metrics/")  # Fetch data from FastAPI

    if data:
        df = flatten_data(data)  # Flatten nested data
        # st.write("Health Metrics Data:")
        # st.dataframe(df)

        if not df.empty:
            # Pie Chart - Daily Metrics Availability
            if "daily_metrics_flow" in df.columns:
                plot_pie_chart(df, "daily_metrics_flow", "Daily Metrics Availability")

            # Pie Chart - Optional Metrics Availability
            if "optional_metrics_height" in df.columns:
                plot_pie_chart(
                    df, "optional_metrics_height", "Optional Metrics Availability"
                )

            # Line Chart - Steps Over Time
            if "date" in df.columns and "daily_metrics_steps" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                plot_line_chart(df, "date", "daily_metrics_steps", "Steps Over Time")
        else:
            st.error("No health metrics data available.")
    else:
        st.error("No health metrics data available.")


# Main app logic
def main_app():
    # Streamlit App Title
    st.set_page_config(
        page_title="Health Metrics and Candidates Dashboard", layout="wide"
    )
    st.title("Health Metrics and Candidates Dashboard")

    # Sidebar options
    st.sidebar.header("Navigation")
    st.sidebar.markdown("Use the dropdown below to select the data you want to view.")
    options = ["Candidates", "Health Metrics"]
    option = st.sidebar.selectbox("Choose data to view:", options)

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


# Run the app
if __name__ == "__main__":
    main_app()
