import json
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
import streamlit as st
from langchain.retrievers import WikipediaRetriever
from langchain.schema import BaseOutputParser, output_parser


class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json", "")
        return json.loads(text)


output_parser = JsonOutputParser()

st.set_page_config(
    page_title="QuizGPT",
    page_icon="❓",
)

st.title("QuizGPT")

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-1106",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
    As an intelligent quiz master, your task is to generate 10 (TEN) true or false (O/X) questions based on the provided context. 
    Your questions should be clear, factual, and cover a variety of subjects to ensure a broad test of the user's knowledge.
    
    Please mark true statements with "O" and false statements with "X". 
    
    Here are a few examples to get you started:
    
    Question: The Eiffel Tower is located in Berlin.
    Answers : (X)
    
    Question: Water boils at 100 degrees Celsius at sea level. 
    Answers : (O)
    
    Question: Light travels faster than sound. 
    Answers : (O)
    
    Question: Penguins are mammals. 
    Answers : (X)
    
    Your turn!

            Context: {context}
            """,
        )
    ]
)

questions_chain = {"context": format_docs} | questions_prompt | llm

formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
    As an adept formatting algorithm, your role is to convert the true or false (O/X) quiz questions into a structured JSON format.
    Each question will be marked with an "O" for true or "X" for false. 
    
    Your task is to format these questions and their answers into a clean, easy-to-read JSON format, where true statements are represented as true and false statements as false.
    
    Example Input:
    
    Question: The Eiffel Tower is located in Berlin. 
    Answers : (X)

    Question: Water boils at 100 degrees Celsius at sea level. 
    Answers : (O)

    Question: Light travels faster than sound. 
    Answers : (O)
    
    Question: Penguins are mammals. 
    Answers : (X)
    
    
    Example Output:
    
    ```json
    {{
      "questions": [
        {{
          "question": "The Eiffel Tower is located in Berlin.",
          "answers": [{{"answer":"X",
                        "correct":true
                      }},
                      {{"answer":"O",
                        "correct":false                      
                      }}
                    ]
        }},
        {{
          "question": "Water boils at 100 degrees Celsius at sea level.",
          "answers": [{{"answer":"O",
                        "correct":true
                      }},
                      {{"answer":"X",
                        "correct":false                 
                      }}
                    ]
        }},
        {{
          "question": "Light travels faster than sound.",
          "answers": [{{"answer":"O",
                        "correct":true
                      }},
                      {{"answer":"X",
                        "correct":false                 
                      }}
                    ]
        }},
        {{
          "question": "Penguins are mammals",
          "answers": [{{"answer":"X",
                        "correct":true
                      }},
                      {{"answer":"O",
                        "correct":false                      
                      }}
                    ]
        }},


      ]
    }}
    ```
    Your turn!

    Questions: {context}

""",
        )
    ]
)

formatting_chain = formatting_prompt | llm


@st.cache_data(show_spinner="Loading file...")
def split_file(file):
    file_content = file.read()
    file_path = f"./.cache/quiz_files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs


@st.cache_data(show_spinner="Making quiz...")
def run_quiz_chain(_docs, topic):
    chain = {"context": questions_chain} | formatting_chain | output_parser
    return chain.invoke(_docs)


@st.cache_data(show_spinner="Searching Wikipedia...")
def wiki_search(term):
    retriever = WikipediaRetriever(top_k_results=5)
    docs = retriever.get_relevant_documents(term)
    return docs


with st.sidebar:
    docs = None
    topic = None
    choice = st.selectbox(
        "Choose what you want to use.",
        (
            "File",
            "Wikipedia Article",
        ),
    )
    if choice == "File":
        file = st.file_uploader(
            "Upload a .docx , .txt or .pdf file",
            type=["pdf", "txt", "docx"],
        )
        if file:
            docs = split_file(file)
    else:
        topic = st.text_input("Search Wikipedia...")
        if topic:
            docs = wiki_search(topic)


if not docs:
    st.markdown(
        """
    Welcome to QuizGPT.
                
    I will make a quiz from Wikipedia articles or files you upload to test your knowledge and help you study.
                
    Get started by uploading a file or searching on Wikipedia in the sidebar.
    """
    )
else:
    response = run_quiz_chain(docs, topic if topic else file.name)
    
    with st.form("questions_form"):
        submitted = st.form_submit_button("Submit")
        st.write(response)
        correct_answers = 0
        # user_responses = []
        for i, question in enumerate(response["questions"]):
            st.write(question["question"])
            value =  st.radio(
                    "Select True or False:",
                    ["True", "False"],
                    key=f"question_{i}",
                    )
            # user_responses.append(value)
            if submitted:
                
                # for user_response, question in zip(value, response["questions"]):
                if value == "True":
                    is_collect = 'O'
                else:
                    is_collect = 'X'
                if {"answer" : is_collect, "correct": True} in question["answers"]:
                    correct_answers += 1
                    st.success("Correct!")
                else:
                    st.error("Wrong")
        if correct_answers == 10:
            st.balloons()