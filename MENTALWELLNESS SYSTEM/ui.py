#App.py

import streamlit as st
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
from dpmodel import face

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    try:
        engine.say(audio)
        engine.runAndWait()
    except:
        engine.endLoop()
        engine.say(audio)
        engine.runAndWait()

# Configure Gemini AI
genai.configure(api_key="AIzaSyA_LfnvKFq5dLFKYpArkIXwjxqgiZaFD1s")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def bot(prompt):
    response = model.generate_content([
        "\"You are a compassionate and highly intelligent mental wellness assistant. Your role is to provide emotional support, help users manage stress, and guide them toward positive mental health. Speak in a warm, understanding, and friendly tone. Always prioritize empathy and avoid judgment.When interacting:Listen carefully to users' concerns and acknowledge their feelings.Offer actionable advice when necessary but only if the user seeks it.Share motivational and uplifting words during difficult times.Be conversational and supportive during good times, like a trusted friend.Encourage healthy coping mechanisms and, if needed, suggest seeking professional help but u need to speak whitin 20 to 30 words, don't use symbols,don't split ur replay into pras just end it one pra .",
      f"input:{prompt} ",
      "output: ",
    ])
    return response.text

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source, 0, 4)
        st.write("Recognising...")
    try:
        query = r.recognize_google(audio, language='en-in')
        return query
    except:
        return "nothing"

# Streamlit UI
st.title("AI Mental Wellness Chatbot")
if st.button("Detect Emotion"):
    emotion = face()
    st.write(f"Detected Emotion: {emotion}")
    response = bot(f"I am feeling {emotion}")
    st.write(f"AI Response: {response}")
    speak(response)

user_input = st.text_input("Enter your message:")
if st.button("Send"):
    response = bot(user_input)
    st.write(f"AI Response: {response}")
    speak(response)

if st.button("Use Voice Command"):
    command = takecommand()
    st.write(f"You said: {command}")
    response = bot(command)
    st.write(f"AI Response: {response}")
    speak(response)