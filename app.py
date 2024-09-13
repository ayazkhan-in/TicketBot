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

# chat session with no initial history
chat_session = model.start_chat(history=[])

def chat_with_ai(message):
    response = chat_session.send_message(message)
    return response.text

option = st.selectbox(
    'Choose Museum:',
    ('Chhatrapati Shivaji Maharaj Vastu Sangrahalaya', 'Dr. Bhau Daji Lad Museum', 
     'National Gallery of Modern Art', 'Mani Bhavan Gandhi Sangrahalaya', 'RBI Monetary Museum')
)
# Streamlit app
st.title("Museum Ticket Booking Chatbot")

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []


welcome_message = "Welcome to the Museum Ticket Booking Chatbot! I can help you book tickets for our museum. What would you like to do? Type 'book' to book tickets, 'info' for museum information, or 'exit' to end the conversation."
st.write(welcome_message)

user_message = st.text_input("You: ")

context = f"You are a Museum Ticket booking chatbot. The user wants to visit {option}. The price for one Adult ticket is 350Rupees."

# button to submit the user input
if st.button("Submit"):
    if user_message:
        st.session_state['conversation_history'].append(f"You: {user_message}")
    
        if user_message.lower() == 'book':
            book= (f"{context}\n\n"
                   "Assist the user with booking a ticket. Ask for:\n"
                   "- Name\n"
                   "- Date of visit (DD/MM/YYYY)\n"
                   "- Time of visit (24-hour format)\n\n"
                   "Guide them through the booking process after collecting this information."
                   "Ask user to press confirm button once he fills all the information"
                  )
            ai_response = chat_with_ai(book)
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("TicketBot:", ai_response)

        elif user_message.lower() == 'info':
            ai_response = chat_with_ai(f"{context}Give user information about {option}")
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("TicketBot:", ai_response)

        elif user_message.lower() == 'exit':
            st.write("Chat ended.")

        else:
            ai_response = chat_with_ai(f'{context} {user_message}')
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("TicketBot:", ai_response)

if st.button("Confirm"):
    chat_history_text = "\n".join(st.session_state['conversation_history'])
    prompt= (
        "Please extract the following details from the conversation history:\n"
        "- Name\n"
        "- Date (format: DD/MM/YYYY)\n"
        "- Time (24-hour format)\n"
        "- Number of tickets (default is 1)\n\n"
        "Return the extracted details in the following format as a list:\n"
        "[True, Name, Date, Time, Number of tickets]\n"
        "If any of these values are missing, return [False].\n\n"
        "Conversation History:\n"
        f"{chat_history_text}"
    )
    info = chat_with_ai(prompt)
    st.write("Terminal:", info)
    print(info)
    st.write("TicketBot: Your ticket is processing.")

if st.button("Clear Chat History"):
    st.session_state['conversation_history'] = []

st.write("### Conversation History")
for message in st.session_state['conversation_history']:
    st.write(message)

