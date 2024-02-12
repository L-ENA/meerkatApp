import requests
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
import base64
import json
import pandas as pd

def V_SPACE(lines):
    for _ in range(lines):
        st.write('&nbsp;')

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

        #####################add a notes field

        study=row.get("CRGStudyID", False)
        if study:
            notes="This record belongs to study <{}>.".format(study)
        else:
            notes="This is a single record. Use the Study search tab on the MK-2 website to retrieve all assonciated reports. On study search, keep the automatically selected 'Reports' setting and use this query: CRGReportID:{}".format(str(row["CRGReportID"]))

        lines.append("N1  - {}".format(notes))
        lines.append('ER  - ')
        lines.append("")

    lines='\n'.join(lines)
    return lines


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def build_markup_for_logo(
    png_file,
    background_position="60% 10%",
    margin_top="1%",
    image_width="40%",
    image_height="",
):
    binary_string = get_base64(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
                [data-testid="stSidebarNav"]::before {
                content: "MK-2";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file, imsize):
    logo_markup = build_markup_for_logo(png_file,image_width=imsize)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

###################################show results and select hits
@st.cache_data
def get_data(q,ind):
    res = requests.post('http://localhost:9090/api/direct_retrieval',
                        json={"input": q,
                              "index": ind})
    print(res)
    json_data = json.loads(res.text)
    return json_data

@st.cache_data
def get_study_data(q, ind):
    res = requests.post('http://localhost:9090/api/direct_retrieval',
                        json={"input": q,
                              "index": ind})
    print(res)
    json_dat = json.loads(res.text)
    json_data=pd.DataFrame(json_dat['response'])
    print(json_data.columns)
    if json_data.shape[0]>0:

        if ind == 'tblreport':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "report", "input": list(json_data['CRGReportID'])})

        elif ind == 'tblstudy':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "study", "input": list(json_data['CRGStudyID'])})
        elif ind == 'tbloutcome':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "outcome", "input": list(json_data['OutcomeID'])})
        elif ind == 'tblintervention':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "intervention", "input": list(json_data['InterventionID'])})
        elif ind == 'tblhealthcarecondition':
            res = requests.post('http://localhost:9090/api/studyfromanyid', json={"table": "condition", "input": list(json_data['HealthCareConditionID'])})

        j_data = json.loads(res.text)

        return j_data
    else:
        print('-------------no data-------------------------------------')
        return json_dat