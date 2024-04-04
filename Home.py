import streamlit as st
import os

st.set_page_config(
    page_title="FullstackGPT Home",
    page_icon="🤖",
)

api_key = st.sidebar.text_input("Please put in OpenAI API Key", type="password")

st.sidebar.markdown("## Github Repository")
st.sidebar.markdown("[Github Repo Link](https://github.com/ljj1199/_FullStack/compare/main...ljj1100:_FullStack:main)")


def save_api(directory, key):
    directory = directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    if open(directory + "/" + "api.txt", "r").readline() != "":
        with open(os.path.join(directory, "api.txt"), 'wb') as f:
            key = key.encode()
            f.write(key)
        return st.success("Saved file : {}".format(directory))
    else:
        return 0

directory = "./envAPI"
save_api(directory, api_key)

st.markdown(
    """
# Hello!
            
Welcome to my FullstackGPT Portfolio!
            
Here are the apps I made:
            
- [ ] [DocumentGPT](/DocumentGPT)
- [ ] [PrivateGPT](/PrivateGPT)
- [ ] [QuizGPT](/QuizGPT)
- [ ] [SiteGPT](/SiteGPT)
- [ ] [MeetingGPT](/MeetingGPT)
- [ ] [InvestorGPT](/InvestorGPT)
"""
)