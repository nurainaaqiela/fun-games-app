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

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "answered" not in st.session_state:
    st.session_state.answered = False

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

    # -----------------------
    # QUIZ NOT FINISHED
    # -----------------------
    if st.session_state.i < len(questions):

        q = questions[st.session_state.i]

        st.subheader(f"Q{st.session_state.i + 1}: {q['q']}")

        # Disable radio after answering
        choice = st.radio(
            "Choose answer:",
            q["options"],
            disabled=st.session_state.answered
        )

        # -----------------------
        # SUBMIT ANSWER
        # -----------------------
        if not st.session_state.answered:
            if st.button("Submit Answer"):
                correct = q["answer"]

                if choice == correct:
                    st.session_state.score += 1
                    st.session_state.feedback = "✅ Correct!"
                else:
                    st.session_state.feedback = f"❌ Wrong! Correct answer: {correct}"

                st.session_state.answered = True

        # -----------------------
        # SHOW FEEDBACK
        # -----------------------
        if st.session_state.feedback:
            st.info(st.session_state.feedback)

        # -----------------------
        # NEXT BUTTON
        # -----------------------
        if st.session_state.answered:
            if st.button("Next ➜"):
                st.session_state.i += 1
                st.session_state.feedback = ""
                st.session_state.answered = False
                st.rerun()

    # -----------------------
    # FINISHED QUIZ
    # -----------------------
    else:
        st.success("🎉 Quiz Completed!")
        st.write(f"Name: **{st.session_state.name}**")
        st.write(f"Score: **{st.session_state.score} / {len(questions)}**")

        # SAVE SCORE
        st.session_state.leaderboard[st.session_state.name] = st.session_state.score

        if st.button("Play Again"):
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.feedback = ""
            st.session_state.answered = False
            st.rerun()

        # -----------------------
        # LEADERBOARD (ONLY AT END)
        # -----------------------
        st.divider()
        st.subheader("🏆 Leaderboard")

        sorted_board = sorted(
            st.session_state.leaderboard.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for name, score in sorted_board:
            st.write(f"👤 {name} — ⭐ {score}")