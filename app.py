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
if "started" not in st.session_state:
    st.session_state.started = False

if "name" not in st.session_state:
    st.session_state.name = ""

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

# -----------------------
# TITLE (BIG GAME STYLE)
# -----------------------
st.markdown(
    """
    <h1 style='text-align:center; font-size:52px; color:#2E86C1;'>
    🎯 Family Day Quiz Challenge
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; font-size:22px; color:gray;'>
    Compete with your family and see who is the smartest! 🏆
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------
# START SCREEN CARD
# -----------------------
if not st.session_state.name:
    st.markdown(
        """
        <div style="
            text-align:center;
            padding:25px;
            border-radius:20px;
            background-color:#f5f7ff;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        ">
            <h2 style="font-size:28px;">👋 Welcome Player!</h2>
            <p style="font-size:18px;">Enter your name to start the challenge</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.session_state.name = st.text_input("", placeholder="Type your name here...")

# -----------------------
# START BUTTON (ONLY AFTER NAME)
# -----------------------
if st.session_state.name and not st.session_state.started:
    st.success(f"Welcome {st.session_state.name} 👏")

    st.markdown(
        """
        <p style='font-size:20px; text-align:center;'>
        Ready to test your family knowledge? 😄
        </p>
        """,
        unsafe_allow_html=True
    )

    if st.button("🚀 START QUIZ"):
        st.session_state.started = True
        st.rerun()

# -----------------------
# QUIZ GAME
# -----------------------
if st.session_state.started:

    if st.session_state.i < len(questions):

        q = questions[st.session_state.i]

        st.subheader(f"Question {st.session_state.i + 1} / {len(questions)}")
        st.write(q["q"])

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
                    if choice == q["answer"]:
                        st.session_state.score += 1
                        st.session_state.feedback = "✅ Correct!"
                    else:
                        st.session_state.feedback = "❌ Wrong!"

                    st.session_state.answered = True

        # -----------------------
        # FEEDBACK
        # -----------------------
        if st.session_state.feedback:
            st.info(st.session_state.feedback)

        # -----------------------
        # NEXT BUTTON
        # -----------------------
        if st.session_state.answered:
            if st.button("Next ➜"):
                st.session_state.i += 1
                st.session_state.answered = False
                st.session_state.feedback = ""
                st.rerun()

    # -----------------------
    # FINAL SCREEN
    # -----------------------
    else:
        st.success("🎉 Quiz Completed!")

        st.write(f"👤 Name: **{st.session_state.name}**")
        st.write(f"⭐ Score: **{st.session_state.score} / {len(questions)}**")

        # SAVE SCORE
        st.session_state.leaderboard[st.session_state.name] = st.session_state.score

        if st.button("Play Again"):
            st.session_state.started = False
            st.session_state.name = ""
            st.session_state.i = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.feedback = ""
            st.rerun()

        # -----------------------
# SIDEBAR LEADERBOARD (PERSISTENT)
# -----------------------
st.sidebar.title("🏆 Leaderboard")

if st.session_state.leaderboard:
    sorted_board = sorted(
        st.session_state.leaderboard.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for name, score in sorted_board:
        st.sidebar.write(f"👤 {name} — ⭐ {score}")
else:
    st.sidebar.write("No scores yet.")

        # -----------------------
        # ANALYTICS (NO AVERAGE SCORE)
        # -----------------------
        st.divider()
        st.subheader("📊 Analytics Dashboard")

        total_players = len(st.session_state.leaderboard)
        highest_score = max(st.session_state.leaderboard.values(), default=0)

        st.write(f"👥 Total Players: {total_players}")
        st.write(f"🏆 Highest Score: {highest_score}")