import streamlit as st
import pandas as pd
import plotly.express as px
from helper import *
from datetime import datetime
from pymongo import MongoClient


# MongoDB Atlas Connection
MONGODB_URI = "mongodb+srv://gangaputrachandan:Chandan123@weighttrackercluster.qd3ku.mongodb.net/?retryWrites=true&w=majority&appName=WeightTrackerCluster"
client = MongoClient(MONGODB_URI)
db = client["weight_tracker"]
collection = db["weights"]
authenticator, name, username = authenticate_user()

if name:
    st.write(f"Welcome {name}!")
    
    if "user_weights" not in st.session_state:
        st.session_state["user_weights"] = {user : [] for user in ["Ravinder", "Latha", "Chandan", "Vaishnavi"]}

    # if "user_weights" not in st.session_state:
    #     st.session_state["user_weights"] = {
    #     "Ravinder": [("01-10-2024", 75), ("08-10-2024", 74.5), ("15-10-2024", 73.8)],
    #     "Latha": [("01-10-2024", 65), ("08-10-2024", 64.7), ("15-10-2024", 64.2)],
    #     "Chandan": [("01-10-2024", 80), ("08-10-2024", 79.5), ("15-10-2024", 79.0)],
    #     "Vaishnavi": [("01-10-2024", 55), ("08-10-2024", 54.8), ("15-10-2024", 54.4)]
    #     }
    st.subheader("Enter your weight for today")
    weight = st.number_input("Enter your weight", min_value=0.0, max_value=500.0, step=1.0)

    if st.button("Add Weight"):
        today_date = datetime.today().strftime('%d-%m-%Y')
        # st.session_state["user_weights"][username].append((today_date, weight))
        collection.insert_one({"username": username, "date": today_date, "weight": weight})
        st.success("Weight Added")

    # user_data = pd.DataFrame(st.session_state["user_weights"][username], columns=["Date", "Weight"])
    user_weights = collection.find({"username":username})
    data = [(entry['date'], entry["weight"]) for entry in user_weights]
    if data:
        user_data = pd.DataFrame(data, columns=["Date", "Weight"])
        user_data["Date"] = pd.to_datetime(user_data["Date"], format='%d-%m-%Y')

        st.subheader("Your Weight History")
        fig = px.line(user_data, x="Date", y="Weight", title="Weight Tracker",
                      labels={"Date": "Date", "Weight": "Weight (kg)"})
        st.plotly_chart(fig, use_container_width=True)
    # if not user_data.empty:
    #     st.subheader("Your Weight History")

    #     fig = px.line(user_data, x="Date", y="Weight", title="Weight Tracker",
    #                   labels={"Date": "Date", "Weight": "Weight(kg)"})
    #     st.plotly_chart(fig, use_container_width=True)

    authenticator.logout("Logout", "sidebar")

else:
    st.write("Please Login to add weight")
