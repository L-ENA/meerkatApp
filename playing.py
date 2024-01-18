"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
##############################################sortable table
# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })
#
# df
#
# "Hi there, this is a variable"

#######################################highlight max cells
# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))
#
# st.dataframe(dataframe.style.highlight_max(axis=0))
######################################plot stuff
# import streamlit as st
# import numpy as np
# import pandas as pd
#
# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])
#
# st.line_chart(chart_data)
##################################maps
# import streamlit as st
# import numpy as np
# import pandas as pd
#
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])
#
# st.map(map_data)
###############################widgets slider
# import streamlit as st
# x = st.slider('bla')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
############################user input
# import streamlit as st
# st.text_input("Enter search query", key="query")
#
# # You can access the value at any point with:
# st.session_state.query
#############################checkbox to hide stuff
#
# import streamlit as st
# import numpy as np
# import pandas as pd
#
# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns=['a', 'b', 'c'])
#
#     chart_data
    ######################################singlechoice
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option