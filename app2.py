import streamlit as st
import json
import os
import re
import string
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0


def signup(json_file_path="data.json"):
    st.title("Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")

        if st.form_submit_button("Signup"):
            if password == confirm_password:
                user = create_account(name, email, age, sex, password, json_file_path)
                session_state["logged_in"] = True
                session_state["user_info"] = user
            else:
                st.error("Passwords do not match. Please try again.")

def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            if user["email"] == username and user["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = user
                st.success("Login successful!")
                return user
                st.error("Invalid credentials. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None
def initialize_database(json_file_path="data.json"):
    try:
        # Check if JSON file exists
        if not os.path.exists(json_file_path):
            # Create an empty JSON structure
            data = {"users": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
    except Exception as e:
        print(f"Error initializing database: {e}")
        
def create_account(name, email, age, sex, password, json_file_path="data.json"):
    try:
        # Check if the JSON file exists or is empty
        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            data = {"users": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        # Append new user data to the JSON structure
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,

        }
        data["users"].append(user_info)

        # Save the updated data to JSON
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Account created successfully! You can now login.")
        return user_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return None

def login(json_file_path="data.json"):
    st.title("Login Page")
    username = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    login_button = st.button("Login")

    if login_button:
        user = check_login(username, password, json_file_path)
        if user is not None:
            session_state["logged_in"] = True
            session_state["user_info"] = user
        else:
            st.error("Invalid credentials. Please try again.")

def get_user_info(email, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for user in data["users"]:
                if user["email"] == email:
                    return user
        return None
    except Exception as e:
        st.error(f"Error getting user information: {e}")
        return None


def render_dashboard(user_info, json_file_path="data.json"):
    try:
        st.title(f"Welcome to the Dashboard, {user_info['name']}!")
        st.subheader("User Information:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Sex: {user_info['sex']}")
        st.write(f"Age: {user_info['age']}")

    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")

def main(json_file_path="data.json"):
    st.sidebar.title("Arrhythmia Detection")
    page = st.sidebar.radio(
        "Go to",
        ("Signup/Login", "Dashboard", "Arrhythmia Detection"),
        key="Arrhythmia Detection",
    )

    if page == "Signup/Login":
        st.title("Signup/Login Page")
        login_or_signup = st.radio(
            "Select an option", ("Login", "Signup"), key="login_signup"
        )
        if login_or_signup == "Login":
            login(json_file_path)
        else:
            signup(json_file_path)

    elif page == "Dashboard":
        if session_state.get("logged_in"):
            render_dashboard(session_state["user_info"])
        else:
            st.warning("Please login/signup to view the dashboard.")

    elif page == "Arrhythmia Detection":
        if session_state.get("logged_in"):
            st.title("Arrhythmia Detection")
            label={
            1: 'Normal',
            2: 'Ischemic changes (Coronary Artery Disease)',
            3: 'Old Anterior Myocardial Infarction',
            4: 'Old Inferior Myocardial Infarction',
            5: 'Sinus tachycardy',
            6: 'Sinus bradycardy',
            7: 'Ventricular Premature Contraction (PVC)',
            8: 'Supraventricular Premature Contraction',
            9: 'Left bundle branch block',
            10: 'Right bundle branch block',
            11: '1. degree AtrioVentricular block',
            12: '2. degree AV block',
            13: '3. degree AV block',
            14: 'Left ventricule hypertrophy',
            15: 'Atrial Fibrillation or Flutter',
            16: 'Others'
            }
            columns = ['QRSduration', 'PRinterval', 'chDI_Rwave', 'chV3_Swave', 'chV6_Rwave',
            'chV2_JJwaveAmp', 'chV2_QRSA']
            QRSduration= st.number_input('QRSduration:')
            PRinterval=st.number_input('PRinterval:')
            chDI_Rwave = st.number_input('chDI_Rwave:')
            chV3_Swave=st.number_input('chV3_Swave:')
            chV6_Rwave=st.number_input('chV6_Rwave:')
            chV2_JJwaveAmp=st.number_input('chV2_JJwaveAmp')
            chV2_QRSA=st.number_input('chV2_QRSA')  
            a = [QRSduration, PRinterval, chDI_Rwave, chV3_Swave, chV6_Rwave,
            chV2_JJwaveAmp, chV2_QRSA]
            data = pd.DataFrame([a], columns=columns)
            if st.button("Submit"):
                try:
                    # # Load the scaler first
                    # with open('scaler.pkl', 'rb') as f:
                    #     scaler = pickle.load(f)

                    # Load the model
                    with open('hybrid_features.pkl', 'rb') as f:
                        model = pickle.load(f)

                    # Scale the input data
                    

                    # Make prediction
                    pred = model.predict(data)[0]
                    st.write(pred)
                    label_name = label.get(pred, 'Invalid prediction')

                    st.write(f'The Predicted condition is **{label_name}**')

                except Exception as e:
                    st.error(f"Error during prediction: {e}")

    else:
        st.warning("Please login/signup to use app!!")




if __name__ == "__main__":
    initialize_database()
    main()
