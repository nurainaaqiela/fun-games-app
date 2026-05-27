import streamlit as st

st.set_page_config(page_title="Family Quiz 🎯", layout="centered")

# -----------------------
# DATA (EDIT YOUR QUESTIONS HERE)
# -----------------------
questions = [
    {
        "q": "Who is the oldest cousin in the family?",
        "options": ["Ali", "Siti", "Ahmad", "Maya"],
        "answer": "Ali"
    },
    {
        "q": "Family Day is usually held in which month?",
        "options": ["January", "May", "December", "August"],
        "answer": "May"
    },
    {
        "q": "How many days are there in a week?",
        "options": ["5", "6", "7", "8"],
        "answer": "7"
    },
    {
        "q": "Which activity is most fun in Family Day?",
        "options": ["Sleeping", "Games", "Studying", "Working"],
        "answer": "Games"
    }
]

# -----------------------
# SESSION STATE (SAVE PROGRESS)
# -----------------------
if "index" not in st.session_state:
    st.session_state.index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

# -----------------------
# TITLE
# -----------------------
st.title("🎯 Family Day Quiz Game")
st.write("Answer the questions and see who gets the highest score! 🎉")

# -----------------------
# GAME LOGIC
# -----------------------
if not st.session_state.finished:

    q = questions[st.session_state.index]

    st.subheader(f"Q{st.session_state.index + 1}: {q['q']}")

    choice = st.radio("Choose your answer:", q["options"], key=st.session_state.index)

    if st.button("Submit Answer"):

        if choice == q["answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! Correct answer: {q['answer']}")

        st.session_state.index += 1

        if st.session_state.index >= len(questions):
            st.session_state.finished = True
        else:
            st.rerun()

# -----------------------
# RESULT PAGE
# -----------------------
else:
    st.success("🎉 Quiz Completed!")
    st.write(f"Your final score: **{st.session_state.score} / {len(questions)}**")

    if st.button("Play Again 🔄"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.rerun()