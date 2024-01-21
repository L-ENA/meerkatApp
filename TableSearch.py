import streamlit as st
import pandas as pd
from utils import tablemaker
import requests
import json

####################session state variables
# if 'num_export' not in st.session_state:
#     st.session_state['num_export']=0

if 'reload' not in st.session_state:
    st.session_state.reload = False
if 'previous_query' not in st.session_state:
    st.session_state.previous_query = ""
if 'elasticindex' not in st.session_state:
    st.session_state.elasticindex = ""
if 'nhits' not in st.session_state:
    st.session_state.nhits = 0


st.markdown("# Simple Table Search ")
st.sidebar.markdown("# Simple Table Search ")



st.sidebar.write("## 🛠️ Control Panel 🛠️ ️\n")
#############################table selection
"The Table search page can be used to search information within the tables belonging to Meerkat, the Cochrane Schizophrenia Group's study-based register. Select a table, for example 'Reports', 'Studies', 'Interventions', 'Outcomes', and many more."

tables = pd.DataFrame({
    'first column': ['Reports', 'Studies', 'Interventions','Outcomes', 'Health Conditions']
    })
option = st.sidebar.selectbox(
    'Select a table to search 👇',
    tables['first column'],
    index=0)
if option=='Reports':
    st.session_state.elasticindex='tblreport'
elif option=='Studies':
    st.session_state.elasticindex='tblstudy'
elif option=='Outcomes':
    st.session_state.elasticindex='tbloutcome'
elif option=='Interventions':
    st.session_state.elasticindex='tblintervention'
elif option=='Health Conditions':
    st.session_state.elasticindex='tblhealthcarecondition'

if 'export{}'.format(option) not in st.session_state:
    st.session_state['export{}'.format(option)] = pd.DataFrame()
################################export
"\n\n"
if st.session_state.elasticindex=='tblreport':
    chosen= st.sidebar.radio(
            'Export format 💾',
            ("RIS", "CSV"))
else:
    st.sidebar.write('Export format 💾')
    st.sidebar.write('CSV')
st.sidebar.divider()


#st.sidebar.button('Download results', key='export', type='primary')

def convert_df(dff):
    print('SHAPE')
    print(dff.shape)
    dff=dff.to_csv(index=False).encode('utf-8')

    return dff


csv = convert_df(st.session_state['export{}'.format(option)])

st.sidebar.download_button(
   "Press to Download",
   csv,
   "{}_{}.csv".format(option,st.session_state.nhits),
   "text/csv",
   key='download-csv'
)



#####################################main panel
st.divider()
'⬅️ You selected to search: ', option
st.divider()

st.text_input("Enter search query", key="query_{}".format(option), placeholder="Abstract:schizo* AND Authors:*dams")

# You can access the value at any point with:


###################################show results and select hits

if st.session_state["query_{}".format(option)]:
    #st.session_state.reload=True
    res = requests.post('http://localhost:9090/api/direct_retrieval',json={"input": st.session_state["query_{}".format(option)], "index": st.session_state.elasticindex})
    print(res)
    json_data = json.loads(res.text)
    # print(json_data.keys())
    data_df = pd.DataFrame(json_data['response'])
    # print(data_df.head())



    st.text("")
    st.session_state.nhits =data_df.shape[0]
    str(str(st.session_state.nhits)) + ' Results'  # idea: add autmatic search documentation with: time, db status, query

    if st.session_state["query_{}".format(option)]==st.session_state.previous_query:
        st.session_state.reload = False
    else:
        st.session_state.reload = True
    print(st.session_state.reload)
    print(st.session_state["query_{}".format(option)])
    print(st.session_state.previous_query)
    tablemaker(data_df, option)
    st.session_state.previous_query=st.session_state["query_{}".format(option)]
    #data_df["Select"] = [False for i in data_df.index]


    ########################### Function to reset checkbox states




