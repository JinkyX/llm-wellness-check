# Run inference on input text (Mistral format)# CSV helpers, prompt builder, inference formatting
from app.prompting import build_prompt, format_inference

def call_model(row, model):
    prompt = build_prompt(row)
    payload = format_inference(prompt)

    try:
        response = model(**payload)
        text = response['choices'][0]['text']
        # if '[/INST]' in text:
        #     return text.split('[/INST]', 1)[1].strip()
        return text.strip()
    except Exception as e:
        return f"Error: {e}"