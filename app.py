import streamlit as st

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
# SESSION STATE
# -----------------------
if "i" not in st.session_state:
    st.session_state.i = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "bonus" not in st.session_state:
    st.session_state.bonus = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if "name" not in st.session_state:
    st.session_state.name = ""

# -----------------------
# TITLE
# -----------------------
st.title("🎯 Family Day Quiz (Bonus Fixed)")

# -----------------------
# NAME
# -----------------------
if not st.session_state.name:
    st.session_state.name = st.text_input("Enter your name 👇")

# -----------------------
# GAME
# -----------------------
if st.session_state.name:

    if st.session_state.i < len(questions):

        q = questions[st.session_state.i]

        st.subheader(f"Q{st.session_state.i + 1}: {q['q']}")

        options = ["-- Select an answer --"] + q["options"]

        choice = st.radio(
            "Choose your answer:",
            options,
            index=0,
            disabled=st.session_state.answered
        )

        # -----------------------
        # SUBMIT
        # -----------------------
        if not st.session_state.answered:

            if st.button("Submit Answer"):

                if choice == "-- Select an answer --":
                    st.warning("⚠️ Please select an answer first!")
                else:
                    correct = q["answer"]

                    if choice == correct:
                        st.session_state.score += 1
                        st.session_state.streak += 1

                        # ⭐ BONUS RULE (FIXED)
                        if st.session_state.streak >= 2:
                            st.session_state.bonus += 1
                            st.session_state.feedback = "✅ Correct! +1 ⭐ BONUS (streak!)"
                        else:
                            st.session_state.feedback = "✅ Correct!"

                    else:
                        st.session_state.streak = 0
                        st.session_state.feedback = "❌ Wrong!"

                    st.session_state.answered = True

        # -----------------------
        # FEEDBACK
        # -----------------------
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
    # END
    # -----------------------
    else:
        total = st.session_state.score + st.session_state.bonus

        st.success("🎉 Quiz Completed!")
        st.write(f"⭐ Score: {st.session_state.score}")
        st.write(f"⚡ Bonus: {st.session_state.bonus}")
        st.write(f"🏆 Total: **{total}**")

        st.session_state.leaderboard[st.session_state.name] = total

        if st.button("Play Again"):
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.bonus = 0
            st.session_state.streak = 0
            st.session_state.answered = False
            st.session_state.feedback = ""
            st.rerun()

        st.divider()
        st.subheader("🏆 Leaderboard")

        sorted_board = sorted(
            st.session_state.leaderboard.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for name, score in sorted_board:
            st.write(f"👤 {name} — 🏆 {score}")