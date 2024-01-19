import streamlit as st
import pandas as pd

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

################################export format
"\n\n"
chosen= st.sidebar.radio(
        'Export format 💾',
        ("RIS", "CSV"))

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

    if st.session_state.get('selectall'):
        data_df["Select"] = [True for i in data_df.index]

    st.text("")
    str(str(data_df.shape[0])) + ' Results'  # idea: add autmatic search documentation with: time, db status, query
    data_df["Select"]=[False for i in data_df.index]
    cols=list(data_df.columns)
    cols=[c for c in cols if c != "Select"]
    st.button('Select all', key='selectall')


    st.data_editor(
        data_df,
        column_config={
            "Select": st.column_config.CheckboxColumn(
                "Select hits",
                help="Select data to export",
                default=False,
            )
        },
        disabled=cols,
        hide_index=True,
    )

    if sum(data_df["Select"])>1:
        st.sidebar.button("Download Results", type='primary')



    #df



