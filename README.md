# LimblessGPT
LimblessGPT is a Discord bot that can hold concurrent, cross-channel conversations using OpenAI's [GPT-4 Model](https://platform.openai.com/docs/guides/chat/introduction)

If you fork this repo, run `pip install -r requirements.txt` to install dependencies

If you want to have LimblessGPT in your Discord server, [click here!](https://discord.com/api/oauth2/authorize?client_id=1084338217274322964&permissions=8&scope=bot)

## Usage ⚙️
`/welcome` introduces the bot and how to get started:

![image](https://github.com/Scriptize/LimblessGPT/assets/87991619/fe90c8f7-1589-4ba7-8ada-cf7ed6ea26c8)

## How it works 🤔
As soon as the bot enters a Discord server, it begins listening for messages in all channels that start with "Limbless,"

![image](https://github.com/Scriptize/LimblessGPT/assets/87991619/0fe02240-9297-4a52-aa63-dd150b678fa6)

One of the challenges of using GPT-3 models through API calls is that conversation context can't be maintained through consecutive calls.

In other words, follow-up questions aren't really possible.

LimblessGPT, however, can store the context of previous API responses to effectively hold back-and-forth conversations, similar to ChatGPT.
##### See the following conversation about SQL Databases 👇

![image](https://github.com/Scriptize/LimblessGPT/assets/87991619/6a6a2538-078b-41eb-ba7d-48bc419c9100)

By leveraging GPT-3.5-Turbo, we can open the door to concurrent conversations, where multiple users can have conversations with LimblessGPT at once — definitely appealing for collaborative-esque use cases.

Not only that, but it can also keep note of messages not addressed to it. Discord is a place where multiple people are constantly talking, and LimblessGPT keeps track of this to make responses more relevant.
##### The following image highlights this 👇

![image](https://user-images.githubusercontent.com/87991619/228068613-dbaa0638-4cc5-418b-96a7-4e3453ef32cb.png)

Obviously, storing the context for all these messages takes up many tokens (there is a limit), so LimblessGPT can resize the context its been maintaining to answer relevantly without token overload 👇

![image](https://user-images.githubusercontent.com/87991619/228068391-a333ff02-657b-4dc1-8c62-e946ca526738.png)


## Developer Notes 📝
* Application seems to be working fine even though logs show some Discord API errors; continuing to look into it 
