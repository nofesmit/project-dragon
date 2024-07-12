import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt

# ---- CONFIG ----
st.set_page_config(page_title="Bevételek", layout="wide")

# ---- FUNCTIONS ----

#Data cleaning

@st.cache_data
def inc_clean(df_income):
    df_income = df_income.replace('_x000D_', '', regex=True)
    df_income = df_income.replace('\n', '', regex=True)
    df_income = df_income[['Kiállítás','partner','Bizonylat II.','Megjegyzés','Szállítási mód','Cikk','ar','penznem', 'mennyiseg','teljes_ar','HUF_ar','EUR_HUF']]
    df_income['Kiállítás'] = pd.to_datetime(df_income['Kiállítás'], format='%Y%m%d')
    df_income['month_year'] = df_income['Kiállítás'].dt.to_period('m')
    return df_income

#Summary plots
def plot_metric(value, prefix="", suffix="", show_graph=False, graph_x="", graph_y="", color_graph=""):

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
            domain={'x': [0, 1], 'y': [0.9, 1]}
            #title={
            #    "text": label,
            #    "font": {"size": 24},
            #}
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
                line={
                    "color": color_graph,
                },
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

if 'df_income' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Bevételek vizsgálatához a bevételi adatok feltöltése szükséges!')
else:
    df_income = st.session_state['df_income']
    
    df_income = inc_clean(df_income)

    st.title('Bevételek')
    
    st.dataframe(df_income)
    st.write(df_income.dtypes)
    st.write(df_income['HUF_ar'].sum())