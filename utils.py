import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode

def gbmaker(ddf):
    gb = GridOptionsBuilder.from_dataframe(ddf, min_column_width=100)
    return gb

def tablemaker(df, this_key):
    if 'sid{}'.format(this_key) not in st.session_state:
        st.session_state['sid{}'.format(this_key)] = None





    df.insert(loc=0, column='Select', value=["" for i in list(df.index)])


    gb=gbmaker(df)

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
    # st.session_state['export{}'.format(this_key)] = pd.DataFrame(selected_rows)
    # #print(selected_rows)
    print(len(selected_rows))
    #x=[print(r) for r in selected_rows]
    myindices=[ i['_selectedRowNodeInfo']['nodeRowIndex'] for i in selected_rows]
    st.session_state.exportindices=myindices
    # print(myindices)
        #
        # {'_selectedRowNodeInfo': {'nodeRowIndex': 3, 'nodeId': '3'}, 'Select': '',
        #  'InterventionDescription': 'Form - Risperidone (Oral)', 'InterventionID': 12851}

    # print(st.session_state['export{}'.format(this_key)].shape)





    # Save the row index of the selected row.
    if len(selected_rows):
        ind = selected_rows[0]['_selectedRowNodeInfo']['nodeRowIndex']
        st.session_state.sid = ind

    if len(selected_rows) != 0:
        selected_rows[0]

def adding(lines,key, value):
    if len(value)>0:
        lines.append("{}  - {}".format(key,value.strip()))
    return lines

def to_ris(df):
    lines = []
    for i,row in df.iterrows():
        lines.append('TY  - JOUR')
        lines=adding(lines,"T1", str(row["Title"]))
        lines = adding(lines, "N2", str(row["Abstract"]))
        for a in row["Authors"].split("//"):
            lines = adding(lines, "A1", str(a))
        lines = adding(lines, "IS", str(row["Issue"]))
        lines = adding(lines, "VL", str(row["Volume"]))

        lines = adding(lines, "JO", str(row["Journal"]))
        lines = adding(lines, "SP", str(row["Pages"]))
        lines = adding(lines, "PY", str(row["Year"]))

        lines = adding(lines, "AD", str(row["UDef3"]))
        lines = adding(lines, "SN", str(row["UDef4"]))
        lines = adding(lines, "DO", str(row["UDef2"]))
        lines = adding(lines, "ET", str(row["Edition"]))
        lines = adding(lines, "ID", str(row["CRGReportID"]))

        lines.append('ER  - ')
        lines.append("")

    lines='\n'.join(lines)
    return lines






outcomefields=["OutcomeID",	"OutcomeDescription"]
interventionfields=["InterventionID",	"InterventionDescription"]
conditionfields=["HealthCareConditionID",	"HealthCareConditionDescription"]
studyfields=["CENTRALStudyID","CRGStudyID","ShortName","StatusofStudy","TrialistContactDetails","CENTRALSubmissionStatus","Notes","DateEntered","DateToCENTRAL","DateEdited","Search_Tagged","UDef1","UDef2","UDef3","UDef4","UDef5","ISRCTN","UDef6","UDef7","UDef8","UDef9","UDef10"]
reportfields=["Abstract","Authors","CENTRALReportID","CENTRALSubmissionStatus","CRGReportID","City","CopyStatus","DateEdited","Dateentered","DatetoCENTRAL","DupString","Edition","Editors","Issue","Journal","Language","Medium","Notes","OriginalTitle","Pages","PublicationTypeID","Publisher","ReportNumber","Title","TypeofReportID","UDef1","UDef10","UDef2","UDef3","UDef4","UDef5","UDef6","UDef7","UDef8","UDef9","Volume","Year"]