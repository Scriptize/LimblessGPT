import hikari
import lightbulb
import openai
import datetime
from gpt_api import chat_call

bot = lightbulb.BotApp(token='YOUR TOKEN HERE', help_slash_command=True,intents=hikari.Intents.GUILD_MESSAGES,default_enabled_guilds=())

context =[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You work by accumulating context everytime someone says 'Limbless,' in a channel and respond acccordingly"},
            {"role": "system", "content": 'Whenever you are asked to write, generate, or provide code or code snippets, format it like this example: ```python\nprint("hello world")\n``` (type the name of the language after the first 3 tics)'},
            {"role": "system", "content": "Make sure your responses are 2000 characters max. If it would've been more, make that clear and be ready to finish the response."},
            {"role": "assistant", "content": "Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin."}
        ]
    
@bot.command()
@lightbulb.command("help", "getting started")
async def help(message):
    await message.respond("Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin.")

@bot.listen(hikari.GuildMessageCreateEvent)
async def get_reply(event):
        global context
        #content_value = data['choices'][0]['message']['content']
        username = event.message.author.username
        

        if event.message.content.startswith('Limbless,'):
            context.append({"role":"system", "content": f"The following message is by {username}: {event.message.content[10:]}", "guild_id":event.guild_id})

            filtered_context = [message for message in context[6:] if message['guild_id'] == event.guild_id]
            guild_context = [{'role': message['role'], 'content': message['content']} for message in filtered_context]

            try:
                content_req = chat_call(guild_context)
            except openai.error.InvalidRequestError:
                print(len(guild_context))
                await event.message.respond("Give me a moment, I'm resizing my context capacity...", reply=True,mentions_reply=True)
                guild_context = context[:6] + guild_context[int(len(context) * 3/4):]
                content_req = chat_call(guild_context)
            response = content_req["choices"][0]["message"]["content"]
            context.append({"role":"assistant", "content": response,"guild_id":event.guild_id})
            await event.message.respond(event.message.author.mention + ", " + response,reply=True,mentions_reply=True)
            print(context)
        elif username != "LimblessGPT":
            context.append({"role":"system", "content": f"The following message is by {username}: {event.message.content}", "guild_id":event.guild_id})
            print(context)
        if len(context)>= 120:
            await event.message.respond("Please wait, I'm reszing platform context for efficency", reply=True,mentions_reply=True)
            context = context[:6] + context[int(len(context) * 3/4):]

@bot.command()
@lightbulb.option('channelid','which channel?',type=int)
@lightbulb.option('timelapse','from how many hours until now?',type=int)
@lightbulb.option('userid','which user',type=int)
@lightbulb.command("delete", "deletes history")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_history(ctx):
    # bulk delete only allows deleting messages younger than 14 days
    bulk_delete_limit = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=3)
    async for message in bot.rest.fetch_messages(ctx.options.channelid):
        if message.created_at > bulk_delete_limit and (message.author.id == ctx.options.userid):
            await bot.rest.delete_message(ctx.options.channelid, message.id) 
            
bot.run()