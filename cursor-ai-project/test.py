import openai
import streamlit as st
import re
from streamlit_chat import message

openai.api_key = ""



with open("questions.txt", "r") as f:
    content = f.read()
    questions = content.split("\n\n")
    only_questions = [question.split("\n")[0] for question in questions]
    only_answers = re.split(r'[abcd]\.', str(questions))
    only_answers = [r.strip() for r in only_answers if r.strip()]

message("choose what applies to you")
answers = []
for i, question in enumerate(questions):
    st.code(f"{question}")
    list_of_options = ["A", "B", "C", "D"]
    list_o_answers = []
    test_list = []
    for id, option in enumerate(list_of_options):
        answer = st.checkbox(f"{option}", key=f"{i}{id}")
        list_o_answers.append(answer)
        if answer:
            test_list.append(option)
    answers.append(list_o_answers)

done = st.button("Done")
# remove existing results.txt data
try:
    with open("results.txt", "w") as f:
        f.write("")
except:
    pass

if done:
    choices_list = []
    for question in questions:
        choices = re.findall(r'\n([a-d])\. (.+)', question)
        choices_list.append(choices)

    # results = {
    #     0: "Visual",
    #     1: "Auditory",
    #     2: "Read/Write",
    #     3: "Kinesthetic"
    # }

    results_list = []
    for answer, choices in zip(answers, choices_list):
        result = [choices[i] for i, ans in enumerate(answer) if ans]
        results_list.append(result) 

    for i, only_question in enumerate(only_questions):
        # st.write(f"{only_question} {results_list[i]}")
        
        with open("results.txt", "a") as f:
            output = f"{only_question} {results_list[i]}\n"
            f.write(f"{only_question} {results_list[i]}\n")
    message('The VARK test results are:')
    
    PROMPET_TEMPLATE = "make a suggestion for me of the best way to learn the school subjects (math, physics, calculus, chemistry,biology, mechanics, languages) according to the VARK test results i took, make it as a bullit-point for each subject and the best way to learn it. The VARK test results are:"
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{PROMPET_TEMPLATE} {output}"}])
    results = chat_completion.choices[0].message.content
    message(str(results))

    
    # st.write(results_list) 

