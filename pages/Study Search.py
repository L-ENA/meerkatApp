import streamlit as st
import pandas as pd
from utils import *
import requests
import json

st.markdown("# Study Search ️")
st.sidebar.markdown("# Study Search ️")





st.sidebar.write("## 🛠️ Control Panel 🛠️ ️\n")
#############################table selection
"The study search page can be used ....."

tables = pd.DataFrame({
    'first column': ['Reports', 'Studies', 'Interventions','Outcomes', 'Health Conditions']
    })
option = st.sidebar.selectbox(
    'Select a table to search 👇',
    tables['first column'],
    index=0)
if option=='Reports':
    st.session_state.elasticindex='tblreport'
    st.session_state.fieldinfo =", ".join(reportfields)

elif option=='Studies':
    st.session_state.elasticindex='tblstudy'
    st.session_state.fieldinfo = ", ".join(studyfields)
elif option=='Outcomes':
    st.session_state.elasticindex='tbloutcome'
    st.session_state.fieldinfo = ", ".join(outcomefields)
elif option=='Interventions':
    st.session_state.elasticindex='tblintervention'
    st.session_state.fieldinfo = ", ".join(interventionfields)
elif option=='Health Conditions':
    st.session_state.elasticindex='tblhealthcarecondition'
    st.session_state.fieldinfo = ", ".join(conditionfields)

if 'export{}'.format(option) not in st.session_state:
    st.session_state['export{}'.format(option)] = pd.DataFrame()
################################export
"\n\n"
chosen= st.sidebar.radio(
            'Export format 💾',
            ("RIS", "CSV"))
if chosen=='RIS':
        st.session_state.chosen = "RIS"
else:
        st.session_state.chosen = "CSV"

st.sidebar.divider()







#####################################main panel
st.divider()
'⬅️ You selected to search: ', option
st.divider()
html_string="<p>Typing a search term or phrase without field declaration results in all fields being searched.<br>For example Title:schizo* searches only the specified field; typing the term schizo* alone results in all fields being searched.<br>Here are the fields available for searching in your selected table:</p>"
st.link_button("🛈 Query syntax help", "https://lucene.apache.org/core/2_9_4/queryparsersyntax.html")
with st.expander("🛈 Searchable fields for '{}'".format(option)):
    st.markdown(html_string, unsafe_allow_html=True)
    st.write(st.session_state.fieldinfo)
st.divider()


# You can access the value at any point with:


###################################show results and select hits
@st.cache_data
def get_data(q):
    res = requests.post('http://localhost:9090/api/direct_retrieval',
                        json={"input": q,
                              "index": st.session_state.elasticindex})
    print(res)
    json_dat = json.loads(res.text)
    json_data=pd.DataFrame(json_dat['response'])
    print(json_data.columns)
    if json_data.shape[0]>0:

        if st.session_state.elasticindex == 'tblreport':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "report", "input": list(json_data['CRGReportID'])})

        elif st.session_state.elasticindex == 'tblstudy':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "study", "input": list(json_data['CRGStudyID'])})
        elif st.session_state.elasticindex == 'tbloutcome':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "outcome", "input": list(json_data['OutcomeID'])})
        elif st.session_state.elasticindex == 'tblintervention':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "intervention", "input": list(json_data['InterventionID'])})
        elif st.session_state.elasticindex == 'tblhealthcarecondition':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "condition", "input": list(json_data['HealthCareConditionID'])})

        j_data = json.loads(res.text)

        return j_data
    else:
        print('-------------no data-------------------------------------')
        return json_dat

if st.text_input("Enter search query", key="query_{}".format(option), placeholder="Abstract:schizo* AND Authors:*dams"):
    #st.session_state.reload=True
    json_data=get_data(st.session_state["query_{}".format(option)])
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

if st.sidebar.button('Export', key='export', type='primary'):
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
    "{}_{}.{}".format(option,len(st.session_state.exportindices),st.session_state.chosen.lower()),
    "text/csv",
    key='download-results')


