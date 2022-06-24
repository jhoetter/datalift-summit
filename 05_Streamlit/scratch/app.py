import streamlit as st
import numpy as np
import pandas as pd
import requests
import json

# This HTML will be used to render the stories
CARD_HTML = """
<div class="card">
    <div class="container">
        <h4><b>$TITLE</b></h4>
        <p>$TEXT</p>
    </div>
</div>"""

# Variable where your fastAPI-service is running
LOCALHOST = "http://127.0.0.1:8000"

# Streamlit CSS Hack - Executing this will set the css properties for the rest of the app
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("streamlit.css")

# ++++++++++++++++++++++++++++++++
# ++++++++ UTIL FUNCTIONS ++++++++
# ++++++++++++++++++++++++++++++++



# ++++++++++++++++++++++++++++++
# ++++++++ API REQUESTS ++++++++
# ++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++++++
# ++++++++ LOADING INITIAL DATA ++++++++
# ++++++++++++++++++++++++++++++++++++++



# +++++++++++++++++++++++++
# ++++++++ SIDEBAR ++++++++
# +++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++++
# ++++++++ REC AND SIM SEARCH ++++++++
# ++++++++++++++++++++++++++++++++++++

        

# +++++++++++++++++++++++++++++++
# ++++++++ STORY BROWSER ++++++++
# +++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++
# ++++++++ FULL HTML VIEWER ++++++++
# ++++++++++++++++++++++++++++++++++


        
