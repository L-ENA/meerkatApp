import streamlit as st

import pandas as pd
from utils import *
#####################################################
if 'reload' not in st.session_state:
    st.session_state.reload = False
if 'previous_query' not in st.session_state:
    st.session_state.previous_query = ""
if 'elasticindex' not in st.session_state:
    st.session_state.elasticindex = ""
if 'nhits' not in st.session_state:
    st.session_state.nhits = 0
if 'exportindices' not in st.session_state:
    st.session_state.exportindices = []
if 'query_df' not in st.session_state:
    st.session_state.query_df = pd.DataFrame()
if 'fieldinfo' not in st.session_state:
    st.session_state.fieldinfo = ", ".join(reportfields)
if 'chosen' not in st.session_state:
    st.session_state.chosen = "CSV"
####################################################
st.markdown("# MK-2 Schizophrenia ")
st.sidebar.markdown("## Navigate page ")

st.sidebar.markdown('## [Welcome](#welcome)')
st.sidebar.markdown('## [What it is](#what-it-is)')
st.sidebar.markdown('## [What it contains](#what-it-contains)')
st.sidebar.markdown('## [What it is](#what-it-is)')
st.sidebar.markdown('## [What it is](#what-it-is)')

st.markdown("## Welcome ")

"""Thank you for investigating MK-2.

We have tried to make this a valuable, time-saving resource for reviewers of treatment trials.

Currently it is focusing solely on people with schizophrenia or related problems but we hope the value of MK-2 will be obvious to a wide group of researchers and information specialists."""

st.markdown("## What it is ")

"""MK-2 is a relational database of randomized controlled trials relevant to people with schizophrenia or similar or related problems."""

st.markdown("## What it contains")

""" MK-2 aims to contain:

• electronic record of every report of every randomized trial – and, were possible, links to free full text;

• all reports batched under their ‘parent’ study record;

• records (electronic) of every relevant study linked to:

  ◦ every relevant ‘child’ report;

  ◦ tables of descriptions of each study’s characteristics;

  ◦ tables containing each study’s extracted numerical data;

  ◦ links to measures of outcomes, their descriptions, reports, and reliable estimates of their validity and utility; and, in a small number of the studies

  ◦ hyperlinks from every piece of extracted data – qualitative and quantitative – back to the original full report"""