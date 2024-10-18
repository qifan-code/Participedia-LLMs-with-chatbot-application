import time
import gradio as gr


table = {
    "How many Cases are there on Participedia?":
        "There are currently 2263 Cases on Participedia.",
    "How many Methods are there on Participedia?":
        "There are currently 373 Methods on Participedia.",
    "How many Organizations are there on Participedia?":
        "There are currently 858 Organizations on Participedia.",
    "How many Collections are there on Participedia?":
        "There are currently 20 Collections on Participedia.",
    "How many Countries are there on Participedia?":
        "There are currently 159 Countries on Participedia.",
}

def echo(message, history):
    answer = table.get(message)
    if not answer:
        answer = ("I currently don't have answer to your question yet, "
                  "but I keep updating myself with Participedia's dataset, "
                  "and I would probably have the answer in the future. "
                  "Please reset this chat and try another example.")
    answer = answer.split()
    for i in range(len(answer)):
        time.sleep(0.2)
        yield ' '.join(answer[:i+1])


if __name__ == '__main__':
    demo = gr.ChatInterface(
        fn=echo,
        type="messages",
        examples=list(table.keys()),
        title="Participedia Bot Demo")
    demo.launch()
