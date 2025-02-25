import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# Set page config at the very top (first Streamlit command)
st.set_page_config(page_title="Health Metrics and Candidates Dashboard", layout="wide")

# FastAPI Base URL
BASE_URL = "http://127.0.0.1:8000"

# Load credentials from YAML file
def load_credentials():
    with open('streamlit_credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

# Authenticate user
def authenticate():
    config = load_credentials()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    return authenticator


# Main app logic
def main_app():
    def fetch_data(endpoint):
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching {endpoint}: {e}")
            return []

    st.title("Health Metrics and Candidates Dashboard")

    # Sidebar options
    st.sidebar.header("Navigation")
    st.sidebar.markdown("Use the dropdown below to select the data you want to view.")
    options = ["Candidates", "Health Metrics"]
    option = st.sidebar.selectbox("Choose data to view:", options)

    if option == "Candidates":
        st.subheader("Candidates")
        data = fetch_data("candidates/")  # Fetch data from FastAPI
        if data:
            df = pd.DataFrame(data)
            if not df.empty:
                st.write("Candidates Data:")
                st.dataframe(df)

                # Example: Bar Chart - Age Distribution
                if "age" in df.columns:
                    fig = px.histogram(df, x="age", title="Age Distribution of Candidates", color_discrete_sequence=["#636EFA"])
                    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)

                # Example: Pie Chart - Email Availability
                if "email" in df.columns:
                    email_status = df["email"].apply(lambda x: "Available" if pd.notna(x) else "Not Available")
                    email_status_counts = email_status.value_counts().reset_index(name="count")
                    email_status_counts.columns = ["status", "count"]
                    fig = px.pie(email_status_counts, names="status", values="count", title="Email Availability", color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No candidates data available.")
        else:
            st.error("No candidates data available.")

    elif option == "Health Metrics":
        st.subheader("Health Metrics")
        data = fetch_data("metrics/")  # Fetch data from FastAPI
        if data:
            df = pd.DataFrame(data)
            if not df.empty:
                st.write("Health Metrics Data:")
                st.dataframe(df)
                # st.write(df["daily_metrics"])
                st.write(df['daily_metrics'].iloc[0]['flow'])

                # Example: Pie Chart - Daily metrics Availability
                if "daily_metrics" in df.columns:
                    daily_metrics = df["daily_metrics"].apply(lambda x: "Available" if pd.notna(x) else "Not Available")
                    daily_metrics_status_counts = daily_metrics.value_counts().reset_index(name="count")
                    daily_metrics_status_counts.columns = ["status", "count"]
                    fig = px.pie(daily_metrics_status_counts, names="status", values="count", title="Daily Metrics Availability", color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)

                # Example: Pie Chart - Optional metrics Availability
                if "optional_metrics" in df.columns:
                    optional_metrics = df["optional_metrics"].apply(lambda x: "Available" if pd.notna(x) else "Not Available")
                    optional_metrics_status_counts = optional_metrics.value_counts().reset_index(name="count")
                    optional_metrics_status_counts.columns = ["status", "count"]
                    fig = px.pie(optional_metrics_status_counts, names="status", values="count", title="Optional Metrics Availability", color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)

                # # Example: Line Chart - Steps Over Time
                # if "date" in df.columns and "daily_metrics.steps" in df.columns:
                #     df["date"] = pd.to_datetime(df["date"])
                #     fig = px.line(df, x="date", y="daily_metrics.steps", title="Steps Over Time", color_discrete_sequence=["#00CC96"])
                #     fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                #     st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No health metrics data available.")
        else:
            st.error("No health metrics data available.")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Contact Information**")
    st.sidebar.markdown("For more information, please contact us at [email@gmail.com](mailto:email@gmail.com).")

# Login and authentication logic
def login():
    authenticator = authenticate()
    name, authentication_status, username = authenticator.login()
    if "authentication_status" not in st.session_state:
        authentication_status = st.session_state["authentication_status"]
    if authentication_status:
        authenticator.logout(location='sidebar')
        main_app()
    elif authentication_status == False:
        st.error("Username or password are incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username & password")

# Run the app
if __name__ == "__main__":
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    
    if st.session_state["authentication_status"]:
        main_app()
    else:
        login()