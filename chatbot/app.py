import gradio as gr
import requests


def ask(message, history):
    response = requests.post(
        url='http://localhost:5000/ask',
        json={'question': message}
    )
    response.raise_for_status()
    return response.json()['answer']


if __name__ == '__main__':
    demo = gr.ChatInterface(fn=ask, type="messages", title="Participedia Question Answering Bot")
    demo.launch()
