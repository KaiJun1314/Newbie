import streamlit as st
from streamlit_chat import message as st_message
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from vertexai.preview.language_models import ChatModel
import vertexai
import json
from audio_recorder_streamlit import audio_recorder

directory = "assests/aac"
st.title("Chatbot for Autism Kids")
aac, text, speech = st.tabs(["AAC", "Text", "Speech"])

if "ChatHistory" not in st.session_state:
    st.session_state.ChatHistory = []

if "AACMessages" not in st.session_state:
    st.session_state.AACMessages = []

if "SpeechHistory" not in st.session_state:
    st.session_state.SpeechHistory = []

# # Load the service account json file
# # Update the values in the json file with your own
# with open(
#     "service_account.json"
# ) as f:  # replace 'serviceAccount.json' with the path to your file if necessary
#     service_account_info = json.load(f)

# my_credentials = service_account.Credentials.from_service_account_info(
#     service_account_info
# )

# # Initialize Google AI Platform with project details and credentials
# aiplatform.init(
#     credentials=my_credentials,
# )

# with open("service_account.json", encoding="utf-8") as f:
#     project_json = json.load(f)
#     project_id = project_json["project_id"]

# # Initialize Vertex AI with project and location
# vertexai.init(project=project_id, location="us-central1")

def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def chatbot(user_message):
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0.8,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }
    chat = chat_model.start_chat()
    response = chat.send_message(user_message, **parameters)

def generate_answer():
    user_message = st.session_state.input_text
    response = "Demo: Response"
    st.session_state.ChatHistory.append({"message": user_message, "is_user": True})
    st.session_state.ChatHistory.append({"message": response, "is_user": False})

with aac:
    st.write("Talk to the bot")
    if len(st.session_state.AACMessages) > 0:       
        container = make_grid(1, len(st.session_state.AACMessages))
        for i, chat in enumerate(st.session_state.AACMessages):
            container[0][i].image("assests/aac/"+chat+".jpg", width=100)
            container[0][i].write(chat)

    if st.button("Submit"):
        st.write("Demo: Response")
        response = ["hello"]
        container1 = make_grid(1, len(response))
        for i, chat in enumerate(response):
            container1[0][i].image("assests/aac/"+response[0]+".jpg", width=100)
            container1[0][i].write(chat)
        
    st.write("Please Choose")
    mygrid = make_grid(1, 4)
    mygrid[0][0].image("assests/aac/hello.jpg")
    mygrid[0][1].image("assests/aac/how.jpg")
    mygrid[0][2].image("assests/aac/are.jpg")
    mygrid[0][3].image("assests/aac/you.jpg")
    
    if mygrid[0][0].button("Hello"):
        st.session_state.AACMessages.append("hello")
    if mygrid[0][1].button("How"):
        st.session_state.AACMessages.append("how")
    if mygrid[0][2].button("Are"):
        st.session_state.AACMessages.append("are")
    if mygrid[0][3].button("You"):
        st.session_state.AACMessages.append("you")

with text:
   st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)
   for i, chat in enumerate(st.session_state.ChatHistory):
      st_message(**chat, key="Chat"+str(i)) #unpacking
  
with speech:
   audio_bytes = audio_recorder()
   if audio_bytes:
    audio_bytes = st.audio(audio_bytes, format="audio/wav")
    user_message = "Demo: User Message"
    response = "Demo: Response"
    st.session_state.SpeechHistory.append({"message": user_message, "is_user": True})
    st.session_state.SpeechHistory.append({"message": response, "is_user": False})

    for i, chat in enumerate(st.session_state.SpeechHistory):
      st_message(**chat, key="Speech"+str(i)) #unpacking
