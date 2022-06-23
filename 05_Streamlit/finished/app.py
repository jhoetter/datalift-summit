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

# 
@st.cache()
def read_dataframe(path, sep=",") -> pd.DataFrame:
    df = pd.read_csv(path, sep=sep).sort_values("date", ascending=False)
    return df

@st.cache()
def get_filtered_dataframe(df, topics, newsletters) -> pd.DataFrame:
    return df.loc[(df["newsletter"].isin(newsletters)) & (df["topic"].isin(topics))]

@st.cache()
def get_replaced_html_template(title, body):
    return CARD_HTML.replace("$TITLE", title).replace("$TEXT", body)

# Cautionary measure to prevent un-initialized key access
def get_session_state_value(key : str):
    if key not in st.session_state:
        return None
    else:
        return st.session_state[key]

# Updates the currently selected HTML
def show_full_html_of_story(newsletter, date, lookup_df):
    df_with_full_html = lookup_df[(lookup_df["newsletter"].str.lower() == newsletter.lower()) & (lookup_df["date"] == date)]
    if(not df_with_full_html.empty):
        st.session_state["fully_displayed_html"] = df_with_full_html["content"].item()

# I am pretty sure the 4 following functions can be summed up in a single function but I was too lazy that day
def increase_recommendation_index():
    st.session_state["recommendations_index"] = st.session_state["recommendations_index"] + 1

def reset_recommendation_index():
    st.session_state["recommendations_index"] = 0

def increase_similarity_index():
    st.session_state["similarity_index"] = st.session_state["similarity_index"] + 1

def reset_similarity_index():
    st.session_state["similarity_index"] = 0

# ++++++++++++++++++++++++++++++
# ++++++++ API REQUESTS ++++++++
# ++++++++++++++++++++++++++++++

def fetch_recommended_articles():
    r = requests.get(LOCALHOST + "/recommend")
    if(r.status_code == 200):
        content = json.loads(r.json())
        st.session_state["recommendations"] = content
        st.session_state["recommendations_index"] = 0
    else:
        st.session_state["recommendations"] = [{"headline" : "ERROR OCCURRED", "body" : "please refetch recommendations", "date":"2000-01-01 00:00:00+00:00"}]
        st.session_state["recommendations_index"] = 0

def fetch_similar_stories(headline:str = ""):
    r = requests.get(LOCALHOST + "/similar", params={"headline" : headline})
    if(r.status_code == 200):
        content = json.loads(r.json())
        st.session_state["similar_stories"] = content
        st.session_state["similarity_index"] = 0
    else:
        st.session_state["similar_stories"] = [{"headline" : "ERROR OCCURRED", "body" : "please refetch similar stories", "date":"2000-01-01 00:00:00+00:00"}]
        st.session_state["similarity_index"] = 0

# Fetching the data can be cached
@st.cache()
def fetch_data():
    r = requests.get(LOCALHOST + "/data")
    if(r.status_code == 200):
        content = json.loads(r.json())
        st.session_state["data"] = content
    else:
        raise SystemError("Error occurred when trying to fetch record data from the backend")

# Fetch the data from the backend 
fetch_data()

# Transform the data into an easy-to-use DataFrame
data = get_session_state_value("data")
if(data is not None):
    df = pd.DataFrame(st.session_state["data"])
else:
    print("[WARNING] Fallback option - reading data from disk")
    df = read_dataframe("../../04_ModelPipeline/output.csv")

# Load the full html lookup dataframe - could also be in the backend if you want to
full_html_lookup_df = read_dataframe("html_lookup.csv")

# The sidebar consists of the filtering options and the "fetch recommendation" button 
with st.sidebar:
    with st.container():
        st.header("Settings")

        topic_options = st.multiselect(
            'Topic selection',
            df["topic"].unique().tolist(),
            [],
            key = "selected_topics")

        newsletter_options = st.multiselect(
            'Newsletter selection',
            df["newsletter"].unique().tolist(),
            [],
            key = "selected_newsletters")

        st.button("Fetch recommendations", key="recommendation_button", on_click=fetch_recommended_articles)

        check = st.checkbox("show session state")
        if(check):
            st.write(st.session_state)

# Recommendation and Similar Search
top_col1, top_col2 = st.columns(2)
with st.container():
    with top_col1:
        recs = get_session_state_value("recommendations")
        rec_index = get_session_state_value("recommendations_index")
        if(rec_index is not None):
            st.header(f"Recommendations - {rec_index+1}/10")
        else:
            st.header(f"Recommendations")
        
        if(recs is not None and rec_index is not None):
            rec_title = recs[rec_index]["headline"]
            rec_body = recs[rec_index]["body"]

            st.markdown(get_replaced_html_template(rec_title, rec_body), unsafe_allow_html=True)
            if(rec_index<9):
                st.button("Next recommendation",help="Cycle through the top 10 recommendations based on your preferences",key="next_recommendation_button", on_click=increase_recommendation_index)
            else:
                st.button("Reset", on_click = reset_recommendation_index)
        else:
            st.write("Please fetch the newest recommendations in the sidebar")

    with top_col2:
        similar_stories = get_session_state_value("similar_stories")
        similarity_index = get_session_state_value("similarity_index")

        if(similarity_index is not None):
            st.header(f"Similar Stories - {similarity_index+1}/10")
        else:
            st.header("Similar Stories")

        if(similar_stories is not None and similarity_index is not None):
            sim_title = similar_stories[similarity_index]["headline"]
            sim_body = similar_stories[similarity_index]["body"]

            st.markdown(get_replaced_html_template(sim_title, sim_body), unsafe_allow_html=True)
            if(similarity_index<9):
                st.button("Next similar", on_click=increase_similarity_index)
            else:
                st.button("Reset", on_click=reset_similarity_index)
        else:
            st.write("No similarity search started yet")
        

col1, col2 = st.columns(2)

# Left-hand side consists of the newsletter browser
with col1:
    # Newsletter Story Browser
    with st.container():
        st.header("Story Browser")

        selected_topics = get_session_state_value("selected_topics")
        selected_newsletters = get_session_state_value("selected_newsletters")

        # TODO replace only this
        dataframe_to_display = get_filtered_dataframe(df, selected_topics, selected_newsletters)
        print(dataframe_to_display.shape)
        if(not dataframe_to_display.empty):
            for i, row in dataframe_to_display.iterrows():
                
                st.markdown(get_replaced_html_template(str(row["headline"]), str(row["body"])), unsafe_allow_html=True)
                st.button("View full newsletter", key="full_newsletter_button_" + str(i), on_click=show_full_html_of_story, args=(row["newsletter"], row["date"], full_html_lookup_df))
                st.button("Get similar stories", key="similar_stories_button_" + str(i), on_click=fetch_similar_stories, kwargs={"headline" : str(row["headline"])})
        else:
            st.write("Please select a topic or newsletter")


# Right-hand side consists of the full HTML view of the selected newsletter
with col2:
    with st.container():
        st.header("Full Newsletter HTML")
        #print(get_session_state_value("fully_displayed_html"))
        if(get_session_state_value("fully_displayed_html")):
            displayed_html = get_session_state_value("fully_displayed_html")
            st.components.v1.html(displayed_html, width=None, height=8024, scrolling=True)
        else:
            st.write("Please select a newsletter story to see the full HTML")
        
