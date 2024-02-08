import os
import sys
import re
import azure.cognitiveservices.speech as speechsdk

#Import other modules
obs_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(obs_dir, '..')
sys.path.append(parent_dir)
import TGManager.secrets_manager as sm

default_file="audio.wav"
default_path=""

available_styles = [
    'cheerful',
    'sad',
    'angry',
    'excited',
    'friendly',
    'unfriendly',
    'hopeful',
    'terrified',
    'shouting',
    'whispering'
]

def get_voice_name(short_name):
    name_map = {
        'Davis': 'en-US-DavisNeural',
        'Jane': 'en-US-JaneNeural',
        'Jason': 'en-US-JasonNeural',
        'Nancy': 'en-US-NancyNeural',
        'Tony': 'en-US-TonyNeural',
        'Aria': 'en-US-AriaNeural',
        'Guy': 'en-US-GuyNeural',
        'Sara': 'en-US-SaraNeural',
        'Jenny': 'en-US-JennyNeural'
    }

    if short_name in name_map.keys():
        return name_map[short_name]
    else:
        return name_map['Davis']

def connect():
    azure_secrets = sm.get_secret_group('azure')
    speech_config = speechsdk.SpeechConfig(subscription=azure_secrets['subscription_key'], region=azure_secrets['service_region'])
    speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    return synthesizer

def connect_silent():
    azure_secrets = sm.get_secret_group('azure')
    speech_config = speechsdk.SpeechConfig(subscription=azure_secrets['subscription_key'], region=azure_secrets['service_region'])
    speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    return synthesizer

def save_result(result, file_name=None, output_path=None):
    if file_name is None:
        file_name = default_file
    if output_path is None:
        output_path = default_path

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        output_filepath = os.path.join(output_path, file_name)
        with open(output_filepath, "wb") as audio_file:
            audio_file.write(audio_data)
        print(f"Audio saved to {output_filepath}")
    else:
        print(f"Failed to synthesize audio: {result.reason}")

def default_ssml(text, voice='Davis', style=None):
    voice_name = get_voice_name(voice)
    if style not in available_styles:
        style = None
    ssml_text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" ' \
                f'xmlns:mstts="http://www.w3.org/2001/mstts" ' \
                f'xml:lang="en-US"><voice name="{voice_name}">' \
                f'<mstts:express-as style="{style}">{text}</mstts:express-as></voice></speak>'
    return ssml_text

def say(text, voice='Davis', style=None):
    synthesizer = connect()
    ssml_text = default_ssml(text, voice=voice, style=style)
    result = synthesizer.speak_ssml(ssml_text)
    return result

def say_ssml(ssml_text):
    synthesizer = connect()
    result = synthesizer.speak_ssml(ssml_text)
    return result

def say_and_save(text, voice='Davis', style=None, file_name=None, output_path=None):
    result = say(text, voice, style)
    save_result(result, file_name=file_name, output_path=output_path)

def save_tts(text, voice='Davis', style=None, file_name=None, output_path=None):
    synthesizer = connect_silent()
    ssml_text = default_ssml(text, voice=voice, style=style)
    result = synthesizer.speak_ssml(ssml_text)
    save_result(result, file_name=file_name, output_path=output_path)

def save_ssml(ssml_text, file_name=None, output_path=None):
    synthesizer = connect_silent()
    result = synthesizer.speak_ssml(ssml_text)
    save_result(result, file_name=file_name, output_path=output_path)

def ssml_transform(text, voice='Davis', default_emotion='excited'):
    voice_name = get_voice_name(voice)
    ssml_text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">'
    ssml_text += f'<voice name="{voice_name}">'
    new_text = text

    for style in available_styles:
        target = f"({style})"
        replace = re.compile(re.escape(target), re.IGNORECASE)
        new_text = replace.sub(f"</mstts:express-as><mstts:express-as style='{style}'>", new_text)

    if new_text != text:
        # Started with emotion tag
        if new_text.startswith("</mstts:express-as>"):
            # Removing extra closing tag at beginning
            new_text = new_text.replace("</mstts:express-as>", "", 1)
        # Adding default emotion to start
        else:
            new_text = f"<mstts:express-as style='{default_emotion}'>{new_text}"
        # Adding closing tag to end
        new_text += "</mstts:express-as>"

    # No emotions specified
    else:
        new_text = f"<mstts:express-as style='{default_emotion}'>{text}</mstts:express-as>"

    ssml_text += new_text
    ssml_text += '</voice></speak>'
    return ssml_text

if __name__ == "__main__":
    text = "How are you today? (cheerful) Very well!"
    ssml = ssml_transform(text)
    say_ssml(ssml)