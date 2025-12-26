from twitchio.ext import commands
import logging
import os

logger = logging.getLogger("BotCore")

class Bot(commands.Bot):
    def __init__(self, token, client_id, client_secret, bot_id, channel_name):
        super().__init__(token=token, client_id=client_id, client_secret=client_secret, bot_id=bot_id, prefix='!', initial_channels=[channel_name])

    async def event_ready(self):
        # self.nick might not be available in newer twitchio versions immediately or requires different access
        logger.info(f'Logged in as | User ID: {self.user_id}')
    
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
                    await self.load_module(module_name)
                    logger.info(f"Loaded module: {module_name}")
                except Exception as e:
                    logger.error(f"Failed to load module {module_name}: {e}")
