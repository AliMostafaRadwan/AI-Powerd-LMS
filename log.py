import pandas as pd
from st_on_hover_tabs import on_hover_tabs
import streamlit as st

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def login():
    
    username = st.text_input("User Name")
    password = st.text_input("Password",type='password')
    if st.button("Login"):
        # if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(username,check_hashes(password,hashed_pswd))
        if result:

            st.success("Logged In as {}".format(username))

            task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
            if task == "Add Post":
                st.subheader("Add Your Post")
                data = view_all_users()
                data = pd.DataFrame(data,columns=["Username","Password"])
                st.text(data)
                

            elif task == "Analytics":
                st.subheader("Analytics")
            elif task == "Profiles":
                st.subheader("User Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                st.dataframe(clean_db)
        else:
            st.warning("Incorrect Username/Password")
    

def main():
    # st.title("Simple Login App")

    st.set_page_config(layout="wide")

    st.header("Custom tab component for on-hover navigation bar")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'login', 'signup'], 
                            iconName=['dashboard', 'money', 'economy'], default_choice=0)

    if tabs =='Dashboard':
        st.title("Navigation Bar")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'login':
        login()


    elif tabs == 'signup':
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

         

# def main():
# 	"""Simple Login App"""

# 	st.title("Simple Login App")

# 	menu = ["Home","Login","SignUp"]
# 	choice = st.sidebar.selectbox("Menu",menu)

# 	if choice == "Home":
# 		st.subheader("Home")

# 	elif choice == "Login":
# 		st.subheader("Login Section")

# 		username = st.sidebar.text_input("User Name")
# 		password = st.sidebar.text_input("Password",type='password')
# 		if st.sidebar.checkbox("Login"):
# 			# if password == '12345':
# 			create_usertable()
# 			hashed_pswd = make_hashes(password)

# 			result = login_user(username,check_hashes(password,hashed_pswd))
# 			if result:

# 				st.success("Logged In as {}".format(username))

# 				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
# 				if task == "Add Post":
# 					st.subheader("Add Your Post")
# 					data = view_all_users()
# 					data = pd.DataFrame(data,columns=["Username","Password"])
# 					st.text(data)
                    

# 				elif task == "Analytics":
# 					st.subheader("Analytics")
# 				elif task == "Profiles":
# 					st.subheader("User Profiles")
# 					user_result = view_all_users()
# 					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
# 					st.dataframe(clean_db)
# 			else:
# 				st.warning("Incorrect Username/Password")





# 	elif choice == "SignUp":
# 		st.subheader("Create New Account")
# 		new_user = st.text_input("Username")
# 		new_password = st.text_input("Password",type='password')

# 		if st.button("Signup"):
# 			create_usertable()
# 			add_userdata(new_user,make_hashes(new_password))
# 			st.success("You have successfully created a valid Account")
# 			st.info("Go to Login Menu to login")



if __name__ == '__main__':
    main()