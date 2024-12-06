Therapy Chatbot: Interactive Mental Health Support
===================================================

This section of the script creates a **therapy chatbot** using **Streamlit**, **Ollama**, and **Chroma**. The chatbot is designed to support mental health conversations by retrieving contextually relevant information from a database and engaging users in meaningful interactions.

Overview
--------

The chatbot is built with the following features:

- **Text and Speech Input**: Accepts user messages via text input or audio recording.
- **Role-Specific Responses**: Provides empathetic and supportive replies tailored to mental health topics.
- **Retrieval-Augmented Generation (RAG)**: Combines user queries with relevant data from the Chroma vector database for informed responses.
- **Session State**: Maintains a history of the conversation for context continuity.

Dependencies
------------

Ensure the following Python libraries are installed:

- `streamlit`
- `speech_recognition`
- `langchain`
- `langchain_community`
- `chromadb`
- `ollama`

To install these libraries, use:

.. code-block:: bash

   pip install streamlit speechrecognition langchain chromadb

Key Components
--------------
^^^^^^^^^^^^^^^^^^^^^^^^^^
Initialize Chroma Database
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Chroma vector database is loaded with embedded documents to enable similarity-based retrieval:

.. code-block:: python

   persist_directory = "rag/Psycho_db"
   vecdb = Chroma(
       persist_directory=persist_directory,
       embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"),
       collection_name="rag-chroma"
   )
^^^^^^^^^^^^^^^
Retrieval Logic
^^^^^^^^^^^^^^^

The `retrieve_from_db` function retrieves relevant documents from the Chroma database based on the user's query:

.. code-block:: python

   def retrieve_from_db(question):
       model = OllamaLLM(model="llama3.2")
       retriever = vecdb.as_retriever()
       retrieved_docs = retriever.invoke(question)
       return retrieved_docs[1].page_content

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Chatbot Response Generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `generate_response` function creates a reply to the user's query. It defines the chatbot's role, ensuring responses are empathetic and contextually relevant:

.. code-block:: python

   def generate_response(user_message: str, chat_history: list = [], doc=""):
       system_msg = (
           """You are a Chatbot for mental health support, don't overtalk. When the users are trying to harm themselves, remind them that they're loved by someone.
           When asked about someone (celebrity for example) say "sorry, I don't wanna talk about other people". Stick to the context of mental health. 
           If the situation is serious refer to Moroccan health services. Combine what you know and verify it using the Relevant Documents : {document}
           Question: {question}. Don't say "Based on the provided context". If there is no answer, say "I'm sorry, the context is not enough to answer the question." """
       )
       my_message = [{"role": "system", "content": system_msg, "document": doc}]
       for chat in chat_history:
           my_message.append({"role": chat["name"], "content": chat["msg"]})
       my_message.append({"role": "user", "content": user_message, "document": doc})

       response = ollama.chat(
           model="llama3.2",
           messages=my_message
       )
       return response["message"]["content"]

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Streamlit UI and Interaction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The chatbot interface is implemented using Streamlit:

1. **Chat History**: Displays the history of user and chatbot interactions.
2. **Input Methods**:
   - Text input: Users can type messages in a text box.
   - Audio input: Users can record their voice, which is transcribed into text.
3. **Real-Time Responses**: The chatbot processes the input and displays a response.

^^^^^^^^^^^^^
Main Function
^^^^^^^^^^^^^

The `main` function initializes the chatbot interface and handles user inputs:

.. code-block:: python

   def main():
       if "chat_log" not in st.session_state:
           st.session_state.chat_log = []

       for chat in st.session_state.chat_log:
           with st.chat_message(chat["name"]):
               st.write(chat["msg"])

       input_container = st.empty()

       with input_container:
           col1, col2 = st.columns([4, 1])

           with col1:
               user_message = st.chat_input("What is up?", key="user_input")
           with col2:
               record_audio = st.button("🎙️")

       if user_message:
           with st.chat_message("user"):
               st.write(user_message)
           doc = retrieve_from_db(user_message)
           response = generate_response(user_message, chat_history=st.session_state.chat_log, doc=doc)

           if response:
               with st.chat_message("assistant"):
                   st.write(response)

               st.session_state.chat_log.append({"name": "user", "msg": user_message})
               st.session_state.chat_log.append({"name": "assistant", "msg": response})

       elif record_audio:
           r = sr.Recognizer()
           with sr.Microphone() as source:
               st.write("Talk...")
               audio_text = r.listen(source)
               try:
                   user_message = r.recognize_google(audio_text)
                   with st.chat_message("user"):
                       st.write(user_message)
                   doc = retrieve_from_db(user_message)
                   response = generate_response(user_message, chat_history=st.session_state.chat_log, doc=doc)

                   if response:
                       with st.chat_message("assistant"):
                           st.write(response)

                       st.session_state.chat_log.append({"name": "user", "msg": user_message})
                       st.session_state.chat_log.append({"name": "assistant", "msg": response})
               except:
                   st.write("Sorry, I did not get that.")

       if __name__ == "__main__":
           main()

Outputs
-------

- **Interactive Chat Interface**: Provides real-time interactions with users.
- **Mental Health Support**: Tailored responses based on user queries.
- **Document-Aided Replies**: Incorporates data from the Chroma database to provide relevant answers.

Notes
-----

- Ensure the Chroma database is initialized with the appropriate data.
- Configure the API keys and microphone permissions correctly for full functionality.
