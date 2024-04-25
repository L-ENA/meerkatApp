import streamlit as st
from utils import *
from config import *


import streamlit as st
import pandas as pd
from utils import *
from config import *
import requests
import json
from datetime import datetime
set_background(pngfile)
add_logo(logofile, "40%")
####################session state variables
# if 'num_export' not in st.session_state:
#     st.session_state['num_export']=0

if 'last_page' not in st.session_state or st.session_state.last_page != "RAPTOR":#check if the user changed the page, if yes then clear cache to avoil table re-loading with different headings bug
    session_state_init("RAPTOR")
    st.cache_data.clear()


set_background(pngfile)
add_logo(logofile, "40%")
st.markdown("# Raptor Data Search 🦖")
st.sidebar.markdown("# Raptor Data Search 🦖")

"Welcome to the Data Search. We extracted bias ratings, outcome data, and study characteristics from Cochrane Schizophrenia reviews. These datapoints can be re-used by researchers who would like to include the same studies in their meta-analyses. We do advise users to always manually check exported data for completeness. Data can be used, for example, to simulate a 'second reviewer' during data extraction."

V_SPACE(1)

st.markdown("Please see the video on the bottom of this page for further information on using this website. More information about the RAPTOR dataset and how it was curated can be found in our paper: Schmidt, L., Shokraneh, F., Steinhausen, K., Adams, CE. Introducing RAPTOR: RevMan Parsing Tool for Reviewers. Syst Rev 8, 151 (2019). [https://doi.org/10.1186/s13643-019-1070-0](https://doi.org/10.1186/s13643-019-1070-0)")

st.sidebar.write("## 🛠️ Control Panel 🛠️ ️\n")
#############################table selection

tables = pd.DataFrame({
    'first column': ['References', 'Outcomes', "ReferenceIDs",'Characteristics','Bias']
    })
option = st.sidebar.selectbox(
    'Select a table to search 👇',
    tables['first column'],
    index=0)
if option=='References':
    st.session_state.elasticindex='raptorreferences'
    st.session_state.fieldinfo =", ".join([])
    print("Selected {}".format(st.session_state.elasticindex))
elif option=='Outcomes':
    st.session_state.elasticindex='raptoroutcomes'
    st.session_state.fieldinfo = ", ".join([])
    print("Selected {}".format(st.session_state.elasticindex))
elif option=='Characteristics':
    st.session_state.elasticindex='raptorcharacteristics'
    st.session_state.fieldinfo = ", ".join([])
    print("Selected {}".format(st.session_state.elasticindex))
elif option=='ReferenceIDs':
    st.session_state.elasticindex='raptorrefids'
    st.session_state.fieldinfo = ", ".join([])
    print("Selected {}".format(st.session_state.elasticindex))
elif option=='Bias':
    st.session_state.elasticindex='raptorbias'
    st.session_state.fieldinfo = ", ".join([])
    print("Selected {}".format(st.session_state.elasticindex))

if st.session_state.elasticindex != st.session_state.last_option:
    st.session_state.previous_query=""
    st.session_state.last_option=st.session_state.elasticindex

st.sidebar.write('Export format 💾')
st.sidebar.write('CSV')
st.session_state.chosen = "CSV"








#####################################main panel
V_SPACE(1)
'⬅️ In the control panel you selected to search: ', option

html_string="<p>Typing a search term or phrase without field declaration results in all fields being searched.<br>For example Title:schizo* searches only the specified field; typing the term schizo* alone results in all fields being searched.<br>Here are the fields available for searching in your selected table:</p>"
st.link_button("🛈 Query syntax help", "https://lucene.apache.org/core/2_9_4/queryparsersyntax.html")
with st.expander("🛈 Searchable fields for '{}'".format(option)):
    st.markdown(html_string, unsafe_allow_html=True)
    st.write(st.session_state.fieldinfo)

# You can access the value at any point with:




if st.text_input("Enter search query 🔎", key="query_{}".format(option), placeholder="Abstract:schizo* AND Authors:*dams"):
    #st.session_state.reload=True
    json_data=get_data(st.session_state["query_{}".format(option)], st.session_state.elasticindex)
    # print(json_data.keys())
    st.session_state.query_df = pd.DataFrame(json_data['response'])
    # print(data_df.head())



    st.text("")
    st.session_state.nhits =st.session_state.query_df.shape[0]
    str(str(st.session_state.nhits)) + ' Results'  # idea: add autmatic search documentation with: time, db status, query
    #str(len(st.session_state.exportindices)) + ' Selected'  #

    if st.session_state.nhits>0:
        if st.session_state["query_{}".format(option)]==st.session_state.previous_query:
            st.session_state.reload = False
        else:
            st.session_state.reload = True
        print(st.session_state.reload)
        print(st.session_state["query_{}".format(option)])
        print(st.session_state.previous_query)
        tablemaker(st.session_state.query_df, option)
        st.session_state.previous_query=st.session_state["query_{}".format(option)]
        #data_df["Select"] = [False for i in data_df.index]




def convert_df(dff):
    print('SHAPE')
    print(dff.shape)
    dff=dff.to_csv(index=False).encode('utf-8')
    return dff

if st.sidebar.button('Prepare export', key='export', type='primary'):
    import time

    start = time.time()

    thisdf = st.session_state.query_df[st.session_state.query_df.index.isin(st.session_state.exportindices)]  # get selected rows from the original input

    if st.session_state.chosen == "CSV":
        output = convert_df(thisdf)
    else:
        output=to_ris(thisdf)

    print(f'Time to convert: {time.time() - start}')

    st.sidebar.download_button("Press to Download",
    output,
    "{}_{}_{}.{}".format("RAPTOR",option,len(st.session_state.exportindices),st.session_state.chosen.lower()),
    "text/csv",
    key='download-results')

    refinfo=set()
    for i, row in thisdf.iterrows():
        refinfo.add("{}$$${}".format(row["revManID"],row["reviewTitle"]))
    with open(raptorlog, 'a') as file:


        file.write("\n{};{};{}".format(datetime.now().strftime('%Y_%m_%d_%H-%M-%S'), st.session_state.elasticindex,
                                       list(refinfo)))  # Date,Table,Studyids



V_SPACE(3)

st.video("https://youtu.be/Em6vD6KYuMQ?si=BzFunzhXuiUXTpAu")





