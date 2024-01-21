import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode


def tablemaker(df, this_key):
    if 'sid{}'.format(this_key) not in st.session_state:
        st.session_state['sid{}'.format(this_key)] = None





    df.insert(loc=0, column='Select', value=["" for i in list(df.index)])

    gb = GridOptionsBuilder.from_dataframe(df,min_column_width=100)

    # Add pre_selected_rows param.
    gb.configure_selection(selection_mode="multiple", use_checkbox=True,
                           pre_selected_rows=[st.session_state['sid{}'.format(this_key)]])
    gb.configure_column("Select", headerCheckboxSelection = True)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_side_bar()
    gridOptions = gb.build()

    # Add key.
    data = AgGrid(df,
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                  #columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                  fit_columns_on_grid_load=True,
                  reload_data=st.session_state.reload,
                  key=this_key)

    selected_rows = data["selected_rows"]
    st.session_state['export{}'.format(this_key)] = pd.DataFrame(selected_rows)
    #print(selected_rows)
    print(len(selected_rows))
    print(st.session_state['export{}'.format(this_key)].shape)





    # Save the row index of the selected row.
    if len(selected_rows):
        ind = selected_rows[0]['_selectedRowNodeInfo']['nodeRowIndex']
        st.session_state.sid = ind

    if len(selected_rows) != 0:
        selected_rows[0]


