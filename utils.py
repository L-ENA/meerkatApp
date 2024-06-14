import requests
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
import base64
import json
import pandas as pd
import os
import zipfile
from config import reportfields

def session_state_init(current_page):


    if 'reload' not in st.session_state:  # reloading output tables
        st.session_state.reload = False
    if 'previous_query' not in st.session_state:  # the last query, to make sure table selection state is retained
        st.session_state.previous_query = ""
    if 'elasticindex' not in st.session_state:  # elasticindex to search
        st.session_state.elasticindex = ""
    if 'nhits' not in st.session_state:  # how many hots did the search produce
        st.session_state.nhits = 0
    if 'exportindices' not in st.session_state:  # which rows in the results table were selected for export
        st.session_state.exportindices = []
    if 'query_df' not in st.session_state:  # data table with results
        st.session_state.query_df = pd.DataFrame()
    if 'fieldinfo' not in st.session_state:
        st.session_state.fieldinfo = ", ".join(reportfields)
    if 'chosen' not in st.session_state:
        st.session_state.chosen = "CSV"
    if 'last_option' not in st.session_state:  # the last index that was selected for searching. to determine if previous_query can be reset to ""
        st.session_state.last_option = ""
    if 'submitted' not in st.session_state:  # the last index that was selected for searching. to determine if previous_query can be reset to ""
        st.session_state.submitted = False

    if not "picogroups" in st.session_state:
            st.session_state.picogroups = []
    if not "multiselect" in st.session_state:
            st.session_state.multiselect = []
    if not "searchdoc" in st.session_state:
            st.session_state.searchdoc = []
    if not "picooptions" in st.session_state:
            st.session_state.picooptions = {}

    st.session_state.last_page=current_page

def V_SPACE(lines):
    for _ in range(lines):
        st.write('&nbsp;')

def gbmaker(ddf):
    gb = GridOptionsBuilder.from_dataframe(ddf, min_column_width=100)
    return gb

def tablemaker(df, this_key):
    if 'sid{}'.format(this_key) not in st.session_state:
        st.session_state['sid{}'.format(this_key)] = None




    try:
        df.insert(loc=0, column='Select', value=["" for i in list(df.index)])
    except:
        pass

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
                  enable_enterprise_modules=False,
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

def add_record(lines, i, row):
    ptypes={"1":"Journal article", "2":"Book", "3":"Section of book", "4":"Conference proceedings", "5":"Correspondence", "6":"Computer program", "7":"Unpublished data", "8":"Other", "9": "Cochrane review" }
    pt=str(row["PublicationTypeID"]).strip()
    pt=ptypes.get(pt, "")

    lines.append('TY  - JOUR')
    lines = adding(lines, "T1", str(row["Title"]))
    lines = adding(lines, "OP", str(row["OriginalTitle"]))
    lines = adding(lines, "N2", str(row["Abstract"]))
    for a in row["Authors"].split("//"):
        lines = adding(lines, "A1", str(a))
    lines = adding(lines, "IS", str(row["Issue"]))
    lines = adding(lines, "VL", str(row["Volume"]))

    lines = adding(lines, "JO", str(row["Journal"]))
    lines = adding(lines, "SP", str(row["Pages"]))
    try:
        lines = adding(lines, "PY", str(int(row["Year"])))  # or else we will get a float, ie. year 2022.0
    except:
        lines = adding(lines, "PY", str(row["Year"]))
    lines = adding(lines, "LA", str(row["Language"]))
    lines = adding(lines, "AD", str(row["User defined 3"]))
    lines = adding(lines, "SN", str(row["User defined 4"]))
    lines = adding(lines, "DO", str(row["User defined 2"]))

    lines = adding(lines, "KW", str(row["Language"]))
    lines = adding(lines, "KW", pt)
    lines = adding(lines, "KW", str(row["Language"]))
    # lines = adding(lines, "ET", str(row["Edition"]))

    rep_num = str(row["CRGReportID"])
    if rep_num == "0":
        lines = adding(lines, "ID", "unk_{}".format(i))
        notes = "This is a single record of the type <{}> for which we weren't able to retrieve data or match a study record.".format(pt)


    else:
        lines = adding(lines, "ID", rep_num)
        notes = "This is a single record of the type <{}>. Use the Study search tab on the MK-2 website to retrieve all assonciated reports. On study search, keep the automatically selected 'Reports' setting and use this query: CRGReportID:{}".format(
            pt,str(row["CRGReportID"]))

    #####################add a notes field

    study = row.get("CRGStudyID", False)
    if study:
        notes = "This record of type <{}> belongs to study <{}>.".format(pt,study)

    lines.append("N1  - {}".format(notes))
    lines.append('ER  - ')
    lines.append("")
    return lines

def to_ris(df, ignore_0=True):
    lines = []
    for i,row in df.iterrows():

        if ignore_0:
            if str(row["CRGReportID"])=="0":
                print(str(row["CRGReportID"]))
                pass
            else: lines=add_record(lines, i, row)
        else:
            lines = add_record(lines, i, row)

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


def zip(src, dst):
    zf = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname))
            zf.write(absname, arcname)
    zf.close()


def convert_df(dff):
    print('SHAPE')
    print(dff.shape)
    dff=dff.to_csv(index=False).encode('utf-8')
    return dff

def commenter(q):
    to_comment=["{","}","[","]"]
    for cha in to_comment:
        q=q.replace(cha, "\\"+cha)
    return q
###################################show results and select hits
@st.cache_data(show_spinner=False)
def get_data(q,ind):
    print("------------------")
    print(q)
    print(commenter(q))
    print("------------------")
    res = requests.post('http://localhost:9090/api/direct_retrieval',
                        json={"input": commenter(q),
                              "index": ind})
    print("Response: ")
    print(res)
    json_data = json.loads(res.text)
    return json_data

@st.cache_data(show_spinner=False)
def get_study_data(q, ind):
    res = requests.post('http://localhost:9090/api/direct_retrieval',
                        json={"input": commenter(q),
                          "index": ind})
    print("Response: ")
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

@st.cache_data(show_spinner=False)
def get_reports(some_df):

    targets=list(some_df["CRGStudyID"])
    print("---------------------------------------getting reports for {}".format(targets))
    outdfs=[]
    #ts=[targets[i:i+15] for i in range(0, len(targets), 15)]
    total = len(targets)
    progress_text = "Collected data for 0/{} studies".format(total)
    my_bar = st.sidebar.progress(0, text=progress_text)

    for count, t in enumerate(targets):
        my_bar.progress((count+1)/total, text="Collected data for {}/{} studies".format(count+1,total))
        print(t)
        res=requests.post('http://localhost:9090/api/reportsfromstudyid', json={"input":[t]})
        #print(res)
        #print(res.text)
        json_dat = json.loads(res.text)
        new_df = pd.DataFrame(json_dat['response'])

        # print("xxxxx")
        # print(list(new_df['CRGReportID']))
        # print(new_df.shape)
        # print(json_dat['reportids'])

        #print(json_dat['studyids'])


        #new_df['CRGStudyID'] = json_dat['studyids']
        new_df['CRGStudyID'] = t
        outdfs.append(new_df)
    new_df=pd.concat(outdfs)
    #print(new_df.shape)
    return new_df