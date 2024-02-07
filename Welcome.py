import streamlit as st
from PIL import Image
import pandas as pd
from utils import *
import base64
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



add_logo(logofile, "40%")
# def add_logo():
#     st.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"] {
#                 background-image: url(http://placekitten.com/200/200);
#                 background-repeat: no-repeat;
#                 padding-top: 120px;
#                 background-position: 20px 20px;
#             }
#             [data-testid="stSidebarNav"]::before {
#                 content: "Navigate Page";
#                 margin-left: 20px;
#                 margin-top: 20px;
#                 font-size: 30px;
#                 position: relative;
#                 top: 100px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# add_logo()

st.markdown("# MK-2 Schizophrenia ")
st.sidebar.markdown("## Navigate page ")

st.sidebar.markdown('## [Welcome](#welcome)')
st.sidebar.markdown('## [What it is](#what-it-is)')
st.sidebar.markdown('## [What it contains](#what-it-contains)')
st.sidebar.markdown('## [What you get](#what-you-get)')
st.sidebar.markdown('## [History and rationale](#history-and-rationale)')




set_background(pngfile)
#Photo by <a href="https://unsplash.com/@resul?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Resul Mentes 🇹🇷</a> on <a href="https://unsplash.com/photos/white-clouds-and-blue-skies-DbwYNr8RPbg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>

# image = Image.open(pngfile)
# st.image(image)

st.markdown("## Welcome ")

"""Thank you for investigating MK-2.

We have tried to make this a valuable, time-saving resource for reviewers of treatment trials.

Currently it is focusing solely on people with schizophrenia or related problems but we hope the value of MK-2 will be obvious to a wide group of researchers and information specialists."""

st.markdown('Explore the [Study](MK-2_Study_Search), [Table](MK-2_Table_Search), or the [Data](Raptor_Data_Search) search pages.')


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

st.markdown("## What you get")
"""
When a search is undertaken data are supplied as ready-curated studies. If, for example, you sought a report known to you, authored by J Smith, of a randomised trial that went under the

acronym of STAR then MK-2 will identify that report and supply various levels of STAR-specific data including the bibliographic references of every publication of STAR.

We run this database on a not-for-profit basis. The funding model aims to allow maintenance and improvement of the database and no more.

Level A Level A ––Basic curated record (Basic curated record (freefree))

· Basic study-level data including information on participants, interventions and outcomes.

· A bibliographic list of all known reports of this study, including, where possible, a link to free online access of full text

Level B Level B ––Data extraction Data extraction ––level 1 (level 1 ($1/study$1/study))

· Tabulated detailed study-level data on participants, interventions and outcomes.

· A bibliographic list of all known reports of this study, including, where possible, a link to free online access of full text

· All/choice of fields to export in CSV format.

Level C Level C ––Data extraction Data extraction ––level 2 (level 2 ($10/study$10/study))

· Tabulated detailed study-level data on participants, interventions and outcomes.

· A bibliographic list of all known reports of this study, including, where possible, a link to free online access of full text

· Full extracted, tabulated qualitative and quantitate study data (with a limited number of study reports containing hyper-links back to origin of each piece of data in relevant reports)

· All/choice of fields to export in CSV format.
"""

st.markdown("## History and rationale")

"""
Reviews of studies of the effects of treatments have always been required to summarize evidence with authority.

This process began to be undertaken in a rigorous, reproducible – systematic - way in the 1970s but it was not until the advent of the Cochrane Collaboration in the 1990s that the process became ‘industrialized’.

In a systematic review of treatments great efforts are made to quantify the outcomes of the interventions and these numbers are extracted from published reports and then synthesized in the review.

Reviewers make great efforts to avoid multiple counting of individuals in studies who have had results of the same study reported in many publications and it is often difficult to determine the number randomized.
"""

image = Image.open("C:/Users/c1049033/PycharmProjects/meerkatApp/welcome.JPG")
st.image(image)


"""
It became increasingly obvious to reviewers that

• the building block of the review was the study and not the report;

• that expensive efforts were made to curate multiple reports into representations of their parent studies;

• that these study-based data were used within the review only for the curated hard-won ‘parent’ study not to be made widely available;

• subsequent reviewers would have to repeat the process, recreating the study from the lengthening list of publications; and finally that

• although replication is important, waste within systematic review work was enormous.

In 2004 the UK Cochrane Centre supported Update Software with modest public funding to work with Information Specialists, and reviewers to create a more sophisticated study-based register system holding curated reports in groups of their parent studies. This relational database, built in MS Access, was named MeerKat.

Despite good functionality and support, this programme was not widely adopted across the Cochrane Collaboration. Only Renal and Schizophrenia of the then fifty Cochrane groups use this programme. There are many reasons why software is not adopted and why MeerKat was not widely used within Cochrane but poor functionality was not among them. MeerKat brought a positive step-change in the level of sophistication of information provision and, by supply of study-based data, an incalculable reduction in time wastage.

There are benefits to use of MS Access but these are now outweighed by the advantages of more online connectivity. MeerKat has to be renamed – there are many meerkats to be found on the

internet – but is nevertheless reborn in this pilot, study-based register – MK-2. We hope you enjoy it, use it, and tell us how we can improve it.

"""
V_SPACE(2)

st.write("Background image credit: [Abstract blue geometric shapes background Vectors by doyandesign on Vecteezy](https://www.vecteezy.com/vector-art/2715000-abstract-blue-geometric-shapes-background). The logo image on the sidebar was created with the help of [DALL-E 2](https://openai.com/dall-e-2)")
