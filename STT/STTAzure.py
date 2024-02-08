import os
import sys
import keyboard
import time
import azure.cognitiveservices.speech as speechsdk

#Import other modules
obs_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(obs_dir, '..')
sys.path.append(parent_dir)
import TGManager.secrets_manager as sm


def connect():
    azure_secrets = sm.get_secret_group('azure')
    speech_config = speechsdk.SpeechConfig(subscription=azure_secrets['subscription_key'], region=azure_secrets['service_region'])
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    return recognizer

def speech_to_text():
    recognizer = connect()
    result = recognizer.recognize_once_async().get()
    return_text = ""

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #print("Recognized: {}".format(result.text))
        return_text = result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    
    return return_text

def save_speech_text(filepath="./speech.txt"):
    speech_text = speech_to_text()
    with open(filepath, "w") as f:
        f.write(speech_text)

if __name__ == "__main__":
    finished = False

    while not finished:
        if keyboard.is_pressed('shift+backspace'):
            finished = True
        elif keyboard.is_pressed('space'):
            print("Detecting speech...")
            save_speech_text()

        time.sleep(0.25)
