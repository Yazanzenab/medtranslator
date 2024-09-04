from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# API keys
api_keys = ["a5b0c1d5a38542488d947aaa0c7f7044", "a20bd7d490cb4192afd9ff220252c3ce"]
api_key_index = 0  # Default to the first API key

# System message for OpenAI
system_content = "You are a professional translator that takes English medical text and translates it to Arabic. Please be specific and be aware of the medical terms."

def translate(text):
    # Create the OpenAI client using the current API key
    client = openai.OpenAI(
        api_key=api_keys[api_key_index],
        base_url="https://api.aimlapi.com"
    )
    try:

        # Use the client to create a chat completion
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f'Translate this text to Arabic: {text}'},
            ],
            temperature=1,
        )

        # Extract the translated text from the response
        response = chat_completion.choices[0].message.content
        return response, None
    except:
         return None, "Timeout error: Please switch the API key."

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    original_text = ""
    error_message = None

    if request.method == 'POST':
        original_text = request.form.get('text', '')
        action = request.form.get('action', 'translate')

        if action == 'translate':
            translated_text = translate(original_text)

        elif action == 'switch':
            global api_key_index
            api_key_index = (api_key_index + 1) % len(api_keys)

    return render_template('index.html', original_text=original_text, translated_text=translated_text,error_message=error_message, api_key=api_keys[api_key_index])

if __name__ == '__main__':
    app.run(debug=True)
