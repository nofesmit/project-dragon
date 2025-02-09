import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import calendar
import locale

# --- CONFIG ---

st.set_page_config(page_title="Összahasonlítás", layout="wide", page_icon='dragon')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

try:
    locale.setlocale(locale.LC_TIME, 'hu_HU.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # Fallback to default

# --- THEME ---

graph_color = '#30826B'

# --- FUNCTIONS ---

def total_netto(label, value, prefix="", suffix="", show_graph=False, graph_x="", graph_y="", color_graph=""):
    if graph_x is None:
        graph_x = []
    if graph_y is None:
        graph_y = []
    # Set locale to Hungarian
    locale.setlocale(locale.LC_TIME, 'hu_HU.UTF-8')
    # Hungarian month names
    hungarian_months = [
        "január", "február", "március", "április", "május", "június",
        "július", "augusztus", "szeptember", "október", "november", "december"
    ]
    if isinstance(graph_x, pd.Series) and isinstance(graph_x.iloc[0], pd.Period):
        graph_x = graph_x.dt.strftime('%Y. %B')
    elif isinstance(graph_x, list) and isinstance(graph_x[0], pd.Period):
        graph_x = [x.strftime('%Y. %B') for x in graph_x]
    
    # Create a mapping of English to Hungarian month names
    month_mapping = {calendar.month_name[i]: hungarian_months[i-1] for i in range(1, 13)}
    
    # Replace English month names with Hungarian ones using the mapping
    graph_x = [' '.join(month_mapping.get(word, word) for word in x.split()) for x in graph_x]

    if isinstance(graph_y, pd.Series) and isinstance(graph_y.iloc[0], pd.Period):
        graph_y = graph_y.astype(str)
    elif isinstance(graph_y, list) and isinstance(graph_y[0], pd.Period):
        graph_y = [str(y) for y in graph_y]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
                'valueformat':',.0f'
            },
            domain={'x': [0, 1], 'y': [0.99, 1]}
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                x=graph_x,
                y=graph_y,
                hovertemplate='<b>%{x}</b>' +
                            '<br>Nettó: %{y} Ft<extra></extra>',
                fill="tonexty",
                fillcolor=color_graph,
                mode='none'
            )
        )

    fig.update_xaxes(visible=True, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        margin=dict(t=20, b=0),
        showlegend=False,
        height=160,
    )
    st.plotly_chart(fig, use_container_width=True)

def sunburst(df, path):

    fig = px.sunburst(
        data_frame=df,
        path=path,
        values='netto',
        maxdepth=3,
        color_discrete_sequence= px.colors.qualitative.T10
    )
    
    fig.update_layout(
        margin=dict(t=20, l=10, r=10, b=10),
        height=600
    )

    fig.update_traces(
        hovertemplate='<b>%{label}</b>' + 
                    '<br>Netto: %{value: ,.0d} Ft<extra></extra>' +
                    '<br>Arány: %{percentRoot:.2%}%',
        rotation=90
    )
    
    st.plotly_chart(fig, use_container_width=True)

def comp_bar(inc_df, exp_df, emp_df, emp_type, i_years, e_years):
    
    fig1 = make_subplots(
        rows=1, cols=1,
        shared_yaxes=False
        )
    
    fig2 = make_subplots(
        rows=1, cols=1,
        shared_yaxes=False
        )
    
    # Define Hungarian month names
    hungarian_months = [
        "Január", "Február", "Március", "Április", "Május", "Június",
        "Július", "Augusztus", "Szeptember", "Október", "November", "December"
    ]
    hungarian_months_abbr = [month[:3] for month in hungarian_months]

    # Define Hungarian quarter names
    hungarian_quarters = ["I. negyedév", "II. negyedév", "III. negyedév", "IV. negyedév"]

    # Create functions to get Hungarian month and quarter names
    def get_hungarian_month_name(month_number):
        return hungarian_months[month_number - 1]

    def get_hungarian_quarter_name(quarter_number):
        return hungarian_quarters[quarter_number - 1]

    inc_emp_data = inc_df.groupby(['year', 'month', 'quarter' ,'month_year'])['netto'].sum().reset_index()
    exp_emp_data = exp_df.groupby(['year', 'month', 'quarter' ,'month_year'])['netto'].sum().reset_index()
    
    i_monthly_data = pd.merge(inc_emp_data, emp_df, on=['year', 'quarter' ,'month_year'], how='left')
    e_monthly_data = pd.merge(exp_emp_data, emp_df, on=['year', 'quarter' ,'month_year'], how='left')
    
    q_emp_df = emp_df.groupby(['year','quarter'])[['vam','penzugy','egyeb','osszes']].mean().round(1)
    
    q_inc_emp_data = inc_df.groupby(['year','quarter'])['netto'].sum().reset_index()
    q_exp_emp_data = exp_df.groupby(['year','quarter'])['netto'].sum().reset_index()
    
    i_quarterly_data = pd.merge(q_inc_emp_data, q_emp_df, on=['year', 'quarter'], how='left')
    e_quarterly_data = pd.merge(q_exp_emp_data, q_emp_df, on=['year', 'quarter'], how='left')
    
    if emp_type == 'Vám':
        divider_type = 'vam'
    elif emp_type == 'Pénzügy':
        divider_type = 'penzugy'
    elif emp_type == 'Egyéb':
        divider_type = 'egyeb'
    elif emp_type == 'Összes':
        divider_type = 'osszes'
        
    for year in i_years:
        year_cat_data = i_monthly_data[(i_monthly_data['year'] == year)]
        fig1.add_trace(
            go.Bar(
                x=year_cat_data['month'], 
                y=year_cat_data['netto'] / year_cat_data[divider_type], 
                name=f"{year} - Bevétel", 
                legendgroup=f"{year} - Bevétel",
                hovertemplate='<b>%{customdata[0]} - Bevétel</b><br>' +
                                '%{customdata[1]}<br>' +
                                'Netto: %{y:,.0f} Ft<extra></extra>',
                customdata=np.column_stack((
                    year_cat_data['year'],
                    year_cat_data['month'].apply(get_hungarian_month_name)
                ))
            ),
            row=1, col=1
        )
    
    for year in e_years:    
        year_cat_data = e_monthly_data[(e_monthly_data['year'] == year)]
        fig1.add_trace(
            go.Bar(
                x=year_cat_data['month'], 
                y=year_cat_data['netto'] / year_cat_data[divider_type], 
                name=f"{year} - Kiadás", 
                legendgroup=f"{year} - Kiadás",
                hovertemplate='<b>%{customdata[0]} - Kiadás</b><br>' +
                                '%{customdata[1]}<br>' +
                                'Netto: %{y:,.0f} Ft<extra></extra>',
                customdata=np.column_stack((
                    year_cat_data['year'],
                    year_cat_data['month'].apply(get_hungarian_month_name)
                ))
            ),
            row=1, col=1
        )  

    for year in i_years:
        year_cat_data = i_quarterly_data[(i_quarterly_data['year'] == year)]
        fig2.add_trace(
            go.Bar(
                x=year_cat_data['quarter'], 
                y=year_cat_data['netto'] / year_cat_data[divider_type], 
                name=f"{year} - Bevétel", 
                legendgroup=f"{year} - Bevétel",
                hovertemplate='<b>%{customdata[0]} %{x} - Bevétel</b><br>' +
                                '%{customdata[1]}<br>' +
                                'Netto: %{y:,.0f} Ft<extra></extra>',
                customdata=np.column_stack((
                    year_cat_data['year'],
                    year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                ))
            ),
            row=1, col=1
        )

    for year in e_years:
        year_cat_data = e_quarterly_data[(e_quarterly_data['year'] == year)]
        fig2.add_trace(
            go.Bar(
                x=year_cat_data['quarter'], 
                y=year_cat_data['netto'] / year_cat_data[divider_type], 
                name=f"{year} - Kiadás", 
                legendgroup=f"{year} - Kiadás",
                hovertemplate='<b>%{customdata[0]} %{x} - Kiadás</b><br>' +
                                '%{customdata[1]}<br>' +
                                'Netto: %{y:,.0f} Ft<extra></extra>',
                customdata=np.column_stack((
                    year_cat_data['year'],
                    year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                ))
            ),
            row=1, col=1
        )       

    # Update layout
    fig1.update_layout(title="Havi költség összehasonlítás", showlegend=True, height=500)
    fig2.update_layout(title="Negyedéves költség összehasonlítás", showlegend=True, height=500)

    # Update x-axis to show Hungarian month names
    fig1.update_xaxes(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = hungarian_months_abbr
    )

    # Update x-axis for quarterly chart
    fig2.update_xaxes(
        tickmode = 'array',
        tickvals = [1, 2, 3, 4],
        ticktext = ["Q1", "Q2", "Q3", "Q4"]
    )
    
    # --- TABLES ---
    
    # Function to format month-year
    def format_month_year(row):
        year = row['year']
        month = hungarian_months[row['month'] - 1]
        return f"{year} {month}"

    # Function to format quarter-year
    def format_quarter_year(row):
        year = row['year']
        quarter = row['quarter']
        return f"{year} Q{quarter}"

    # Income Monthly Table
    i_monthly_table = i_monthly_data[['year', 'month', 'month_year', 'netto', divider_type]]
    i_monthly_table['Arányos'] = i_monthly_data['netto'] / i_monthly_data[divider_type]
    i_monthly_table['netto'] = i_monthly_table['netto'].round(0)
    i_monthly_table['netto'] = i_monthly_table['netto'].apply(lambda x: f"{int(x):,} Ft")
    i_monthly_table[divider_type] = i_monthly_table[divider_type].apply(lambda x: f"{int(x)} fő")
    i_monthly_table['Arányos'] = i_monthly_table['Arányos'].round(0)
    i_monthly_table['Arányos'] = i_monthly_table['Arányos'].apply(lambda x: f"{int(x):,} Ft")
    i_monthly_table['Időszak'] = i_monthly_table.apply(format_month_year, axis=1)
    i_monthly_table = i_monthly_table.rename(columns={'netto': 'Nettó', divider_type: emp_type})
    i_monthly_table = i_monthly_table[['Időszak', 'Nettó', emp_type, 'Arányos']].set_index('Időszak')

    # Expense Monthly Table
    e_monthly_table = e_monthly_data[['year', 'month', 'month_year', 'netto', divider_type]]
    e_monthly_table['Arányos'] = e_monthly_data['netto'] / e_monthly_data[divider_type]
    e_monthly_table['netto'] = e_monthly_table['netto'].round(0)
    e_monthly_table['netto'] = e_monthly_table['netto'].apply(lambda x: f"{int(x):,} Ft")
    e_monthly_table[divider_type] = e_monthly_table[divider_type].apply(lambda x: f"{int(x)} fő")
    e_monthly_table['Arányos'] = e_monthly_table['Arányos'].round(0)
    e_monthly_table['Arányos'] = e_monthly_table['Arányos'].apply(lambda x: f"{int(x):,} Ft")
    e_monthly_table['Időszak'] = e_monthly_table.apply(format_month_year, axis=1)
    e_monthly_table = e_monthly_table.rename(columns={'netto': 'Nettó', divider_type: emp_type})
    e_monthly_table = e_monthly_table[['Időszak', 'Nettó', emp_type, 'Arányos']].set_index('Időszak')

    # Income Quarterly Table
    i_quarterly_table = i_quarterly_data[['year', 'quarter', 'netto', divider_type]]
    i_quarterly_table['Arányos'] = i_quarterly_data['netto'] / i_quarterly_data[divider_type]
    i_quarterly_table['netto'] = i_quarterly_table['netto'].round(0)
    i_quarterly_table['netto'] = i_quarterly_table['netto'].apply(lambda x: f"{int(x):,} Ft")
    i_quarterly_table[divider_type] = i_quarterly_table[divider_type].apply(lambda x: f"{x:.1f} fő")
    i_quarterly_table['Arányos'] = i_quarterly_table['Arányos'].round(0)
    i_quarterly_table['Arányos'] = i_quarterly_table['Arányos'].apply(lambda x: f"{int(x):,} Ft")
    i_quarterly_table['Időszak'] = i_quarterly_table.apply(format_quarter_year, axis=1)
    i_quarterly_table = i_quarterly_table.rename(columns={'netto': 'Nettó', divider_type: emp_type})
    i_quarterly_table = i_quarterly_table[['Időszak', 'Nettó', emp_type, 'Arányos']].set_index('Időszak')

    # Expense Quarterly Table
    e_quarterly_table = e_quarterly_data[['year', 'quarter', 'netto', divider_type]]
    e_quarterly_table['Arányos'] = e_quarterly_data['netto'] / e_quarterly_data[divider_type]
    e_quarterly_table['netto'] = e_quarterly_table['netto'].round(0)
    e_quarterly_table['netto'] = e_quarterly_table['netto'].apply(lambda x: f"{int(x):,} Ft")
    e_quarterly_table[divider_type] = e_quarterly_table[divider_type].apply(lambda x: f"{x:.1f} fő")
    e_quarterly_table['Arányos'] = e_quarterly_table['Arányos'].round(0)
    e_quarterly_table['Arányos'] = e_quarterly_table['Arányos'].apply(lambda x: f"{int(x):,} Ft")
    e_quarterly_table['Időszak'] = e_quarterly_table.apply(format_quarter_year, axis=1)
    e_quarterly_table = e_quarterly_table.rename(columns={'netto': 'Nettó', divider_type: emp_type})
    e_quarterly_table = e_quarterly_table[['Időszak', 'Nettó', emp_type, 'Arányos']].set_index('Időszak')

    # Display tables and charts in Streamlit

    st.plotly_chart(fig1)
    with st.expander("Havi adatok"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("Bevétel")
            st.table(i_monthly_table)
        with col2:
            st.write("Kiadás")
            st.table(e_monthly_table)

    st.plotly_chart(fig2)

    with st.expander("Negyedéves adatok"):
        col3, col4 = st.columns(2)
        with col3:
            st.write("Bevétel")
            st.table(i_quarterly_table)
        with col4:
            st.write("Kiadás")
            st.table(e_quarterly_table)

    
    
def multi_comparison(multi_comp_type, i_comp_df, i_comp_years, i_comp_cats, i_comp_subcats, i_comp_items, e_comp_df, e_comp_years, e_comp_cats, e_comp_subcats, e_comp_items):
    
    fig1 = make_subplots(
        rows=1, cols=1,
        shared_yaxes=False
        )
    
    fig2 = make_subplots(
        rows=1, cols=1,
        shared_yaxes=False
        )
    
    # Define Hungarian month names
    hungarian_months = [
        "Január", "Február", "Március", "Április", "Május", "Június",
        "Július", "Augusztus", "Szeptember", "Október", "November", "December"
    ]
    hungarian_months_abbr = [month[:3] for month in hungarian_months]

    # Define Hungarian quarter names
    hungarian_quarters = ["I. negyedév", "II. negyedév", "III. negyedév", "IV. negyedév"]

    # Create functions to get Hungarian month and quarter names
    def get_hungarian_month_name(month_number):
        return hungarian_months[month_number - 1]

    def get_hungarian_quarter_name(quarter_number):
        return hungarian_quarters[quarter_number - 1]

    if multi_comp_type == 'Kategória':
        
        i_monthly_data = i_comp_df.groupby(['year', 'month', 'kategoria'])['netto'].sum().reset_index()
        i_quarterly_data = i_comp_df.groupby(['year', 'quarter', 'kategoria'])['netto'].sum().reset_index()
        
        e_monthly_data = e_comp_df.groupby(['year', 'month', 'kategoria'])['netto'].sum().reset_index()
        e_quarterly_data = e_comp_df.groupby(['year', 'quarter', 'kategoria'])['netto'].sum().reset_index()
        
        for category in i_comp_cats:
            for year in i_comp_years:
                year_cat_data = i_monthly_data[(i_monthly_data['year'] == year) & (i_monthly_data['kategoria'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"B - {year} - {category}", 
                        legendgroup=f"B - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{customdata[2]}</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['kategoria'],
                            year_cat_data['month'].apply(get_hungarian_month_name)
                        ))
                    ),
                    row=1, col=1
                )
                
        for category in e_comp_cats:
            for year in e_comp_years:
                year_cat_data = e_monthly_data[(e_monthly_data['year'] == year) & (e_monthly_data['kategoria'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"K - {year} - {category}", 
                        legendgroup=f"K - {year} - {category}",
                        hovertemplate='Kiadás<br>' +
                                      '<b>%{customdata[0]} %{customdata[2]}</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['kategoria'],
                            year_cat_data['month'].apply(get_hungarian_month_name)
                        ))
                    ),
                    row=1, col=1
                )

        for category in i_comp_cats:
            for year in i_comp_years:
                year_cat_data = i_quarterly_data[(i_quarterly_data['year'] == year) & (i_quarterly_data['kategoria'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"B - {year} - {category}", 
                        legendgroup=f"B - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['kategoria'],
                            year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                        ))
                    ),
                    row=1, col=1
                )
                
        for category in e_comp_cats:
            for year in e_comp_years:
                year_cat_data = e_quarterly_data[(e_quarterly_data['year'] == year) & (e_quarterly_data['kategoria'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"K - {year} - {category}", 
                        legendgroup=f"K - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['kategoria'],
                            year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                        ))
                    ),
                    row=1, col=1
                )              
        
    elif multi_comp_type == 'Alkategória':
         
        i_monthly_data = i_comp_df.groupby(['year', 'month', 'alkategoria'])['netto'].sum().reset_index()
        i_quarterly_data = i_comp_df.groupby(['year', 'quarter', 'alkategoria'])['netto'].sum().reset_index()
        
        e_monthly_data = e_comp_df.groupby(['year', 'month', 'alkategoria'])['netto'].sum().reset_index()
        e_quarterly_data = e_comp_df.groupby(['year', 'quarter', 'alkategoria'])['netto'].sum().reset_index()
        
        for category in i_comp_cats:
            for year in i_comp_years:
                year_cat_data = i_monthly_data[(i_monthly_data['year'] == year) & (i_monthly_data['alkategoria'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"B - {year} - {category}", 
                        legendgroup=f"B - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{customdata[2]}</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['alkategoria'],
                            year_cat_data['month'].apply(get_hungarian_month_name)
                        ))
                    ),
                    row=1, col=1
                )
                
        for category in e_comp_cats:
            for year in e_comp_years:
                year_cat_data = e_monthly_data[(e_monthly_data['year'] == year) & (e_monthly_data['alkategoria'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"K - {year} - {category}", 
                        legendgroup=f"K - {year} - {category}",
                        hovertemplate='Kiadás<br>' +
                                      '<b>%{customdata[0]} %{customdata[2]}</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['alkategoria'],
                            year_cat_data['month'].apply(get_hungarian_month_name)
                        ))
                    ),
                    row=1, col=1
                )

        for category in i_comp_cats:
            for year in i_comp_years:
                year_cat_data = i_quarterly_data[(i_quarterly_data['year'] == year) & (i_quarterly_data['alkategoria'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"B - {year} - {category}", 
                        legendgroup=f"B - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['alkategoria'],
                            year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                        ))
                    ),
                    row=1, col=1
                )
                
        for category in e_comp_cats:
            for year in e_comp_years:
                year_cat_data = e_quarterly_data[(e_quarterly_data['year'] == year) & (e_quarterly_data['alkategoria'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"K - {year} - {category}", 
                        legendgroup=f"K - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['alkategoria'],
                            year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                        ))
                    ),
                    row=1, col=1
                )              
    elif multi_comp_type == 'Elem':
        
        i_monthly_data = i_comp_df.groupby(['year', 'month', 'elem'])['netto'].sum().reset_index()
        i_quarterly_data = i_comp_df.groupby(['year', 'quarter', 'elem'])['netto'].sum().reset_index()
        
        e_monthly_data = e_comp_df.groupby(['year', 'month', 'elem'])['netto'].sum().reset_index()
        e_quarterly_data = e_comp_df.groupby(['year', 'quarter', 'elem'])['netto'].sum().reset_index()
        
        for category in i_comp_cats:
            for year in i_comp_years:
                year_cat_data = i_monthly_data[(i_monthly_data['year'] == year) & (i_monthly_data['elem'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"B - {year} - {category}", 
                        legendgroup=f"B - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{customdata[2]}</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['elem'],
                            year_cat_data['month'].apply(get_hungarian_month_name)
                        ))
                    ),
                    row=1, col=1
                )
                
        for category in e_comp_cats:
            for year in e_comp_years:
                year_cat_data = e_monthly_data[(e_monthly_data['year'] == year) & (e_monthly_data['elem'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"K - {year} - {category}", 
                        legendgroup=f"K - {year} - {category}",
                        hovertemplate='Kiadás<br>' +
                                      '<b>%{customdata[0]} %{customdata[2]}</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['elem'],
                            year_cat_data['month'].apply(get_hungarian_month_name)
                        ))
                    ),
                    row=1, col=1
                )

        for category in i_comp_cats:
            for year in i_comp_years:
                year_cat_data = i_quarterly_data[(i_quarterly_data['year'] == year) & (i_quarterly_data['elem'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"B - {year} - {category}", 
                        legendgroup=f"B - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['elem'],
                            year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                        ))
                    ),
                    row=1, col=1
                )
                
        for category in e_comp_cats:
            for year in e_comp_years:
                year_cat_data = e_quarterly_data[(e_quarterly_data['year'] == year) & (e_quarterly_data['elem'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"K - {year} - {category}", 
                        legendgroup=f"K - {year} - {category}",
                        hovertemplate='Bevétel<br>' +
                                      '<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
                                      '%{customdata[1]}<br>' +
                                      'Netto: %{y:,.0f} Ft<extra></extra>',
                        customdata=np.column_stack((
                            year_cat_data['year'], 
                            year_cat_data['elem'],
                            year_cat_data['quarter'].apply(get_hungarian_quarter_name)
                        ))
                    ),
                    row=1, col=1
                )              

    # Update layout
    fig1.update_layout(title="Havi költség összehasonlítás", showlegend=True, height=500)
    fig2.update_layout(title="Negyedéves költség összehasonlítás", showlegend=True, height=500)

    # Update x-axis to show Hungarian month names
    fig1.update_xaxes(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = hungarian_months_abbr
    )

    # Update x-axis for quarterly chart
    fig2.update_xaxes(
        tickmode = 'array',
        tickvals = [1, 2, 3, 4],
        ticktext = ["Q1", "Q2", "Q3", "Q4"]
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

def table_formating():
    st.markdown(
                    """
                    <style>
                    table {
                        width: 100%;
                    }
                    th, td {
                        text-align: right !important;
                    }
                    th:first-child, td:first-child {
                        text-align: left !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

# --- PAGE ---

st.title('Összehasonlítás')
st.divider()

# --- SESSION VARIABLES ---

if 'df_income' and 'df_expense' not in st.session_state:
    st.subheader('Nincs feltöltve vizsgálandó adat.')
    st.write('')
    st.write('Az adatok feltöltéséhez kattintson az alábbi gonbra:')
    st.write('')
    st.page_link('pages/Adatfeltöltés.py', label=' Adatfeltöltés', icon='📝')
else:
    df_income = st.session_state['df_income']
    df_expense = st.session_state['df_expense']
    
# --- FILTERING ---

    fcol1, fcol2 = st.columns((1,1))

# --- INCOME ---

    with fcol1.expander('Bevétel keresés és szűrés'):
        yfcol1, yfcol2, yfcol3 = st.columns((1,1,1), gap='medium')
        cfcol1, cfcol2 = st.columns((1,1), gap='medium')
        cfcol3, cfcol4 = st.columns((1,1), gap='medium')
        cfcol5, cfcol6 = st.columns((3,1), gap='medium')
    
    # --- TIME FILTERS ---

    quarter_mapping = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
    months_in_quarter = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]}
    month_names = { 1: 'Január', 2: 'Február', 3: 'Március', 4: 'Április', 5: 'Május', 6: 'Június', 7: 'Július', 8: 'Augusztus', 9: 'Szeptember', 10: 'Október', 11: 'November', 12: 'December'}
    
    i_year = sorted(df_income['year'].unique())
    i_years = yfcol1.multiselect('Bevétel tárgyév', options=i_year, placeholder='Válassz évet',)
    if len(i_years) == 0:
        i_years = sorted(df_income['year'].unique())

    i_quarters = yfcol2.multiselect('Bevétel negyedév', options=quarter_mapping, placeholder='Válassz negyedévet')
    i_selected_quarters = [quarter_mapping[q] for q in i_quarters]
    if len(i_selected_quarters) == 0:
        i_selected_quarters = sorted(df_income['quarter'].unique())
    
    i_available_months = set()
    for q in i_selected_quarters:
        i_available_months.update(months_in_quarter[q])
        
    i_available_month_names = [month_names[m] for m in i_available_months]
    
    i_months = yfcol3.multiselect('Bevétel hónap', options=i_available_month_names, placeholder='Válassz hónapot')
    i_selected_months = [k for k, v in month_names.items() if v in i_months]
    if len(i_selected_months) == 0:
        i_selected_months = sorted(df_income['month'].unique())

    # --- CATEGORY FILTERS ---

    i_kategoria = sorted(df_income['kategoria'].unique())
    i_kategoriak = cfcol1.multiselect('Bevétel kategória', options=i_kategoria, placeholder='Válassz kategóriát')
    if len(i_kategoriak) == 0:
        i_kategoriak = sorted(df_income['kategoria'].unique())

    i_alkategoria = sorted(df_income.loc[df_income['kategoria'].isin(i_kategoriak), 'alkategoria'].unique())
    i_alkategoriak = cfcol2.multiselect('Bevétel alkategória', options=i_alkategoria, placeholder='Válassz alkategóriát')
    if len(i_alkategoriak) == 0:
        i_alkategoriak = sorted(df_income['alkategoria'].unique())
        
    i_elem = sorted(df_income.loc[df_income['alkategoria'].isin(i_alkategoriak), 'elem'].unique())
    i_elemek = cfcol3.multiselect('Bevétel kategória elem', options=i_elem, placeholder='Válassz kategória elemet')
    if len(i_elemek) == 0:
        i_elemek = sorted(df_income['elem'].unique())
    
    i_kat_kod = sorted(df_income['kat_kod'].unique())
    i_kat_kodok = cfcol4.multiselect('Bevétel kategória kód', options=i_kat_kod, placeholder='Válassz kategória kódot')
    if len(i_kat_kodok) == 0:
        i_kat_kodok = sorted(df_income['kat_kod'].unique())

    i_partner = sorted(df_income['partner'].unique())
    i_partnerek = cfcol5.multiselect('Bevétel partner', options=i_partner, placeholder='Válassz partnert')
    if len(i_partnerek) == 0:
        i_partnerek = sorted(df_income['partner'].unique())

    i_in_or_not = cfcol6.selectbox('Bevétel szűrés típusa', options=['Tartalmazza','Kivéve'], help='Kivéve esetén ha nincs megadott feltétel, akkor nem jelenik meg adat! Először adja meg a kivételt, utána álltsa a mezőt Kivéve értékre!')
    
    if i_in_or_not == 'Tartalmazza':
        selected_income_df = df_income[
            (df_income['year'].isin(i_years)) &
            (df_income['quarter'].isin(i_selected_quarters)) &
            (df_income['month'].isin(i_selected_months)) &
            (df_income['kat_kod'].isin(i_kat_kodok)) &
            (df_income['kategoria'].isin(i_kategoriak)) &
            (df_income['alkategoria'].isin(i_alkategoriak)) &
            (df_income['elem'].isin(i_elemek)) &
            (df_income['partner'].isin(i_partnerek))]
    elif i_in_or_not == 'Kivéve':
       selected_income_df = df_income[
            (~df_income['year'].isin(i_years)) |
            (~df_income['quarter'].isin(i_selected_quarters)) |
            (~df_income['month'].isin(i_selected_months)) |
            (~df_income['kat_kod'].isin(i_kat_kodok)) |
            (~df_income['kategoria'].isin(i_kategoriak)) |
            (~df_income['alkategoria'].isin(i_alkategoriak)) |
            (~df_income['elem'].isin(i_elemek)) |
            (~df_income['partner'].isin(i_partnerek))] 

    if selected_income_df.empty:
        st.divider()
        st.error('A kiválasztott szűrési feltételeknek megfelelő adat nem létezik, ellenőrizze a beállított szűrési feltételeket! Kizáró szűrés esetén először meg kell adni a kizárt feltételt!')
    else:
        selected_income_df['percentage'] = (selected_income_df['netto'] / selected_income_df['netto'].sum()) * 100
        
# --- EXPENSE ---
    
    # --- FILTERING ---
    with fcol2.expander('Kiadás keresés és szűrés'):
        yfcol1, yfcol2, yfcol3 = st.columns((1,1,1), gap='medium')
        cfcol1, cfcol2 = st.columns((1,1), gap='medium')
        cfcol3, cfcol4, cfcol5 = st.columns((1,1,1), gap='medium')
        pfcol1, pfcol2, = st.columns((3,1))
    
    # --- TIME FILTERS ---
    
    e_year = sorted(df_expense['year'].unique())
    e_years = yfcol1.multiselect('Kiadás tárgyév', options=e_year, placeholder='Válassz évet',)
    if len(e_years) == 0:
        e_years = sorted(df_expense['year'].unique())

    e_quarters = yfcol2.multiselect('Kiadás negyedév', options=quarter_mapping, placeholder='Válassz negyedévet')
    e_selected_quarters = [quarter_mapping[q] for q in e_quarters]
    if len(e_selected_quarters) == 0:
        e_selected_quarters = sorted(df_expense['quarter'].unique())
    
    e_available_months = set()
    for q in e_selected_quarters:
        e_available_months.update(months_in_quarter[q])
        
    e_available_month_names = [month_names[m] for m in e_available_months]
    
    e_months = yfcol3.multiselect('Kiadás hónap', options=e_available_month_names, placeholder='Válassz hónapot')
    e_selected_months = [k for k, v in month_names.items() if v in e_months]
    if len(e_selected_months) == 0:
        e_selected_months = sorted(df_expense['month'].unique())

# --- CATEGORY FILTERS ---

    e_kategoria = sorted(df_expense['kategoria'].unique())
    e_kategoriak = cfcol1.multiselect('Kiadás kategória', options=e_kategoria, placeholder='Válassz kategóriát')
    if len(e_kategoriak) == 0:
        e_kategoriak = sorted(df_expense['kategoria'].unique())

    e_alkategoria = sorted(df_expense.loc[df_expense['kategoria'].isin(e_kategoriak), 'alkategoria'].unique())
    e_alkategoriak = cfcol2.multiselect('Kiadás alkategória', options=e_alkategoria, placeholder='Válassz alkategóriát')
    if len(e_alkategoriak) == 0:
        e_alkategoriak = sorted(df_expense['alkategoria'].unique())
        
    e_elem = sorted(df_expense.loc[df_expense['alkategoria'].isin(e_alkategoriak), 'elem'].unique())
    e_elemek = cfcol4.multiselect('Kiadás kategória elem', options=e_elem, placeholder='Válassz kategória elemet')
    if len(e_elemek) == 0:
        e_elemek = sorted(df_expense['elem'].unique())

    e_fo_kat = sorted(df_expense['fo_kat'].unique())
    e_fo_katok = cfcol3.multiselect('Kiadás fő kategória', options=e_fo_kat, placeholder='Válassz fő kategóriát', help='A 0. kategória a nem besorolt!')
    if len(e_fo_katok) == 0:
        e_fo_katok = sorted(df_expense['fo_kat'].unique())
    
    e_kat_kod = sorted(df_expense['kat_kod'].unique())
    e_kat_kodok = cfcol5.multiselect('Kiadás kategória kód', options=e_kat_kod, placeholder='Válassz kategória kódot')
    if len(e_kat_kodok) == 0:
        e_kat_kodok = sorted(df_expense['kat_kod'].unique())

    e_partner = sorted(df_expense['partner'].unique())
    e_partnerek = pfcol1.multiselect('Kiadás partner', options=e_partner, placeholder='Válassz partnert')
    if len(e_partnerek) == 0:
        e_partnerek = sorted(df_expense['partner'].unique())

    e_in_or_not = pfcol2.selectbox('Kiadás szűrés típusa', options=['Tartalmazza','Kivéve'], help='Kivéve esetén ha nincs megadott feltétel, akkor nem jelenik meg adat! Először adja meg a kivételt, utána álltsa a mezőt Kivéve értékre!')
    
    if e_in_or_not == 'Tartalmazza':
        selected_expense_df = df_expense[
            (df_expense['year'].isin(e_years)) &
            (df_expense['quarter'].isin(e_selected_quarters)) &
            (df_expense['month'].isin(e_selected_months)) &
            (df_expense['fo_kat'].isin(e_fo_katok)) &
            (df_expense['kat_kod'].isin(e_kat_kodok)) &
            (df_expense['kategoria'].isin(e_kategoriak)) &
            (df_expense['alkategoria'].isin(e_alkategoriak)) &
            (df_expense['elem'].isin(e_elemek)) &
            (df_expense['partner'].isin(e_partnerek))]
    elif e_in_or_not == 'Kivéve':
       selected_expense_df = df_expense[
            (~df_expense['year'].isin(e_years)) |
            (~df_expense['quarter'].isin(e_selected_quarters)) |
            (~df_expense['month'].isin(e_selected_months)) |
            (~df_expense['fo_kat'].isin(e_fo_katok)) |
            (~df_expense['kat_kod'].isin(e_kat_kodok)) |
            (~df_expense['kategoria'].isin(e_kategoriak)) |
            (~df_expense['alkategoria'].isin(e_alkategoriak)) |
            (~df_expense['elem'].isin(e_elemek)) |
            (~df_expense['partner'].isin(e_partnerek))] 

    if selected_expense_df.empty:
        st.divider()
        st.error('A kiválasztott szűrési feltételeknek megfelelő adat nem létezik, ellenőrizze a beállított szűrési feltételeket! Kizáró szűrés esetén először meg kell adni a kizárt feltételt!')
    else:
        selected_expense_df['percentage'] = (selected_expense_df['netto'] / selected_expense_df['netto'].sum()) * 100
      
# --- TABS ---
        
    tabs = st.tabs(['Összesítő adatok','Napsugár diagram','Összehasonlítás','Vizsgált adatok'])
    
    ### Osszesito adatok
        
    with tabs[0]:
        
        sumcol1, sumcol2 = st.columns((1,1), gap='large')
        st.write('')
    
        # --- TOTAL INCOME ---

        with sumcol1:
            
            total_df = selected_income_df.groupby(['month_year'], as_index=False)['netto'].sum().round(0)
            total_expense = selected_income_df['netto'].sum().round(0)
            
            st.subheader('Teljes bevétel', divider='grey')
            total_netto(
                label='Teljes kiadás',
                value=total_expense,
                suffix=' Ft',
                show_graph=True,
                graph_x=total_df['month_year'],
                graph_y=total_df['netto'],
                color_graph=graph_color
            )
        
        # --- TOTAL EXPENSE ---
            
        with sumcol2:
            
            total_df = selected_expense_df.groupby(['month_year'], as_index=False)['netto'].sum().round(0)
            total_income = selected_expense_df['netto'].sum().round(0)
            
            st.subheader('Teljes kiadás', divider='grey')
            total_netto(
                label='Teljes kiadás',
                value=total_income,
                suffix=' Ft',
                show_graph=True,
                graph_x=total_df['month_year'],
                graph_y=total_df['netto'],
                color_graph=graph_color
            )
        
        # --- EMPLOYEE COMP ---
        
        st.subheader('Költségek munkavállalóra vetítve', divider='grey')
        
        if 'df_employees' not in st.session_state:
            st.subheader('Nincs feltöltve munkavállalói adat.')
            st.write('')
            st.write('Az adatok feltöltéséhez kattintson az alábbi gonbra:')
            st.write('')
            st.page_link('pages/Adatfeltöltés.py', label=' Adatfeltöltés', icon='📝')
        else:
            df_employees = st.session_state['df_employees']
            emp_type = st.selectbox('Viszonyítási csoport', options=['Vám','Pénzügy','Egyéb','Összes'])
            
            comp_bar(
                inc_df=selected_income_df,
                exp_df=selected_expense_df,
                emp_df=df_employees,
                emp_type=emp_type,
                i_years=i_years,
                e_years=e_years
                )
            
            table_formating()
        
        ### SUNBURST COMPARIONS
        
        with tabs[1]:

            suncomp1, suncomp2 , suncomp3= st.columns((4,1,4))
             
            sun_type = suncomp2.selectbox('Összehasonlítás', options=['Partner','Kategória','Alkategória','Elem'], help='Alkategória és elem összehasonlításnál érdemes az adatokat előre szűrni, hogy könnyebben áttekinthető legyen a változás!')
                    
            with suncomp1:
                sun_year1 = st.selectbox('Bevételi év', options=i_year, placeholder='Válassz évet')
                df_sun_year1 = selected_income_df[selected_income_df['year'] == sun_year1]
                
                if sun_type == 'Partner':
                    path = ['partner']
                    
                if sun_type == 'Kategória':
                    path = ['kategoria']
                    
                if sun_type == 'Alkategória':
                    path = ['alkategoria']
                    
                if sun_type == 'Elem':
                    path = ['elem']

                sunburst(df_sun_year1, path)                    
                
            with suncomp3:
                sun_year2 = st.selectbox('Kiadási év', options=e_year, placeholder='Válassz évet')
                df_sun_year2 = selected_expense_df[selected_expense_df['year'] == sun_year2]

                if sun_type == 'Partner':
                    path = ['partner']
                    
                if sun_type == 'Kategória':
                    path = ['kategoria']
                    
                if sun_type == 'Alkategória':
                    path = ['alkategoria']
                    
                if sun_type == 'Elem':
                    path = ['elem']

                sunburst(df_sun_year2, path)
            
        with tabs[2]:
            
            st.write('')
            
            comphead1, comphead2 = st.columns((3,1))
            
            with comphead1.container(border=True):
                
                st.write('❗ Az összhasonlítás a fent beállított szűrésektől független! A összehasonlítási szinttől függően jelennek meg a válaszható szűrési lehetőségek!')
            
            multi_comp_type = comphead2.selectbox('Összehasonlítási szint', options=['Kategória','Alkategória','Elem'])
            
            i_comp_years = sorted(selected_income_df['year'].unique())
            i_comp_cats = sorted(selected_income_df['kategoria'].unique())
            i_comp_subcats = sorted(selected_income_df['alkategoria'].unique())
            i_comp_items = sorted(selected_income_df['elem'].unique())
            
            e_comp_years = sorted(selected_expense_df['year'].unique())
            e_comp_cats = sorted(selected_expense_df['kategoria'].unique())
            e_comp_subcats = sorted(selected_expense_df['alkategoria'].unique())
            e_comp_items = sorted(selected_expense_df['elem'].unique())
            
            if multi_comp_type == 'Kategória':
                
                subcomp1, subcomp2 = st.columns((1,2))
                
                i_comp_year = sorted(selected_income_df['year'].unique())
                i_comp_years = subcomp1.multiselect('Bevétel évek', options=i_comp_year, placeholder='Válassz évet')
                if len(i_comp_years) == 0:
                    i_comp_years = sorted(selected_income_df['year'].unique())

                i_comp_cat = sorted(selected_income_df['kategoria'].unique())
                i_comp_cats = subcomp2.multiselect('Bevétel kategóriák', options=i_comp_cat, placeholder='Válassz kategóriát')
                if len(i_comp_cats) == 0:
                    i_comp_cats = sorted(selected_income_df['kategoria'].unique())

                i_comp_df = selected_income_df[
                    (selected_income_df['year'].isin(i_comp_years)) &
                    (selected_income_df['kategoria'].isin(i_comp_cats))
                    ]
                
                e_comp_year = sorted(selected_expense_df['year'].unique())
                e_comp_years = subcomp1.multiselect('Kiadás évek', options=e_comp_year, placeholder='Válassz évet')
                if len(e_comp_years) == 0:
                    e_comp_years = sorted(selected_expense_df['year'].unique())

                e_comp_cat = sorted(selected_expense_df['kategoria'].unique())
                e_comp_cats = subcomp2.multiselect('Kiadás kategóriák', options=e_comp_cat, placeholder='Válassz kategóriát')
                if len(e_comp_cats) == 0:
                    e_comp_cats = sorted(selected_expense_df['kategoria'].unique())

                e_comp_df = selected_expense_df[
                    (selected_expense_df['year'].isin(e_comp_years)) &
                    (selected_expense_df['kategoria'].isin(e_comp_cats))
                    ]
     
            elif multi_comp_type == 'Alkategória':
                
                subcomp1, subcomp2, subcomp3 = st.columns((1,2,2))
                
                with subcomp1:
                    i_comp_year = sorted(selected_income_df['year'].unique())
                    i_comp_years = st.multiselect('Bevétel évek', options=i_comp_year, placeholder='Válassz évet')
                    if len(i_comp_years) == 0:
                        i_comp_years = sorted(selected_income_df['year'].unique())
                        
                    e_comp_year = sorted(selected_expense_df['year'].unique())
                    e_comp_years = st.multiselect('Kiadás évek', options=e_comp_year, placeholder='Válassz évet')
                    if len(e_comp_years) == 0:
                        e_comp_years = sorted(selected_expense_df['year'].unique())
                
                with subcomp2:
                    
                    i_comp_cat = sorted(selected_income_df['kategoria'].unique())
                    i_comp_cats = st.multiselect('Bevétel kategóriák', options=i_comp_cat, placeholder='Válassz kategóriát')
                    if len(i_comp_cats) == 0:
                        i_comp_cats = sorted(selected_income_df['kategoria'].unique())
                        
                    e_comp_cat = sorted(selected_expense_df['kategoria'].unique())
                    e_comp_cats = st.multiselect('Kiadás kategóriák', options=e_comp_cat, placeholder='Válassz kategóriát')
                    if len(e_comp_cats) == 0:
                        e_comp_cats = sorted(selected_expense_df['kategoria'].unique())
                
                with subcomp3:
                 
                    i_comp_subcat = sorted(selected_income_df.loc[selected_income_df['kategoria'].isin(i_comp_cats), 'alkategoria'].unique())
                    i_comp_subcats = st.multiselect('Bevétel alkategóriák', options=i_comp_subcat, placeholder='Válassz alkategóriát')
                    if len(i_comp_subcats) == 0:
                        i_comp_subcats = sorted(selected_income_df['alkategoria'].unique())
                        
                    e_comp_subcat = sorted(selected_expense_df.loc[selected_expense_df['kategoria'].isin(e_comp_cats), 'alkategoria'].unique())
                    e_comp_subcats = st.multiselect('Kiadás alkategóriák', options=e_comp_subcat, placeholder='Válassz alkategóriát')
                    if len(e_comp_subcats) == 0:
                        e_comp_subcats = sorted(selected_expense_df['alkategoria'].unique())

                i_comp_df = selected_income_df[
                    (selected_income_df['year'].isin(i_comp_years)) &
                    (selected_income_df['kategoria'].isin(i_comp_cats)) &
                    (selected_income_df['alkategoria'].isin(i_comp_subcats))
                    ]

                e_comp_df = selected_expense_df[
                    (selected_expense_df['year'].isin(e_comp_years)) &
                    (selected_expense_df['kategoria'].isin(e_comp_cats)) &
                    (selected_expense_df['alkategoria'].isin(e_comp_subcats))
                    ]

            elif multi_comp_type == 'Elem':
                
                subcomp1, subcomp2, subcomp3, subcomp4 = st.columns((1,2,2,2))
                
                with subcomp1:
                    i_comp_year = sorted(selected_income_df['year'].unique())
                    i_comp_years = st.multiselect('Bevétel évek', options=i_comp_year, placeholder='Válassz évet')
                    if len(i_comp_years) == 0:
                        i_comp_years = sorted(selected_income_df['year'].unique())
                        
                    e_comp_year = sorted(selected_expense_df['year'].unique())
                    e_comp_years = st.multiselect('Kiadás évek', options=e_comp_year, placeholder='Válassz évet')
                    if len(e_comp_years) == 0:
                        e_comp_years = sorted(selected_expense_df['year'].unique())
                
                with subcomp2:                  
                    i_comp_cat = sorted(selected_income_df['kategoria'].unique())
                    i_comp_cats = st.multiselect('Bevétel kategóriák', options=i_comp_cat, placeholder='Válassz kategóriát')
                    if len(i_comp_cats) == 0:
                        i_comp_cats = sorted(selected_income_df['kategoria'].unique())
                        
                    e_comp_cat = sorted(selected_expense_df['kategoria'].unique())
                    e_comp_cats = st.multiselect('Kiadás kategóriák', options=e_comp_cat, placeholder='Válassz kategóriát')
                    if len(e_comp_cats) == 0:
                        e_comp_cats = sorted(selected_expense_df['kategoria'].unique())
                
                with subcomp3:
                 
                    i_comp_subcat = sorted(selected_income_df.loc[selected_income_df['kategoria'].isin(i_comp_cats), 'alkategoria'].unique())
                    i_comp_subcats = st.multiselect('Bevétel alkategóriák', options=i_comp_subcat, placeholder='Válassz alkategóriát')
                    if len(i_comp_subcats) == 0:
                        i_comp_subcats = sorted(selected_income_df['alkategoria'].unique())
                        
                    e_comp_subcat = sorted(selected_expense_df.loc[selected_expense_df['kategoria'].isin(e_comp_cats), 'alkategoria'].unique())
                    e_comp_subcats = st.multiselect('Kiadás alkategóriák', options=e_comp_subcat, placeholder='Válassz alkategóriát')
                    if len(e_comp_subcats) == 0:
                        e_comp_subcats = sorted(selected_expense_df['alkategoria'].unique())

                with subcomp4:
                
                    i_comp_item = sorted(selected_income_df.loc[selected_income_df['alkategoria'].isin(i_comp_subcats), 'elem'].unique())
                    i_comp_items = st.multiselect('Bevétel elemek', options=i_comp_item, placeholder='Válassz elemet')
                    if len(i_comp_items) == 0:
                        i_comp_items = sorted(selected_income_df['elem'].unique())
                        
                    e_comp_item = sorted(selected_expense_df.loc[selected_expense_df['alkategoria'].isin(e_comp_subcats), 'elem'].unique())
                    e_comp_items = st.multiselect('Kiadás elemek', options=e_comp_item, placeholder='Válassz elemet')
                    if len(e_comp_items) == 0:
                        comp_items = sorted(selected_expense_df['elem'].unique())                
                
                i_comp_df = selected_income_df[
                    (selected_income_df['year'].isin(i_comp_years)) &
                    (selected_income_df['kategoria'].isin(i_comp_cats)) &
                    (selected_income_df['alkategoria'].isin(i_comp_subcats)) &
                    (selected_income_df['elem'].isin(i_comp_items))
                    ]

                e_comp_df = selected_expense_df[
                    (selected_expense_df['year'].isin(e_comp_years)) &
                    (selected_expense_df['kategoria'].isin(e_comp_cats)) &
                    (selected_expense_df['alkategoria'].isin(e_comp_subcats)) &
                    (selected_expense_df['elem'].isin(e_comp_items))
                    ]                       
   
            multi_comparison(multi_comp_type, i_comp_df, i_comp_years, i_comp_cats, i_comp_subcats, i_comp_items, e_comp_df, e_comp_years, e_comp_cats, e_comp_subcats, e_comp_items)
            
        with tabs[3]:
            st.subheader('Bevételi adatok')
            st.write(selected_income_df)
            
            st.write('')
            
            st.subheader('Kiadási adatok')
            st.write(selected_expense_df)