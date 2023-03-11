import pandas as pd
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_elements import dashboard

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
    st.subheader("Login Section")
    username = st.text_input("User Name")
    password = st.text_input("Password",type='password')
    if st.button("Login"):
        # if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(username,check_hashes(password,hashed_pswd))
        if result:
            # redirect to home page
            st.success("Logged In as {}".format(username))
            st.subheader("User Profiles")
            user_result = view_all_users()
            clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
            st.dataframe(clean_db)
            
        else:
            st.warning("Incorrect Username/Password")
        
def signup():
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

    

def main():
    # st.title("Simple Login App")

    st.set_page_config(layout="wide")

    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'login', 'signup'], 
                            iconName=['dashboard', 'money', 'economy'], default_choice=0)

    if tabs =='Dashboard':
        st.title("Navigation Bar")
        
        

    elif tabs == 'login':
        login()


    elif tabs == 'signup':
        signup()

if __name__ == '__main__':
    main()