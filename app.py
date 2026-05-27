
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Family Quiz 🎯", layout="centered")

# =======================
# ADMIN PASSWORD
# =======================
ADMIN_PASSWORD = "family123"  # change this if you want

# =======================
# QUESTIONS
# =======================
questions = [
    {"q": "Who is the oldest cousin in the family?", "options": ["Ali", "Siti", "Ahmad", "Maya"], "answer": "Ali"},
    {"q": "Family Day is usually held in which month?", "options": ["January", "May", "August", "December"], "answer": "May"},
    {"q": "How many days are there in a week?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"q": "Which activity is most common in Family Day?", "options": ["Sleeping", "Games", "Studying", "Working"], "answer": "Games"},
    {"q": "What is the main purpose of Family Day?", "options": ["Compete", "Bonding", "Travel alone", "Work"], "answer": "Bonding"},
]

# =======================
# LEADERBOARD FILE
# =======================
FILE = "leaderboard.csv"

def load_board():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["name", "score"])

def save_board(df):
    df.to_csv(FILE, index=False)

def reset_board():
    df = pd.DataFrame(columns=["name", "score"])
    df.to_csv(FILE, index=False)

# =======================
# SESSION STATE
# =======================
defaults = {
    "name": "",
    "started": False,
    "finished": False,
    "i": 0,
    "score": 0,
    "answered": False,
    "feedback": "",
    "saved": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =======================
# TITLE
# =======================
st.markdown(
    "<h1 style='text-align:center; color:#2E86C1;'>🎯 Family Quiz Challenge</h1>",
    unsafe_allow_html=True
)

st.divider()

# =======================
# SIDEBAR LEADERBOARD
# =======================
st.sidebar.title("🏆 Leaderboard")

board = load_board()

if not board.empty:
    board = board.sort_values(by="score", ascending=False)

    for rank, row in enumerate(board.itertuples(), start=1):
        st.sidebar.write(f"{rank}. 👤 {row.name} — ⭐ {row.score}")
else:
    st.sidebar.write("No scores yet.")

# =======================
# ADMIN RESET (PASSWORD PROTECTED)
# =======================
st.sidebar.divider()
st.sidebar.subheader("🔐 Admin Panel")

password = st.sidebar.text_input("Enter admin password", type="password")

if st.sidebar.button("🧹 Reset Leaderboard"):
    if password == ADMIN_PASSWORD:
        reset_board()
        st.sidebar.success("Leaderboard reset successfully!")
        st.rerun()
    else:
        st.sidebar.error("❌ Wrong password!")

# =======================
# NAME INPUT
# =======================
if not st.session_state.name:
    st.session_state.name = st.text_input("👋 Enter your name")

# =======================
# START BUTTON
# =======================
if st.session_state.name and not st.session_state.started:
    st.success(f"Welcome {st.session_state.name} 👏")

    if st.button("🚀 START QUIZ"):
        st.session_state.started = True
        st.rerun()

# =======================
# QUIZ FLOW
# =======================
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

        if st.session_state.answered:
            if st.button("Next ➜"):
                st.session_state.i += 1
                st.session_state.answered = False
                st.session_state.feedback = ""
                st.rerun()

    # =======================
    # FINAL SCREEN (SAVE SCORE)
    # =======================
    else:
        st.session_state.finished = True

        st.success("🎉 Quiz Completed!")

        st.write(f"👤 Name: **{st.session_state.name}**")
        st.write(f"⭐ Score: **{st.session_state.score} / {len(questions)}**")

        # SAVE ONLY ONCE
        if not st.session_state.saved:

            board = load_board()

            new_row = pd.DataFrame(
                [[st.session_state.name, st.session_state.score]],
                columns=["name", "score"]
            )

            board = pd.concat([board, new_row], ignore_index=True)

            # keep best score per user
            board = board.groupby("name", as_index=False)["score"].max()

            save_board(board)

            st.session_state.saved = True

        st.rerun()

# =======================
# PLAY AGAIN
# =======================
if st.session_state.finished:
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