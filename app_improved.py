
import streamlit as st
import json
import random

# Load questions from JSON
@st.cache_data
def load_questions():
    with open("parsed_questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions_data = load_questions()

# Sidebar - chapter selection
st.sidebar.title("📚 Quiz Settings")
selected_chapters = st.sidebar.multiselect(
    "Select Chapter(s):",
    options=list(questions_data.keys()),
    default=list(questions_data.keys()),
    key="chapter_selector"
)

# Restart or refresh the quiz
def initialize_quiz():
    st.session_state.questions = []
    for chapter in st.session_state.chapter_selector:
        st.session_state.questions.extend(questions_data.get(chapter, []))
    random.shuffle(st.session_state.questions)
    st.session_state.current = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.answered = False
    st.session_state.user_answer = None

# Track if chapters were changed
if "prev_chapters" not in st.session_state:
    st.session_state.prev_chapters = selected_chapters.copy()

if selected_chapters != st.session_state.prev_chapters:
    st.session_state.prev_chapters = selected_chapters.copy()
    initialize_quiz()

# Button to manually restart quiz
if st.sidebar.button("🔄 Restart Quiz"):
    initialize_quiz()

# Initialize quiz state if first load
if "questions" not in st.session_state:
    initialize_quiz()

# Dashboard sidebar
total = len(st.session_state.questions)
attempted = st.session_state.current
score = st.session_state.correct
progress = score / attempted * 100 if attempted else 0

st.sidebar.markdown("### 📊 Progress")
st.sidebar.write(f"Questions Selected: {total}")
st.sidebar.write(f"Questions Attempted: {attempted}")
st.sidebar.write(f"Correct: {st.session_state.correct}")
st.sidebar.write(f"Incorrect: {st.session_state.incorrect}")
st.sidebar.progress(progress / 100)

# Main quiz interface
if st.session_state.current < total:
    question = st.session_state.questions[st.session_state.current]
    st.markdown(f"### Question {st.session_state.current + 1} of {total}")
    st.write(question["question"])

    selected_option = st.radio("Options:", question["options"], key=f"q_{st.session_state.current}")

    if not st.session_state.answered:
        if st.button("✅ Submit", key=f"submit_{st.session_state.current}"):
            if selected_option == question["answer"]:
                st.success("✅ Correct!")
                st.session_state.correct += 1
            else:
                st.error(f"❌ Incorrect! The correct answer is: **{question['answer']}**")
                st.session_state.incorrect += 1
            st.session_state.answered = True
    else:
        if st.button("➡️ Next", key=f"next_{st.session_state.current}"):
            st.session_state.current += 1
            st.session_state.answered = False
            st.session_state.user_answer = None
else:
    st.markdown("## 🏁 Quiz Completed!")
    st.success(f"Final Score: {st.session_state.correct} / {total} "
               f"({round(st.session_state.correct / total * 100, 2)}%)")
    if st.button("🔁 Restart Quiz Now"):
        initialize_quiz()
