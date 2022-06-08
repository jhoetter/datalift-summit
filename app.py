import streamlit as st
import numpy as np
import pandas as pd
from card_html import CARD_HTML

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit CSS Hack - Executing this will set the css properties for the rest of the app
local_css("streamlit.css")

st.header("Newsletter Dashboard")

@st.cache()
def get_random_data():
    return np.random.randn(50, 3)

@st.cache()
def read_dataframe(path, sep=","):
    df = pd.read_csv(path, sep=sep).sort_values("date", ascending=False)
    return df

@st.cache()
def get_filtered_dataframe(df, topics, newsletters) -> pd.DataFrame:
    # TODO add topic selection when it is added to the data
    return df.loc[(df["from"].isin(newsletters))]

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
        # TODO add callback function
        topic_options = st.multiselect(
            'Topic selection',
            ['Stock market', 'AI', 'Ethics'],
            [],
            key = "selected_topics")

        # TODO add callback function
        newsletter_options = st.multiselect(
            'Newsletter selection',
            df["from"].unique().tolist(),
            [],
            key = "selected_newsletters")

    # Newsletter Story Browser
    with st.container():
        selected_topics = get_session_state_value("selected_topics")
        selected_newsletters = get_session_state_value("selected_newsletters")

        dataframe_to_display = get_filtered_dataframe(df, selected_topics, selected_newsletters)
        print(dataframe_to_display.shape)
        for i, row in dataframe_to_display.iterrows():
            
            st.markdown(replace_html_template(row["subject"], row["text"]), unsafe_allow_html=True)


# Right-hand side consists of the pick of the day and the full HTML view of the selected newsletter
with col2:
    sample = df.sample(1)
    # Pick of the day
    with st.container():
        st.write(st.session_state)
 
        st.markdown("**This is a headline.**")
        st.markdown("And this is the corresponding Article to it. Lorem Ipsum")

    with st.container():
        st.components.v1.html(sample["content"].item(), width=None, height=1024, scrolling=True)
