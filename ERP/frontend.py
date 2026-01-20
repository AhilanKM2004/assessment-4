import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"
st.title("ERP DASHBOARD")
if "login" not in st.session_state:
    st.session_state.login = False
if "token" not in st.session_state:
    st.session_state.token = None
if not st.session_state.login == True:

    st.subheader("Login")
    login_tab , signin_tab = st.tabs(["login" , "signup"])
    with login_tab:
        email = st.text_input("email",key = "login_email")
        password = st.text_input("Password", type="password" , key = "login_password")
        if st.button("LOGIN"):
            response = requests.post(
                f"{API_URL}/login",
                json={
                    "email": email,
                    "password": password})
        
            if response.status_code == 200:
                data = response.json()
                st.session_state.login = True
                st.session_state.token = data["access_token"] 
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password in login state")
    with signin_tab:
        user = st.text_input("username")
        email = st.text_input("email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Select your role",["admin", "common"])

        if st.button("sign up"):
            response = requests.post(
                f"{API_URL}/signup",     
                json={
                    "username" : user,
                    "email": email,
                    "password": password,
                    "role" : role         
                }
            )
            if response.status_code == 200:
                data = response.json()
                st.write(data["message"])
                st.success("Login successful")
                
            else:
                st.error("something error - please report")

elif st.session_state.login == True:
    st.success("You are logged in")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/me",headers=headers)               
    if response.status_code == 200:
        user = response.json()
        st.session_state.role = user["role"] 
        st.write("Name:", user["name"])
        st.write("Role:", user["role"])
        if user["role"] == "admin":
            st.write("AI-Powered ERP Mini Dashboard")
            cc,cc2,cc3=st.columns(3)
            with cc2:
                st.subheader("OVERVIEW")
            st.write("-----------------------------------------------------------------")
            c1,c2,c3 = st.columns(3)
            with c1:
                st.subheader("INVENTORY")
                st.write("our inventory conisted of ai assissting data analysis and dynamic chart visualizer")
                st.page_link(label = ">>INVENTORY",page = "pages/INVENTORY.py")
            with c2:
                st.subheader("SALES")
                st.write("To check the sales details ,where you can find summarize of perfomance and more, click")
                st.page_link(label = ">>SALES" , page = "pages/SALES.py")
            with c3:
                st.subheader("PRODUCTS")
                st.write("To see the images of the product and details  , just go to product page")
                st.page_link(label = ">>PRODUCTS" , page = "pages/PRODUCTS.py")
            st.write("-----------------------------------------------------------------") 
        if user["role"] == "common":
            st.page_link(label = ">>PRODUCTS" , page = "pages/PRODUCTS.py")
    if st.session_state.login == True:
        if st.sidebar.button("LOG-OUT"):
            st.session_state.login = False
            st.session_state.token = None
            st.rerun()
            
