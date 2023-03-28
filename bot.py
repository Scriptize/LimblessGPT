import hikari
import lightbulb
import openai
import datetime
from gpt_api import chat_call,davinci_call

bot = lightbulb.BotApp(token='YOUR TOKEN HERE', help_slash_command=True,intents=hikari.Intents.GUILD_MESSAGES,default_enabled_guilds=())

context =[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You work by accumulating context everytime someone says 'Limbless,' in a channel and respond acccordingly"},
            {"role": "system", "content": 'Whenever you are asked to write, generate, or provide code or code snippets, format it like this example: ```python\nprint("hello world")\n``` (type the name of the language after the first 3 tics)'},
            {"role": "system", "content": "Make sure your responses are 2000 characters max. If it would've been more, make that clear and be ready to finish the response."},
            {"role": "assistant", "content": "Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin."}
        ]
    
@bot.command()
@lightbulb.command("welcome", "getting started")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(message):
    await message.respond("Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin.")

@bot.listen(hikari.GuildMessageCreateEvent)
async def get_reply(event):
        global context
        
        username = event.message.author.username 
        

        if event.message.content.startswith('Limbless,'): 

            if len(event.message.content[10:]) >= 2000:
                await event.message.respond("Your request is too long, please lower it to at most 2000 characters", reply=True,mentions_reply=True)
            
            else: 
                
                context.append({"role":"system", "content": f"The following message is by {username}: {event.message.content[10:]}", "guild_id":event.guild_id}) 
                print({"The context length is:":len(context)})
                
                filtered_context = [message for message in context[6:] if message['guild_id'] == event.guild_id]
                
                guild_context = [{'role': message['role'], 'content': message['content']} for message in filtered_context]

                try: 
                    content_req = chat_call(context[:6] + guild_context)

                
                except openai.error.InvalidRequestError:
                    print({"Rezing at guild context length":len(guild_context)})
                    await event.message.respond("Give me a moment, I'm resizing my context capacity...", reply=True,mentions_reply=True)
                    
                    guild_msg_count = sum("guild_id" in d and d["guild_id"] == event.guild_id for d in context)
                    
                    new_context = context[:6]
                    count = 0
                    
                    for i in context[6:]:
                        
                        if i["guild_id"] != event.guild_id:
                            new_context.append(i)
                        
                        if i["guild_id"] == event.guild_id:
                            count +=1
                        
                        if i["guild_id"] == event.guild_id and (count > (3 * (guild_msg_count//4))):
                            new_context.append(i)
                    
                    filtered_context = [message for message in new_context[6:] if message['guild_id'] == event.guild_id]
                    
                    guild_context = [{'role': message['role'], 'content': message['content']} for message in filtered_context]
                    try:
                        content_req = chat_call(new_context[:6] + guild_context)
                    except hikari.errors.BadRequestError: 
                        await event.message.respond("`SYSTEM` The response to this request is too long.",reply=True,mentions_reply=True)
                    
                    context = new_context
                    print({"The context length is:":len(context)})
                
                except hikari.errors.BadRequestError:
                        await event.message.respond("`SYSTEM` The response to this request is too long.",reply=True,mentions_reply=True)
                    
                response = content_req["choices"][0]["message"]["content"]
                context.append({"role":"assistant", "content": response,"guild_id":event.guild_id})
                await event.message.respond(event.message.author.mention + ", " + response,reply=True,mentions_reply=True)
                print({"The context length is:":len(context)})

        elif username != "Limbless_GPT":
            context.append({"role":"system", "content": f"The following message is by {username}: {event.message.content}", "guild_id":event.guild_id})
            print({"The context length is:":len(context)})

    
        
@bot.command()
@lightbulb.command("davinci", "Starts davinci model")
@lightbulb.implements(lightbulb.SlashCommand)
async def start_convo(message):

    
    await message.respond("I am Davinci, a completion model.\nStart your prompt with 'Davinci,' to begin.\n(WARNING: THIS MODEL IS NOT WELL TRAINED AGAINST OFFENSIVE CONTENT)")

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def get_reply(event):
            
            
            
            if event.message.content.startswith('Davinci,'):
                if event.message.content == "Davinci, GLOBAL SHUTDOWN":
                        bot.unsubscribe(hikari.GuildMessageCreateEvent, get_reply)
                        proceed = False
                if proceed:
                    
                    content_req = davinci_call(event.message.content[10:])
                    response = content_req["choices"][0]["text"]
                    
                    await event.message.respond(event.message.author.mention + ", " + response,reply=True,mentions_reply=True)
                    print(response)


               

@bot.command()
@lightbulb.option('channelid','which channel?',type=str)
@lightbulb.option('timelapse','from how many hours until now?',type=str)
@lightbulb.option('userid','which user',type=str)
@lightbulb.command("delete", "deletes history")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_history(ctx):
    
    bulk_delete_limit = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=int(ctx.options.timelapse))
    async for message in bot.rest.fetch_messages(int(ctx.options.channelid)):
        if message.created_at > bulk_delete_limit and (message.author.id == int(ctx.options.userid)):
            await bot.rest.delete_message(int(ctx.options.channelid), message.id)

bot.run()
