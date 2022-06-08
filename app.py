import streamlit as st
import numpy as np
import pandas as pd
from card_html import CARD_HTML

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("streamlit.css")

st.header("Newsletter Dashboard")

@st.cache()
def get_random_data():
    return np.random.randn(50, 3)

@st.cache()
def read_dataframe(path, sep=","):
    df = pd.read_csv(path, sep=sep)
    return df

@st.cache()
def replace_html_template(title, body):
    return CARD_HTML.replace("$TITLE", title).replace("$TEXT", body)

def get_session_state_value(key : str):
    # Initialization
    if key not in st.session_state:
        return False
    else:
        return st.session_state[key]

col1, col2 = st.columns(2)

df = read_dataframe("real_mails_20_05_22.csv")

# Left-hand side consists of the filtering options and newsletter browser
with col1:
    # Filtering options
    with st.container():
        # st.write("Filtering options")
       
        # TODO add callback function
        topic_options = st.multiselect(
            'Topic selection',
            ['Stock market', 'AI', 'Ethics'],
            [],
            key = "selected_topics")

        #update_session_state("selected_topics", topic_options)

        # TODO add callback function
        newsletter_options = st.multiselect(
            'Newsletter selection',
            ['info@odsc.com', 'Deeplearning Weekly', 'NBC26'],
            [],
            key = "selected_newsletters")

        #update_session_state("selected_newsletters", newsletter_options)
        print(newsletter_options)
        print(st.session_state)

    # Newsletter Browser
    with st.container():
        # st.write("Newsletter Story Browser")
        # st.dataframe(read_dataframe("real_mails_20_05_22.csv"))
        for i in range(10):
            sample = df.sample(1)
            st.markdown(replace_html_template(sample["subject"].item(), sample["text"].item()), unsafe_allow_html=True)


# Right-hand side consists of the pick of the day and the full HTML view of the selected newsletter
with col2:
    sample = df.sample(1)
    # Pick of the day
    with st.container():
        st.write(st.session_state)
        # st.write("Pick of the day")
        st.markdown("**This is a headline.**")
        st.markdown("And this is the corresponding Article to it. Lorem Ipsum")

    with st.container():
        # st.info("Test")
        st.components.v1.html(sample["content"].item(), width=None, height=512, scrolling=True)

        