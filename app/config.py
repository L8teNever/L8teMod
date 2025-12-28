import os
import sys
import logging
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration Constants
ENV_FILE = '.env'
DATA_DIR = '/app/data'
TOKEN_FILE = os.path.join(DATA_DIR, 'tokens.json')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/callback')

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Config")

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

# Gemini Setup
# Gemini Setup
genai_client = None
if GEMINI_KEY:
    try:
        genai_client = genai.Client(api_key=GEMINI_KEY)
        logger.info("Gemini AI successfully configured.")
        
        # Debug: List available models to find valid names
        try:
            # Paging through models to find generateContent supported ones
            logger.info("--- Available Gemini Models ---")
            for m in genai_client.models.list():
                if 'generateContent' in (m.supported_generation_methods or []):
                    logger.info(f"Model: {m.name}")
            logger.info("-------------------------------")
        except Exception as e:
            logger.warning(f"Could not list models: {e}")

    except Exception as e:
         logger.error(f"Failed to configure Gemini: {e}")
else:
    logger.warning("No GEMINI_API_KEY found. AI features will be disabled.")
