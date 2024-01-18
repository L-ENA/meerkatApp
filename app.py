import streamlit as st
import pandas as pd

st.sidebar.write("Controls\n")
#############################table selection
tables = pd.DataFrame({
    'first column': ['Reports', 'Studies', 'Interventions']
    })
option = st.sidebar.selectbox(
    'Select a table to search',
    tables['first column'],
    index=0)

################################export format
"\n\n"
chosen= st.sidebar.radio(
        'Export format',
        ("RIS", "CSV"))

#####################################main panel
'You selected to search: ', option

st.text_input("Enter search query", key="query")

# You can access the value at any point with:



if st.session_state.query:
    df = pd.DataFrame({
      'first column': [1, 2, 3, 4],
      'second column': [10, 20, 30, 40]
    })

    str(df.shape[0]) + ' Results'#idea: add autmatic search documentation with: time, db status, query

    df


    st.session_state.query
