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
# INIT STATE
# -----------------------
if "i" not in st.session_state:
    st.session_state.i = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

if "name" not in st.session_state:
    st.session_state.name = ""

# -----------------------
# TITLE
# -----------------------
st.title("🎯 Family Day Quiz Game")

# -----------------------
# NAME INPUT (FIXED STABILITY)
# -----------------------
if not st.session_state.name:
    st.session_state.name = st.text_input("Enter your name 👇")

if st.session_state.name:

    # -----------------------
    # GAME LOGIC
    # -----------------------
    if not st.session_state.finished:

        q = questions[st.session_state.i]

        st.subheader(f"Q{st.session_state.i + 1}: {q['q']}")

        # IMPORTANT FIX: NO dynamic key
        choice = st.radio("Choose answer:", q["options"])

        if st.button("Submit Answer"):

            if choice == q["answer"]:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error(f"Wrong! Correct answer: {q['answer']}")

            st.session_state.i += 1

            if st.session_state.i >= len(questions):
                st.session_state.finished = True

            st.rerun()

    # -----------------------
    # RESULT PAGE
    # -----------------------
    else:
        st.success(f"🎉 {st.session_state.name}, Quiz Completed!")
        st.write(f"Score: **{st.session_state.score} / {len(questions)}**")

        if st.button("Play Again"):
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.finished = False
            st.rerun()