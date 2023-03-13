# string = "\n\nLimbless, hello!"
# print(string.strip("\n\n"))
from pprint import pprint
context =[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin."}
             ]

context.append({"role": "assistant", "content": "Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin."})

pprint(len(context))