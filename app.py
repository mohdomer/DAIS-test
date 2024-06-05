import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from streamlit_chat import message
import uuid

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput():
    user_question = st.session_state.user_question
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message_obj in enumerate(st.session_state.chat_history or []):
            content = message_obj.content
            if "message_keys" not in st.session_state:
                st.session_state.message_keys = {}
            if f"key_{i}" not in st.session_state.message_keys:
                st.session_state.message_keys[f"key_{i}"] = str(uuid.uuid4())
            unique_key = st.session_state.message_keys[f"key_{i}"]
            if i % 2 == 0:
                message(content, key=f"bot_{i}_{unique_key}")  # Bot message
            else:
                message(content, is_user=True, key=f"user_{i}_{unique_key}")

    # Clear the input field after processing
    st.session_state.user_question = ""

if "user_question" not in st.session_state:
    st.session_state["user_question"] = ""
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

def main():
    load_dotenv()
    st.set_page_config(page_title="Dubai AI Solutions")
    st.write(css, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            .header {
                position: fixed;
                top: 12%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 100%;
                z-index: 1000;
                padding: 20px 0;
                text-align: center;
            }
            .header-container {
                display: flex;
                align-items: center;
                justify-content: center; 
                background-color: rgba(20,22,23, 0.3); /* white background with 50% opacity */    
                border-radius: 2px;
                padding: 20px 30px;
                box-shadow: 0px 4px 6px rgba(28, 36, 41, 1);
                /* Set the width of the container */
                height: 60px; /* Set the height of the container */
                overflow: auto; /* Enable scrolling if content overflows */
                margin-left: 400px;
                margin-right: 400px;
            }
            .header img {
                width: 50px;
                height: 50px;
                margin-right: 10px;
            }
            .header h1 {
                margin: 0;
                font-size: 28px;
            }
            .user-message {
                background-color: rgba(173, 216, 230, 1);
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
                width: fit-content;
            }
            .bot-message {
                background-color: rgba(240, 255, 255, 1);
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
                width: fit-content;
            }
        </style>
        <div class="header">
            <div class="header-container">
                <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/266a372d898d72466eb796cf6f44f0ead4a312b7d81f2102e8e7d11fa26a3667?apiKey=e95fc8a014c54680a3ca6c582c31b23f">
                <h1>Dubai AI Solutions</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
                with st.spinner("Processing"):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)

    styl = f"""
    <style>
        .stTextInput {{
          position: fixed;
          bottom: 3rem;
          left: 50%;
          transform: translateX(-50%);
          z-index: 1;
          margin-left:50px;
          overlap: auto;
          margin-top: 20px; /* Add margin to avoid overlapping */
          width: 700px; /* Ensure the text input box takes the full width of the container */
          box-sizing: border-box; /* Ensure padding and border are included in the element's total width and height */
        }}
        .styled-container {{
            background-color: rgba(255, 255, 255, 0.8); /* white background with 50% opacity */
            padding: 10px;
            border-radius: 10px;
            width: 300px; /* Set the width of the container */
            height: 200px; /* Set the height of the container */
            overflow: auto; /* Enable scrolling if content overflows */
        }}
        .stConversation {{
          z-index: 2;
        }}
        .stHeader{{
          position: fixed;
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)

    user_question = st.text_input("Ask a question about your documents:", key="user_question", on_change=handle_userinput)
    if st.session_state.user_question:
        handle_userinput()

if __name__ == '__main__':
    main()