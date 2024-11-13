from openai import OpenAI
import base64
from openai import OpenAI

#Set up the API key
client = OpenAI(api_key="")

#Function for processing the image
def response(image_path, prompt):
    """
    Sends an Image and gets a response.
    """ 
    #Catch prompt empty error
    if not prompt:
        return "Error: Prompt is empty."
    #Reformat the image
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
    #Initialize return string
    description = ""
    # Assuming `client.chat.completions.create` returns a complete response when not streaming
    response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"answer the user question: {prompt}"},
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        },
                        },
                    ],
                    }
                ],
                max_tokens=500,
                )
    if response.choices and response.choices[0].message.content:
        description += response.choices[0].message.content
    return description
