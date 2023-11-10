from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {"role": "system", "content": "You are a Software engineering assistant, skilled in writing great Python code. The project is a simple Python tamagotchi game."},
    {"role": "user", "content": "Make 3 buttons that say 'Feed', 'Play', and 'Sleep'."},
    {"role": "system", "content": """ Code right now:
import time

import pytermgui as ptg

def macro_time(fmt: str) -> str:
    return time.strftime(fmt)

ptg.tim.define("!time", macro_time)

with ptg.WindowManager() as manager:
    manager.layout.add_slot("Body")
    manager.add(
        ptg.Window("[bold]The current time is:[/]\n\n[!time 75]%c", box="EMPTY")
    )
     """},
  ]
)

response_content = completion.choices[0].message.content

print(response_content)
