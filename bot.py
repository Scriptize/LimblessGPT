import hikari
from pprint import pprint
import lightbulb
import openai
import asyncio
import datetime
from models import Context_Handler, Resource_Handler
from gpt_api import chat_call
import json
import os

TOKEN = os.environ.get('TOKEN')
CONTEXT = Context_Handler()
RESOURCE = Resource_Handler()
bot = lightbulb.BotApp(token=TOKEN,intents=hikari.Intents.GUILD_MESSAGES,default_enabled_guilds=())

CONTEXT.content.extend([
            {"role": "system", "content": "You are a helpful assistant orginating from the Limbless Discord Server"},
            {"role": "system", "content": "You are unique in that you can handle concurrent conversations in multiple channels and leverage extracontextual tuning for relavance"},
            {"role": "system", "content": "You work by accumulating context everytime someone says 'Limbless,' in a channel and respond acccordingly"},
            {"role": "system", "content": 'Whenever you are asked to write, generate, or provide code or code snippets, format it like this example: ```python\nprint("hello world")\n``` (type the name of the language after the first 3 tics)'},
            {"role": "system", "content": "If you have a lot of information or code before prompted, only respond to the most relevant parts"},
            {"role": "assistant", "content": "Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin."}
        ])
    
@bot.command()
@lightbulb.command("welcome", "getting started")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(message):
    await message.respond("Hello, I am Limbless's AI model.\nStart your prompt with 'Limbless,' to begin.")



#when message occurs
@bot.listen(hikari.GuildMessageCreateEvent)
async def get_reply(event):
        global CONTEXT
        # fetch username
        guild_id = event.guild_id
        username = event.message.author.username
       
        
        #check if its to the bot
        if event.message.content.startswith('Limbless,'): 
            async with bot.rest.trigger_typing(event.message.channel_id):
                #Add message to context
                CONTEXT.content.append({"role":"system", "content":f"This user's name is {username}: {event.message.content[10:]}", "guild_id":guild_id}) 
                print({"The context length is:":len(CONTEXT)})

                #filter for messages in server
                guild_context = CONTEXT.filter(event)
                pprint(guild_context)
                try: 
                    #attempt API req
                        content_req = chat_call(CONTEXT.content[:6] + guild_context)
                        print(content_req)

                #If too many tokens
                except openai.error.InvalidRequestError:
                
                    print({"Rezing at guild context length":len(guild_context)})
                    await bot.rest.trigger_typing(event.message.channel_id)
                    await event.message.respond("Give me a moment, I'm resizing my context capacity...", reply=True,mentions_reply=True)
                    CONTEXT.resize(event)
                    guild_context = CONTEXT.filter(event)
                    await bot.rest.trigger_typing(event.message.channel_id)
                    content_req = chat_call(CONTEXT.content[:6] + guild_context)
                    print({"The context length is:":len(CONTEXT)})
                
                # if content_req["choices"][0]["finish_reason"] == "function_call":
                #     RESOURCE.function_name = content_req["choices"][0]['message']["function_call"]['name']
                #     channel_name = json.loads(content_req["choices"][0]['message']["function_call"]["arguments"])['name']
                #     if RESOURCE.function_name == "create_text_channel":
                #         category = json.loads(content_req["choices"][0]['message']["function_call"]["arguments"])['category']
                #         if category == "None":
                #             category = None
                #         await RESOURCE.create_text_channel(bot,guild_id,channel_name,category)
                #         await event.message.respond(event.message.author.mention + ", " + "successfully created resource!",reply=True,mentions_reply=True)
                    

                else: 
                    await bot.rest.trigger_typing(event.message.channel_id)
                    response = content_req["choices"][0]["message"]["content"]
                    print(response)
                    print(len(response))
                    CONTEXT.content.append({"role":"assistant", "name":"Limbless_GPT", "content": response,"guild_id":guild_id})
                    await event.message.respond(event.message.author.mention + ", " + response,reply=True,mentions_reply=True)
                    print({"The context length is:":len(CONTEXT)})
        
        elif username != "Limbless_GPT":
            CONTEXT.content.append({"role":"system", "content":f"This user's name is {username}: {event.message.content[10:]}", "guild_id":guild_id})
            print({"The context length is:":len(CONTEXT)})
           

        # else:
        #     CONTEXT.content.append({"role":"assistant", "name":username, "content":event.message.content, "guild_id":event.guild_id})
        #     print({"The context length is:":len(CONTEXT)})

#bot.rest.create_guild_text_channel()
   
               

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
