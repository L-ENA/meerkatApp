import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
from utils import tablemaker

####################session state variables
# if 'num_export' not in st.session_state:
#     st.session_state['num_export']=0


st.markdown("# Simple Table Search ")
st.sidebar.markdown("# Simple Table Search ")



st.sidebar.write("## 🛠️ Control Panel 🛠️ ️\n")
#############################table selection
"The Table search page can be used to search information within the tables belonging to Meerkat, the Cochrane Schizophrenia Group's study-based register. Select a table, for example 'Reports', 'Studies', 'Interventions', 'Outcomes', and many more."

tables = pd.DataFrame({
    'first column': ['Reports', 'Studies', 'Interventions']
    })
option = st.sidebar.selectbox(
    'Select a table to search 👇',
    tables['first column'],
    index=0)

################################export
"\n\n"
chosen= st.sidebar.radio(
        'Export format 💾',
        ("RIS", "CSV"))
st.sidebar.divider()


st.sidebar.button('Download results', key='export', type='primary')
#####################################main panel
st.divider()
'⬅️ You selected to search: ', option
st.divider()

st.text_input("Enter search query", key="query")

# You can access the value at any point with:


###################################show results and select hits

if st.session_state.query:
    data_df = pd.DataFrame(
        {
            "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
            "numbers": [1,11,111,1111],
        })



    st.text("")
    str(str(data_df.shape[0])) + ' Results'  # idea: add autmatic search documentation with: time, db status, query

    tablemaker()
    #data_df["Select"] = [False for i in data_df.index]


    ########################### Function to reset checkbox states




