import streamlit as st
from groq import Groq
import pandas as pd
import requests
from frontend import API_URL
import io
if "login" not in st.session_state:
    st.session_state.login = False
if st.session_state.login == False:
    st.page_link(label = "please login before the action", page = "frontend.py" )
    
elif (st.session_state.login == True and st.session_state.token != None):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/me",headers=headers)
    if response.status_code == 200:
        user = response.json()
        
        if user["role"] == "admin":
            st.header("INVENTORY PAGE")
            if "filename" not in st.session_state:
                st.session_state.file = None
            st.subheader("Upload CSV File")
            file_upload = st.file_uploader("Please upload your project report (CSV)",type=["csv"])
            if file_upload is not None:
                st.session_state.file = file_upload
                files = {"file": (file_upload.name, file_upload.getvalue(), file_upload.type)}
                response = requests.post(f"{API_URL}/upload_file",files=files, headers=headers) 
                if response.status_code == 200:
                    st.success("File uploaded successfully")
                else:
                    st.error(response.text)
            if st.session_state.file:
                if st.button("Check RAW file"):
                    if "k" not in st.session_state :
                        st.session_state.k = False
                    st.session_state.k = True
                    if st.button("close"):
                        st.session_state.k = False
                    if st.session_state.k == True:
                        res = requests.get(
                            f"{API_URL}/to_view_raw_file",                                            
                            params={"filename": st.session_state.file.name},headers=headers)
                        if res.status_code == 200:
                            readed = pd.read_csv(io.BytesIO(res.content))
                            st.session_state.readed = readed
                            st.table(readed)
                        else:
                            st.error(res.text)
                            
            if "show_chart" not in st.session_state:
                st.session_state.show_chart = False
            if st.button("chart view"):
                st.session_state.show_chart = True
            if st.session_state.show_chart:
                c1, c2 = st.columns(2)
                with c1:
                    chart_options = ["line chart", "area chart", "scatter chart"]
                    st.radio("SELECT DIAGRAM TYPE",chart_options,key="radio")
                with c2:
                    varying_options = st.session_state.radio
                    res = requests.get(f"{API_URL}/{varying_options}/chart_view",
                    params={"filename": st.session_state.file.name},
                    headers=headers)
                    if res.status_code == 200:
                        readed = res.content
                        st.image(readed, use_container_width=True)
                    else:
                        st.error(res.text)
            st.write("--------------------------------------------------------------------------------------")
            
            c1,c2 = st.columns(2)
            with c1:
                st.page_link(label = "To check sales details", page = "pages/SALES.py" )
            with c2:
                st.page_link(label = "To check product details", page = "pages/PRODUCTS.py" )
                

        elif (st.session_state.login == True and user["role"] == "common"):
            st.subheader("you are restricted")
            st.write("please go to product page or sales page")
            st.write("--------------------------------------------------------------------------------------")
            c1,c2 = st.columns(2)
            with c1:
                st.page_link(label = "To explore our sales and service", page = "pages/SALES.py" )
            with c2:
                st.page_link(label = "To purchase our products", page = "pages/PRODUCTS.py" )
if st.session_state.login == True:
    if st.sidebar.button("LOG-OUT"):
        st.session_state.login = False



















                # if "readed" in st.session_state:
                #     c1, c2 = st.columns(2)

                    # with c1:
                    #     chart_options = ["line chart", "area chart", "scatter chart"]

                    #     if "radio" not in st.session_state:
                    #         st.session_state.radio = chart_options[0]

                    #     st.session_state.radio = st.radio("SELECT DIAGRAM TYPE",chart_options)

                    # with c2:
                
                    #     df = st.session_state.readed

                    #     numeric_cols = df.select_dtypes(include="number").columns.tolist()

                    #     if st.session_state.radio == "line chart":
                    #         st.line_chart(df[numeric_cols])--------------------------------------------------------this too

                    #     elif st.session_state.radio == "area chart":
                    #         st.area_chart(df[numeric_cols])----------------------------------------------------------------------this have to be performed from backend

                    #     elif st.session_state.radio == "scatter chart":
                    #         st.scatter_chart(---------------------------------------------------------------------------this too
                    #             df,
                    #             x=numeric_cols[0],
                    #             y=numeric_cols[1]
                    #         )

                    # client = Groq(api_key="") -----------------------------------------------------------------------------this too
                    # st.header("AI report")
                    # system_prompt=f"""we will give you an csv file and you have to do analys over the file and make small report about the subjected file , declare the current state , postive , negative all important points , remember it's need not be a bigger report but important point , just for the clarification and finally once again make it very  shorter because longer version will be displayed after this portion so make don't make it over 25 lines, and the csv file is = {st.session_state.readed}"""
                    # response = client.chat.completions.create(
                    #         model="llama-3.3-70b-versatile",
                    #         messages=[{"role": "system", "content": system_prompt}])
                    # st.session_state.result = ( response.choices[0].message.content )
                    # st.write(st.session_state.result)



