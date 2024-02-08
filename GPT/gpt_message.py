import os, sys
import keyboard, time

#Import other modules
obs_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(obs_dir, '..')
sys.path.append(parent_dir)
import STT.STTAzure as stt
import TTS.TTSAzure as tts
import GPT.gpt as gpt

# One-off call and response to chat gpt
def call_and_answer(voice='Davis', context="", default_emotion='excited'):
    print("Detecting speech...")
    speech_text = stt.speech_to_text()
    print(speech_text)

    print("GPT is cooking...")
    gpt_response = gpt.gpt_message(speech_text, system_content=context)
    print(f"GPT response: {gpt_response}")
    
    ssml_response = tts.ssml_transform(gpt_response, voice, default_emotion=default_emotion)
    tts.say_ssml(ssml_response)
    
    return speech_text, gpt_response

if __name__ == "__main__":
    finished = False

    while not finished:
        if keyboard.is_pressed('shift+backspace'):
            finished = True
        elif keyboard.is_pressed('space'):
            call_and_answer()

        time.sleep(0.25)