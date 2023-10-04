import openai
import random
from src.bot import Bot, CHAT_MODEL
from discord import Message
from discord.ext import commands

from bots.rhulk import rhulk
from bots.calus import calus
from bots.drifter import drifter
from bots.nezarec import nezarec



RANDOM_CHANCE = 0.005


#? Helper Functions

async def generate_response(chosen_speaker, user_msg: str):
        try:
            completion = openai.ChatCompletion.create(
                    model=CHAT_MODEL,
                    messages=[{"role": "system", "content": "You are in a Discord server, and will be provided a user message you want to respond to. " + chosen_speaker.text.chat_prompt},
                            {"role": "user", "content": user_msg}],
                    n=1,
                    max_tokens=512,
                    temperature=1.2,
                    frequency_penalty=0.9,
                    presence_penalty=0.75
                )
            return completion.choices[0].message.content
        except Exception as e:
            print(e)
            return e


#? Random Chime-In messages Cog

class ChimeEvents(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: Message):
        if not message.author.bot and not message.attachments:
            if random.random() < RANDOM_CHANCE:
                chosen_speaker = random.choice([rhulk, calus, drifter, nezarec])
                response = await generate_response(chosen_speaker, message.content)
                await chosen_speaker.bot.get_channel(message.channel.id).send(response, reference=message)
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(ChimeEvents(bot))