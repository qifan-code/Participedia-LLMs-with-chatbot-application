import gradio as gr


def echo(message, history):
    return message


if __name__ == '__main__':
    demo = gr.ChatInterface(fn=echo, type="messages", examples=["hello", "hola", "bonjour"], title="Echo Bot")
    demo.launch()
