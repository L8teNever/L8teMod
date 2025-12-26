from twitchio.ext import commands
from app.config import genai_client, logger

class LurkCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='lurk')
    async def cmd_lurk(self, ctx: commands.Context, *, reason: str = None):
        user = ctx.author.name
        
        response_text = f"{user} verabschiedet sich in den Lurk." # Fallback

        if genai_client:
            try:
                if reason:
                    # Specific reason provided
                    prompt = (
                        f"Der Twitch-User '{user}' geht in den 'Lurk'-Modus (abwesend). "
                        f"Er hat diesen Grund angegeben: '{reason}'. "
                        f"Schreibe einen kurzen Satz in der dritten Person auf Deutsch, der bestätigt, dass er lurkt "
                        f"und diesen Grund nennt (z.B. '{user} geht in den Lurk, weil er essen muss'). "
                        f"Sei locker und freundlich."
                    )
                else:
                    # No reason provided -> Random excuse
                    prompt = (
                        f"Der Twitch-User '{user}' geht in den 'Lurk'-Modus (abwesend) ohne einen Grund zu nennen. "
                        f"Erfinde eine lustige oder alltägliche Ausrede für ihn (z.B. Hausaufgaben machen, essen, Eltern helfen, Katze füttern). "
                        f"Schreibe einen kurzen Satz in der dritten Person auf Deutsch (z.B. '{user} geht in den Lurk, um Hausaufgaben zu machen')."
                    )
                
                ai_resp = await genai_client.aio.models.generate_content(
                    model='gemini-1.5-flash-latest',
                    contents=prompt
                )
                if ai_resp.text:
                    response_text = ai_resp.text.strip()
            except Exception as e:
                logger.error(f"Gemini Error: {e}")

        await ctx.send(response_text)

def prepare(bot: commands.Bot):
    bot.add_cog(LurkCog(bot))
