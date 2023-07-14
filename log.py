import pandas as pd
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib





access = []

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
    session = st.session_state
    
    if 'logged_in' in st.session_state:
        if st.session_state['logged_in']:
            st.success("Logged In as {}".format(st.session_state['username']))
            return 

    if 'logged_in' not in session:
        session['logged_in'] = False
        
    st.subheader("Login Section")
    username = st.text_input("User Name")
    password = st.text_input("Password",type='password')
    
    if st.button("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username,check_hashes(password,hashed_pswd))
        if result:
            session['logged_in'] = True
            session['username'] = username
            st.success("Logged In as {}".format(username))
            base()
        else:
            st.warning("Incorrect username or password")

def signup():
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

def get_user_input():
    age = st.number_input('Age', min_value=0, max_value=100, value=0)
    nationality = st.text_input('Nationality', '')
    education = st.selectbox('Education', ['High School', 'College', 'Graduate School'])
    interest = st.multiselect('Interest', ['Sports', 'Music', 'Reading', 'Traveling'])
    subject = st.text_input('Subject', '')
    
    # Create a dictionary to store the user's input
    user_data = {'Age': age,
                'Nationality': nationality,
                'Education': education,
                'Interest': interest,
                'Subject': subject}
    
    return user_data

def base():
    # Set the title of the app
    st.title('Student Information')
    # Call the get_user_input function to get the user's input
    user_data = get_user_input()
    # Display the user's input
    st.write('Age:', user_data['Age'])
    st.write('Nationality:', user_data['Nationality'])
    st.write('Education:', user_data['Education'])
    st.write('Interest:', user_data['Interest'])
    st.write('Subject:', user_data['Subject'])

def main():
    # st.title("Simple Login App")
    
    st.set_page_config(layout="wide")
    

    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


    with st.sidebar:
        tabs = on_hover_tabs(tabName=['login', 'Dashboard', 'signup'], 
                            iconName=['money', 'dashboard', 'economy'], default_choice=0)
    
    if tabs =='Dashboard':
        if 'logged_in' in st.session_state:
            if st.session_state['logged_in']:
                base(st.session_state['username'])
            else:
                st.warning("Please login to continue")
        

    elif tabs == 'login':
        login()


    elif tabs == 'signup':
        signup()

if __name__ == '__main__':
    main()