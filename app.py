import streamlit as st
import numpy as np
import pandas as pd
from card_html import CARD_HTML
import requests

LOCALHOST = "http://127.0.0.1:8000"

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit CSS Hack - Executing this will set the css properties for the rest of the app
local_css("streamlit.css")

@st.cache()
def get_random_data():
    return np.random.randn(50, 3)

@st.cache()
def read_dataframe(path, sep=",") -> pd.DataFrame:
    df = pd.read_csv(path, sep=sep).sort_values("date", ascending=False)
    return df

@st.cache()
def get_filtered_dataframe(df, topics, newsletters) -> pd.DataFrame:
    # TODO add topic selection when it is added to the data
    # add checks if topics and newsletters are not False
    return df.loc[(df["newsletter"].isin(newsletters))]

@st.cache()
def replace_html_template(title, body):
    return CARD_HTML.replace("$TITLE", title).replace("$TEXT", body)

def get_session_state_value(key : str):
    # Initialization
    if key not in st.session_state:
        return None
    else:
        return st.session_state[key]

# TODO could be cache optimized, e.g. cache the functions that gets the full html
def show_full_html_of_story(newsletter, date, lookup_df):
    df_with_full_html = lookup_df[(lookup_df["newsletter"] == newsletter) & (lookup_df["date"] == date)]
    if(not df_with_full_html.empty):
        st.session_state["fully_displayed_html"] = df_with_full_html["content"].item()

def increase_recommendation_index():
    st.session_state["recommendations_index"] = st.session_state["recommendations_index"] + 1

# ++++++++++++++++++++++++++++
# ++++++++ API REQUESTS ++++++
# ++++++++++++++++++++++++++++

def fetch_recommended_articles():
    print("FETCHED RECOMMENDATIONS")
    r = requests.get(LOCALHOST + "/recommend")
    content = r.json()
    st.session_state["recommendations"] = content
    st.session_state["recommendations_index"] = 0


df = read_dataframe("datascienceweekly_stories.csv")
full_html_lookup_df = read_dataframe("datascienceweekly_lookup.csv")

with st.sidebar:
    # Filtering options
    with st.container():
        st.button("Fetch recent recommendations", key="recommendation_button", on_click=fetch_recommended_articles)
        st.header("Settings")

        topic_options = st.multiselect(
            'Topic selection',
            ['Stock market', 'AI', 'Ethics'],
            [],
            key = "selected_topics")

        newsletter_options = st.multiselect(
            'Newsletter selection',
            df["newsletter"].unique().tolist(),
            [],
            key = "selected_newsletters")

        st.write(st.session_state)

# Recommendation
top_col1, top_col2 = st.columns(2)
with st.container():
    with top_col1:
        st.header("Recommendations")
        recs = get_session_state_value("recommendations")
        rec_index = get_session_state_value("recommendations_index")
        
        if(recs is not None and rec_index is not None):
            rec_title = recs[rec_index]["headline"]
            rec_body = recs[rec_index]["body"]
            rec_matching_score = np.round(recs[rec_index]["matching_score"], decimals = 2)
            
            st.write(f"Matching Score: {rec_matching_score}")
            st.markdown(replace_html_template(rec_title, rec_body), unsafe_allow_html=True)
            if(rec_index<9):
                st.button("Next recommendation",help="Cycle through the top 10 recommendations based on your preferences",key="next_recommendation_button", on_click=increase_recommendation_index)
            else:
                st.button("Next recommendation", disabled=True)
        else:
            st.write(recs)
            st.write(rec_index)

    with top_col2:
        st.header("Similar Story")
        st.write("Similarity Score: 21.3")
        st.markdown(replace_html_template("similar title", "similar body"), unsafe_allow_html=True)
        st.button("Next similar")

col1, col2 = st.columns(2)

# Left-hand side consists of the filtering options, recommendation and newsletter browser
with col1:
    # Newsletter Story Browser
    with st.container():
        st.header("Story Browser")

        selected_topics = get_session_state_value("selected_topics")
        selected_newsletters = get_session_state_value("selected_newsletters")

        dataframe_to_display = get_filtered_dataframe(df, selected_topics, selected_newsletters)
        print(dataframe_to_display.shape)
        for i, row in dataframe_to_display.iterrows():
            
            st.markdown(replace_html_template(str(row["headline"]), str(row["body"])), unsafe_allow_html=True)
            st.button("View full newsletter", key=str(i), on_click=show_full_html_of_story, args=(row["newsletter"], row["date"], full_html_lookup_df))


# Right-hand side consists of the pick of the day and the full HTML view of the selected newsletter
with col2:
    with st.container():
        #print(get_session_state_value("fully_displayed_html"))
        if(get_session_state_value("fully_displayed_html")):
            displayed_html = get_session_state_value("fully_displayed_html")
        else:
            displayed_html = "Please select a newsletter story to see the full HTML"
        st.components.v1.html(displayed_html, width=None, height=8024, scrolling=True)
