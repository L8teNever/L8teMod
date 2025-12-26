from twitchio.ext import commands
from app.config import model, logger

class LurkCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='lurk')
    async def cmd_lurk(self, ctx: commands.Context):
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

async def prepare(bot: commands.Bot):
    bot.add_cog(LurkCog(bot))
