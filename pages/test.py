import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode


if 'sid' not in st.session_state:
    st.session_state.sid = None

if 'pagenum' not in st.session_state:
    st.session_state.pagenum = 15

number = st.number_input("Results per page", value=15, placeholder="15")
if number:
    st.session_state.pagenum =number
df=pd.read_csv(r'C:\Users\c1049033\PycharmProjects\UNICEF_textmining\changestrategies\v3.csv').fillna("")
df.insert(loc=0, column='Select', value=["" for i in list(df.index)])

gb = GridOptionsBuilder.from_dataframe(df)

# Add pre_selected_rows param.
gb.configure_selection(selection_mode="multiple", use_checkbox=True,
                       pre_selected_rows=[st.session_state.sid])
gb.configure_column("Select", headerCheckboxSelection = True)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=st.session_state.pagenum)
gb.configure_side_bar()
gridOptions = gb.build()

# Add key.
data = AgGrid(df,
              gridOptions=gridOptions,
              enable_enterprise_modules=True,
              allow_unsafe_jscode=True,
              update_mode=GridUpdateMode.SELECTION_CHANGED,
              columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,

              key='mykey')

selected_rows = data["selected_rows"]


# Save the row index of the selected row.
if len(selected_rows):
    ind = selected_rows[0]['_selectedRowNodeInfo']['nodeRowIndex']
    st.session_state.sid = ind

if len(selected_rows) != 0:
    selected_rows[0]