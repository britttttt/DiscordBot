import random
import logging
from discord.ext import commands
from discord.ext.commands import BucketType

log = logging.getLogger(__name__)

class MagicEightBall(commands.Cog):

    ANSWERS = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Yar",
        "Hell No",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="8ball", description="Ask the magic 8‑ball a question")
    @commands.cooldown(1, 5, BucketType.user)
    async def eightball(self, ctx, *, question: str):
        """
        Ask the magic 8-ball a question. Works as both prefix (!8ball) and slash (/8ball).
        The `question` argument captures the user's question text.
        """
        question = (question or "").strip()
        if not question:

            try:
                await ctx.respond("Please ask a question, for example: `/8ball Will I win today?`")
            except Exception:
                await ctx.send("Please ask a question, for example: `!8ball Will I win today?`")
            return

        answer = random.choice(self.ANSWERS)
        response_text = f"As it is written in the stars — {answer}"

        try:
            await ctx.respond(response_text)
        except AttributeError:
            await ctx.send(response_text)
        except Exception:
            log.exception("Failed to respond to 8ball command via ctx.respond(); falling back to ctx.send()")
            await ctx.send(response_text)

async def setup(bot):
    await bot.add_cog(MagicEightBall(bot))