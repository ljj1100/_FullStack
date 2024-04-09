import streamlit as st
import os

st.set_page_config(
    page_title="FullstackGPT Home",
    page_icon="🤖",
)

# api_key = st.sidebar.text_input("Please put in OpenAI API Key", type="password")
# directory = "./envAPI"
# def save_api(directory, key):
#     directory = directory
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     if open(directory + "/" + "api.txt", "r").readline() != "":
#         with open(os.path.join(directory, "api.txt"), 'wb') as f:
#             key = key.encode()
#             f.write(key)
#         return st.success("Saved file : {}".format(directory))
#     else:
#         return 0
# save_api(directory, api_key)

st.sidebar.markdown("## Github Repository")
st.sidebar.markdown("[Github Repo Link](https://github.com/ljj1199/_FullStack/compare/main...ljj1100:_FullStack:main)")




st.markdown(
    """
# Hello!
            
Welcome to my FullstackGPT Portfolio!
            
Here are the apps I made:
            
- [X] [DocumentGPT](/DocumentGPT)
- [X] [PrivateGPT](/PrivateGPT)
- [X] [QuizGPT](/QuizGPT)
- [X] [SiteGPT](/SiteGPT)
- [ ] [MeetingGPT](/MeetingGPT)
- [ ] [InvestorGPT](/InvestorGPT)
"""
)