import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Health & Fitness Tracker", layout="wide")

st.title("🏋️ Health and Fitness Tracking App")

if not os.path.exists("health_log.csv"):
    pd.DataFrame(columns=["Date", "Sleep Hours", "Water Intake (L)", "Mood", "Steps"]).to_csv("health_log.csv", index=False)

if not os.path.exists("workouts.csv"):
    pd.DataFrame(columns=["Date", "Exercise", "Duration (mins)", "Calories Burned"]).to_csv("workouts.csv", index=False)

menu = st.sidebar.radio("Go to", ["Daily Log", "Workout Tracker", "Progress Charts", "About"])

if menu == "Daily Log":
    st.header("📋 Daily Health Log")

    today = date.today()
    sleep = st.number_input("Sleep Hours", 0.0, 24.0, step=0.5)
    water = st.number_input("Water Intake (Liters)", 0.0, 10.0, step=0.1)
    mood = st.selectbox("Mood", ["😊 Happy", "😐 Neutral", "😔 Sad"])
    steps = st.number_input("Steps Taken", 0)

    if st.button("Save Daily Log"):
        df = pd.read_csv("health_log.csv")
        new_data = {"Date": today, "Sleep Hours": sleep, "Water Intake (L)": water, "Mood": mood, "Steps": steps}
        df = df.append(new_data, ignore_index=True)
        df.to_csv("health_log.csv", index=False)
        st.success("Daily log saved!")

    st.subheader("Your Logs")
    st.dataframe(pd.read_csv("health_log.csv"))

elif menu == "Workout Tracker":
    st.header("🏃 Workout Tracker")

    exercise = st.text_input("Exercise Type")
    duration = st.number_input("Duration (minutes)", 0)
    calories = st.number_input("Calories Burned", 0)

    if st.button("Add Workout"):
        df = pd.read_csv("workouts.csv")
        new_data = {"Date": date.today(), "Exercise": exercise, "Duration (mins)": duration, "Calories Burned": calories}
        df = df.append(new_data, ignore_index=True)
        df.to_csv("workouts.csv", index=False)
        st.success("Workout added!")

    st.subheader("Your Workouts")
    st.dataframe(pd.read_csv("workouts.csv"))

elif menu == "Progress Charts":
    st.header("📊 Progress Visualization")

    health_df = pd.read_csv("health_log.csv")
    workout_df = pd.read_csv("workouts.csv")

    if not health_df.empty:
        st.subheader("Sleep Hours Over Time")
        st.line_chart(health_df.set_index("Date")["Sleep Hours"])

        st.subheader("Water Intake Over Time")
        st.line_chart(health_df.set_index("Date")["Water Intake (L)"])

        st.subheader("Steps Over Time")
        st.line_chart(health_df.set_index("Date")["Steps"])

    if not workout_df.empty:
        st.subheader("Calories Burned Over Time")
        st.line_chart(workout_df.set_index("Date")["Calories Burned"])

elif menu == "About":
    st.header("📘 About This App")
    st.write("""
    This health and fitness tracker was created using **Python** and **Streamlit**.
    
    It helps users:
    - Log daily health stats like sleep, water, mood, and steps
    - Track workouts and calories
    - Visualize progress with graphs

    Built by: Selu Saheed Muhammed
    """)

