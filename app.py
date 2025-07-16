import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Health & Fitness Tracker", layout="wide")

st.title("🏋️ Health and Fitness Tracking App")

# CSV File Names
health_file = "health_log.csv"
workout_file = "workouts.csv"

# Ensure CSVs exist
if not os.path.exists(health_file):
    pd.DataFrame(columns=["Date", "Sleep Hours", "Water Intake (L)", "Mood", "Steps"]).to_csv(health_file, index=False)

if not os.path.exists(workout_file):
    pd.DataFrame(columns=["Date", "Exercise", "Duration (mins)", "Calories Burned"]).to_csv(workout_file, index=False)

# Safe CSV loading
def load_csv(file, columns):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame(columns=columns)

# Navigation
menu = st.sidebar.radio("Go to", ["Daily Log", "Workout Tracker", "Progress Charts", "About"])

# Daily Health Log
if menu == "Daily Log":
    st.header("📋 Daily Health Log")

    today = date.today()
    sleep = st.number_input("Sleep Hours", 0.0, 24.0, step=0.5)
    water = st.number_input("Water Intake (Liters)", 0.0, 10.0, step=0.1)
    mood = st.selectbox("Mood", ["😊 Happy", "😐 Neutral", "😔 Sad"])
    steps = st.number_input("Steps Taken", 0)

    if st.button("Save Daily Log"):
        df = load_csv(health_file, ["Date", "Sleep Hours", "Water Intake (L)", "Mood", "Steps"])
        new_data = pd.DataFrame([{
            "Date": today,
            "Sleep Hours": sleep,
            "Water Intake (L)": water,
            "Mood": mood,
            "Steps": steps
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(health_file, index=False)
        st.success("✅ Daily log saved!")

    st.subheader("📄 Your Logs")
    st.dataframe(load_csv(health_file, ["Date", "Sleep Hours", "Water Intake (L)", "Mood", "Steps"]))

# Workout Tracker
elif menu == "Workout Tracker":
    st.header("🏃 Workout Tracker")

    exercise = st.text_input("Exercise Type")
    duration = st.number_input("Duration (minutes)", 0)
    calories = st.number_input("Calories Burned", 0)

    if st.button("Add Workout"):
        df = load_csv(workout_file, ["Date", "Exercise", "Duration (mins)", "Calories Burned"])
        new_data = pd.DataFrame([{
            "Date": date.today(),
            "Exercise": exercise,
            "Duration (mins)": duration,
            "Calories Burned": calories
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(workout_file, index=False)
        st.success("✅ Workout added!")

    st.subheader("📄 Your Workouts")
    st.dataframe(load_csv(workout_file, ["Date", "Exercise", "Duration (mins)", "Calories Burned"]))

# Progress Charts
elif menu == "Progress Charts":
    st.header("📊 Progress Visualization")

    health_df = load_csv(health_file, ["Date", "Sleep Hours", "Water Intake (L)", "Mood", "Steps"])
    workout_df = load_csv(workout_file, ["Date", "Exercise", "Duration (mins)", "Calories Burned"])

    if not health_df.empty:
        health_df["Date"] = pd.to_datetime(health_df["Date"])
        health_df = health_df.sort_values("Date")

        st.subheader("🛌 Sleep Hours Over Time")
        st.line_chart(health_df.set_index("Date")["Sleep Hours"])

        st.subheader("💧 Water Intake Over Time")
        st.line_chart(health_df.set_index("Date")["Water Intake (L)"])

        st.subheader("🚶 Steps Over Time")
        st.line_chart(health_df.set_index("Date")["Steps"])

    if not workout_df.empty:
        workout_df["Date"] = pd.to_datetime(workout_df["Date"])
        workout_df = workout_df.sort_values("Date")

        st.subheader("🔥 Calories Burned Over Time")
        st.line_chart(workout_df.set_index("Date")["Calories Burned"])

# About
elif menu == "About":
    st.header("📘 About This App")
    st.write("""
    This is a simple web app built with **Python** and **Streamlit**.

    It helps users:
    - Log daily health stats like sleep, water intake, mood, and steps
    - Track workouts and calories burned
    - Visualize progress over time

    Built by Selu Saheed Muhammed 🚀
    """)

