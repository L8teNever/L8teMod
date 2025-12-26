from aiohttp import web
import aiohttp
import os
from app.config import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, TOKEN_FILE
from app.utils.token_manager import save_token, load_token

routes = web.RouteTableDef()

@routes.get('/')
async def handle_root(request):
    token_data = load_token()
    
    if token_data:
        # Dashboard View
        html = """
        <html>
        <head>
            <title>L8teBot Dashboard</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #18181b; color: #efeff1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .card { background: #1f1f23; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; max-width: 400px; width: 100%; }
                h1 { color: #a970ff; margin-bottom: 20px; }
                .status { background: #00e600; color: black; padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 0.9em; display: inline-block; margin-bottom: 20px; }
                .btn { display: inline-block; background: #e91916; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; transition: background 0.3s; }
                .btn:hover { background: #b30000; }
                p { color: #adadb8; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🤖 L8teBot Dashboard</h1>
                <div class="status">Bot is Running</div>
                <p>The bot is successfully authenticated and connected.</p>
                <br>
                <a href="/logout" class="btn">Logout / Reset</a>
            </div>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')
    else:
        # Login View
        auth_url = (
            f"https://id.twitch.tv/oauth2/authorize"
            f"?response_type=code"
            f"&client_id={CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope=chat:read+chat:edit"
        )
        html = f"""
        <html>
        <head><title>Twitch Bot Login</title></head>
        <body style="font-family: 'Segoe UI', sans-serif; text-align: center; padding: 50px; background-color: #18181b; color: white;">
            <div style="background: #1f1f23; padding: 40px; border-radius: 10px; display: inline-block;">
                <h1>🤖 L8teBot Setup</h1>
                <p style="color: #adadb8;">Please log in to authorize the bot.</p>
                <br>
                <a href="{auth_url}" style="background: #9146FF; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Login with Twitch</a>
            </div>
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
                # Redirect to Dashboard (Root)
                raise web.HTTPFound('/')
            else:
                return web.Response(text=f"Error getting token: {data}")

@routes.get('/logout')
async def handle_logout(request):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    raise web.HTTPFound('/')
