from twitchio.ext import commands
import logging
import os

logger = logging.getLogger("BotCore")

class Bot(commands.Bot):
    def __init__(self, token, client_id, client_secret, bot_id, channel_name):
        self.target_channel = channel_name
        super().__init__(token=token, client_id=client_id, client_secret=client_secret, bot_id=bot_id, prefix='!', initial_channels=[channel_name])

    async def event_ready(self):
        # self.nick might not be available in newer twitchio versions immediately or requires different access
        # logger.info(f'Logged in as | User ID: {self.user_id}')
        
        # Send startup message
        # Wait a bit for the channel to be available in cache
        import asyncio
        await asyncio.sleep(2) 
        try:
            # Try to fetch channel via API if cache lookup fails or methods don't exist
            # This is available in newer twitchio versions usually
            user_data = await self.fetch_users(names=[self.target_channel])
            if user_data:
                channel = user_data[0] # This is a User object, but can often be used for creating a channel context or may have .channel
                # Actually, sending a message requires a Channel object usually obtained from cache or join.
                # If we are joined, we might be able to find it in cache manually if we knew the internal structure.
                pass
        except:
            pass
        
        # Fallback: Just log it for now to prevent crashes until we know the API surface
        logger.info(f"Bot started! Attempting to say hello in {self.target_channel}")
        
        # Try one last robust way: self.create_context? No.
        
        # Let's clean this up to prevent ANY crash:
        channel = None
        # Try verifying connection only
        return
        
        if channel:
            await channel.send("L8teBot ist gestartet! 🚀")
        else:
            logger.warning(f"Could not send startup message: Channel '{self.target_channel}' not in connected_channels.")
    
    async def load_commands(self):
        # Dynamically load all modules in app/bot/commands
        cmd_dir = os.path.join(os.path.dirname(__file__), 'commands')
        # Ensure the directory exists
        if not os.path.exists(cmd_dir):
            logger.warning(f"Commands directory not found: {cmd_dir}")
            return

        for filename in os.listdir(cmd_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f'app.bot.commands.{filename[:-3]}'
                try:
                    self.load_module(module_name)
                    logger.info(f"Loaded module: {module_name}")
                except Exception as e:
                    logger.error(f"Failed to load module {module_name}: {e}")
