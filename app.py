import streamlit as st
import google.generativeai as genai

file = open("keys\geminiapi.text")
key = file.read()
genai.configure(api_key = key)

# for model in genai.list_models():
#     st.write(model.name)

sys_guide = '''
            You are a code reviewer and you need to generate only potential bug report as well as fixed code
            for every python code given by user.
            If the code is not in python programming language then kindly decline it and tell them to
            provide python code only for review.
            '''

model = genai.GenerativeModel(
            model_name = "gemini-1.5-flash",
            system_instruction = sys_guide
        )

# Function to generate output text
def generate_response(user_query):
    response = model.generate_content(user_query)
    return response.text

# Set page configuration
st.set_page_config(page_title="Code Reviewer", page_icon="✍️", layout="centered")

# Title of the app
st.markdown('''
        <h1 style="
            font-family: 'Arial', sans-serif;
            text-align: center;
            color: #4B0082;
            font-size: 3em;
            margin: 20px 0;
        ">
        Python Code Reviewer
        </h1>
        ''',
        unsafe_allow_html=True
    )

# Input text area
user_query = st.text_area(
        label = "**Enter your python code here:**",
        key = 'user_query',
        value = st.session_state['user_query'] if 'user_query' in st.session_state else None,
        height = 150,
        placeholder = 'start writing your python code'
    )

# Submit button
with st.columns([0.4,0.2,0.4])[1]:
    button = st.button("Submit", key='submit', type='primary', use_container_width=True, help="Click to generate result")

if(button):
    # check for empty user input
    if(not user_query or len(user_query)==0):
        st.rerun()

    # generate the text
    result = generate_response(user_query)
    
    # Output area
    st.subheader("Review result:")
    st.write(result)