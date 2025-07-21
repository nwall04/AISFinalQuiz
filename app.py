
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
    default=list(questions_data.keys())
)

# Restart quiz button
if st.sidebar.button("🔄 Restart Quiz"):
    st.session_state.clear()

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
    for chapter in selected_chapters:
        st.session_state.questions.extend(questions_data[chapter])
    random.shuffle(st.session_state.questions)
    st.session_state.current = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.answered = False

# Progress dashboard
total = len(st.session_state.questions)
attempted = st.session_state.current
score = st.session_state.correct
progress = score / attempted * 100 if attempted else 0
st.sidebar.markdown("### 📊 Progress")
st.sidebar.write(f"Questions Attempted: {attempted}")
st.sidebar.write(f"Correct: {st.session_state.correct}")
st.sidebar.write(f"Incorrect: {st.session_state.incorrect}")
st.sidebar.progress(progress / 100)

# Main quiz display
if st.session_state.current < total:
    question = st.session_state.questions[st.session_state.current]
    st.markdown(f"### Question {st.session_state.current + 1}")
    st.write(question["question"])
    user_answer = st.radio("Options:", question["options"], key=st.session_state.current)

    if not st.session_state.answered:
        if st.button("Submit Answer"):
            if user_answer == question["answer"]:
                st.success("✅ Correct!")
                st.session_state.correct += 1
            else:
                st.error(f"❌ Incorrect! The correct answer is: **{question['answer']}**")
                st.session_state.incorrect += 1
            st.session_state.answered = True
    else:
        if st.button("Next Question"):
            st.session_state.current += 1
            st.session_state.answered = False
else:
    st.markdown("## 🏁 Quiz Completed!")
    st.success(f"Final Score: {st.session_state.correct} / {total} "
               f"({round(st.session_state.correct / total * 100, 2)}%)")
    if st.button("🔁 Restart"):
        st.session_state.clear()
