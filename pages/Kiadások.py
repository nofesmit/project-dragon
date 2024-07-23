import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import toml

# --- CONFIG ----

st.set_page_config(page_title="Kiadások", layout="wide")

# --- THEME ---

graph_color = '#6D87BD'

# --- FUNCTIONS ---

def plot_metric(label, value, prefix="", suffix="", show_graph=False, graph_x="", graph_y="", color_graph=""):

    if graph_x is None:
        graph_x = []
    if graph_y is None:
        graph_y = []

    if isinstance(graph_x, pd.Series) and isinstance(graph_x.iloc[0], pd.Period):
        graph_x = graph_x.astype(str)
    elif isinstance(graph_x, list) and isinstance(graph_x[0], pd.Period):
        graph_x = [str(x) for x in graph_x]
        
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
                #hoverinfo="skip",
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
        height=120,
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_top10(df, x_data:str, y_data:str, marker_color:str):
    
    fig = px.bar(
        data_frame=df,
        x=x_data,
        y=y_data,
        #title=label,
        text_auto='.2s'
    )
    
    fig.update_traces(marker_color=marker_color, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}
        )
    st.plotly_chart(fig, use_container_width=True)

def detailed_bar(df, x_data:str, y_data:str, color:str):
    fig = px.bar(
        data_frame=df,
        x=x_data,
        y=y_data,
        color=color,
        text_auto='.2s',
        color_discrete_sequence= px.colors.qualitative.T10
    )
    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}
        )
    
    st.plotly_chart(fig, use_container_width=True)

def sunburst(df):

    fig = px.sunburst(
        data_frame=df,
        path=['kategoria', 'alkategoria', 'elem'],
        values='netto',
        color_discrete_sequence= px.colors.qualitative.T10
    )
    
    fig.update_layout(
        #title='Treemap of Kategoria, Alkategoria, and Elem',
        margin=dict(t=20, l=10, r=10, b=10),
        height=800
    )

    fig.update_traces(
        hovertemplate='<b>%{label}</b>' + 
                    '<br>Netto: %{value: ,.0d} Ft<extra></extra>',
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
    
def comparison(df):

    # Monthly comparison
    monthly_data = selected_df.groupby(['year', 'month'])['netto'].sum().reset_index()

    # Quarterly comparison
    quarterly_data = selected_df.groupby(['year', 'quarter'])['netto'].sum().reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Monthly Cost Comparison", "Quarterly Cost Comparison"),
        shared_yaxes=False
    )

    # Add monthly data to subplot
    for year in comp_selected_years:
        year_data = monthly_data[monthly_data['year'] == year]
        fig.add_trace(
            go.Bar(x=year_data['month'], y=year_data['netto'], name=f"Year {year}", legendgroup=f"Year {year}"),
            row=1, col=1
        )

    # Add quarterly data to subplot
    for year in comp_selected_years:
        year_data = quarterly_data[quarterly_data['year'] == year]
        fig.add_trace(
            go.Bar(x=year_data['quarter'], y=year_data['netto'], name=f"Year {year}", legendgroup=f"Year {year}"),
            row=1, col=2
        )

    # Update layout
    fig.update_layout(barmode='group', title="Monthly and Quarterly Cost Comparison", showlegend=True)

    st.plotly_chart(fig)

# --- SESSION VARIABLES ---

if 'df_expense' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Bevételek vizsgálatához a bevételi adatok feltöltése szükséges!')
else:
    df = st.session_state['df_expense']

# --- PAGE ---

    st.title('Kiadások')
    
    # --- FILTERING ---
    with st.expander('Szűrési feltételek kiválasztása'):
        #st.markdown('**A szűrési feltételek kiválaszhatók a legürgülő listából, de a mezőbe kattintva be lehet írni a keresett elemet, majd arra rákattintva kiválasztani.**')
        yfcol1, yfcol2, yfcol3 = st.columns((1,1,1), gap='medium')
        cfcol1, cfcol2, cfcol3 = st.columns((1,1,1), gap='medium')
        cfcol4, cfcol5 = st.columns((1,1), gap='medium')
        pfcol1, pfcol2, = st.columns((10,2))
    
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
    if "Mind" in kategoriak or len(kategoriak) == 0:
        kategoriak = sorted(df['kategoria'].unique())

    alkategoria = sorted(df.loc[df['kategoria'].isin(kategoriak), 'alkategoria'].unique())
    alkategoriak = cfcol2.multiselect('Válassz alkategóriát:', options=alkategoria, placeholder='Válassz alkategóriát')
    if "Mind" in alkategoriak or len(alkategoriak) == 0:
        alkategoriak = sorted(df['alkategoria'].unique())
        
    elem = sorted(df.loc[df['alkategoria'].isin(alkategoriak), 'elem'].unique())
    elemek = cfcol3.multiselect('Kategória elem', options=elem, placeholder='Válassz kategória elemet')
    if "Mind" in elemek or len(elemek) == 0:
        elemek = sorted(df['elem'].unique())

    fo_kat = sorted(df['fo_kat'].unique())
    fo_katok = cfcol4.multiselect('Fő kategória', options=fo_kat, placeholder='Válassz fő kategóriát', help='A 0. kategória a nem besorolt!')
    if "Mind" in fo_katok or len(fo_katok) == 0:
        fo_katok = sorted(df['fo_kat'].unique())
    
    kat_kod = sorted(df['kat_kod'].unique())
    kat_kodok = cfcol5.multiselect('Válassz kategória kódot:', options=kat_kod, placeholder='Válassz kategória kódot')
    if "Mind" in kat_kodok or len(kat_kodok) == 0:
        kat_kodok = sorted(df['kat_kod'].unique())

    partner = sorted(df['partner'].unique())
    partnerek = pfcol1.multiselect('Válassz partnert:', options=partner, placeholder='Válassz partnert')
    if "Mind" in partnerek or len(partnerek) == 0:
        partnerek = sorted(df['partner'].unique())

    in_or_not = pfcol2.selectbox('Szűrés típusa:', options=['Tartalmazza','Kivéve'])
    
    if in_or_not == 'Tartalmazza':
        selected_df = df[
            (df['year'].isin(years)) &
            (df['quarter'].isin(selected_quarters)) &
            (df['month'].isin(selected_months)) &
            (df['fo_kat'].isin(fo_katok)) &
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
            (~df['fo_kat'].isin(fo_katok)) |
            (~df['kat_kod'].isin(kat_kodok)) |
            (~df['kategoria'].isin(kategoriak)) |
            (~df['alkategoria'].isin(alkategoriak)) |
            (~df['elem'].isin(elemek)) |
            (~df['partner'].isin(partnerek))] 

    if selected_df.empty:
        st.divider()
        st.subheader('A kiválasztott szűrési feltételeknek megfelelő adat nem létezik, válaszonn másik szűrési feltételeket az adatok elemzéséhez!')
    else:
        
        # --- VISUALISATION ---
        scol1, scol2 = st.columns((1,2))
        
        # --- TOTAL EXPENSE ---

        with scol1:
            
            total_df = selected_df.groupby(['month_year'], as_index=False)['netto'].sum().round(0)
            total_expense = selected_df['netto'].sum().round(0)
            
            st.subheader('Teljes kiadás', divider='grey')
            plot_metric(
                label='Teljes kiadás',
                value=total_expense,
                suffix=' Ft',
                show_graph=False,
                graph_x=total_df['month_year'],
                graph_y=total_df['netto'],
                color_graph=graph_color
            )

        # --- TOTAL COUNT ---
        
        with scol1:
            
            count_df = selected_df.groupby(['month_year'], as_index=False)['partner'].count()
            total_count = selected_df['partner'].count()
            
            st.subheader('Darabszám', divider='grey')
            plot_metric(
                label='Teljes darabszám',
                value=total_count,
                suffix=' db',
                show_graph=False,
                graph_x=count_df['month_year'],
                graph_y=count_df['partner'],
                color_graph=graph_color
            )
        
        # --- SUNBURST ---
        
        with scol2:
            
            sunburst(selected_df)
        
        
        # --- SUM CATEGORY ---
        
        st.subheader('Összesített kategóriák', divider='gray')

        summ_category = selected_df[['kategoria', 'alkategoria', 'netto']].groupby('kategoria', as_index=False).sum().sort_values('netto',ascending=False).head(10)

        #plot_top10(
        #    df=summ_category,
        #    x_data='netto',
        #    y_data='kategoria',
        #    marker_color=graph_color
        #)
        
        df_categories = selected_df[['kategoria', 'alkategoria', 'netto']].groupby(['kategoria', 'alkategoria']).sum().sort_values(['kategoria', 'netto'], ascending=False).round(0).reset_index()
        
        detailed_bar(
            df=df_categories,
            x_data='netto',
            y_data='kategoria',
            color='alkategoria'
        )
        
        
        # --- SUM SUBCATEGORY ---
        
        st.subheader('TOP10 alkategória', divider='gray')

        summ_category = selected_df[['alkategoria', 'elem', 'netto']].groupby('alkategoria', as_index=False).sum().sort_values('netto',ascending=False).head(10)

        plot_top10(
            df=summ_category,
            x_data='netto',
            y_data='alkategoria',
            marker_color=graph_color
            
        )        
        # --- SUM ITEM ---
        
        st.subheader('TOP10 elem', divider='gray')

        summ_category = selected_df[['elem', 'netto']].groupby('elem', as_index=False).sum().sort_values('netto',ascending=False).head(10)

        plot_top10(
            df=summ_category,
            x_data='netto',
            y_data='elem',
            marker_color=graph_color
            
        )        
        
        # --- CATEGORY TREEMAP ---
        
        st.subheader('Kategória faábra', divider='grey')
        
        plot_treemap(selected_df)
        
        # --- COMPARISON ---
        
        comp_years = df['year'].unique().tolist()
        comp_selected_years = st.multiselect('Select years to compare', years, default=years)
        
            # Monthly comparison
        monthly_data = selected_df.groupby(['year', 'month'])['netto'].sum().reset_index()

        # Quarterly comparison
        quarterly_data = selected_df.groupby(['year', 'quarter'])['netto'].sum().reset_index()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Monthly Cost Comparison", "Quarterly Cost Comparison"),
            shared_yaxes=False
        )

        # Add monthly data to subplot
        for year in comp_selected_years:
            year_data = monthly_data[monthly_data['year'] == year]
            fig.add_trace(
                go.Bar(x=year_data['month'], y=year_data['netto'], name=f"Year {year}", legendgroup=f"Year {year}"),
                row=1, col=1
            )

        # Add quarterly data to subplot
        for year in comp_selected_years:
            year_data = quarterly_data[quarterly_data['year'] == year]
            fig.add_trace(
                go.Bar(x=year_data['quarter'], y=year_data['netto'], name=f"Year {year}", legendgroup=f"Year {year}"),
                row=1, col=2
            )

        # Update layout
        fig.update_layout(barmode='group', title="Monthly and Quarterly Cost Comparison", showlegend=True)

        st.plotly_chart(fig)
        
        st.dataframe(selected_df)
        