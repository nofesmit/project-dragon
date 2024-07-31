import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import calendar
import locale

# --- CONFIG ---

st.set_page_config(page_title="Bevételek", layout="wide", page_icon='dragon')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

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

def total_count(label, value, prefix="", suffix="", show_graph=False, graph_x="", graph_y="", color_graph=""):
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
                            '<br>%{y} db<extra></extra>',
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

def plot_top10(df, x_data: str, y_data: str, marker_color: str, x_axis_title: str = '', y_axis_title: str = ''):
    fig = px.bar(
        data_frame=df,
        x=x_data,
        y=y_data,
        text_auto='.2s',
        orientation='h'
    )
    
    fig.update_traces(
        marker_color=marker_color,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>%{x:,.0f} Ft<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(t=20, l=10, r=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def detailed_bar(df, x_data:str, y_data:str, color:str, x_axis_title: str = '', y_axis_title: str = ''):
    fig = px.bar(
        data_frame=df,
        x=x_data,
        y=y_data,
        color=color,
        text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.T10
    )
    
    fig.update_traces(
        textangle=0, 
        textposition="outside", 
        cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>%{fullData.name}<br>%{x:,.0f} Ft<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        yaxis={'categoryorder':'total ascending'},
        margin=dict(t=20, l=10, r=10, b=10),
        height=600
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

def plot_treemap(df):
    
    fig = px.treemap(
        df,
        path=['kategoria', 'alkategoria', 'elem'],
        values='netto',
        hover_data={'kat_kod':True},
        color_discrete_sequence=px.colors.qualitative.T10
    )

    fig.update_layout(
        #title='Treemap of Kategoria, Alkategoria, and Elem',
        margin=dict(t=20, l=10, r=10, b=10),
        height=500
    )

    fig.update_traces(
        hovertemplate='<b>%{label}</b>' + 
                    '<br>Netto: %{value: ,.0d} Ft<extra></extra>' +
                    '<br>Kategória kód: %{customdata[0]}',
    )

    st.plotly_chart(fig, use_container_width=True)
    
def comparison(df, type, years, comp_cats, comp_subcats, comp_items):
    
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

    if type == 'Kategória':
        monthly_data = df.groupby(['year', 'month', 'kategoria'])['netto'].sum().reset_index()
        quarterly_data = df.groupby(['year', 'quarter', 'kategoria'])['netto'].sum().reset_index()
        
        for category in comp_cats:
            for year in years:
                year_cat_data = monthly_data[(monthly_data['year'] == year) & (monthly_data['kategoria'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"{year} - {category}", 
                        legendgroup=f"{year} - {category}",
                        hovertemplate='<b>%{customdata[0]} %{customdata[2]}</b><br>' +
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

        for category in comp_cats:
            for year in years:
                year_cat_data = quarterly_data[(quarterly_data['year'] == year) & (quarterly_data['kategoria'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"{year} - {category}", 
                        legendgroup=f"{year} - {category}",
                        hovertemplate='<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
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
        
    elif type == 'Alkategória':
        
        monthly_data = df.groupby(['year', 'month', 'alkategoria'])['netto'].sum().reset_index()
        quarterly_data = df.groupby(['year', 'quarter', 'alkategoria'])['netto'].sum().reset_index()
        
        for category in comp_subcats:
            for year in years:
                year_cat_data = monthly_data[(monthly_data['year'] == year) & (monthly_data['alkategoria'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"{year} - {category}", 
                        legendgroup=f"{year} - {category}",
                        hovertemplate='<b>%{customdata[0]} %{customdata[2]}</b><br>' +
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

        for category in comp_subcats:
            for year in years:
                year_cat_data = quarterly_data[(quarterly_data['year'] == year) & (quarterly_data['alkategoria'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"{year} - {category}", 
                        legendgroup=f"{year} - {category}",
                        hovertemplate='<b>%{customdata[0]} %{x} (%{customdata[2]})</b><br>' +
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

    elif type == 'Elem':
        
        monthly_data = df.groupby(['year', 'month', 'elem'])['netto'].sum().reset_index()
        quarterly_data = df.groupby(['year', 'quarter', 'elem'])['netto'].sum().reset_index()
        
        for category in comp_items:
            for year in years:
                year_cat_data = monthly_data[(monthly_data['year'] == year) & (monthly_data['elem'] == category)]
                fig1.add_trace(
                    go.Bar(
                        x=year_cat_data['month'], 
                        y=year_cat_data['netto'], 
                        name=f"{year} - {category}", 
                        legendgroup=f"{year} - {category}",
                        hovertemplate='<b>%{customdata[0]} %{customdata[2]}</b><br>' +
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

        for category in comp_items:
            for year in years:
                year_cat_data = quarterly_data[(quarterly_data['year'] == year) & (quarterly_data['elem'] == category)]
                fig2.add_trace(
                    go.Bar(
                        x=year_cat_data['quarter'], 
                        y=year_cat_data['netto'], 
                        name=f"{year} - {category}", 
                        legendgroup=f"{year} - {category}",
                        hovertemplate='<b>%{customdata[0]} Q%{x} (%{customdata[2]})</b><br>' +
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

st.title('Bevételek')
st.divider()

# --- SESSION VARIABLES ---

if 'df_income' not in st.session_state:
    st.subheader('Nincs feltöltve vizsgálandó adat.')
    st.write('')
    st.write('Az adatok feltöltéséhez kattintson az alábbi gonbra:')
    st.write('')
    st.page_link('pages/Adatfeltöltés.py', label=' Adatfeltöltés', icon='📝')
else:
    df = st.session_state['df_income']
    
    # --- FILTERING ---
    with st.expander('Keresés és szűrés'):
        st.markdown('**A szűrési feltételek kiválaszhatók a legürgülő listából, de a mezőbe kattintva be lehet írni a keresett elemet, majd arra rákattintva kiválasztani.**')
        yfcol1, yfcol2, yfcol3 = st.columns((1,1,1), gap='medium')
        cfcol1, cfcol2, cfcol3 = st.columns((1,1,1), gap='medium')
        cfcol4, cfcol5, cfcol6 = st.columns((3,1,1), gap='medium')
    
# --- TIME FILTERS ---

    quarter_mapping = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
    months_in_quarter = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]}
    month_names = { 1: 'Január', 2: 'Február', 3: 'Március', 4: 'Április', 5: 'Május', 6: 'Június', 7: 'Július', 8: 'Augusztus', 9: 'Szeptember', 10: 'Október', 11: 'November', 12: 'December'}
    year = sorted(df['year'].unique())
    years = yfcol1.multiselect('Tárgyév', options=year, placeholder='Válassz évet',)
    if len(years) == 0:
        years = sorted(df['year'].unique())

    quarters = yfcol2.multiselect('Negyedév', options=quarter_mapping, placeholder='Válassz negyedévet')
    selected_quarters = [quarter_mapping[q] for q in quarters]
    if len(selected_quarters) == 0:
        selected_quarters = sorted(df['quarter'].unique())
    
    available_months = set()
    for q in selected_quarters:
        available_months.update(months_in_quarter[q])
        
    available_month_names = [month_names[m] for m in available_months]
    
    months = yfcol3.multiselect('Hónap', options=available_month_names, placeholder='Válassz hónapot')
    selected_months = [k for k, v in month_names.items() if v in months]
    if len(selected_months) == 0:
        selected_months = sorted(df['month'].unique())

# --- CATEGORY FILTERS ---

    kategoria = sorted(df['kategoria'].unique())
    kategoriak = cfcol1.multiselect('Kategória', options=kategoria, placeholder='Válassz kategóriát')
    if len(kategoriak) == 0:
        kategoriak = sorted(df['kategoria'].unique())

    alkategoria = sorted(df.loc[df['kategoria'].isin(kategoriak), 'alkategoria'].unique())
    alkategoriak = cfcol2.multiselect('Alkategória', options=alkategoria, placeholder='Válassz alkategóriát')
    if len(alkategoriak) == 0:
        alkategoriak = sorted(df['alkategoria'].unique())
        
    elem = sorted(df.loc[df['alkategoria'].isin(alkategoriak), 'elem'].unique())
    elemek = cfcol3.multiselect('Kategória elem', options=elem, placeholder='Válassz kategória elemet')
    if len(elemek) == 0:
        elemek = sorted(df['elem'].unique())
    
    kat_kod = sorted(df['kat_kod'].unique())
    kat_kodok = cfcol5.multiselect('Kategória kód', options=kat_kod, placeholder='Válassz kategória kódot')
    if len(kat_kodok) == 0:
        kat_kodok = sorted(df['kat_kod'].unique())

    partner = sorted(df['partner'].unique())
    partnerek = cfcol4.multiselect('Partner', options=partner, placeholder='Válassz partnert')
    if len(partnerek) == 0:
        partnerek = sorted(df['partner'].unique())

    in_or_not = cfcol6.selectbox('Szűrés típusa', options=['Tartalmazza','Kivéve'], help='Kivéve esetén ha nincs megadott feltétel, akkor nem jelenik meg adat! Először adja meg a kivételt, utána álltsa a mezőt Kivéve értékre!')
    
    if in_or_not == 'Tartalmazza':
        selected_df = df[
            (df['year'].isin(years)) &
            (df['quarter'].isin(selected_quarters)) &
            (df['month'].isin(selected_months)) &
            (df['kat_kod'].isin(kat_kodok)) &
            (df['kategoria'].isin(kategoriak)) &
            (df['alkategoria'].isin(alkategoriak)) &
            (df['elem'].isin(elemek)) &
            (df['partner'].isin(partnerek))]
    elif in_or_not == 'Kivéve':
       selected_df = df[
            (~df['year'].isin(years)) |
            (~df['quarter'].isin(selected_quarters)) |
            (~df['month'].isin(selected_months)) |
            (~df['kat_kod'].isin(kat_kodok)) |
            (~df['kategoria'].isin(kategoriak)) |
            (~df['alkategoria'].isin(alkategoriak)) |
            (~df['elem'].isin(elemek)) |
            (~df['partner'].isin(partnerek))] 

    if selected_df.empty:
        st.divider()
        st.error('A kiválasztott szűrési feltételeknek megfelelő adat nem létezik, ellenőrizze a beállított szűrési feltételeket! Kizáró szűrés esetén először meg kell adni a kizárt feltételt!')
    else:
        
        selected_df['percentage'] = (selected_df['netto'] / selected_df['netto'].sum()) * 100
        
        
# --- SUB DATAFRAMES ---

        df_cat_data = selected_df[['kategoria', 'netto', 'percentage']].groupby(['kategoria']).sum().sort_values(['netto'], ascending=False)
        df_cat_data['netto'] = df_cat_data['netto'].round(0)
        df_cat_data['netto'] = df_cat_data['netto'].apply(lambda x: f"{int(x):,} Ft")
        df_cat_data['percentage'] = df_cat_data['percentage'].round(2)
        df_cat_data['percentage'] = df_cat_data['percentage'].apply(lambda x: f"{x:.2f}%")
        df_cat_data = df_cat_data.rename(columns={'netto': 'Nettó', 'percentage': 'Százalék'})
        
        df_subcat_data = selected_df[['alkategoria', 'netto', 'percentage']].groupby(['alkategoria']).sum().sort_values(['netto'], ascending=False)
        df_subcat_data['netto'] = df_subcat_data['netto'].round(0)
        df_subcat_data['netto'] = df_subcat_data['netto'].apply(lambda x: f"{int(x):,} Ft")
        df_subcat_data['percentage'] = df_subcat_data['percentage'].round(2)
        df_subcat_data['percentage'] = df_subcat_data['percentage'].apply(lambda x: f"{x:.2f}%")
        df_subcat_data = df_subcat_data.rename(columns={'netto': 'Nettó', 'percentage': 'Százalék'})
        
        df_item_data = selected_df[['elem', 'netto', 'percentage']].groupby(['elem']).sum().sort_values(['netto'], ascending=False)
        df_item_data['netto'] = df_item_data['netto'].round(0)
        df_item_data['netto'] = df_item_data['netto'].apply(lambda x: f"{int(x):,} Ft")
        df_item_data['percentage'] = df_item_data['percentage'].round(2)
        df_item_data['percentage'] = df_item_data['percentage'].apply(lambda x: f"{x:.2f}%")
        df_item_data = df_item_data.rename(columns={'netto': 'Nettó', 'percentage': 'Százalék'})       
        
        df_partner_data = selected_df[['partner', 'netto', 'percentage']].groupby(['partner']).sum().sort_values(['netto'], ascending=False)
        df_partner_data['netto'] = df_partner_data['netto'].round(0)
        df_partner_data['netto'] = df_partner_data['netto'].apply(lambda x: f"{int(x):,} Ft")
        df_partner_data['percentage'] = df_partner_data['percentage'].round(2)
        df_partner_data['percentage'] = df_partner_data['percentage'].apply(lambda x: f"{x:.2f}%")
        df_partner_data = df_partner_data.rename(columns={'netto': 'Nettó', 'percentage': 'Százalék'})  
            
# --- TABS ---

        tabs = st.tabs(['Összesítő adatok','Napsugár diagram','Napsugár diagram összehasonlítás', 'Összesített kategória','Összesített alkategória','Összesített elem','Összehasonlítás','Vizsgált adatok'])
        
    ### Osszesito adatok
        
        with tabs[0]:
            
            sumcol1, sumcol2 = st.columns((1,1), gap='large')
            st.write('')
            st.divider()
            st.write('')
            sumcol3, sumcol4, sumcol5 = st.columns((1,1,1), gap='large')
        
            # --- TOTAL INCOME ---

            with sumcol1:
                
                total_df = selected_df.groupby(['month_year'], as_index=False)['netto'].sum().round(0)
                total_income = selected_df['netto'].sum().round(0)
                
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

            # --- TOTAL COUNT ---
            
            with sumcol2:
                
                count_df = selected_df.groupby(['month_year'], as_index=False)['partner'].count()
                total_count_num = selected_df['partner'].count()
                
                st.subheader('Darabszám', divider='grey')
                total_count(
                    label='Teljes darabszám',
                    value=total_count_num,
                    suffix=' db',
                    show_graph=True,
                    graph_x=count_df['month_year'],
                    graph_y=count_df['partner'],
                    color_graph=graph_color
                )

            with sumcol3:
                st.subheader('Kategóriák nettó és százalékos megoszlása', divider='grey')
                st.table(df_cat_data)
                table_formating()

            with sumcol4:
                st.subheader('Alkategóriák nettó és százalékos megoszlása', divider='grey')
                st.table(df_subcat_data)
                table_formating()
        
            with sumcol5:
                    st.subheader('Elemek nettó és százalékos megoszlása', divider='grey')
                    st.table(df_item_data)
                    table_formating()
        
        ### SUNBURST
        
        with tabs[1]:
            
            st.write('')
            sun1, sun2 = st.columns((4,3))
            
            with sun1:
                sun_data_type = st.selectbox('Kategória vagy pertner alapú csoportosítás', options=['Kategória','Partner'])
                
                if sun_data_type == 'Kategória':
                    path = ['kategoria', 'alkategoria', 'elem']
                    sunburst(selected_df,path)
                
                elif sun_data_type == 'Partner':
                    sun_data_lvl = st.selectbox('Legkisebb szint', options=['Partner','Kategória','Alkategória','Elem'])
                    
                    if sun_data_lvl == 'Partner':
                        path = ['partner']
                        
                    if sun_data_lvl == 'Kategória':
                        path = ['partner','kategoria']
                        
                    if sun_data_lvl == 'Alkategória':
                        path = ['partner','kategoria', 'alkategoria']
                        
                    if sun_data_lvl == 'Elem':
                        path = ['partner','kategoria', 'alkategoria', 'elem']

                    sunburst(selected_df, path)
                    
            with sun2:
                sun_data = st.selectbox('Vizsgált szint', options=['Partner','Kategória','Alkategória','Elem'])
                
                if sun_data == 'Partner':
                    st.write('')
                    st.table(df_partner_data)
                    table_formating()
                
                if sun_data == 'Kategória':
                    st.write('')
                    st.table(df_cat_data)
                    table_formating()
                
                if sun_data == 'Alkategória':
                    st.write('')
                    st.table(df_subcat_data)
                    table_formating()

                if sun_data == 'Elem':
                    st.write('')
                    st.table(df_item_data)
                    table_formating()
                    
                    
        ### SUNBURST COMPARIONS
        
        with tabs[2]:

            suncomp1, suncomp2 , suncomp3= st.columns((4,2,4))
            sun_years = sorted(selected_df['year'].unique())
             
            sun_type = suncomp2.selectbox('Összehasonlítás', options=['Partner','Kategória','Alkategória','Elem'], help='Alkategória és elem összehasonlításnál érdemes az adatokat előre szűrni, hogy könnyebben áttekinthető legyen a változás!')
                    
            with suncomp1:
                sun_year1 = st.selectbox('Hasonlítási év', options=year, placeholder='Válassz évet')
                df_sun_year1 = selected_df[selected_df['year'] == sun_year1]
                
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
                sun_year2 = st.selectbox('Vizsgált év', options=year, placeholder='Válassz évet')
                df_sun_year2 = selected_df[selected_df['year'] == sun_year2]

                if sun_type == 'Partner':
                    path = ['partner']
                    
                if sun_type == 'Kategória':
                    path = ['kategoria']
                    
                if sun_type == 'Alkategória':
                    path = ['alkategoria']
                    
                if sun_type == 'Elem':
                    path = ['elem']

                sunburst(df_sun_year2, path)   
            
            with suncomp2:
                
                if sun_type == 'Partner':
                    df_sun1 = df_sun_year1 = selected_df[selected_df['year'] == sun_year1][['partner', 'netto']].groupby(['partner']).sum()
                    df_sun2 = df_sun_year2 = selected_df[selected_df['year'] == sun_year2][['partner', 'netto']].groupby(['partner']).sum()
                    df_sun_merge = pd.merge(left=df_sun1,right=df_sun2,on='partner',how='right')
                    df_sun_merge['diff'] = (df_sun_merge['netto_y']/df_sun_merge['netto_x'])*100-100
                    df_sun_merge['diff'] = df_sun_merge['diff'].round(2)
                    df_sun_merge['netto_y'] = df_sun_merge['netto_y'].round()
                    df_sun_merge = df_sun_merge.sort_values(['netto_y'], ascending=False)
                    for key, values in df_sun_merge.iterrows():
                        netto_y_formatted = f"{values['netto_y']:,.0f} Ft"
                        diff_formated  = f"{values['diff']:,.2f} %"
                        st.metric(f'{key}',value=netto_y_formatted ,delta=diff_formated)
                
                if sun_type == 'Kategória':
                    df_sun1 = df_sun_year1 = selected_df[selected_df['year'] == sun_year1][['kategoria', 'netto']].groupby(['kategoria']).sum()
                    df_sun2 = df_sun_year2 = selected_df[selected_df['year'] == sun_year2][['kategoria', 'netto']].groupby(['kategoria']).sum()
                    df_sun_merge = pd.merge(left=df_sun1,right=df_sun2,on='kategoria',how='right')
                    df_sun_merge['diff'] = (df_sun_merge['netto_y']/df_sun_merge['netto_x'])*100-100
                    df_sun_merge['diff'] = df_sun_merge['diff'].round(2)
                    df_sun_merge['netto_y'] = df_sun_merge['netto_y'].round()
                    df_sun_merge = df_sun_merge.sort_values(['netto_y'], ascending=False)
                    for key, values in df_sun_merge.iterrows():
                        netto_y_formatted = f"{values['netto_y']:,.0f} Ft"
                        diff_formated  = f"{values['diff']:,.2f} %"
                        st.metric(f'{key}',value=netto_y_formatted ,delta=diff_formated)
                    
                if sun_type == 'Alkategória':
                    df_sun1 = df_sun_year1 = selected_df[selected_df['year'] == sun_year1][['alkategoria', 'netto']].groupby(['alkategoria']).sum()
                    df_sun2 = df_sun_year2 = selected_df[selected_df['year'] == sun_year2][['alkategoria', 'netto']].groupby(['alkategoria']).sum()
                    df_sun_merge = pd.merge(left=df_sun1,right=df_sun2,on='alkategoria',how='right')
                    df_sun_merge['diff'] = (df_sun_merge['netto_y']/df_sun_merge['netto_x'])*100-100
                    df_sun_merge['diff'] = df_sun_merge['diff'].round(2)
                    df_sun_merge['netto_y'] = df_sun_merge['netto_y'].round()
                    df_sun_merge = df_sun_merge.sort_values(['netto_y'], ascending=False)
                    for key, values in df_sun_merge.iterrows():
                        netto_y_formatted = f"{values['netto_y']:,.0f} Ft"
                        diff_formated  = f"{values['diff']:,.2f} %"
                        st.metric(f'{key}',value=netto_y_formatted ,delta=diff_formated)

                if sun_type == 'Elem':
                    df_sun1 = df_sun_year1 = selected_df[selected_df['year'] == sun_year1][['elem', 'netto']].groupby(['elem']).sum()
                    df_sun2 = df_sun_year2 = selected_df[selected_df['year'] == sun_year2][['elem', 'netto']].groupby(['elem']).sum()
                    df_sun_merge = pd.merge(left=df_sun1,right=df_sun2,on='elem',how='right')
                    df_sun_merge['diff'] = (df_sun_merge['netto_y']/df_sun_merge['netto_x'])*100-100
                    df_sun_merge['diff'] = df_sun_merge['diff'].round(2)
                    df_sun_merge['netto_y'] = df_sun_merge['netto_y'].round()
                    df_sun_merge = df_sun_merge.sort_values(['netto_y'], ascending=False)
                    for key, values in df_sun_merge.iterrows():
                        netto_y_formatted = f"{values['netto_y']:,.0f} Ft"
                        diff_formated  = f"{values['diff']:,.2f} %"
                        st.metric(f'{key}',value=netto_y_formatted ,delta=diff_formated)

        
        ### CATEGORY
        
        with tabs[3]:

            catcol1, catcol2 = st.columns((2,1),gap='large')

            with catcol1:
                st.subheader('TOP 10 kategória', divider='grey')
                sum_category = selected_df[['kategoria', 'alkategoria', 'netto']].groupby('kategoria', as_index=False).sum().sort_values('netto',ascending=False).head(10)
                plot_top10(
                    df=sum_category,
                    x_data='netto',
                    y_data='kategoria',
                    marker_color=graph_color,
                    x_axis_title='Nettó összeg',
                    y_axis_title='Kategória neve'
                )
                
                st.subheader('Összes kategória alkategóriákra bontva', divider='grey')
                df_categories = selected_df[['kategoria', 'alkategoria', 'netto']].groupby(['kategoria', 'alkategoria']).sum().sort_values(['kategoria', 'netto'], ascending=False).round(0).reset_index()
                detailed_bar(
                    df=df_categories,
                    x_data='netto',
                    y_data='kategoria',
                    color='alkategoria',
                    x_axis_title='Nettó összeg',
                    y_axis_title='Kategória neve'
                )
            
            with catcol2:
                    st.subheader('Kategóriák nettó és százalékos megoszlása', divider='grey')
                    st.table(df_cat_data)
                    table_formating()
            
        ### Alkategoria
            
        with tabs[4]:

            subcatcol1, subcatcol2 = st.columns((2,1),gap='large')

            with subcatcol1:
                st.subheader('TOP 10 alkategória', divider='grey')
                sum_category = selected_df[['alkategoria', 'elem', 'netto']].groupby('alkategoria', as_index=False).sum().sort_values('netto',ascending=False).head(10)
                plot_top10(
                    df=sum_category,
                    x_data='netto',
                    y_data='alkategoria',
                    marker_color=graph_color,
                    x_axis_title='Nettó összeg',
                    y_axis_title='Alategória neve'
                )
                
                st.subheader('Összes alkategória elemekre bontva', divider='grey')
                df_categories = selected_df[['alkategoria', 'elem', 'netto']].groupby(['alkategoria', 'elem']).sum().sort_values(['alkategoria', 'netto'], ascending=False).round(0).reset_index()
                detailed_bar(
                    df=df_categories,
                    x_data='netto',
                    y_data='alkategoria',
                    color='elem',
                    x_axis_title='Nettó összeg',
                    y_axis_title='Allategória neve'
                )
            
            with subcatcol2:
                    st.subheader('Alkategóriák nettó és százalékos megoszlása', divider='grey')
                    st.table(df_subcat_data)
                    table_formating()
                    
        ### Elem
        
        with tabs[5]:

            itemcol1, itemcol2 = st.columns((2,1),gap='large')

            with itemcol1:
                st.subheader('TOP 10 elem', divider='grey')
                sum_category = selected_df[['elem', 'netto']].groupby('elem', as_index=False).sum().sort_values('netto',ascending=False).head(10)
                plot_top10(
                    df=sum_category,
                    x_data='netto',
                    y_data='elem',
                    marker_color=graph_color,
                    x_axis_title='Nettó összeg',
                    y_axis_title='Elem neve'
                )
            
            with itemcol2:
                    st.subheader('Elemek nettó és százalékos megoszlása', divider='grey')
                    st.table(df_item_data)
                    table_formating()
        
        ### Osszehasonlitas
        
        with tabs[6]:
            
            st.write('')
            
            with st.container(border=True):
                
                st.write('❗ Az összhasonlítás a fent beállított szűrésektől független! A szükséges szűrési paramétereket alább lehet beállítani. A összehasonlítási szinttől függően jelennek meg a válaszható szűrési lehetőségek!')
            
            comp_col1, comp_col2 = st.columns((1,4))
            comp_type = comp_col1.selectbox('Összehasonlítási szint', options=['Kategória','Alkategória','Elem'])
            
            comp_years = sorted(df['year'].unique())
            comp_cats = sorted(df['kategoria'].unique())
            comp_subcats = sorted(df['alkategoria'].unique())
            comp_items = sorted(df['elem'].unique())
            
            if comp_type == 'Kategória':
                
                with comp_col2:
                    subcomp1, subcomp2 = st.columns((1,2))
                    
                    comp_year = sorted(df['year'].unique())
                    comp_years = subcomp1.multiselect('Összehasonlított évek', options=comp_year, placeholder='Válassz évet')
                    if len(comp_years) == 0:
                        comp_years = sorted(df['year'].unique())

                    comp_cat = sorted(df['kategoria'].unique())
                    comp_cats = subcomp2.multiselect('Összehasonlított kategóriák', options=comp_cat, placeholder='Válassz kategóriát')
                    if len(comp_cats) == 0:
                        comp_cats = sorted(df['kategoria'].unique())

                    comp_df = df[
                        (df['year'].isin(comp_years)) &
                        (df['kategoria'].isin(comp_cats))
                        ]
     
            elif comp_type == 'Alkategória':
                
                with comp_col1:
                    comp_year = sorted(df['year'].unique())
                    comp_years = st.multiselect('Összehasonlított évek', options=comp_year, placeholder='Válassz évet')
                    if len(comp_years) == 0:
                        comp_years = sorted(df['year'].unique())
                
                with comp_col2:
                    subcomp1, subcomp2 = st.columns((1,2))
                    
                    comp_cat = sorted(df['kategoria'].unique())
                    comp_cats = subcomp1.multiselect('Összehasonlított kategóriák', options=comp_cat, placeholder='Válassz kategóriát')
                    if len(comp_cats) == 0:
                        comp_cats = sorted(df['kategoria'].unique())
                        
                    comp_subcat = sorted(df.loc[df['kategoria'].isin(comp_cats), 'alkategoria'].unique())
                    comp_subcats = subcomp2.multiselect('Összehasonlított alkategóriák', options=comp_subcat, placeholder='Válassz alkategóriát')
                    if len(comp_subcats) == 0:
                        comp_subcats = sorted(df['alkategoria'].unique())

                comp_df = df[
                    (df['year'].isin(comp_years)) &
                    (df['kategoria'].isin(comp_cats)) &
                    (df['alkategoria'].isin(comp_subcats))
                    ]

            elif comp_type == 'Elem':
                
                with comp_col1:
                    comp_year = sorted(df['year'].unique())
                    comp_years = st.multiselect('Összehasonlított évek', options=comp_year, placeholder='Válassz évet')
                    if len(comp_years) == 0:
                        comp_years = sorted(df['year'].unique())
                
                with comp_col2:
                    subcomp1, subcomp2 = st.columns((1,2))
                    
                    comp_cat = sorted(df['kategoria'].unique())
                    comp_cats = subcomp1.multiselect('Összehasonlított kategóriák', options=comp_cat, placeholder='Válassz kategóriát')
                    if len(comp_cats) == 0:
                        comp_cats = sorted(df['kategoria'].unique())
                        
                    comp_subcat = sorted(df.loc[df['kategoria'].isin(comp_cats), 'alkategoria'].unique())
                    comp_subcats = subcomp2.multiselect('Összehasonlított alkategóriák', options=comp_subcat, placeholder='Válassz alkategóriát')
                    if len(comp_subcats) == 0:
                        comp_subcats = sorted(df['alkategoria'].unique())

                    comp_item = sorted(df.loc[df['alkategoria'].isin(comp_subcats), 'elem'].unique())
                    comp_items = st.multiselect('Összehasonlított elemek', options=comp_item, placeholder='Válassz elemet')
                    if len(comp_items) == 0:
                        comp_items = sorted(df['elem'].unique())                    
                    
                comp_df = df[
                    (df['year'].isin(comp_years)) &
                    (df['kategoria'].isin(comp_cats)) &
                    (df['alkategoria'].isin(comp_subcats)) &
                    (df['elem'].isin(comp_items))
                    ]                         
   
            comparison(comp_df, comp_type, comp_years, comp_cats, comp_subcats, comp_items)

        ### Adatok
        
        with tabs[7]:
            st.dataframe(selected_df)