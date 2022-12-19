import os
import openai
import gradio as gr

#Tip: If you've OpenAI API key as an environment variable, enable the code commented below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#Tip:If you have OpenAI API key as a string, enable the below
openai.api_key = "your api key here"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with a Legal AI assistant. The assistant is insightful, helpful, friendly, creative, informative, and professional.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

#function takes one argument -a prompt.
def openai_create(prompt):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    return response.choices[0].text

# the second function takes in two argument, input & history (output)
# this is required for Gradio
#input is a text, history -stores the state of the Graio application

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input) #appends history with current input (text), that way it continues/remembers previous text input
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history


block = gr.Blocks()


with block:
    gr.Markdown("""<h1>ChatGPT with OpenAI API & Gradio</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

    #Gradio app calls the chatgpt_clone function, takes a text & state as input and sends an output as well as state
block.launch(debug = True)  #this will launch the application.

