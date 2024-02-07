import streamlit as st
import pandas as pd
from utils import *
import requests
import json
from datetime import datetime
import os
import zipfile


set_background(pngfile)
add_logo(logofile, "40%")

if 'reload' not in st.session_state:
    st.session_state.reload = False
if 'previous_query' not in st.session_state:
    st.session_state.previous_query = ""
if 'elasticindex' not in st.session_state:
    st.session_state.elasticindex = ""
if 'nhits' not in st.session_state:
    st.session_state.nhits = 0
if 'exportindices' not in st.session_state:
    st.session_state.exportindices = []
if 'query_df' not in st.session_state:
    st.session_state.query_df = pd.DataFrame()
if 'fieldinfo' not in st.session_state:
    st.session_state.fieldinfo = ", ".join(reportfields)
if 'chosen' not in st.session_state:
    st.session_state.chosen = "CSV"

st.markdown("# Study Search ️")
st.sidebar.markdown("# Study Search ️")





st.sidebar.write("## 🛠️ Control Panel 🛠️ ️\n")
#############################table selection
"The study search page can be used to retrieve data from whole studies. Please see the tutorial video on the bottom of this page."

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
            ( "Study CSV flat", "Report RIS flat","Structured Data"))
if chosen=='Report RIS flat':
        st.session_state.chosen = "RIS"
elif chosen=='Study CSV flat':
        st.session_state.chosen = "CSV"
else:
    st.session_state.chosen='combo'








#####################################main panel
st.markdown('##')
'⬅️ In the control panel you selected to search: ', option

html_string="<p>Typing a search term or phrase without field declaration results in all fields being searched.<br>For example Title:schizo* searches only the specified field; typing the term schizo* alone results in all fields being searched.<br>Here are the fields available for searching in your selected table:</p>"
st.link_button("🛈 Query syntax help", "https://lucene.apache.org/core/2_9_4/queryparsersyntax.html")
with st.expander("🛈 Searchable fields for '{}'".format(option)):
    st.markdown(html_string, unsafe_allow_html=True)
    st.write(st.session_state.fieldinfo)

st.markdown('##')


# You can access the value at any point with:


###################################show results and select hits
@st.cache_data
def get_reports(some_df):

    targets=list(some_df["CRGStudyID"])
    ##print("---------------------------------------getting reports for {}".format(targets))
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

# @st.cache_data
# def get_reports(some_df):
#     targets=list(some_df["CRGStudyID"])
#
#     res=requests.post('http://localhost:9090/api/reportsfromstudyid', json={"input":targets})
#     json_dat = json.loads(res.text)
#     new_df = pd.DataFrame(json_dat['response'])
#
#
#     return new_df


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

if st.text_input("## Enter search query 🔎", key="query_{}".format(option), placeholder="Abstract:schizo* AND Authors:*dams"):
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
        print(f'Time to convert: {time.time() - start}')


    elif st.session_state.chosen == "RIS":
        reportdf=get_reports(thisdf)
        output=to_ris(reportdf)
        print(f'Time to convert: {time.time() - start}')


    else:
        output_csv = convert_df(thisdf)#csv study file
        reportdf = get_reports(thisdf)
        output_ris = to_ris(reportdf)
        time_name=datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
        tmp_name=os.path.join(r"C:\Users\c1049033\PycharmProjects\meerkatApp\temp",time_name)
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
        # with zipfile.ZipFile(zipped, 'w') as f:
        #     for file in glob.glob('{}/*'.format(tmp_name)):
        #         f.write(file)

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


        zip(tmp_name, zipped)

        with open(zipped, "rb") as fp:
            btn = st.sidebar.download_button(
                label="Download ZIP",
                data=fp,
                file_name="{}_{}.zip".format(option, len(st.session_state.exportindices)),
                mime="application/zip"
            )

    if st.session_state.chosen != 'combo':
        st.sidebar.download_button("Press to Download",
                                   output,
                                   "{}_{}.{}".format(option, len(st.session_state.exportindices),
                                                     st.session_state.chosen.lower()),
                                   "text/csv",
                                   key='download-results')






