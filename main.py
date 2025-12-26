import asyncio
import logging
import aiohttp
from aiohttp import web
from app.config import CHANNEL_NAME, CLIENT_ID, CLIENT_SECRET
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

    # Fetch Bot User ID (required for newer twitchio versions?)
    bot_id = None
    headers = {
        'Client-Id': CLIENT_ID,
        'Authorization': f'Bearer {token_data["access_token"]}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.twitch.tv/helix/users', headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data['data']:
                    bot_id = data['data'][0]['id']
                    logger.info(f"Fetched Bot ID: {bot_id}")
            else:
                logger.error(f"Failed to fetch Bot ID: {await resp.text()}")

    if not bot_id:
        logger.error("Could not determine Bot ID. Exiting.")
        return

    logger.info("Token found, starting bot...")
    bot = Bot(token=token_data['access_token'], client_id=CLIENT_ID, client_secret=CLIENT_SECRET, bot_id=bot_id, channel_name=CHANNEL_NAME)
    
    # Load commands
    await bot.load_commands()
    
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
