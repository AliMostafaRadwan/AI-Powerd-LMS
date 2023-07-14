import re

# Read the text file
with open('questions.txt', 'r') as file:
    text = file.read()

# Split the text into questions and choices
result = re.split(r'\n\d+\. ', text)[0:]
# result = text.split("\n\n")
nested_list = []

# Process each question and its choices
for question in result:
    question_number, question_text = question.split('. ', 1)
    choices = re.findall(r'\n([a-d])\. (.+)', question_text)
    nested_list.append([question_text.strip()] + choices)

# Access the choices using nested_list[question_number - 1][choice_number - 1]
print(nested_list[0][3])  # Accesses the 1st question, 4th choice
