import streamlit as st
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d
from tempeDB import *
from datetime import datetime

tempeDB = TempeDB(host = '192.168.10.174', user = 'invite')

st.sidebar.title("T-HOME")
liste_capteurs = [None] + tempeDB.get_capteurs()
capteur1 = st.sidebar.selectbox("Capteur 1 : ",liste_capteurs)
capteur2 = st.sidebar.selectbox("Capteur 2 : ",liste_capteurs)
date_debut = st.sidebar.date_input("Date de début")
date_fin = st.sidebar.date_input("Date de fin")
multi_axes = st.sidebar.checkbox("Multi_axes Y", value = False)

date_format = "%Y-%m-%d %H:%M:%S"

@st.cache
def get_data(capteur,date_debut, date_fin):
    '''Renvoie un tuple ([x0,x1,...],[y0,y1,...])
    '''
    data = tempeDB.historique(capteur,date_debut, date_fin)
    x = [datetime.strptime(i[0], date_format) for i in data]
    y = [float(i[1]) for i in data]
    return x,y

if st.sidebar.button("Go"):
    titre = ""
    fig = figure(
        #title=capteur1,
        x_axis_label='date',
        x_axis_type = "datetime")
    if capteur1:
        titre += capteur1
        if capteur2:
            titre += " vs %s"%capteur2
        x1,y1= get_data(capteur1,date_debut, date_fin)
        fig.line(x1,y1,line_width = 2, legend_label = capteur1)
    else:
        if capteur2:
            titre = " (%s)"%capteur2
    if capteur2:
        x2,y2 = get_data(capteur2,date_debut, date_fin)
        if multi_axes == False:
            fig.line(x2,y2,line_width = 2, line_color = "red", legend_label = capteur2)
        else:
            fig.extra_y_ranges = {"yextra":Range1d(start = min(y2), end = max(y2))}
            fig.line(x2,y2,line_width = 2, y_range_name = "yextra", line_color = "red", legend_label = capteur2)
            fig.add_layout(LinearAxis(y_range_name = "yextra"), 'right')

    st.title(titre)
    st.bokeh_chart(fig, use_container_width=True)
