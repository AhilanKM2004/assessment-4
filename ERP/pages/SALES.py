import streamlit as st
from groq import Groq
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"
if "token" not in st.session_state:
    st.session_state.token = None

if "login" not in st.session_state:
    st.session_state.login = False
if st.session_state.login == False:
    st.page_link(label = "please login before the acion", page = "frontend.py" )
if (st.session_state.login == True and st.session_state.role != "common"):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    st.header("SALES PAGE")
    if "file" not in st.session_state or st.session_state.file is None:
        st.warning("Please upload a file first")
    else:
        file = st.session_state.file
        st.write("File name:", file.name)
        df = pd.read_csv(file)
        with st.expander("Click to see raw file"):
            st.dataframe(df)
       
if (st.session_state.login == True):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    st.header("AI sales and service manager")
    search = st.text_input("search for a product")
    res = requests.post(f"{API_URL}/ai_search",headers=headers,json = {"search" : search }) 
    if res.status_code != 200:
        st.error(res.text)
        st.stop()
    elif res.status_code == 200 :
        data = res.json()
        st.write("RESULT---------",data["result"])

    
if st.session_state.login == True:
    if st.sidebar.button("LOG-OUT"):
        st.session_state.login = False


