import streamlit as st
import pandas as pd
from utils import *
from config import *
import requests
import json
from datetime import datetime
from annotated_text import annotated_text, annotation

if st.session_state.last_page != "PICO":
    session_state_init("PICO")
    st.cache_data.clear()

set_background(pngfile)
add_logo(logofile, "40%")
####################session state variables
# if 'num_export' not in st.session_state:
#     st.session_state['num_export']=0




st.markdown("# PICO Search ")


st.sidebar.write("## 🛠️ Control Panel 🛠️ ️\n")
#############################table selection
"The PICO search is an interactive way to search MK-2 by PICOs that were defined within the MK-2 structured vocabulary. Please see the tutorial video on the bottom of this page."


if not "picogroups" in st.session_state:
    st.session_state.picogroups = []
if not "multiselect" in st.session_state:
    st.session_state.multiselect = []
if not "searchdoc" in st.session_state:
    st.session_state.searchdoc = []
if not "picooptions" in st.session_state:
    st.session_state.picooptions={}

    json_data=get_data("*", "tblintervention")
    qdf = pd.DataFrame(json_data['response'])
    st.session_state.picooptions['Intervention']=sorted(list(set(qdf['InterventionDescription'])))

    json_data = get_data("*", "tbloutcome")
    qdf = pd.DataFrame(json_data['response'])
    st.session_state.picooptions['Outcome'] = sorted(list(set(qdf['OutcomeDescription'])))

    json_data = get_data("*", "tblhealthcarecondition")
    qdf = pd.DataFrame(json_data['response'])
    st.session_state.picooptions['Health Condition'] = sorted(list(set(qdf['HealthCareConditionDescription'])))




picooption = st.selectbox(
        "Select PICO",
        ("Intervention", "Outcome", "Health Condition"),
        index=0,
        placeholder="Click here to select",
        key="picooption"
    )

multi = st.multiselect("Search MK-2 {} concepts".format(picooption), st.session_state.picooptions[picooption], key="multiselect")

def clear_multi():
    st.session_state.multiselect = []
    return

def clear_all():
    st.session_state.multiselect = []
    st.session_state.picogroups = []
    st.session_state.searchdoc = []


def submit_all():
    final_studies=set()#using a python set to combine search results (AND operation)
    dfs=[]
    options=[]
    queries=[]
    for pgrp in st.session_state.picogroups:
        query=" OR ".join(list(pgrp.values())[0])
        print("Query is "+query)
        queries.append(query)
        option=list(pgrp.keys())[0]#table to search
        options.append(option)
        #st.session_state["query_{}".format(option)]=query
        json_data = get_study_data(query, option)
        # print(json_data.keys())
        dfs.append(pd.DataFrame(json_data['response']))
        # print(data_df.head())


    st.session_state.query_df = pd.concat(dfs)
    st.text("")
    st.session_state.nhits = st.session_state.query_df.shape[0]
    str(str(
        st.session_state.nhits)) + ' Results'  # idea: add autmatic search documentation with: time, db status, query
    # str(len(st.session_state.exportindices)) + ' Selected'  #
    #option=" ".join(options)#to be compatible with previous code that compared these variables in the table updating
    query = " ".join(queries)
    st.session_state["query_{}".format(option)] = query
    # print('ddb')
    # print(st.session_state["query_{}".format(option)])
    # print(st.session_state.previous_query)
    # print(st.session_state["query_{}".format(option)] == st.session_state.previous_query)
    if st.session_state.nhits > 0:
        if st.session_state["query_{}".format(option)] == st.session_state.previous_query:
            st.session_state.reload = False
            print("reload is false")
        else:
            st.session_state.reload = True
            print("reload is true")
        print("----debug stuff-----")
        print(option)
        print(st.session_state.reload)
        print(st.session_state["query_{}".format(option)])
        print(st.session_state.previous_query)
        tablemaker(st.session_state.query_df, option)
        st.session_state.previous_query = st.session_state["query_{}".format(option)]
        # data_df["Select"] = [False for i in data_df.index]


def add_pico():
    if st.session_state.multiselect !=[]:

        if picooption=="Intervention":#make colored output
            col="#faa"
            tblname="tblintervention"
        elif picooption=="Outcome":
            col = "#afa"
            tblname = "tbloutcome"
        elif picooption=="Health Condition":
            col="#8ef"
            tblname = "tblhealthcarecondition"
        st.session_state.picogroups.append({tblname: st.session_state.multiselect})  # for search

        thislist=[]
        for sel in st.session_state.multiselect:
            thislist.append((sel,picooption,col))
            thislist.append(" OR ")
        del thislist[-1]#delete last OR
        st.session_state.searchdoc.append(thislist)
        #st.session_state.searchdoc.append("{}: {}".format(picooption, " OR ".join(st.session_state.multiselect)))
        clear_multi()
    return
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Add selection", on_click=add_pico)
with col2:
    st.button("Submit search", on_click=submit_all)

with col3:
    st.button("⚠️Delete this search", on_click=clear_all)


for i, sd in enumerate(st.session_state.searchdoc):
    if i != 0:
        annotated_text(annotation("AND", "","#faf", border="2px dashed red"))
    annotated_text(sd)

################################################################Sidebar
chosen= st.sidebar.radio(
            'Export format 💾',
            ( "Study CSV flat", "Report RIS flat","Structured Data"))
if chosen=='Report RIS flat':
        st.session_state.chosen = "RIS"
elif chosen=='Study CSV flat':
        st.session_state.chosen = "CSV"
else:
    st.session_state.chosen='combo'

##########################################export stuff

if st.sidebar.button('Export', key='export', type='primary'):
    import time

    start = time.time()

    thisdf = st.session_state.query_df[st.session_state.query_df.index.isin(st.session_state.exportindices)]  # get selected rows from the original input
    time_name = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')

    if st.session_state.chosen == "CSV":
        output = convert_df(thisdf)
        print(f'Time to convert: {time.time() - start}')


    elif st.session_state.chosen == "RIS":
        reportdf=get_reports(thisdf)
        output=to_ris(reportdf)
        print(f'Time to convert: {time.time() - start}')


    else:
        output_csv = convert_df(thisdf)#csv study file
        reportdf = get_reports(thisdf)
        output_ris = to_ris(reportdf)

        tmp_name=os.path.join(tmppath,time_name)
        print("----------------------{}".format(tmp_name))
        try:
            os.mkdir(tmp_name)
        except:
            print(tmp_name, ' exists')
        with open(os.path.join(tmp_name, "all.ris"), "w", encoding='utf-8') as f:
            f.write(output_ris)
        #output_csv.to_csv(os.path.join(tmp_name, "study_overview.csv"), index=False)
        thisdf.to_csv(os.path.join(tmp_name, "study_overview.csv"), index=False)

        ids=reportdf['CRGStudyID'].unique()
        for i in ids:
            tmpdf=reportdf[reportdf['CRGStudyID']==i]
            tmp_ris = to_ris(tmpdf)
            subfolder=os.path.join(tmp_name,str(i))
            try:
                os.mkdir(subfolder)
            except:
                print(subfolder, " already existed")
            with open(os.path.join(subfolder, "study_{}_references.ris".format(i)), "w", encoding='utf-8') as f:
                f.write(tmp_ris)

        zipped="{}.zip".format(tmp_name)