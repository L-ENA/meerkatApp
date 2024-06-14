import streamlit as st
import pandas as pd
from utils import *
from config import *
import requests
import json
from datetime import datetime
from annotated_text import annotated_text, annotation
import shutil

#http://localhost:8501/MK-2_PICO_Search

if 'last_page' not in st.session_state or st.session_state.last_page != "PICO":
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
"The PICO search is an interactive way to search MK-2 by PICOs (Population, Intervention/Control, Outcome), defined within the MK-2 structured vocabulary and hand-curated by an information specialist (with the exception of outcomes)."
V_SPACE(1)
"This search builder interface allows users to build boolean queries to search MK-2, for example for studies comparing two selected interventions. The study population within MK-2 trials is people with schizophrenia, but whenever a related health condition other than schizophrenia is present then this can be filtered by using 'Health Conditions' (eg. psychosis, schizoaffective)."
V_SPACE(1)
"Outcomes were curated manually in the past, but may be less structured or incomplete for recent trials. We therefore don't recomment using outcomes in the query builder when setting up a systematic serch, as this information may only be useful for initial scoping for reviews focussing on specific outcomes. Please also see the 'Raptor Data Search' tab on the left for a searchable version of all extracted outcome data from the schizophrenia reviews."
V_SPACE(1)
"For more information, see the tutorial video on the bottom of this page."



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
    st.session_state.submitted=False




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

def submission():
    st.session_state.submitted=True

with col1:
    st.button("Add selection", on_click=add_pico)
with col2:
    st.button("Submit search", on_click=submission)

with col3:
    st.button("⚠️Delete this search", on_click=clear_all)

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
    ##################################################################

for i, sd in enumerate(st.session_state.searchdoc):
    if i != 0:
        annotated_text(annotation("AND", "","#faf", border="2px dashed red"))
    annotated_text(sd)

if st.session_state.submitted:
    final_studies=set()#using a python set to combine search results (AND operation)
    dfs=[]
    options=[]
    queries=[]
    for pgrp in st.session_state.picogroups:#create a query for each term selection
        myvals=["\"{}\"".format(l.strip()) for l in list(pgrp.values())[0]]
        query=" OR ".join(myvals)
        print("Query is "+query)
        queries.append(query)
        option=list(pgrp.keys())[0]#table to search
        options.append(option)
        #st.session_state["query_{}".format(option)]=query

    opp=" ".join(options)#to be compatible with previous code that compared these variables in the table updating
    que = " ".join(queries)
    st.session_state["query_{}".format(opp)] = que

    if st.session_state["query_{}".format(opp)] != st.session_state.previous_query:
        for i, o in enumerate(options):
            json_data = get_study_data(queries[i], o)
            # print(json_data.keys())
            dfs.append(pd.DataFrame(json_data['response']))
            # print(data_df.head())

        tokeep=set(dfs[0]["CRGStudyID"])######only keep studies that appear in all queries
        for d in dfs:
            tokeep=tokeep.intersection(set(d["CRGStudyID"]))#only keep the study ID if it was already present in the previous df
        mydf=dfs[0][dfs[0]["CRGStudyID"].isin(list(tokeep))]#keep only studies that intersected in all dfs
        mydf=mydf.reset_index(drop=True)
        st.session_state.query_df = mydf
        st.text("")
        st.session_state.nhits = st.session_state.query_df.shape[0]
        str(str(
            st.session_state.nhits)) + ' Results'  # idea: add autmatic search documentation with: time, db status, query
        # str(len(st.session_state.exportindices)) + ' Selected'  #

        # print('ddb')
        # print(st.session_state["query_{}".format(option)])
        # print(st.session_state.previous_query)
        # print(st.session_state["query_{}".format(option)] == st.session_state.previous_query)


    if st.session_state.nhits > 0:
        if st.session_state["query_{}".format(opp)] == st.session_state.previous_query:
            st.session_state.reload = False
            print("reload is false")
        else:
            st.session_state.reload = True
            print("reload is true")
        # print("----debug stuff-----")
        # print(option)
        # print(st.session_state.reload)
        # print(st.session_state["query_{}".format(opp)])
        # print(st.session_state.previous_query)
        tablemaker(st.session_state.query_df, opp)
        st.session_state.previous_query = st.session_state["query_{}".format(opp)]
        # data_df["Select"] = [False for i in data_df.index]
        # st.session_state.tbm=thistbl




##########################################export stuff

if st.sidebar.button('Export', key='export', type='primary'):
    import time

    start = time.time()

    thisdf = st.session_state.query_df[st.session_state.query_df.index.isin(st.session_state.exportindices)]  # get selected rows from the original input
    time_name = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
    print("--------------------debug export-------------")
    print(st.session_state.query_df.shape)
    print(thisdf.head())
    print(st.session_state.exportindices)
    print("--------------------debug export-------------")
    if st.session_state.chosen == "CSV":
        output = convert_df(thisdf)
        #print(f'Time to convert: {time.time() - start}')


    elif st.session_state.chosen == "RIS":
        reportdf=get_reports(thisdf)
        output=to_ris(reportdf)
        #print(f'Time to convert: {time.time() - start}')


    else:
        output_csv = convert_df(thisdf)  # csv study file
        reportdf = get_reports(thisdf)
        output_ris = to_ris(reportdf)


        tmp_name = os.path.join(tmppath, time_name)
        try:
            os.mkdir(tmp_name)
            # print(os.path.exists(tmp_name))

        except:
            print(tmp_name, ' exists or error in creating it')
        with open(os.path.join(tmp_name, "all.ris"), "w", encoding='utf-8') as f:
            f.write(output_ris)
        # output_csv.to_csv(os.path.join(tmp_name, "study_overview.csv"), index=False)
        thisdf.to_csv(os.path.join(tmp_name, "study_overview.csv"), index=False)


        ids = reportdf['CRGStudyID'].unique()
        for i in ids:
            tmpdf = reportdf[reportdf['CRGStudyID'] == i]
            tmp_ris = to_ris(tmpdf)
            subfolder = os.path.join(tmp_name, str(i))
            try:
                os.mkdir(subfolder)
            except:
                print(subfolder, " already existed")
            with open(os.path.join(subfolder, "study_{}_references.ris".format(i)), "w", encoding='utf-8') as f:
                f.write(tmp_ris)


        zipped = "{}.zip".format(tmp_name)

        # with zipfile.ZipFile(zipped, 'w') as f:
        #     for file in glob.glob('{}/*'.format(tmp_name)):
        #         f.write(file)

        zip(tmp_name, zipped)


        with open(zipped, "rb") as fp:
            btn = st.sidebar.download_button(
                label="Download ZIP",
                data=fp,
                file_name="{}_{}.zip".format(option, len(st.session_state.exportindices)),
                mime="application/zip"
            )

        shutil.rmtree(tmppath)
        if not os.path.exists(tmppath):
            os.mkdir(tmppath)
        # output_csv = convert_df(thisdf)#csv study file
        # reportdf = get_reports(thisdf)
        # output_ris = to_ris(reportdf)
        # print(output_ris)
        # print(" 6 Made files: {} {}".format(len(reportdf.index), len(output_ris)))
        #
        #
        # tmp_name=os.path.join(tmppath,time_name)
        # print("----------------------{}".format(tmp_name))
        # try:
        #     os.mkdir(tmp_name)
        #     print(os.path.exists(tmp_name))
        # except:
        #     print(tmp_name, ' exists')
        # with open(os.path.join(tmp_name, "all.ris"), "w", encoding='utf-8') as f:
        #     f.write(output_ris)
        # #output_csv.to_csv(os.path.join(tmp_name, "study_overview.csv"), index=False)
        # thisdf.to_csv(os.path.join(tmp_name, "study_overview.csv"), index=False)
        #
        # ids=reportdf['CRGStudyID'].unique()
        # for i in ids:
        #     tmpdf=reportdf[reportdf['CRGStudyID']==i]
        #     tmp_ris = to_ris(tmpdf)
        #     subfolder=os.path.join(tmp_name,str(i))
        #     try:
        #         os.mkdir(subfolder)
        #     except:
        #         print(subfolder, " already existed")
        #     with open(os.path.join(subfolder, "study_{}_references.ris".format(i)), "w", encoding='utf-8') as f:
        #         f.write(tmp_ris)
        #
        # zipped="{}.zip".format(tmp_name)
        #
        # zip(tmp_name, zipped)
        #
        # with open(zipped, "rb") as fp:
        #     btn = st.sidebar.download_button(
        #         label="Download ZIP",
        #         data=fp,
        #         file_name="{}_{}.zip".format(option, len(st.session_state.exportindices)),
        #         mime="application/zip"
        #     )
        #
        # shutil.rmtree(tmppath)

    if st.session_state.chosen != 'combo':
        st.sidebar.download_button("Press to Download",
                                   output,
                                   "{}_{}.{}".format(option, len(st.session_state.exportindices),
                                                     st.session_state.chosen.lower()),
                                   "text/csv",
                                   key='download-results')

    with open(studylog, 'a') as file:
        file.write("\n{};{};{}".format(time_name, st.session_state.elasticindex,
                                       list(thisdf["CRGStudyID"])))  # Date,Table,Studyids

V_SPACE(3)

st.video("https://youtu.be/7sWau1jv8XU?si=_3I-7P1K66Plmka9")