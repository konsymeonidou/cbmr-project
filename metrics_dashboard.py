#code pulled from repo: https://github.com/saqiba123/shopify-app-using-fastapi-and-streamlit
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# FastAPI Base URL
BASE_URL = "http://127.0.0.1:8000/"
# Fetch data from FastAPI endpoints
def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint}: {e}")
        return []
    
# Extract nested fields into a DataFrame
def parse_daily_metrics(data):
    if not data:
        return pd.DataFrame()
    st.write("Data structure:", data)
    try:
        daily_metrics = [health_metrics["daily_metrics"] for health_metrics in data if isinstance(health_metrics, dict) and "daily_metrics" in health_metrics]
        return pd.json_normalize(daily_metrics)  # Flatten nested JSON structures
    except Exception as e:
        st.error(f"Error parsing metrics: {e}")
        return pd.DataFrame()
    
# Streamlit App
st.title("Menstrual Metrics Dashboard")
options = ["Candidates", "Metrics"]
option = st.sidebar.selectbox("Choose candidates or metrics to view:", options)
if option == "Orders":
    st.subheader("Shopify Orders")
    data = fetch_data("get-orders")  # Fetch data from FastAPI
    orders = data.get("orders", [])
    df = pd.json_normalize(orders)  # Flatten the list of orders
    if not df.empty:
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"])
        if "created_at" in df.columns and "total_price" in df.columns:
            fig = px.line(df, x="created_at", y="total_price", title="Order Totals Over Time")
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

        # Example: Bar Chart - Number of orders by day
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce") 
            df = df.dropna(subset=["created_at"])
            df["day"] = df["created_at"].dt.date  
            order_count_by_day = df.groupby("day").size().reset_index(name="order_count")
            fig = px.bar(order_count_by_day, x="day", y="order_count", title="Order Count by Day")
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
        # Order Status Breakdown (Pie Chart)
        if "financial_status" in df.columns:
            order_status_counts = df["financial_status"].value_counts().reset_index(name="order_count")
            order_status_counts.columns = ["status", "order_count"]
            fig = px.pie(order_status_counts, names="status", values="order_count", title="Order Status Breakdown")
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No orders data available.")
   
elif option == "Products":
    st.subheader("Shopify Products")
    data = fetch_data("get-products")
    if data:
        df = pd.DataFrame(data)
        if "products" in df.columns:
            products_data = pd.json_normalize(df["products"]) 
            if "title" in products_data.columns and "image.src" in products_data.columns:    
                for index, row in products_data.iterrows():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{row['title']}**")
                    with col2:
                        if "image.src" in row and pd.notna(row["image.src"]):
                            st.image(row["image.src"], caption=row["title"], width=200)
                        else:
                            st.write("No image available")
        else:
            st.warning("No 'products' column found in the fetched data.")
    else:
        st.warning("No data available for products.")