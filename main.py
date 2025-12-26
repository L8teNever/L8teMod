import os
import json
import asyncio
import logging
from aiohttp import web
from twitchio.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration Constants
ENV_FILE = '.env'
DATA_DIR = '/app/data'
TOKEN_FILE = os.path.join(DATA_DIR, 'tokens.json')
REDIRECT_URI = 'http://localhost:5000/callback'

def setup_wizard():
    """Interactively asks for configuration if missing."""
    print("\n--- 🤖 L8teBot Setup Assistent ---")
    print("Es scheint, als würden einige Konfigurationen fehlen.")
    print("Bitte gib die folgenden Daten ein (Bestätigen mit Enter).\n")

    try:
        client_id = input("Twitch Client ID: ").strip()
        client_secret = input("Twitch Client Secret: ").strip()
        gemini_key = input("Gemini API Key: ").strip()
        bot_nick = input("Bot Nickname (z.B. L8teBot): ").strip()
        channel_name = input("Target Channel Name: ").strip()
        
        if not all([client_id, client_secret, channel_name]):
            print("\n❌ Fehler: Wichtige Daten fehlen! Setup abgebrochen.")
            sys.exit(1)

        with open(ENV_FILE, 'w') as f:
            f.write(f"TWITCH_CLIENT_ID={client_id}\n")
            f.write(f"TWITCH_CLIENT_SECRET={client_secret}\n")
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
            f.write(f"BOT_NICK={bot_nick}\n")
            f.write(f"CHANNEL_NAME={channel_name}\n")
        
        print(f"\n✅ Konfiguration in '{ENV_FILE}' gespeichert! Lade neu...\n")
        load_dotenv(override=True)
        
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ Setup abgebrochen. Bitte .env manuell erstellen.")
        sys.exit(1)

# Check for essential variables and run setup if needed
if not os.getenv('TWITCH_CLIENT_ID') or not os.getenv('CHANNEL_NAME'):
    # Check if we are in an interactive terminal
    if sys.stdin.isatty():
        setup_wizard()
    else:
        logger.warning("Keine .env Konfiguration gefunden und kein interaktives Terminal.")
        logger.warning("Bitte erstelle die .env Datei manuell oder starte den Container interaktiv.")

# Re-fetch variables after potential setup
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
BOT_NICK = os.getenv('BOT_NICK', 'LurkBot')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Bot")

# Gemini Setup
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    logger.warning("No GEMINI_API_KEY found. AI features will be disabled.")
    model = None

# Token Management
def save_token(token_data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def load_token():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

# Web Server for Auth
routes = web.RouteTableDef()

@routes.get('/')
async def handle_root(request):
    auth_url = (
        f"https://id.twitch.tv/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=chat:read+chat:edit"
    )
    html = f"""
    <html>
    <head><title>Twitch Bot Setup</title></head>
    <body style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>Twitch Bot Setup</h1>
        <p>Please log in to authorize the bot.</p>
        <a href="{auth_url}" style="background: #9146FF; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login with Twitch</a>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

@routes.get('/callback')
async def handle_callback(request):
    code = request.query.get('code')
    if not code:
        return web.Response(text="Error: No code provided.")
    
    # Exchange code for token
    async with aiohttp.ClientSession() as session:
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
        async with session.post('https://id.twitch.tv/oauth2/token', params=params) as resp:
            data = await resp.json()
            if 'access_token' in data:
                save_token(data)
                return web.Response(text="Success! Token saved. You can close this window. restart the bot container to apply changes if it doesn't start automatically.")
            else:
                return web.Response(text=f"Error getting token: {data}")

# Twitch Bot
class Bot(commands.Bot):
    def __init__(self, token):
        super().__init__(token=token, prefix='!', initial_channels=[CHANNEL_NAME])

    async def event_ready(self):
        logger.info(f'Logged in as | {self.nick}')
        logger.info(f'User id is | {self.user_id}')

    @commands.command()
    async def lurk(self, ctx: commands.Context):
        reason = ctx.message.content.replace('!lurk', '').strip()
        user = ctx.author.name
        
        response_text = f"{user} geht in den Lurk." # Fallback

        if model:
            try:
                if reason:
                    prompt = (
                        f"Ein Twitch-User namens '{user}' geht in den 'Lurk'-Modus (abwesend/zuschauen). "
                        f"Er hat diesen Grund angegeben: '{reason}'. "
                        f"Formuliere eine kurze, lustige oder passende Nachricht auf Deutsch in der dritten Person, "
                        f"die bestätigt, dass er lurkt und warum. Behalte den Kern des Grundes bei."
                    )
                else:
                    prompt = (
                        f"Ein Twitch-User namens '{user}' geht in den 'Lurk'-Modus (abwesend). "
                        f"Erledige eine kurze, lustige, zufällige Ausrede auf Deutsch in der dritten Person, warum er lurkt."
                    )
                
                ai_resp = await model.generate_content_async(prompt)
                if ai_resp.text:
                    response_text = ai_resp.text.strip()
            except Exception as e:
                logger.error(f"Gemini Error: {e}")

        await ctx.send(response_text)

# Main runner
async def main():
    # Start Web Server
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    logger.info("Webserver started on port 5000")

    # Check for token and start bot if available
    token_data = load_token()
    
    # Simple loop to check for token if not present (waiting for user to login via web)
    while not token_data:
        logger.info("Waiting for access token... Visit http://localhost:5000 to login.")
        await asyncio.sleep(5)
        token_data = load_token()

    logger.info("Token found, starting bot...")
    bot = Bot(token=token_data['access_token'])
    await bot.start()

if __name__ == "__main__":
    import aiohttp # Imported here to be available in 'main' scope if needed, though used in handlers
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
