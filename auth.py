import streamlit as st
from database import get_db_connection, hash_password
DB_CONFIG = st.secrets["db_config"]


def register_form():
    st.markdown('<h2 class="header" style="text-align: center;">Register</h2>', unsafe_allow_html=True)
    email = st.text_input("Email", key="reg_email")
    username = st.text_input("Username", key="reg_username")
    password = st.text_input("Password", type="password", key="reg_password")
    password2 = st.text_input("Confirm Password", type="password", key="reg_password2")
    if st.button("Register"):
        if not email or not username or not password:
            st.error("Please fill out all fields.")
        elif password != password2:
            st.error("Passwords do not match.")
        else:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    st.error("User with this email already exists. Please login.")
                else:
                    password_hash = hash_password(password)
                    cursor.execute(
                        "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                        (email, username, password_hash)
                    )
                    conn.commit()
                    st.success("Registration successful! Please switch to Login mode.")
            conn.close()

def login_form():
    st.markdown('<h2 class="header" style="text-align: center;">Login</h2>', unsafe_allow_html=True)
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            password_hash = hash_password(password)
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, password_hash))
                user = cursor.fetchone()
            conn.close()
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
                st.session_state["username"] = user[2]  # assuming username is at index 2
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

def logout_action():
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = ""
    st.session_state["username"] = ""
    st.rerun()
