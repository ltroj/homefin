# -*- coding: utf-8 -*-
"""Dashboard Landing Page."""

import streamlit as st
import time
import json

# Set wide mode by default
st.set_page_config(page_title='homefin.py', page_icon="📊", layout="wide")

# Reset widget_values
widget_values = {}

with st.sidebar:
    # Upload button
    uploaded_file = st.file_uploader("Load inputs from file", type="json", accept_multiple_files=False)
    if uploaded_file is not None:  # if settings file is uploaded use these values
        widget_values = json.loads(uploaded_file.getvalue())
        # Write to session_state
        for key in widget_values:
            st.session_state[key] = widget_values[key]

    else:  # use default values but replace with modified values which are stored in session_state
        with open('defaults.json') as f:
            widget_values = json.load(f)
        # st.write("st.session_state")
        # st.write(st.session_state)
        for key in widget_values:
            if key not in st.session_state:
                st.session_state[key] = float(widget_values[key])

        # st.write("st.session_state")
        # st.write(st.session_state)

for key in widget_values:
    widget_values[key] = st.session_state[key]

# st.write("widget_values")
# st.write(widget_values)
with st.sidebar:
    # Download button
    widget_values_json = json.dumps(widget_values, sort_keys=True, indent=4)
    st.download_button("Save inputs to file", widget_values_json, file_name=time.strftime("%Y%m%d-%H%M%S")+"_homefin.json")

tab1, tab2 = st.tabs(["English", "Deutsch"])

with tab1:

    st.markdown(
        r"""
        # homefin.py 📊

        ## Personal toolbox for monetary decisions

        ### Resources
        - [numpy-financial](https://numpy.org/numpy-financial/latest/index.html)
        - [Github Repo](https://github.com/ltroj/)
        - [Current mortgage interest rates](https://www.baufi24.de/tagesaktuelle-hypothekenzinsen/)

        ### How to use
        **👈 Select a page from the sidebar** to enter calculations

    """
    )

with tab2:

    st.markdown(
        r"""
        # homefin.py 📊

        *Coming soon*
    """
    )
