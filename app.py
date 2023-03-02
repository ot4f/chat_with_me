import os
# import numpy as np

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = []
total_tokens = 0

# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         animal = request.form["animal"]
#         response = openai.Completion.create(
#             model="gpt-3.5-turbo",#"text-davinci-003",
#             prompt=generate_prompt1(animal),
#             temperature=0.6,
#         )
#         # print(response.choices[0])
#         return redirect(url_for("index", result=response.choices[0].text))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)

@app.route("/", methods=("GET", "POST"))
def index():
    global messages,total_tokens
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",#"text-davinci-003",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            # temperature=0.6,
        )
        n_tokens = response['usage']['total_tokens']
        total_tokens += n_tokens
        print('#total tokens:', total_tokens)
        message = response['choices'][0]['message']['content']
        messages = ['++++++++++++++++++++++++++++++++++++++',
                    'user: '+prompt, 
                    'assistant: '+message,
                    '++++++++++++++++++++++++++++++++++++++'] + messages
        results = '\n'.join(messages)
        with open('messages.txt','w',encoding='utf-8') as f:
            f.write(results)
        return redirect(url_for("index", result=results))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

def generate_prompt1(topic):
    return """Write a poem about {}""".format(
        topic
    )