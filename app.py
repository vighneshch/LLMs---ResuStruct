
#Importing the necesary libraries

import os
import PyPDF2
from pathlib import Path
from zipfile import ZipFile
import pandas as pd
from langchain.chains import create_extraction_chain
from langchain.chat_models import ChatOpenAI
import re

import streamlit as st
import time
import base64
import json

os.environ['OPENAI_API_KEY'] = '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'

#Reading the each pdf
def read_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''''''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text.splitlines()

#Parsing each file from the folder
def read_pdf_from_folder(folder_path):
    data = []

    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            file_path = os.path.join(folder_path, file)
            text_lines = read_pdf(file_path)
            data.append(text_lines)
    return data

#Extracting the PDF from the ZIP
def extract_pdf_from_zip(zip_file):

    folder_path = Path('PDFs')
    
    print("Received the file..")
    
    with ZipFile(zip_file,'r') as zip_file:
        print("Unzipping the file...")
        zip_file.extractall(folder_path)
        print("Successfully unzipped the file...")
    pdf_data = read_pdf_from_folder(folder_path)
    return pdf_data
    
def create_download_link(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:text/csv;base64,{b64}" download="{filename}">Download CSV file</a>'
    return href

#App Display Streamlit Code

st.set_page_config(layout='wide',
                   page_title='ResuStruct',
                   page_icon="🧊",
                   initial_sidebar_state="expanded")
st.title('_ResuStruct_ :sunglasses:')
st.markdown('Streamline :blue[Resumes], Supercharge :blue[Hiring]!')

uploaded_file = st.sidebar.file_uploader("Upload a ZIP file",
                                         type="zip")

if uploaded_file is not None:
    st.sidebar.success("File uploaded successfully!",icon="✅")
schema = {
    "properties": {
        "name": {"type": "string"},
        "linkedin_url": {"type": "string"},
        "email": {"type": "string"},
        "mobile_number": {"type":"integer"},
        "postgraduation_degree" : {"type":"string"},
        "postgraduation_university" : {"type":"string"},
        "postgraduation_cgpa" : {"type" : "string"},
        "degree_or_engineering" : {"type":"string"},
        "degree_or_engineering_university" : {"type":"string"},
        "degree_or_engineering_cgpa" : {"type" : "string"},
        "XII_college" : {"type":"string"},
        "XII_cgpa" : {"type":"string"},
        "X_school_name" : {"type":"string"},
        "X_cgpa" : {"type":"string"},
        "total_working_experience" : {"type":"integer"},
        "certificate1" : {"type":"string"},
        "certificate2" : {"type":"string"},
        "certificate3" : {"type":"string"},
        "certificate4" : {"type":"string"},
        "Technical_skill_1" : {"type":"string"},
        "No.of years experience in Technical_skill_1" : {"type":"integer"},
        "Technical_skill_2" : {"type":"string"},
        "No.of years experience in Technical_skill_2" : {"type":"integer"},
        "Technical_skill_3" : {"type":"string"},
        "No.of years experience in Technical_skill_3" : {"type":"integer"},
        "Technical_skill_4" : {"type":"string"},
        "No.of years experience in Technical_skill_4" : {"type":"integer"},
        "Technical_skill_5" : {"type":"string"},
        "No.of years experience in Technical_skill_5" : {"type":"integer"},
        "Technical_skill_6" : {"type":"string"},
        "No.of years experience in Technical_skill_6" : {"type":"integer"},
        "Technical_skill7" : {"type":"string"},
        "No.of_years_experience in Technical_skill_7" : {"type":"integer"},
        "Technical_skill_8" : {"type":"string"},
        "No.of years experience in Technical_skill_8" : {"type":"integer"},
        "Technical_skill_9" : {"type":"string"},
        "No.of years experience in Technical_skill_9" : {"type":"integer"},
        "Technical_skill_10" : {"type":"string"},
        "No.of years experience in Technical_skill_10" : {"type":"integer"},
        "Technical_skill_11" : {"type":"string"},
        "No.of years experience in Technical_skill_11" : {"type":"integer"},
        "Technical_skill_12" : {"type":"string"},
        "No.of years experience in Technical_skill_12" : {"type":"integer"},
        "soft_skills" : {"type":"string"},
        "project_1 name" : {"type":"string"},
        "skills_used_in_Project_1" : {"type":"string"},
        "time_taken_to_do_project_1" : {"type":"integer"},
        "project_2 name" : {"type":"string"},
        "skills_used_in_Project_2" : {"type":"string"},
        "time_taken_to_do_project_2" : {"type":"integer"},
        "project_3 name" : {"type":"string"},
        "skills_used_in_Project_3" : {"type":"string"},
        "time_taken_to_do_project_3" : {"type":"integer"},
        "project_4 name" : {"type":"string"},
        "skills_used_in_Project_4" : {"type":"string"},
        "time_taken_to_do_project_4" : {"type":"integer"},
        "Company1" : {"type":"string"},
        "Company1 role" : {"type":"string"},
        "Company1 working years and number" : {"type":"string"},
        "Company2" : {"type":"string"},
        "Company2 role" : {"type":"string"},
        "Company2 working years and number" : {"type":"string"},
        "Company3" : {"type":"string"},
        "Company3 role" : {"type":"string"},
        "Company3 working years and number" : {"type":"string"},
        "Company4" : {"type":"string"},
        "Company4 role" : {"type":"string"},
        "Company4 working years and number" : {"type":"string"},
        "Company5" : {"type":"string"},
        "Company5 role" : {"type":"string"},
        "Company5 working years" : {"type":"string"},
#         "Company2 along with role and years" : {"type":"string"},
#         "Company3 along with role and years" : {"type":"string"},
#         "Company4 along with role and years" : {"type":"string"},
#         "Company5 along with role and years" : {"type":"string"},
#         "Roles" : {"type":"string"},
#         "Company2" : {"type":"string"},
#         "Role" : {"type":"string"},
#         "Company3" : {"type":"string"},
#         "Role" : {"type":"string"},
#         "Company4" : {"type":"string"},
#         "Role" : {"type":"string"},
    },
    "required": ["name","linkedin_url","email","mobile_number"],
#     "required": ["name", "height"],
}
df = pd.DataFrame(columns = ['name','linkedin_url','email','mobile_number','postgraduation_degree','postgraduation_university','postgraduation_cgpa','bachelors_degree','bachelors_degree_university','degree_cgpa','XII_college','XII_cgpa','X_school_name','X_cgpa','total_working_experience','Technical_skills','Soft_Skills','Companies along with role'])
js = []
if st.sidebar.button("Extract Text 🚀",type='primary'):
    pdf_data = extract_pdf_from_zip(uploaded_file)
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(10)
    my_bar.empty()
    for i in pdf_data:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        chain = create_extraction_chain(schema, llm)
        output = chain.run(i)
        #st.write(output)
        for i in output:
            for key,value in i.items():
                if value is None or value == 'Not mentioned':
                    i[key] = '<Not Found>'
        
        json_format = re.sub('\'',"\"",str(output))
        json_format = json.dumps(output)
        js.append(pd.read_json(json_format))
    df = pd.concat(js,axis=0,ignore_index=True)
    st.dataframe(df)
    
    st.download_button(label="Download CSV :arrow_double_down:", data=df.to_csv(index=False), file_name='data.csv', mime='text/csv',type='secondary')
