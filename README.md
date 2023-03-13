# LimblessGPT
LimblessGPT is a Discord bot that can hold conversations using the GPT-3.5-Turbo Model through OpenAI's API

## Usage ⚙️
`/start` begins the conversation

![image](https://user-images.githubusercontent.com/87991619/224593417-04f60b46-7c29-423d-b57d-48f43c24c586.png)

## How it works 🤔
After the `/start` command is ran, the bot begins listening for messages in the current channel that start with "Limbless,"

![image](https://user-images.githubusercontent.com/87991619/224593917-c7c1ff96-7999-4699-a91a-d26b50a011e6.png)

One of the challenges of using GPT-3 models through API calls is that conversation context can't be maintained through consecutive calls.

In other words, follow up questions aren't really possible.

LimblessGPT however, is able to store the context of previous API responses to effectively hold back-and-forth conversations.
##### See the following conversation about quantum mechanics 👇

![image](https://user-images.githubusercontent.com/87991619/224595079-6e77de26-65cd-4e2c-8f5c-5120e5d78f0b.png)


## Developer Notes 📝
* Bug with tokens not being enough to fully generate some prompts
