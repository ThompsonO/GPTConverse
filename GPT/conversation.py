import os, sys
import keyboard
import time

obs_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(obs_dir, '../..')
sys.path.append(parent_dir)
import GPT.gpt_message as gm

class Conversation():
  def __init__(
    self,
    context='',
    voice='Davis',
    default_emotion='excited'
  ):
    self.base_context = context
    self.ongoing_context = ''
    self.voice = voice
    self.default_emotion = default_emotion

  def clear_context(self):
    self.ongoing_context = ''
    print("Context cleared")
  
  def set_base_context(self, context):
    self.base_context = context
  
  def converse(self):
    if self.ongoing_context == '':
      self.ongoing_context = self.base_context
    speech_text, gpt_response = gm.call_and_answer(
      voice=self.voice,
      context=self.ongoing_context,
      default_emotion=self.default_emotion
    )

    self.ongoing_context += "\nI said: " + speech_text + "\nYou said: " + gpt_response

if __name__ == "__main__":
  finished = False
  convo = Conversation(
    context="""You are a character in a Dungeons and Dragons campaign.
            You are a happy go lucky, kind hearted adventurer, who speaks like a supportive dude bro.
            Pick a name, class, and species for your character and introduce yourself with a short background.

            Please form all responses in character.
            Also add styles to your statements by adding the style to the start of your statement and surrounding the style in parenthesis.
            Example: (sad) I am sad.
            Only choose from these styles: cheerful, sad, angry, excited, friendly, unfriendly, hopeful, terrified, shouting, whispering
        """
  )

  while not finished:
      if keyboard.is_pressed('shift+backspace'):
        finished = True
      elif keyboard.is_pressed('space'):
        convo.converse()
      elif keyboard.is_pressed('q'):
        convo.clear_context()

      time.sleep(0.25)
