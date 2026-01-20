import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"
st.header("PRODUCT PAGE")
if "token" not in st.session_state:
    st.session_state.token = None
if "login" not in st.session_state:
    st.session_state.login = False
if st.session_state.login == False:
    st.page_link(label = "please login before the acion", page = "frontend.py" )
elif st.session_state.login == True:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    if st.session_state.role == "admin":
        st.header("Add Product (Admin)")

        name = st.text_input("Product name")
        price = st.number_input("Price", min_value=1)
        image_file = st.file_uploader(
            "Upload product image",
            type=["jpg", "jpeg", "png"]
        )

        if st.button("Add Product"):
            if not name or not image_file:
                st.error("All fields are required")
            else:
                files = {
                    "image": (image_file.name, image_file.getvalue(), image_file.type)
                }

                data = {
                    "name": name,
                    "price": price
                }

                res = requests.post(
                    f"{API_URL}/add_product",
                    data=data,
                    files=files,
                    headers=headers
                )

                if res.status_code == 200:
                    st.success("Product added successfully")
                else:
                    st.error(res.text)

    res = requests.get(f"{API_URL}/products", headers=headers)

    if res.status_code != 200:
        st.error(f"Failed to load products ({res.status_code})")
        st.write(res.text)
        st.stop()
    products = res.json()
    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None
    for p in products:
        with st.container(border=True):
            col1, col2 = st.columns([2, 1])
            col1.image(p["image"], caption=p["name"], width=180)
            if col2.button("Select", key=p["id"]):
                st.session_state.selected_product = p
                
    if st.session_state.selected_product:
        st.divider()
        st.subheader("Order")
        st.write("Product:", st.session_state.selected_product["name"])
        qty = st.number_input("Quantity", min_value=0, step=1)
        if st.button("Use my profile address"):
            if qty == 0:
                st.error("Quantity cannot be zero")
            else:
                res = requests.post(f"{API_URL}/place_order",json={"product_id": st.session_state.selected_product["id"],"quantity": qty},headers = headers)
                if res.status_code == 200:
                    st.success("Order placed successfully")
                else:
                    st.error(res.text)
        if st.button("Reset"):
            st.session_state.selected_product = None
            st.rerun()







            
if st.session_state.login == True:
    if st.sidebar.button("LOG-OUT"):
        st.session_state.login = False


    # st.header("PRODUCT PAGE")
    # products = [
    # {"id": 101, "name": "fruit basket", "image": "https://i.pinimg.com/736x/9c/d5/bc/9cd5bcd17774460c382d1162840e2735.jpg"},
    # {"id": 102, "name": "milk", "image": "https://i.pinimg.com/736x/4f/71/a5/4f71a52e88313fd0dc12664871937838.jpg"},
    # {"id": 103, "name": "T shirt", "image": "https://i.pinimg.com/1200x/8b/f6/2e/8bf62edb1c05322a4d74921075c07275.jpg"},]

    # if not "x" in st.session_state :
    #     st.session_state.x = False
   
    # for p in products:
    #     with st.container(border=True):
    #         c1, c2 , c3 = st.columns(3)
    #         c1.image(p["image"], caption=p["name"], width=200)
    #         if c2.button("Select", key=f"select_{p['id']}"):
    #             st.session_state.x=True
    #             st.write("Selected product:", st.session_state.get("selected_product"))
    #             st.session_state.selected_product = p["id"]
    # if st.session_state.x == True:
    #     st.session_state.num = st.number_input("enter the quantity",min_value=0)
    #     x=st.button("use my profile address for delivery details")
    #     if x and st.session_state.num!=0:
    #         st.success("success")
    #     elif x and st.session_state.num == 0:
    #         st.write("quantity cannot be zero") 
    #     button = st.button("reset")
    #     if button:
    #         st.rerun()