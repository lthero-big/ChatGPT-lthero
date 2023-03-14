import gradio as gr
import requests
import markdown

prompt = "The following is a conversation with an AI assistant"
LastResponse = ""
ResponseInHtml = ""
userApiKey = "sk-aaa"
temperature = 1
topP = 0.5
presencePenalty = 0
frequencyPenalty = 0
maxTokens = 500
openAPIHost = 'https://api.openai.com/v1/chat/completions'


def openai_create(user_prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % userApiKey,
    }

    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': str(user_prompt),
            },
        ],
        'max_tokens': maxTokens,
        'temperature': temperature,
        'presence_penalty': presencePenalty,
        'top_p': topP,
        'frequency_penalty': frequencyPenalty,
    }
    response = requests.post(openAPIHost, headers=headers, json=json_data)
    # we have to remove the first two '\n'
    return parse_text(str(response.json()["choices"][0]["message"]["content"]).strip('\n'))


def conversation_history(userInput, history):
    global LastResponse, ResponseInHtml
    history = history or []
    s = list(sum(history, ()))
    s.append(userInput)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((userInput, output))
    LastResponse = output
#     ResponseInHtml = markdown.markdown(LastResponse, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
    return history, history


def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def upDateMD():
    return LastResponse


def upDateHtml():
    return ResponseInHtml


def Clear():
    global LastResponse
    LastResponse = ""
    return LastResponse


def changeAPI(setuserApiKey):
    global userApiKey
    userApiKey = setuserApiKey


def changeApiHost(setchangeApiHost):
    global openAPIHost
    openAPIHost = setchangeApiHost


def changeTemper(setTemperature):
    global temperature
    temperature = setTemperature


def changeTop(setTop):
    global topP
    topP = setTop


def changeFrequencyPenalty(setFrequencyPenalty):
    global frequencyPenalty
    frequencyPenalty = setFrequencyPenalty


def changePresencePenalty(setPresencePenalty):
    global presencePenalty
    presencePenalty = setPresencePenalty


blocks = gr.Blocks()
with blocks:
    gr.Markdown(
        """
        ### Please Enter your own OpenAI API Key in the Setting to remove the 500 token limit.
        """
    )
    with gr.Tab("Chat"):
        with gr.Row():
            with gr.Column(scale=1, variant="compact"):
                gr.Markdown(
                    """
                    # LastResponse:
                    """
                )
                md = gr.Markdown(
                    """
                    """
                )
            with gr.Column(scale=1, variant="panel"):
                gr.Markdown(
                    """
                    ## ChatBot:
                    """
                )
                with gr.Row():
                    with gr.Column(scale=0.85):
                        chatbot = gr.Chatbot(elem_id="chatbot", )
                        state = gr.State()

                with gr.Row():
                    with gr.Column(scale=0.85):
                        message = gr.Textbox(show_label=False, placeholder=prompt).style(container=False)
                    with gr.Column(scale=0.15, min_width=0):
                        btn = gr.Button(value="ClearAll")
        with gr.Row():
            html = gr.HTML("""
                    HTML
                    """)
    with gr.Tab("Setting"):
        with gr.Row():
            apiKey = gr.Textbox(elem_id="Input", show_label=False,
                                placeholder="Enter your own OpenAI API Key to remove "
                                            "the 500 token "
                                            "limit.").style(container=False)
            apiHost = gr.Textbox(elem_id="Input", show_label=False, placeholder="Enter API Host").style(container=False)
        with gr.Row():
            TemperSlider = gr.Slider(0, 1, step=0.01, label="temperature", info="If the temperature is low, the model "
                                                                                "will probably output the most correct "
                                                                                "text, but rather boring, with small "
                                                                                "variation.If the temperature is high, "
                                                                                "the generated text will be more "
                                                                                "diverse, but there is a higher "
                                                                                "possibility of grammar mistakes and "
                                                                                "generation of nonsense.",
                                     value=temperature)
        with gr.Row():
            topPSlider = gr.Slider(0, 1, step=0.01, label="Top_p", info="Top P can generate text with accuracy and "
                                                                        "correctness", value=topP)
        with gr.Row():
            presencePenaltySlider = gr.Slider(0, 1, step=0.01, label="presencePenalty", info="presencePenalty",
                                              value=presencePenalty)
        with gr.Row():
            frequencyPenaltySlider = gr.Slider(0, 1, step=0.01, label="frequencyPenaltySlider", info="frequencyPenalty",
                                               value=frequencyPenalty)

    message.submit(conversation_history, inputs=[message, state], outputs=[chatbot, state], show_progress=True)
    message.submit(lambda: "", None, message)
    # output response content into markdown
    chatbot.change(upDateMD, None, md)
    # output response content into Html
#     chatbot.change(upDateHtml, None, html)
    # clear textBox
    btn.click(lambda: "", None, state)
    btn.click(Clear, None, md)
    btn.click(lambda: "", None, chatbot)
    # TemperSlider
    TemperSlider.change(changeTemper, inputs=TemperSlider)
    # topPSlider
    topPSlider.change(changeTop, inputs=topPSlider)
    # presencePenaltySlider
    presencePenaltySlider.change(changePresencePenalty, inputs=presencePenaltySlider)
    # frequencyPenaltySlider
    frequencyPenaltySlider.change(changeFrequencyPenalty, inputs=frequencyPenaltySlider)
    # api
    apiKey.change(changeAPI, inputs=apiKey)
    apiHost.change(changeApiHost, inputs=apiHost)

blocks.launch(server_name="0.0.0.0", server_port=7860, debug=False)
