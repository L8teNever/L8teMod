from aiohttp import web
import aiohttp
from app.config import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET
from app.utils.token_manager import save_token

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
                html = """
                <html>
                <body style="font-family: sans-serif; text-align: center; padding: 50px; background-color: #f0f0f0;">
                    <div style="background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h1 style="color: #4CAF50;">Login Successful! ✅</h1>
                        <p>The access token has been securely saved.</p>
                        <hr style="margin: 20px 0; border: 0; border-top: 1px solid #eee;">
                        <p style="font-weight: bold;">Usage:</p>
                        <p>The bot should start automatically within a few seconds.</p>
                        <p style="color: #666; font-size: 0.9em;">If nothing happens, please restart the Docker container.</p>
                    </div>
                </body>
                </html>
                """
                return web.Response(text=html, content_type='text/html')
            else:
                return web.Response(text=f"Error getting token: {data}")
