import gradio as gr
from gradio_backend import response 
from conversational_transcribe import conversation_transcription

# Paths to example images
examples = [
    [r"test_data\1.jpg", "何があっていますか？"],
    [r"test_data\2.jpeg", "左側はなんですか？"],
    [r"test_data\3.jpg", "今何時見たいですか？"],
]

def process_prompt(img_path, audio):
    # Call the response func
    prompt = conversation_transcription(audio)
    content = response(img_path, prompt)

    return content

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            img_path = gr.Image(label="Image", type="filepath")
            prompt_mic = gr.Microphone(label="Microphone Input", type="filepath")
            processed_button = gr.Button(value="Process")
        with gr.Column():
            content = gr.Textbox(label="Image Content")

    # Bind the button click event to the process_image function
    processed_button.click(
        fn=process_prompt,
        inputs=[img_path, prompt_mic],
        outputs=[content] 
    )

    # Add image examples
    examples = gr.Examples(
        examples=examples,  # Assuming example_images is defined elsewhere
        inputs=[img_path, prompt_mic],
        label="Example Images"
    )



demo.launch(share=True)