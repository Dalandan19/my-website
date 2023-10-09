import streamlit as st
from streamlit_option_menu import option_menu
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Hasher
import streamlit_authenticator as stauth
import requests
from streamlit_lottie import st_lottie
from inventory_management import Product, Inventory

st.set_page_config(page_title='Dashboard', page_icon='🚀')

#sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home", "Projects","ToDo"],
        icons = ["house-heart", "lightbulb", "pin-angle"],
        menu_icon="calendar",
    )

if selected == "Home":
    st.title(f"Welcome to {selected}")
    

    # Load configuration from YAML file
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Create an authentication object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Authenticate the user
    if not st.session_state.get("authentication_status"):
        # Retrieve user credentials from user input
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            if username in config['credentials']['usernames'] and config['credentials']['usernames'][username]['password'] == password:
                authentication_status = True
                user_info = config['credentials']['usernames'][username]
                st.session_state["authentication_status"] = authentication_status
                st.session_state["name"] = user_info.get("name", "")
                st.session_state["username"] = username
            else:
                authentication_status = False
                st.session_state["authentication_status"] = authentication_status
            
    # Main Page Content
    if st.session_state["authentication_status"]:
        st.write(f'Welcome {st.session_state["name"]}!')
        
        st.title("Inventory Management 📦")
        st.text('Welcome to the Inventory Management')

        # initialize session state
        if "inventory" not in st.session_state:
            st.session_state.inventory = Inventory()

        # create product objects with streamlit
        product_name = st.text_input("Product Name")
        product_price = st.number_input("Product Price", step=0.01)
        product_quantity = st.number_input("Product Quantity", step=1)

        # create product object
        add_product = st.button("Add Product")

        if add_product:
            product = Product(product_name, product_price, product_quantity)
            st.session_state.inventory.add_product(product)

        # display inventory
        if st.session_state.inventory.items:
            st.header("Inventory:")
            for product in st.session_state.inventory.items:
                st.write(f"Product: {product.name} | Price: ${product.price} | Quantity: {product.quantity}")
        else:
            st.write("Inventory is empty.")

        # Product Deletion
        if st.session_state.inventory.items:
            st.header("Delete Inventory:")
            for product in st.session_state.inventory.items:
                st.write(f"Product: {product.name} | Price: ${product.price} | Quantity: {product.quantity}")
                
                # Add a checkbox for each product
                delete_product = st.checkbox(f"Delete {product.name}")
                
                if delete_product:
                    st.session_state.inventory.remove_product(product)
                    st.success(f"{product.name} has been deleted from the inventory.")
        

        
        # Password Reset Widget
        # if st.button("Reset Password"):
        #     try:
        #         if authenticator.reset_password(st.session_state["username"], 'Reset password'):
        #             st.success('Password modified successfully')
                    
        #             # Update the configuration file after password reset
        #             with open('config.yaml', 'w') as file:
        #                 yaml.dump(config, file, default_flow_style=False)
                        
        #     except Exception as e:
        #         st.error(e)
        # else:
        #     if st.session_state["authentication_status"] is False:
        #         st.error('Username/password is incorrect')
        #     elif st.session_state["authentication_status"] is None:
        #         st.warning('Please enter your username and password')

        
        # Logout
        if st.button("Logout"):
            authenticator.logout('Logout', 'main', key='unique_key')
            st.session_state["authentication_status"] = None
            st.session_state["name"] = None
            st.session_state["username"] = None
            st.success('You have been logged out')
            
    else:
        if st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')



    st.markdown("Copyright © 2023 Your Company")
    
if selected == "Projects":
    
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    
    st.title(f"Welcome to {selected}")
    st.write("Working in Progress...")
    # Load Assets
    lottie_coding = load_lottieurl("https://lottie.host/6d72f590-d4d0-4e08-a8fb-6ff0f29b9649/16sdxvXKoB.json")
        
    st_lottie(lottie_coding, height=300, key="coding")
    
    
if selected == "ToDo":
    st.title(f"Welcome to {selected} List")
    
        #initialize session state
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []
    if "completed_tasks" not in st.session_state:
        st.session_state["completed_tasks"] = []

    #create task objects with streamlit
    def add_task(task, due_date):
        st.session_state["tasks"].append({"task": task, "due_date": due_date, "done": False})    

    # Input field for adding tasks
    task = st.text_input("Add a new task:")

    # Input field for adding due dates
    due_date = st.date_input("Due date:")

    # Add task to the list when "Add" button is clicked
    if st.button("Add"):
        if task:
            add_task(task, due_date)  # Use the function to add the task and due date to the session state

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        # Display tasks with checkboxes and due dates
        st.write("### Tasks:")
        st.write("Check the box next to the tasks you want to mark as completed")
        for i, t in enumerate(st.session_state["tasks"]):
            # Display a checkbox, the task text, and the due date
            done = st.checkbox(f"{t['task']} (Due: {t['due_date']})", key=i )  # Use a unique key for each checkbox
            t['done'] = done

            # Move task to completed tasks if checkbox is checked
            if done:
                st.session_state["completed_tasks"].append(t)
                st.session_state["tasks"].remove(t)  # Remove the task from the tasks list

    with col2:
        # Display completed tasks
        st.write("### Completed Tasks:")
        for t in st.session_state["completed_tasks"]:
            st.write(f"{t['task']} (Due: {t['due_date']})")

        # Add a "Clear" button to clear all completed tasks
        if col2.button("Clear"):
            st.session_state["completed_tasks"] = []

