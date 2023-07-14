import streamlit as st
from vark import VarkTest

# Load questions from file
with open("questions.txt", "r") as f:
    questions = f.readlines()

# Create VarkTest object
vark_test = VarkTest(questions)

# Streamlit app
st.title("VARK Test")

# Display instructions
st.write("Answer the following questions to determine your learning style according to the VARK test.")

# Display questions and get user answers
answers = []
for i, question in enumerate(vark_test.questions):
    answer = st.radio(f"Q{i+1}. {question}", options=vark_test.options, horizontal = True)
    answers.append(answer)

# Calculate and display results
results = vark_test.calculate_results(answers)
st.write(f"Your learning style is {results}.")
