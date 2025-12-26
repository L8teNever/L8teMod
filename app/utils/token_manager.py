import os
import json
from app.config import DATA_DIR, TOKEN_FILE

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
