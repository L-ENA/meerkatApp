import streamlit as st
from utils import *

set_background(pngfile)
add_logo(logofile, "40%")
st.markdown("#Raptor Data Search 🦖")
st.sidebar.markdown("#Raptor Data Search 🦖")

"Welcome to the Data Search. We extracted bias ratings, outcome data, and study characteristics from Cochrane Schizophrenia reviews. These datapoints can be re-used by researchers who would like to include the same studies in their meta-analyses. We do advise users to always manually check exported data for completeness. Data can be used, for example, to replace a 'second reviewer' during data extraction."