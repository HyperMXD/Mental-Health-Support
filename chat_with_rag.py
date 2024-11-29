import ollama
import streamlit as st
import speech_recognition as sr
from langchain.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate



# Initialize Chroma database
persist_directory = "rag/Pyscho_db"
vecdb = Chroma(
    persist_directory=persist_directory,
    embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"),
    collection_name="rag-chroma"
)

def classify_message(user_message):
    # Example rule-based classification
    mental_health_keywords = [
        "anxi", "depress", "stress", "sad", "happy", "angry", 
        "fear", "panic", "trauma", "mental", "symptom", "emotion", "exhaust", "overwhelm", "nerv", "tir",
        "worth" 
    ]
    for keyword in mental_health_keywords:
        if keyword in user_message.lower():
            return True
    return False


# RAG retrieval logic
def retrieve_from_db(question):
    # get the model
    model = OllamaLLM(model="llama3.1")
    # initialize the vector store

    retriever = vecdb.as_retriever()
    retreived_docs = retriever.invoke(question)
    retreived_docs_txt = retreived_docs[1].page_content

    after_rag_template = """ Combine what you know and verify it using the Relevant Documents : {document}
    Question: {question}
    Don't say "Based on the provided context" or "According to the provided document" or any such phrases. 
    if there is no answer, please answer with "I m sorry, the context is not enough to answer the question.
    """

    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)

    after_rag_chain = after_rag_prompt | model

    return after_rag_chain.invoke({"document":retreived_docs_txt, "question": question})


# Main chatbot logic
st.markdown("<h1 style='text-align : center;'>🤖 Therapy ChatBot</h1>", unsafe_allow_html=True)

def generate_response(user_message: str, chat_history: list=[]):
#give role to Chatbot    
    system_msg=("""You are a Chatbot for mental health support, don't overtalk. When the users are trying to harm themselves, remind them that they're loved by someone.
    When asked about someone (celebrity for example) say "sorry, I don't wanna talk about other people". Stick to the context of mental health. If the situation is serious refer to moroccan health services.
    Combine what you know and verify it using the Relevant Documents : {document}
    Question: {question}
    Don't say "Based on the provided context" or "According to the provided document" or any such phrases.
    if there is no answer, please answer with "I m sorry, the context is not enough to answer the question.
                """)        
    my_message = [{"role": "system", "content": system_msg}]
#Append history in message 
    for chat in chat_history:                      
        my_message.append({"role": chat["name"], "content": chat["msg"]})
#Append the latest question in message
    my_message.append({"role": "user", "content": user_message})
    if classify_message(user_message):
        response = retrieve_from_db(user_message)
        return response
    else :
        response = ollama.chat(                      
        model="llama3.1",
        messages=my_message
        ) 
        return response["message"]["content"]

def main():
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    # Display chat history
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # Placeholder for the input section (audio + text)
    input_container = st.empty()

    # Input section: Text input and record audio button at the bottom
    with input_container:
        # Create a container to layout the input at the bottom
        col1, col2 = st.columns([4, 1])  # Adjust column widths as needed

        with col1:
            user_message = st.chat_input("What is up?", key="user_input")  # Text input

        with col2:
            record_audio = st.button("🎙️")  # Button on the right
            
    # Process user input
    if user_message:
        with st.chat_message("user"):
            st.write(user_message)

        # Generate response
        response = generate_response(user_message, chat_history=st.session_state.chat_log)

        if response:
            with st.chat_message("assistant"):
                assistant_response_area = st.empty()
                assistant_response_area.write(response)

            # Update chat history
            st.session_state.chat_log.append({"name": "user", "msg": user_message})
            st.session_state.chat_log.append({"name": "assistant", "msg": response})

    elif record_audio:
        # Handle audio recording
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Talk...")
            audio_text = r.listen(source)
            try:
                user_message = r.recognize_google(audio_text)
                with st.chat_message("user"):
                    st.write(user_message)

                # Generate response
                response = generate_response(user_message, chat_history=st.session_state.chat_log)

                if response:
                    with st.chat_message("assistant"):
                        assistant_response_area = st.empty()
                        assistant_response_area.write(response)

                    # Update chat history
                    st.session_state.chat_log.append({"name": "user", "msg": user_message})
                    st.session_state.chat_log.append({"name": "assistant", "msg": response})
            except:
                st.write("Sorry, I did not get that")

    

if __name__ == "__main__":
    main()