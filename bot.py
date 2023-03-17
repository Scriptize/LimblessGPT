import hikari
import lightbulb
import openai
import asyncio
from gpt_api import chat_call

bot = lightbulb.BotApp(token='YOUR TOKEN HERE', help_slash_command=True,intents=hikari.Intents.GUILD_MESSAGES,default_enabled_guilds=()))

@bot.command()
@lightbulb.command("start", "Starts Convo")
@lightbulb.implements(lightbulb.SlashCommand)
async def start_convo(message):
    
    # all the messages bot considers when responding:
    # system: "keep in mind" info
    # user: what the user has said
    # assistant: what the assistant has said
    context =[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin."}
             ]
    
    await message.respond("Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin.")

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def get_reply(event):
            nonlocal context
            username = event.message.author.username
            if event.message.content.startswith('Limbless,'):
                context.append({"role":"user", "content": event.message.content[10:]})
                content_req = chat_call(context)
                response = content_req["choices"][0]["message"]['content']
                context.append({"role":"assistant", "content": response}) #add what the bot says to refer to former responses
                await event.message.respond(event.message.author.mention + ", " + response,reply=True,mentions_reply=True)
                print(response)
                print(repr(response))
            else:
                context.append({"role":"system", "content": f"The following message is by {username}: {event.message.content}"}) #aware of messages not directed to the bot
            # openai.api_key = 
            
bot.run()