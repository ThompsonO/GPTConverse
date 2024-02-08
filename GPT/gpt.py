import os, sys
from openai import OpenAI

#Import other modules
obs_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(obs_dir, '..')
sys.path.append(parent_dir)
import TGManager.secrets_manager as sm

def connect():
    openai_secrets = sm.get_secret_group('openai')
    client = OpenAI(api_key=openai_secrets['key'])
    return client

def gpt_message(message_content, system_content="", gpt_model="gpt-3.5-turbo"):
    client = connect()

    completion = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": message_content}
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    response = gpt_message("Give me a list of 12 Marvel Characters that has all Avenger members in it.")
    print(response)

    response2 = gpt_message("Replace number 10", system_content=response)
    print(response2)
