import streamlit as st

st.set_page_config(page_title="Family Quiz 🎯", layout="centered")

# -----------------------
# QUESTIONS
# -----------------------
questions = [
    {"q": "Who is the oldest cousin?", "options": ["Ali", "Siti", "Ahmad"], "answer": "Ali"},
    {"q": "Family Day month?", "options": ["Jan", "May", "Dec"], "answer": "May"},
    {"q": "How many days in a week?", "options": ["5", "6", "7"], "answer": "7"},
]

# -----------------------
# GLOBAL LEADERBOARD (SESSION)
# -----------------------
if "board" not in st.session_state:
    st.session_state.board = {}

# -----------------------
# PLAYER NAME
# -----------------------
st.title("🎯 Family Day Quiz Battle")

name = st.text_input("Enter your name 👇")

if name:

    if "i" not in st.session_state:
        st.session_state.i = 0
        st.session_state.score = 0
        st.session_state.finished = False

    if not st.session_state.finished:

        q = questions[st.session_state.i]

        st.subheader(q["q"])
        choice = st.radio("Choose:", q["options"], key=st.session_state.i)

        if st.button("Submit"):
            if choice == q["answer"]:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error("Wrong!")

            st.session_state.i += 1

            if st.session_state.i >= len(questions):
                st.session_state.finished = True
            else:
                st.rerun()

    else:
        st.success(f"🎉 {name}, your score: {st.session_state.score}")

        # SAVE SCORE
        st.session_state.board[name] = st.session_state.score

        if st.button("Play Again"):
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.finished = False
            st.rerun()

# -----------------------
# LEADERBOARD
# -----------------------
st.divider()
st.subheader("🏆 Leaderboard")

if st.session_state.board:
    for k, v in sorted(st.session_state.board.items(), key=lambda x: x[1], reverse=True):
        st.write(f"👤 {k} — ⭐ {v}")
else:
    st.write("No scores yet")