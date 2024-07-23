import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Sample data creation (Replace this with your actual data loading)
np.random.seed(42)  # For reproducibility
data = {
    'date': pd.date_range(start='1/1/2020', periods=100, freq='M'),
    'cost': np.random.rand(100) * 1000,
    'category': np.random.choice(['A', 'B', 'C'], 100)
}
df = pd.DataFrame(data)
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['month_period'] = df['date'].dt.to_period('M')

# Streamlit app
st.title("Financial Data Visualization")

# Year selection
years = df['year'].unique().tolist()
selected_years = st.multiselect('Select years to compare', years, default=years)

# Category selection
categories = df['category'].unique().tolist()
selected_categories = st.multiselect('Select categories to compare', categories, default=categories)

# Filter data based on selected years and categories
filtered_data = df[(df['year'].isin(selected_years)) & (df['category'].isin(selected_categories))]

# Monthly comparison
monthly_data = filtered_data.groupby(['year', 'month', 'category'])['cost'].sum().reset_index()

# Quarterly comparison
quarterly_data = filtered_data.groupby(['year', 'quarter', 'category'])['cost'].sum().reset_index()

# Create subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Monthly Cost Comparison", "Quarterly Cost Comparison"),
    shared_yaxes=True
)

# Add monthly data to subplot
for year in selected_years:
    for category in selected_categories:
        year_cat_data = monthly_data[(monthly_data['year'] == year) & (monthly_data['category'] == category)]
        fig.add_trace(
            go.Bar(x=year_cat_data['month'], y=year_cat_data['cost'], name=f"Year {year} - Category {category}", legendgroup=f"Year {year} - Category {category}"),
            row=1, col=1
        )

# Add quarterly data to subplot
for year in selected_years:
    for category in selected_categories:
        year_cat_data = quarterly_data[(quarterly_data['year'] == year) & (quarterly_data['category'] == category)]
        fig.add_trace(
            go.Bar(x=year_cat_data['quarter'], y=year_cat_data['cost'], name=f"Year {year} - Category {category}", legendgroup=f"Year {year} - Category {category}"),
            row=1, col=2
        )

# Update layout
fig.update_layout(barmode='group', title="Monthly and Quarterly Cost Comparison by Category", showlegend=True)

# Display the plot in Streamlit
st.plotly_chart(fig)