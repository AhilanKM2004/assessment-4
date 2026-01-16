import streamlit as st
import requests
from datetime import date , timedelta
import pandas as pd


API_URL = "http://127.0.0.1:8000"
st.title("TASK MANAGEMENT")


if "login" not in st.session_state:
    st.session_state.login = False

if "token" not in st.session_state:
    st.session_state.token = None

if "show_create" not in st.session_state:
    st.session_state.show_create = False


if not st.session_state.login:
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
                    "password": password
                }
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.login = True
                st.session_state.token = data["access_token"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")
    with signin_tab:
        user = st.text_input("username")
        email = st.text_input("email")
        password = st.text_input("Password", type="password")
        if st.button("sign up"):
            response = requests.post(
                f"{API_URL}/signup",
                json={
                    "username" : user,
                    "email": email,
                    "password": password
                }
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.login = True
                st.session_state.token = data["access_token"]
                st.success("Login successful")
                st.rerun()

            else:
                st.error("Invalid username or password")


elif st.session_state.login == True:
    st.success("You are logged in")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/me", headers=headers)

    if response.status_code == 200:
        user = response.json()
        st.write("hi ", user["name"])

    if st.button("INSERT TASK"):
        st.session_state.show_create = True

    if st.session_state.show_create:

        st.subheader("Enter the following details")

        with st.form("create_task_form"):
            a = st.text_input("Enter the title - already exisiting title are not allowed")
            b = st.text_input("Enter the description")
            c = st.date_input("Enter the date ",    min_value=date.today(),max_value=date.today() + timedelta(days=365) )

            PRIORITY_MAP = {
                "High": 3,
                "Medium": 2,
                "Low": 1
            }

            priority_label = st.selectbox(
                "Select priority",
                list(PRIORITY_MAP.keys())
            )

            d = PRIORITY_MAP[priority_label]

            submit = st.form_submit_button("create")

        if submit:
            header = {"Authorization": f"Bearer {st.session_state.token}"}

            response2 = requests.post(
                f"{API_URL}/create_table",
                json={
                    "title": a,
                    "decription": b,
                    "due_date": c.isoformat(),
                    "priority": d
                },
                headers=headers
            )

            if response2.status_code == 200:
                st.success("done")
                st.session_state.show_create = False
            else:
                st.error(response2.text)

    if "TK" not in st.session_state:
        st.session_state.TK = False
    if st.button("SEE ALL TASKS"):
        st.session_state.TK = True
    if st.session_state.TK:
        response2 = requests.get(
            f"{API_URL}/getalltask",
            headers=headers
    )

        if response2.status_code == 200:
            tasks = response2.json()  

            if len(tasks) == 0:
                st.info("No tasks found")
            else:
                st.subheader("ALL TASKS")
                df = pd.DataFrame(tasks)
                st.dataframe(df, width="stretch")
                
                if "TKk" not in st.session_state:
                     st.session_state.TKk = False
                selection = st.radio("select",["sort by date" , "sort by priority"])
                if selection:
                    st.session_state.TKk = True
                    if selection == "sort by date":
                            response2 = requests.get(
                                f"{API_URL}/sortbydate",headers=headers)
                            if response2.status_code == 200:
                                st.success("sorting_by_date")
                                tasks = response2.json()
                                if len(tasks) == 0:
                                    st.info("No tasks found")
                                else:
                                    st.subheader("SORTED")
                                    df = pd.DataFrame(tasks)
                                    st.dataframe(df, width="stretch")
                                    st.session_state.TKk = False
                            else:
                                st.error(response2.text)

                    if selection == "sort by priority":
                            response2 = requests.get(
                                f"{API_URL}/sortbypriority",headers=headers)
                            if response2.status_code == 200:
                                st.success("sorting_by_priority")
                                tasks = response2.json()
                                if len(tasks) == 0:
                                    st.info("No tasks found")
                                else:
                                    st.subheader("SORTED")
                                    df = pd.DataFrame(tasks)
                                    st.dataframe(df, width="stretch")
                                    st.session_state.TKk = False
                            else:
                                st.error(response2.text)

            if st.button("Close Tasks"):
                st.session_state.TK = False

        else:
            st.error(response2.text)

    a1,a2,a3 = st.tabs(["EDIT TAB" , "DELETE" , "FILE ATTACHMENT"])
    with a1:
        if "a1" not in st.session_state:
            st.session_state.a1 = False
        if st.button("click to edit"):
            st.session_state.a1 = True
        if st.session_state.a1:
            st.subheader("Enter the following details")
            with st.form("create_task_form"):
                z=st.number_input("please enter the id number to be edited")
                a = st.text_input("please enter the new title ")
                b = st.text_input("Enter the new description")
                c = st.date_input("Enter the new date ",    min_value=date.today(),max_value=date.today() + timedelta(days=365) )
                PRIORITY_MAP = {"High": 3,"Medium": 2,"Low": 1}
                priority_label = st.selectbox("Select priority",list(PRIORITY_MAP.keys()))
                d = PRIORITY_MAP[priority_label]
                submit = st.form_submit_button("edit")
                st.rerun()
            if submit:
                response2 = requests.put(
                    f"{API_URL}/editthis/{z}",
                    json={
                        "title": a,
                        "decription": b,
                        "due_date": c.isoformat(),
                        "priority": d
                    },
                    headers=headers)
                if response2.status_code == 200:
                    st.success("file edited successfully")
                    df = pd.DataFrame(tasks)
                    st.dataframe(df, width="stretch")
                    st.session_state.a1 = False
                else:
                    st.error(response2.text)
                    
    with a2:
        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False
        x = st.number_input(
            "Please enter the id number of the task to be deleted",min_value=1,step=1)
        if st.button("Delete Task"):
            st.session_state.confirm_delete = True
        if st.session_state.confirm_delete:
            st.warning("Are you sure you want to delete this task?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete"):
                    response = requests.delete(
                        f"{API_URL}/deletethis/{x}",
                        headers=headers)
                    if response.status_code == 200:
                        st.success("File deleted successfully")
                        st.session_state.confirm_delete = False
                        st.rerun()
                    else:
                        st.error(response.text)
            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_delete = False
                    
    with a3:
        task_id = st.number_input("Enter task id", min_value=1)
        uploaded_file = st.file_uploader("Upload PDF/Image")
        if uploaded_file and st.button("Upload"):
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/attachfile/{task_id}",files=files,headers=headers)
            if response.status_code == 200:
                st.success("File attached successfully")
            else:
                st.error(response.text)









    




























if st.session_state.login == True:
    if st.sidebar.button("LOG-OUT"):
        st.session_state.login = False
        st.session_state.token = None
        st.session_state.show_create = False
        st.rerun()
