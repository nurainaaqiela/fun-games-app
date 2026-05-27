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
# SESSION STATE
# -----------------------
if "i" not in st.session_state:
    st.session_state.i = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if "name" not in st.session_state:
    st.session_state.name = ""

# -----------------------
# TITLE
# -----------------------
st.title("🎯 Family Day Quiz Game")

# -----------------------
# NAME INPUT
# -----------------------
if not st.session_state.name:
    st.session_state.name = st.text_input("Enter your name 👇")

# -----------------------
# GAME START
# -----------------------
if st.session_state.name:

    if not st.session_state.finished:

        q = questions[st.session_state.i]

        st.subheader(f"Q{st.session_state.i + 1}: {q['q']}")

        choice = st.radio("Choose answer:", q["options"])

        if st.button("Submit Answer"):

            correct = q["answer"]

            if choice == correct:
                st.session_state.score += 1
                st.session_state.feedback = "✅ Correct!"
            else:
                st.session_state.feedback = f"❌ Wrong! Correct answer is: {correct}"

            st.session_state.i += 1

            if st.session_state.i >= len(questions):
                st.session_state.finished = True

            st.rerun()

        # SHOW FEEDBACK
        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    # -----------------------
    # RESULT PAGE
    # -----------------------
    else:
        st.success(f"🎉 {st.session_state.name}, Quiz Completed!")
        st.write(f"Final Score: **{st.session_state.score} / {len(questions)}**")

        # SAVE TO LEADERBOARD
        st.session_state.leaderboard[st.session_state.name] = st.session_state.score

        if st.button("Play Again"):
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.finished = False
            st.session_state.feedback = ""
            st.rerun()

# -----------------------
# LEADERBOARD
# -----------------------
st.divider()
st.subheader("🏆 Leaderboard")

if st.session_state.leaderboard:
    sorted_board = sorted(
        st.session_state.leaderboard.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for name, score in sorted_board:
        st.write(f"👤 {name} — ⭐ {score}")
else:
    st.write("No scores yet")