import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data with caching
@st.cache_data  # Use st.cache_data for caching data loading
def load_data():
    customers_df = pd.read_csv("https://raw.githubusercontent.com/icainsyuzuu/proyek-analisis-data/submission/customers_dataset.csv")
    orders_df = pd.read_csv("https://raw.githubusercontent.com/icainsyuzuu/proyek-analisis-data/submission/orders_dataset.csv")
    return customers_df, orders_df

customers_df, orders_df = load_data()

# Data Preparation
customers_df['customer_state'] = customers_df['customer_state'].astype(str)

# Merge DataFrames
merged_df = pd.merge(orders_df, customers_df, on='customer_id', how='inner')

# Convert to datetime
merged_df['order_delivered_customer_date'] = pd.to_datetime(merged_df['order_delivered_customer_date'])
merged_df['order_estimated_delivery_date'] = pd.to_datetime(merged_df['order_estimated_delivery_date'])

# Create late delivery column
merged_df['late_delivery'] = merged_df['order_delivered_customer_date'] > merged_df['order_estimated_delivery_date']

# Calculate late deliveries per state
late_delivery_per_state = merged_df.groupby('customer_state').agg(
    total_orders=('order_id', 'count'),
    late_orders=('late_delivery', 'sum')
).reset_index()

# Calculate late percentage
late_delivery_per_state['late_percentage'] = (late_delivery_per_state['late_orders'] / late_delivery_per_state['total_orders']) * 100

# Streamlit Dashboard
st.title("Order Analysis Dashboard")

# Section 1: Percentage of Late Deliveries by Customer State
st.header("Percentage of Late Deliveries by Customer State")
st.bar_chart(late_delivery_per_state.set_index('customer_state')['late_percentage'])

# Section 2: Order Volume by City and Order Status in the Last 6 Months
st.header("Order Volume by City and Order Status in the Last 6 Months")

# Filter recent orders
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'], errors='coerce')
cut_off_date = orders_df['order_purchase_timestamp'].max() - pd.DateOffset(months=6)
recent_orders = orders_df[orders_df['order_purchase_timestamp'] >= cut_off_date]

# Merge with customers for city data
recent_merged_df = pd.merge(recent_orders, customers_df[['customer_id', 'customer_city']], on='customer_id', how='inner')

# Aggregate order status by city
city_order_status = recent_merged_df.groupby(['customer_city', 'order_status']).size().reset_index(name='order_count')

# Sort by order count and select top N cities
top_n = 15
top_cities = city_order_status.groupby('customer_city')['order_count'].sum().nlargest(top_n).index
filtered_data = city_order_status[city_order_status['customer_city'].isin(top_cities)]

# Pivot the data for plotting
pivot_data = filtered_data.pivot(index='customer_city', columns='order_status', values='order_count').fillna(0)

# Plotting the bar chart
st.subheader("Top Cities by Order Status")
fig, ax = plt.subplots(figsize=(12, 8))
pivot_data.plot(kind='bar', stacked=True, ax=ax)
plt.title('Order Volume by City and Order Status in the Last 6 Months')
plt.xlabel('Customer City')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Order Status")
st.pyplot(fig)