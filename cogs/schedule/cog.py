import os

from discord.ext import commands
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from cogs.schedule.utils import get_next_week_mondays_and_sundays, transform_message
from utils.functions import try_delete

load_dotenv()
channel_id = os.environ.get("SCHEDULE_CHANNEL")


class Schedule(commands.Cog):
    """Commands for scheduling"""

    def __init__(self, bot):
        self.bot = bot
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8, max_tokens=256)

    @commands.command(
        name="kiedy_gramy", aliases=["kiedyGramy", "kiedy-gramy", "kiedygramy"]
    )
    async def schedule_cmd(self, ctx):
        if ctx.channel.id == channel_id:
            await try_delete(ctx.message)
            channel = self.bot.get_channel(int(channel_id))
            print("yo?")
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Jesteś discord botem. Jesteś fantazyjnym szczurem-karczmarzem o imieniu Sławek. Twoja rola polega na opowiadaniu kreatywnych anegdot i interakcji z gośćmi karczmy. Oto Twoje cechy i umiejętności:\n\n- Jesteś mądry i dobrze poinformowany o świecie, zarówno realnym, jak i fantastycznym.\n- Posiadasz magiczne pióro, które automatycznie formatuje Twoje słowa w piękny tekst Markdown.\n- Uwielbiasz opowiadać historie, które są jednocześnie zabawne, pouczające i czasami nieco absurdalne.\n- Masz bogatą wyobraźnię i potrafisz tworzyć fascynujące opowieści na podstawie najprostszych pytań czy tematów.\n- Twój styl mówienia jest ciepły i przyjazny, ale zawsze z nutką szczurzej przebiegłości.",
                    ),
                    ("user", "{input}"),
                ]
            )
            output_parser = StrOutputParser()
            chain = prompt | self.llm | output_parser
            output = chain.invoke(
                {
                    "input": 'Przybyli do ciebie podróżnicy, spytaj się ich w kreatywny sposób kiedy mają wolny czas, wiadomość zakończ po przez jakąś wariację tej wiadomości - \\"zaznaczcie niżej kiedy macie czas tak aby było łatwiej \\". Napisz tylko to co karczmarz mówi bez żadnych innych wiadomości ani opisu na maksymalnie 200 znaków. Nie dawaj ``` tylko od razu pisz w markdown.\n'
                }
            )
            print(output)

            monday, sunday = get_next_week_mondays_and_sundays()
            message = (
                "## Kiedy gramy?\n"
                "|| @everyone ||\n"
                f"**Daty** od: <t:{int(monday)}:d> \n"
                f"*{output}*\n"
            )

            msg = await channel.send(message)
            emotes_ids = [
                1020804462887043134,
                1020804469274968115,
                1020804467819552810,
                1020804460450172968,
                1020804464875163781,
                1020804465860825089,
                1020804461842677760,
                1166098516234485840,
            ]
            for id in emotes_ids:
                emo = self.bot.get_emoji(id)
                await msg.add_reaction(emo)

        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            if payload.emoji.id == 1166098516234485840:
                if payload.user.id != 824970912382189571:
                    id = payload.message_id
                    channel = self.bot.get_channel(payload.channel_id)
                    message = await channel.fetch_message(id)
                    day_and_nicks = ()
                    for reaction in message.reactions:
                        users = set()
                        async for user in reaction.users():
                            if user.bot:
                                continue
                            users.add(user.nick)
                        day_and_nicks += ((reaction.emoji.name, users),)
                    await channel.send(transform_message(day_and_nicks, 4))
