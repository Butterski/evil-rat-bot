import os
import discord
import openai
from discord.ext import commands
from cogs.schedule.utils import get_next_week_mondays_and_sundays, transform_message
from utils.functions import try_delete
from dotenv import load_dotenv

load_dotenv()

channel_id = os.environ.get("SCHEDULE_CHANNEL")


class Schedule(commands.Cog):
    """Commands for scheduling"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kiedy_gramy", aliases=["kiedyGramy", "kiedy-gramy"])
    async def schedule_cmd(self, ctx):
        await try_delete(ctx.message)
        channel = self.bot.get_channel(channel_id)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": 'Jesteś szczurzym karczmarzem w fantastycznym świecie, przybyli do ciebie podróżnicy, spytaj się ich w kreatywny sposób kiedy mają wolny czas, wiadomość zakończ po przez jakąś wariację tej wiadomości - \\"zaznaczcie niżej kiedy macie czas tak aby było łatwiej \\". Napisz tylko to co karczmarz mówi bez żadnych innych wiadomości ani opisu na maksymalnie 200 znaków.',
                },
                {
                    "role": "assistant",
                    "content": "Czy podróżnicy mają wolny czas na nową przygodę? Może jakiś czas na zwiedzanie lochów i zabijanie smoków? Albo może chcecie się zemścić na mrocznych królach? Zaznaczcie na moich magicznych tabliczkach kiedy chcecie się wybrać",
                },
                {
                    "role": "assistant",
                    "content": "Czy jesteście zainteresowani nowym zleceniem? Może wyprawa na poszukiwanie ukrytego skarbu? A może potrzebujecie czasu na odkrywanie magicznych tajemnic? Zaznaczcie niżej tak aby było łatwiej ;)",
                },
                {
                    "role": "assistant",
                    "content": "Czy macie chwilę na szybkie zlecenie? Może chcecie spędzić czas na zbieraniu ziółek lub polowaniu na jednorożce? A może pragniecie wyprawy w poszukiwaniu zaginionego artefaktu? Zaznaczcie niżej kiedy macie czas",
                },
                {
                    "role": "assistant",
                    "content": "Czy macie ochotę na przygodę? Może czas na eksplorację tajemniczych jaskiń lub polowanie na potwory w lesie? A może chcielibyście zaryzykować i wyruszyć na niebezpieczną wyprawę po skarb? Zaznaczcie niżej kiedy macie czas  tak aby było łatwiej ;)",
                },
                {
                    "role": "assistant",
                    "content": "Czy wierzycie w odwagę i przygodę? Może macie czas na poszukiwania zaginionej cywilizacji lub walkę z niezniszczalnym smokiem? A może marzy wam się wyprawa w głąb nieznanych ziem? Zaznaczcie poniżej, kiedy macie czas, tak aby łatwiej było planować ;)",
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        monday, sunday = get_next_week_mondays_and_sundays()
        message = (
            "## Kiedy gramy?\n"
            "|| @here ||\n"
            f"**Daty** od: <t:{int(monday)}:d> \n"
            f"*{response['choices'][0]['message']['content']}*\n"
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

    # TODO: ulepszenie tego przez jakiś embed, google calendar, itp
