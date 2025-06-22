import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="🛍️",
    layout="wide"
)


# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100
    return df

df = load_data()


# Sidebar Filters
st.sidebar.header(" Filter Options")
region = st.sidebar.selectbox("Select Region", df['Region'].unique(), index=0)
category = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
year = st.sidebar.selectbox("Select Year", sorted(df['Order Date'].dt.year.unique()), index=0)

# Apply filters
filtered_df = df[
    (df['Region'] == region) &
    (df['Category'].isin(category)) &
    (df['Order Date'].dt.year == year)
]

# Title
st.title("Sales Dashboard")
st.caption("Superstore Sales Dashboard")


# Key Metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
avg_margin = filtered_df['Profit Margin (%)'].mean()

st.markdown("###  Key Business Metrics")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${total_sales:,.2f}")
kpi2.metric("Total Profit", f"${total_profit:,.2f}")
kpi3.metric("Avg Profit Margin", f"{avg_margin:.2f}%")


# Charts
st.markdown("key Insights")

# Sales by Sub-Category
subcat_sales = filtered_df.groupby("Sub-Category")['Sales'].sum().sort_values().reset_index()
fig1 = px.bar(subcat_sales, x="Sales", y="Sub-Category", orientation='h', color='Sales',
              title="Sales by Sub-Category", color_continuous_scale='Blues')

# Sales Trend Over Time
sales_trend = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
fig2 = px.line(sales_trend, x='Order Date', y='Sales', title='Sales Trend Over Time')

# Sales by State
state_sales = filtered_df.groupby("State")['Sales'].sum().sort_values().reset_index()
fig3 = px.bar(state_sales, x="Sales", y="State", orientation='h', title="Sales by State", color='Sales')

# Layout
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# Raw Data view
with st.expander(" View the Raw Data"):
    st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("superstore")
