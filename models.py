import hikari
import lightbulb


class Context_Handler:
    """Class for managing context of OpenAI's chat completion models."""
    def __init__(self):
        self.content = []
    
    def __len__(self):
        return len(self.content)
    
    def __str__(self):
        return f"context object with length:{len(self.content)}"
    
    def filter(self,event):
        """
        Returns messages from a server based on guild_id
        """
        return [{'role': message['role'], 'content': message['content']} for message in self.content[6:] if message['guild_id'] == event.guild_id]
    
    def resize(self, event):
        """
        Resizes context to account for messages on other servers and the last
        quarter of recent message in the server the event was triggered in.
        """
        guild_msg_count = sum("guild_id" in d and d["guild_id"] == event.guild_id for d in self.content)
        new_content = []
        count = 0
        
        for i in self.content:

            if len(new_content) < 6:
                new_content.append(i)

            if i["guild_id"] != event.guild_id:
                new_content.append(i)
            
            if i["guild_id"] == event.guild_id:
                count +=1
            
            if i["guild_id"] == event.guild_id and (count > (3 * (guild_msg_count//4))):
                new_content.append(i)
        
        self.content = new_content
    
    
class Resource_Handler:
    """Class for handling resource creation through function calls"""
    TEXT = 0
    VOICE = 2

    def __init__(self, function_name=None):
            self.function_name = function_name
    
    async def create_text_channel(self, bot, guild_id, name, category=None):
        categories = {}
        categories = {channel.type:channel.parent_id for channel in await bot.rest.fetch_guild_channels(guild_id) if channel.type not in categories}

        if self.function_name == "create_text_channel" and (category==None):
            await bot.rest.create_guild_text_channel(guild_id ,name)

        elif self.function_name == "create_text_channel" and (category=="text"):
            await bot.rest.create_guild_text_channel(guild_id, name, category=categories[self.TEXT])

        elif self.function_name == "create_text_channel" and (category=="voice"):
            await bot.rest.create_guild_text_channel(guild_id, name, category=categories[self.VOICE])
    
    

    
    
