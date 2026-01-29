import os
from agent import agent
from langchain.messages import HumanMessage
from voice import record_from_mic, speech_to_text, text_to_speech
import subprocess

# One call session = one thread
thread_id = "call_001"

config = {
    "configurable": {
        "thread_id": thread_id
    }
}

print("🎧 AI Call Assistant started")
print("Say 'exit' to end the call\n")

while True:
    try:
        audio_path = record_from_mic() #Record from microphone

        user_text = speech_to_text(audio_path) #Speech → Text
        os.remove(audio_path)

        if not user_text:
            print("⚠️ Didn't catch that, please try again.")
            continue

        if user_text.lower() in ["exit", "stop", "goodbye"]:
            print("👋 Call ended.")
            break

        print("Customer:", user_text)

        response = agent.invoke(
            {"messages": [HumanMessage(content=user_text)]},  
            config=config
        )

        assistant_text = response["messages"][-1].content
        print("Assistant:", assistant_text)

        audio_response = text_to_speech(assistant_text) #Text → Speech

        subprocess.run(["afplay", audio_response])
        os.remove(audio_response)

    except Exception as e:
        print("⚠️ Error processing audio. Please try again.")
        continue
