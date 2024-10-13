# Required Libraries
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
data = pd.read_csv("Imports_Exports_Dataset.csv")

# Sidebar filters
st.sidebar.title("Filters")

# Sampling for performance
sample = data.sample(n=3000, random_state=42)

# Category filter
categories = sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Import/Export filter
import_export_options = sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

# Date filter: Extract Year
sample['Date'] = pd.to_datetime(sample['Date'], format='%d-%m-%Y', errors='coerce')
sample['Year'] = sample['Date'].dt.year
years = sample['Year'].dropna().unique()
selected_years = st.sidebar.multiselect("Select Years", options=years, default=years)

# Filter the data
filtered_data = sample[
    (sample['Category'].isin(selected_categories)) &
    (sample['Import_Export'].isin(selected_import_export)) &
    (sample['Year'].isin(selected_years))
]

# Ensure data is available after filtering
if not filtered_data.empty:
    # Scatter Plot: Quantity vs Value
    st.subheader("1. Scatter Plot of Quantity vs. Value")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Quantity', y='Value', data=filtered_data, color='red')
    plt.title('Scatter Plot of Quantity vs. Value')
    plt.xlabel('Quantity')
    plt.ylabel('Value')
    st.pyplot(plt)

    # Pie Chart: Percentage of High-Value Transactions
    st.subheader("2. Percentage of High-Value Transactions")
    high_value = filtered_data[filtered_data['Value'] >= filtered_data['Value'].quantile(0.90)]
    percentage = len(high_value) / len(filtered_data) * 100

    fig, ax = plt.subplots()
    ax.pie([percentage, 100 - percentage], labels=['High Value', 'Others'], autopct='%1.1f%%',
           startangle=90, colors=['#800080', '#FFC0CB'])
    plt.title('Percentage of High-Value Transactions')
    plt.axis('equal')
    st.pyplot(fig)

    # Bar Plot: Frequency of Shipping Methods
    st.subheader("3. Bar Plot of Shipping Methods")
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Shipping_Method', data=filtered_data, color='brown')
    plt.title('Bar Plot of Shipping Methods')
    plt.xlabel('Shipping Method')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Histogram: Transaction Value Distribution
    st.subheader("4. Transaction Value Distribution")
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_data['Value'], bins=30, kde=True, color='yellow', alpha=0.7)
    sns.histplot(filtered_data['Value'], bins=30, kde=True, color='orange', alpha=0.3)
    plt.title('Transaction Value Distribution')
    plt.xlabel('Transaction Value')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    # Box Plot: Weight Distribution per Product Category
    st.subheader("5. Weight Distribution per Product Category")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Category', y='Weight', data=filtered_data, palette='pastel')
    plt.title('Weight Distribution per Product Category')
    plt.xlabel('Category')
    plt.ylabel('Weight')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Line Plot: Monthly Transaction Trends
    st.subheader("6. Monthly Transaction Trends")
    filtered_data['Month'] = filtered_data['Date'].dt.month
    monthly_data = filtered_data.groupby('Month')['Value'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Month', y='Value', data=monthly_data, color='#D8BFD8', linewidth=2)
    plt.title('Monthly Transaction Trends')
    plt.xlabel('Month')
    plt.ylabel('Total Value')
    plt.xticks(rotation=0)
    st.pyplot(plt)

else:
    st.warning("No data available for the selected filters. Please adjust your filters.")
