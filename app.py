import streamlit as st
import random

st.set_page_config(page_title="Family Day Fun App 🎉", layout="centered")

# SESSION STATE
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = {}

if "quiz_i" not in st.session_state:
    st.session_state.quiz_i = 0
    st.session_state.quiz_score = 0

menu = st.sidebar.radio(
    "🎮 Choose Game",
    ["🏠 Home", "🎯 Quiz", "🎡 Spin Wheel", "🎭 Charades", "🧠 Guess Game", "🏆 Scoreboard"]
)

if menu == "🏠 Home":
    st.title("🎉 Family Day Fun App")
    st.write("Welcome!")

elif menu == "🎯 Quiz":
    questions = [
        {"q": "Who is the oldest cousin?", "options": ["Ali", "Siti", "Ahmad"], "answer": "Ali"},
        {"q": "Family Day month?", "options": ["Jan", "May", "Dec"], "answer": "May"},
    ]

    q = questions[st.session_state.quiz_i]
    st.subheader(q["q"])

    choice = st.radio("Choose:", q["options"])

    if st.button("Submit"):
        if choice == q["answer"]:
            st.session_state.quiz_score += 1
            st.success("Correct!")
        else:
            st.error("Wrong")

        st.session_state.quiz_i += 1
        if st.session_state.quiz_i >= len(questions):
            st.session_state.quiz_i = 0

    st.write("Score:", st.session_state.quiz_score)

elif menu == "🎡 Spin Wheel":
    items = ["Sing 🎤", "Dance 💃", "Selfie 🤳", "Joke 😂"]
    if st.button("SPIN"):
        st.success(random.choice(items))

elif menu == "🎭 Charades":
    words = ["Cooking", "Sleeping", "Football"]
    if st.button("Get Word"):
        st.header(random.choice(words))

elif menu == "🧠 Guess Game":
    answer = "ali"
    guess = st.text_input("Guess family member")

    if st.button("Check"):
        if guess.lower() == answer:
            st.success("Correct!")
        else:
            st.error("Try again")

elif menu == "🏆 Scoreboard":
    name = st.text_input("Name")
    score = st.number_input("Score", 0)

    if st.button("Save"):
        st.session_state.scoreboard[name] = score

    st.write(st.session_state.scoreboard)
