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

if "answered" not in st.session_state:
    st.session_state.answered = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if "name" not in st.session_state:
    st.session_state.name = ""

# -----------------------
# ANALYTICS HELPERS
# -----------------------
def get_stats():
    scores = list(st.session_state.leaderboard.values())
    if not scores:
        return 0, 0, 0
    return len(scores), max(scores), sum(scores) / len(scores)

# -----------------------
# TITLE (GAME STYLE UI)
# -----------------------
st.markdown(
    """
    <h1 style='text-align: center;'>🎯 Family Day Quiz Challenge</h1>
    """,
    unsafe_allow_html=True
)

st.progress(st.session_state.i / len(questions))

st.write(f"📊 Question {st.session_state.i + 1} of {len(questions)}")

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
    # QUIZ
    # -----------------------
    if st.session_state.i < len(questions):

        q = questions[st.session_state.i]

        st.markdown(
            f"""
            <div style="
                padding:20px;
                border-radius:15px;
                background-color:#f2f2f2;
                text-align:center;
                font-size:20px;">
                {q['q']}
            </div>
            """,
            unsafe_allow_html=True
        )

        options = ["-- Select --"] + q["options"]

        choice = st.radio(
            "Choose your answer:",
            options,
            index=0,
            disabled=st.session_state.answered
        )

        if not st.session_state.answered:

            if st.button("Submit Answer"):

                if choice == "-- Select --":
                    st.warning("⚠️ Please choose an answer")
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

    # -----------------------
    # RESULT PAGE
    # -----------------------
    else:
        st.success("🎉 Quiz Completed!")

        st.markdown(f"""
        <div style='text-align:center; font-size:20px;'>
        👤 {st.session_state.name}<br>
        ⭐ Score: {st.session_state.score} / {len(questions)}
        </div>
        """, unsafe_allow_html=True)

        # SAVE SCORE
        st.session_state.leaderboard[st.session_state.name] = st.session_state.score

        if st.button("Play Again"):
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.feedback = ""
            st.rerun()

        # -----------------------
        # LEADERBOARD
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

        # -----------------------
        # ANALYTICS DASHBOARD
        # -----------------------
        st.divider()
        st.subheader("📊 Analytics Dashboard")

        total_players, max_score, avg_score = get_stats()

        st.write(f"👥 Total Players: {total_players}")
        st.write(f"🏆 Highest Score: {max_score}")
        st.write(f"📈 Average Score: {avg_score:.2f}")