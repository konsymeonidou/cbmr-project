import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# FastAPI Base URL
BASE_URL = "http://127.0.0.1:8000"


# with open('streamlit_credentials.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
# )

# authenticator.login(location='main', key='Login')
# if st.session_state['authentication_status']:
    # authenticator.logout()
    # Fetch data from FastAPI endpoints
def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint}: {e}")
        return []

    # Streamlit App
st.set_page_config(page_title="Health Metrics and Candidates Dashboard", layout="wide")
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

            # Example: Line Chart - Steps Over Time
            if "date" in df.columns and "daily_metrics.steps" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                fig = px.line(df, x="date", y="daily_metrics.steps", title="Steps Over Time", color_discrete_sequence=["#00CC96"])
                fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)

            # Example: Bar Chart - Mood Distribution
            if "daily_metrics.mood" in df.columns:
                mood_counts = df["daily_metrics.mood"].value_counts().reset_index(name="count")
                mood_counts.columns = ["mood", "count"]
                fig = px.bar(mood_counts, x="mood", y="count", title="Mood Distribution", color_discrete_sequence=["#AB63FA"])
                fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)

            # Example: Pie Chart - Weight Distribution
            if "daily_metrics.weight" in df.columns:
                weight_bins = pd.cut(df["daily_metrics.weight"], bins=5)
                weight_distribution = weight_bins.value_counts().reset_index(name="count")
                weight_distribution.columns = ["weight_range", "count"]
                fig = px.pie(weight_distribution, names="weight_range", values="count", title="Weight Distribution", color_discrete_sequence=px.colors.sequential.Plasma)
                fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No health metrics data available.")
    else:
        st.error("No health metrics data available.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Contact Information**")
st.sidebar.markdown("For more information, please contact us at [email@gmail.com](mailto:email@gmail.com).")

# elif st.session_state['authentication_status'] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state['authentication_status'] is None:
#     st.warning('Please enter your username and password')