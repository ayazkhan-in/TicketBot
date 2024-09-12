import streamlit as st
import os
import google.generativeai as genai

# API key
os.environ["GEMINI_API_KEY"] = "AIzaSyCGIfKLFbZq0KFXXnvkIpUhyqmHvu_XzME"

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session with no initial history
chat_session = model.start_chat(history=[])

def chat_with_ai(message):
    response = chat_session.send_message(message)
    return response.text

option = st.selectbox(
    'Choose Museum:',
    ('Chhatrapati Shivaji Maharaj Vastu Sangrahalaya', 'Dr. Bhau Daji Lad Museum', 'National Gallery of Modern Art', 'Mani Bhavan Gandhi Sangrahalaya', 'RBI Monetary Museum')
)
# Streamlit app
st.title("Museum Ticket Booking Chatbot")

# Initialize session state for conversation history if it doesn't exist
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []


welcome_message = "Welcome to the Museum Ticket Booking Chatbot! I can help you book tickets for our museum. What would you like to do? Type 'book' to book tickets, 'info' for museum information, or 'exit' to end the conversation."
st.write(welcome_message)

user_message = st.text_input("You: ")

context = f"You are a Museum Ticket booking chatbot. The user wants to visit {option}. The price for one Adult ticket is 350Rupees."

# Create a button to submit the user input
if st.button("Submit"):
    if user_message:
        st.session_state['conversation_history'].append(f"You: {user_message}")

        if user_message.lower() == 'book':
            ai_response = chat_with_ai(f"{context} Your task is to ask user for information like Name, date and time of visit. User wishes to proceed for booking assist them in booking the ticket.")
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("AI:", ai_response)

        elif user_message.lower() == 'info':
            ai_response = chat_with_ai(f"{context}Give user information about {option}")
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("AI:", ai_response)

        elif user_message.lower() == 'exit':
            st.write("Chat ended.")

        else:
            ai_response = chat_with_ai(f'{context} {user_message}')
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("AI:", ai_response)

if st.button("Confirm"):
    chat_history_text = "\n".join(st.session_state['conversation_history'])
    info = chat_with_ai(f"From the following conversation history, extract Name, Date, Time, and Number of tickets and return it as [True,Name,Date(DD/MM/2024),time(24 hour format),No of tickets(1 default)] as list. Give response as [false] if any of those valuses are missing.\n\n{chat_history_text}")
    st.write("Terminal:", info)
    print(info)
    st.write("AI: Your ticket is processing.")

if st.button("Clear Chat History"):
    st.session_state['conversation_history'] = []

st.write("### Conversation History")
for message in st.session_state['conversation_history']:
    st.write(message)

#Qr generation code
