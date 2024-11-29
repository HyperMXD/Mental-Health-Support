import ollama
import streamlit as st
import speech_recognition as sr

st.markdown("<h1 style='text-align : center;'>🤖 Therapy ChatBot</h1>", unsafe_allow_html=True)

def generate_response(user_message: str, chat_history: list=[]):
#give role to Chatbot    
    system_msg=("You are a Chatbot for mental health support, don't overtalk. Don't talk about people or celebrities. Stay in the problem's context.")        
    my_message = [{"role": "system", "content": system_msg}]
#Append history in message 
    for chat in chat_history:                      
        my_message.append({"role": chat["name"], "content": chat["msg"]})
#Append the latest question in message
    my_message.append({"role": "user", "content": user_message})
#define model&input for response 
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

    # Create the layout: Text input at the bottom and audio recorder button on the side
    input_container = st.empty()

    # Input section: Create a layout with columns for text input and audio button
    with input_container:
        col1, col2 = st.columns([4, 1])  # Text input takes 4 parts, button takes 1 part

        with col1:
            # Text input for the user message
            user_message = st.chat_input("What is up?", key="user_input") 

        with col2:
            # Audio record button on the right side
            record_audio = st.button("🎙️")

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