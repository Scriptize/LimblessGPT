# LimblessGPT
LimblessGPT is a Discord bot that can hold conversations using OpenAI's [GPT-3.5-Turbo Model](https://platform.openai.com/docs/guides/chat/introduction)

If you fork this repo, run `pip install -r requirements.txt` to install dependencies

If you want to have access to LimblessGPT in Discord when it is deployed in the future, [click here!](https://discord.com/api/oauth2/authorize?client_id=1084338217274322964&permissions=8&scope=bot)

## Usage ⚙️
`/start` begins the conversation

![image](https://user-images.githubusercontent.com/87991619/224593417-04f60b46-7c29-423d-b57d-48f43c24c586.png)

## How it works 🤔
After the `/start` command is ran, the bot begins listening for messages in all channels that start with "Limbless,"

![image](https://user-images.githubusercontent.com/87991619/224593917-c7c1ff96-7999-4699-a91a-d26b50a011e6.png)

One of the challenges of using GPT-3 models through API calls is that conversation context can't be maintained through consecutive calls.

In other words, follow up questions aren't really possible.

LimblessGPT however, is able to store the context of previous API responses to effectively hold back-and-forth conversations, similiar to ChatGPT.
##### See the following conversation about quantum mechanics 👇

![image](https://user-images.githubusercontent.com/87991619/224595079-6e77de26-65cd-4e2c-8f5c-5120e5d78f0b.png)

By leveraging GPT-3.5-Turbo, we can open the door to concurrent conversations, where multiple users can hold conversations at once, which is definitely appealing for collaborative-esque use cases.

Not only that, but it can also keep note of messages not addressed to it. Discord is a place where multiple people are constantly talking, and LimblessGPT keeps track of this to make responses more relevant.
##### The following image highights this 👇

![image](https://user-images.githubusercontent.com/87991619/225807331-898418eb-98ba-487c-9398-d3fa02a1d356.png)


## Developer Notes 📝
* Bug with tokens not being enough to fully generate some prompts
