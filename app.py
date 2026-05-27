import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Family Quiz 🎯", layout="centered")

# -----------------------
# QUESTIONS
# -----------------------
questions = [
    {"q": "Who is the oldest cousin in the family?", "options": ["Ali", "Siti", "Ahmad", "Maya"], "answer": "Ali"},
    {"q": "Family Day is usually held in which month?", "options": ["January", "May", "August", "December"], "answer": "May"},
    {"q": "How many days are there in a week?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"q": "Which activity is most common in Family Day?", "options": ["Sleeping", "Games", "Studying", "Working"], "answer": "Games"},
    {"q": "What is the main purpose of Family Day?", "options": ["Compete", "Bonding", "Travel alone", "Work"], "answer": "Bonding"},
]

# -----------------------
# LEADERBOARD FILE
# -----------------------
LEADERBOARD_FILE = "leaderboard.csv"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        return pd.read_csv(LEADERBOARD_FILE)
    return pd.DataFrame(columns=["name", "score"])

def save_leaderboard(df):
    df.to_csv(LEADERBOARD_FILE, index=False)

# -----------------------
# SESSION STATE
# -----------------------
if "name" not in st.session_state:
    st.session_state.name = ""

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "i" not in st.session_state:
    st.session_state.i = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "saved" not in st.session_state:
    st.session_state.saved = False

# -----------------------
# TITLE
# -----------------------
st.markdown(
    "<h1 style='text-align:center; color:#2E86C1;'>🎯 Family Quiz Challenge</h1>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------
# LEADERBOARD (SIDEBAR - ALWAYS LIVE)
# -----------------------
st.sidebar.title("🏆 Leaderboard")

leaderboard_df = load_leaderboard()

if not leaderboard_df.empty:
    leaderboard_df = leaderboard_df.sort_values(by="score", ascending=False)

    for rank, row in enumerate(leaderboard_df.itertuples(), start=1):
        st.sidebar.write(f"{rank}. 👤 {row.name} — ⭐ {row.score}")
else:
    st.sidebar.write("No scores yet.")

# -----------------------
# NAME INPUT
# -----------------------
if not st.session_state.name:
    st.session_state.name = st.text_input("👋 Enter your name")

# -----------------------
# START BUTTON
# -----------------------
if st.session_state.name and not st.session_state.started:
    st.success(f"Welcome {st.session_state.name} 👏")

    if st.button("🚀 START QUIZ"):
        st.session_state.started = True
        st.rerun()

# -----------------------
# QUIZ FLOW
# -----------------------
if st.session_state.started and not st.session_state.finished:

    if st.session_state.i < len(questions):

        q = questions[st.session_state.i]

        st.subheader(f"Question {st.session_state.i + 1} / {len(questions)}")
        st.write(q["q"])

        options = ["-- Select --"] + q["options"]

        choice = st.radio(
            "Choose answer:",
            options,
            index=0,
            disabled=st.session_state.answered
        )

        # -----------------------
        # SUBMIT
        # -----------------------
        if not st.session_state.answered:
            if st.button("Submit"):
                if choice == "-- Select --":
                    st.warning("Please select an answer!")
                else:
                    if choice == q["answer"]:
                        st.session_state.score += 1
                        st.session_state.feedback = "✅ Correct!"
                    else:
                        st.session_state.feedback = "❌ Wrong!"

                    st.session_state.answered = True

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

        # -----------------------
        # NEXT
        # -----------------------
        if st.session_state.answered:
            if st.button("Next ➜"):
                st.session_state.i += 1
                st.session_state.answered = False
                st.session_state.feedback = ""
                st.rerun()

    # -----------------------
    # FINAL SCREEN (SAVE ONCE)
    # -----------------------
    else:
        st.session_state.finished = True

        st.success("🎉 Quiz Completed!")

        st.write(f"👤 Name: **{st.session_state.name}**")
        st.write(f"⭐ Score: **{st.session_state.score} / {len(questions)}**")

        # SAVE ONLY ONCE
        if not st.session_state.saved:

            leaderboard_df = load_leaderboard()

            new_row = pd.DataFrame(
                [[st.session_state.name, st.session_state.score]],
                columns=["name", "score"]
            )

            leaderboard_df = pd.concat([leaderboard_df, new_row], ignore_index=True)

            # keep highest score per user
            leaderboard_df = leaderboard_df.groupby("name", as_index=False)["score"].max()

            save_leaderboard(leaderboard_df)

            st.session_state.saved = True

        # -----------------------
        # PLAY AGAIN RESET
        # -----------------------
        if st.button("🔁 Play Again"):
            st.session_state.name = ""
            st.session_state.started = False
            st.session_state.finished = False
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.feedback = ""
            st.session_state.saved = False
            st.rerun()