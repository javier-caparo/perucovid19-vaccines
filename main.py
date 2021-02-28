# -*- coding: utf-8 -*-
"""
Created on Feb 27, 2021
@author: Javier Caparo
"""

import streamlit as st
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
import requests 
import altair as alt

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


@st.cache()
def get_data_ex4():
    #df = pd.read_csv ('./data/vacunas_covid.csv')
    url = 'https://cloud.minsa.gob.pe/s/ZgXoXqK2KLjRLxD/download'
    df = pd.read_csv(url)
    
    df.FECHA_CORTE = df.FECHA_CORTE.astype(str)
    df.FECHA_VACUNACION = df.FECHA_VACUNACION.astype(str)

    df['FECHA_CORTE'] = pd.to_datetime(df['FECHA_CORTE'], format='%Y%m%d')
    df["FECHA_VACUNACION"] =pd.to_datetime(df["FECHA_VACUNACION"],format='%Y%m%d')
    return df

@st.cache(suppress_st_warning=True)
def visualize_data(df):
    with st.spinner('Wait for it...'):
        #time.sleep(8)
        graph = alt.Chart(df).mark_bar().encode(
            x='count():Q',
            y='FECHA_VACUNACION:T',
            color='SEXO:N',
            row='GRUPO_RIESGO:O'
        ).interactive()
        st.altair_chart(graph.mark_line(color='firebrick'))
    st.success('Done!')
    
def main():
# Loading the data
    df = get_data_ex4()
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Exploration"])

    if page == "Homepage":
        st.header('🦠 Covid-19 Vaccines Doses Applied Dashboard 🦠 ')
        st.write("Please select a page on the left.")
        st.sidebar.markdown('🦠 **Covid-19 Dashborad** 🦠 ')
        st.sidebar.markdown(''' 
        This app is to give insights about Covid-19 Vaccines in PERU.
        The data considered for this analysis was obtained from MINSA Open data website
        https://www.datosabiertos.gob.pe/dataset/vacunaci%C3%B3n-contra-covid-19-ministerio-de-salud-minsa
        Select the different options to play with the Visualization
        All the Charts are interactive. 
        Scroll the mouse over the Charts to feel the interactive features like Tool tip, Zoom, Pan
                            
        Designed by:
        **Javier Caparo**  ''')  

        #st.write(df.dtypes)
        today = datetime.date.today()
        st.write('Today is:',today)
        st.write('# of doses already applied',len(df.index))
        st.dataframe(df.head(5))
        # Load a lottie animation
        lottie_url = "https://assets3.lottiefiles.com/packages/lf20_1pf6yomw.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json)
    elif page == "Exploration":
        st.title("Data Exploration")
        st.header('Grouped by SEX & RISK GROUP')
        visualize_data(df)

if __name__ == "__main__":
    main()


# Distribucion x Edad
#values = st.sidebar.slider("Rango Edad", int(df.EDAD.min()), 100,(18,65))
#st.write("Values", values[0], values[1])

#f = px.histogram(df[(df['EDAD'] >=values[0]) & (df['EDAD']<=values[1])], x="EDAD",nbins=15, title="Distribucion x Edad",color_discrete_sequence=['indianred'])
#f.update_xaxes(title="Edad")
#f.update_yaxes(title="Nro de Vacunados")
#st.plotly_chart(f)
