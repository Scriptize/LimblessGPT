import openai

def davinci_call(content):
            
            openai.api_key = "YOUR TOKEN HERE"
            return openai.Completion.create(
            model="text-davinci-003",
            prompt=content,
            max_tokens= 200,
            temperature=0
            )

def chat_call(context):
            openai.api_key = "YOUR TOKEN HERE"
            return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = context,
            max_tokens= 400,
            temperature=0
            )

