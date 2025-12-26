import asyncio
import logging
from aiohttp import web
from app.config import CHANNEL_NAME
from app.utils.token_manager import load_token
from app.web.routes import routes
from app.bot.core import Bot

# Logging setup included in config import, but we can set main logger here
logger = logging.getLogger("Main")

async def main():
    # Start Web Server
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    logger.info("Webserver started on port 5000")

    # Check for token
    token_data = load_token()
    
    # Simple loop to check for token if not present (waiting for user to login via web)
    while not token_data:
        logger.info("Waiting for access token... Visit http://localhost:5000 to login.")
        await asyncio.sleep(5)
        token_data = load_token()

    logger.info("Token found, starting bot...")
    bot = Bot(token=token_data['access_token'], channel_name=CHANNEL_NAME)
    
    # Load commands
    bot.load_commands()
    
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
