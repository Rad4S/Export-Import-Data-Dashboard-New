# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load dataset (you'll need to change this to your actual dataset)
df = pd.read_csv('Imports_Exports_Dataset.csv')  # Replace with your dataset path
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', dayfirst=True)

# Sample for performance (optional)
sample = df.sample(n=3000, random_state=42)

# Sidebar for user selections
st.sidebar.title("Filters")

# Sidebar filter for categories
categories = sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Sidebar filter for import/export types
import_export_options = sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

# Sidebar filter for year
years = sample['Date'].dt.year.unique()
selected_years = st.sidebar.multiselect("Select Years", options=years, default=years)

# Filter the data based on selections
filtered_df = sample[
    (sample['Category'].isin(selected_categories)) &
    (sample['Import_Export'].isin(selected_import_export)) &
    (sample['Date'].dt.year.isin(selected_years))
]

# Title of the Streamlit App
st.title("Imports and Exports Dashboard")

# 1. Scatter Plot: Quantity vs. Value
st.subheader('1. Scatter Plot of Quantity vs. Value')
fig1, ax1 = plt.subplots()
ax1.scatter(filtered_df['Quantity'], filtered_df['Value'], color='red')
ax1.set_title('Scatter Plot of Quantity vs. Value')
ax1.set_xlabel('Quantity')
ax1.set_ylabel('Value')
st.pyplot(fig1)

# 2. Percentage of High-Value Transactions (Pie Chart)
st.subheader('2. Percentage of High-Value Transactions')
high_value_transactions = filtered_df[filtered_df['Value'] >= filtered_df['Value'].quantile(0.90)]
percentage_high_value = len(high_value_transactions) / len(filtered_df) * 100

fig2, ax2 = plt.subplots()
ax2.pie([percentage_high_value, 100 - percentage_high_value],
        labels=['High Value', 'Others'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['#800080', '#FFC0CB'])
ax2.axis('equal')
ax2.set_title('Percentage of High-Value Transactions')
st.pyplot(fig2)

# 3. Bar Plot: Frequency of Shipping Methods
st.subheader('3. Bar Plot of Shipping Methods')
shipping_counts = filtered_df['Shipping_Method'].value_counts()
fig3, ax3 = plt.subplots()
ax3.bar(shipping_counts.index, shipping_counts.values, color='brown')
ax3.set_title('Bar Plot of Shipping Methods')
ax3.set_xlabel('Shipping Method')
ax3.set_ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(fig3)

# 4. Transaction Value Distribution (Histogram)
st.subheader('4. Transaction Value Distribution')
fig4, ax4 = plt.subplots()
ax4.hist(filtered_df['Value'], bins=30, color='orange', alpha=0.7, label='Histogram')
ax4.set_title('Transaction Value Distribution')
ax4.set_xlabel('Transaction Value')
ax4.set_ylabel('Frequency')
st.pyplot(fig4)

# 5. Weight Distribution per Product Category (Box-Whisker)
st.subheader('5. Weight Distribution per Product Category')
fig5, ax5 = plt.subplots(figsize=(12, 6))
filtered_df.boxplot(column='Weight', by='Category', ax=ax5, patch_artist=True, boxprops=dict(facecolor='lightblue'))
ax5.set_title('Weight Distribution per Product Category')
ax5.set_xlabel('Category')
ax5.set_ylabel('Weight')
plt.suptitle('')  # Suppress the default 'Boxplot grouped by Category' title
plt.xticks(rotation=45)
st.pyplot(fig5)

# 6. Monthly Transaction Trends (Line Plot)
st.subheader('6. Monthly Transaction Trends')
filtered_df['Month'] = filtered_df['Date'].dt.month
monthly_transactions = filtered_df.groupby('Month')['Value'].sum().reset_index()

fig6, ax6 = plt.subplots()
ax6.plot(monthly_transactions['Month'], monthly_transactions['Value'], color='#D8BFD8', linewidth=2)
ax6.set_title('Monthly Transaction Trends')
ax6.set_xlabel('Month')
ax6.set_ylabel('Total Value')
st.pyplot(fig6)
