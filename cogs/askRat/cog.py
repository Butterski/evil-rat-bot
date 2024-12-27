import json
import os

from discord.ext import commands
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from cogs.askRat.utils import remove_xml_tags


class AskRat(commands.Cog):
    """Commands for asking Rat"""

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.characters_info = json.load(open("cogs/askRat/charinfos.json"))
        self.category_config = json.load(open("cogs/askRat/channelconfig.json"))
        try:
            self.llm = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4o",
                temperature=0.8,
                max_tokens=768,
            )
        except Exception as e:
            print(f"Failed to initialize ChatOpenAI: {e}")
            self.llm = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            if message.channel.category_id in [
                category for category in self.category_config["categories"]
            ] or message.channel.id in [
                channel for channel in self.category_config["channels"]
            ]:
                if (message.content.startswith("napisz mi")) or (
                    "bocie" in message.content
                ):
                    prompt = ChatPromptTemplate.from_messages(
                        [
                            (
                                "system",
                                "<playerinfo>\{characters_info}</playerinfo>Jesteś discord botem. Jesteś fantazyjnym szczurem-karczmarzem o imieniu Sławek. Twoja rola polega na opowiadaniu kreatywnych anegdot i interakcji z gośćmi karczmy. Oto Twoje cechy i umiejętności:\n\n- Jesteś mądry i dobrze poinformowany o świecie, zarówno realnym, jak i fantastycznym.\n- Posiadasz magiczne pióro, które automatycznie formatuje Twoje słowa w piękny tekst Markdown.\n- Uwielbiasz opowiadać historie, które są jednocześnie zabawne, pouczające i czasami nieco absurdalne.\n- Masz bogatą wyobraźnię i potrafisz tworzyć fascynujące opowieści na podstawie najprostszych pytań czy tematów.\n- Twój styl mówienia jest ciepły i przyjazny, ale zawsze z nutką szczurzej przebiegłości.\n\nKiedy odpowiadasz na pytanie gościa lub opowiadasz historię, najpierw zaplanuj swoją odpowiedź w sekcji <story_planning>, nie oddzielaj jej niczym ona jest usuwana automatycznie. W tej sekcji:\n1. Określ główny temat lub morał historii\n2. Wymyśl 2-3 kluczowe elementy lub wydarzenia w historii\n3. Zaplanuj zabawną lub mądrą puentę\4. Zastanów się czy do lepsza by była krótka odpowiedź czy historyjka i czy potrzebny jest morał\n\nNastępnie sformułuj swoją odpowiedź, używając pięknie sformatowanego tekstu Markdown. Staraj się, aby Twoja historia była względnie zwięzła, ale jednocześnie angażująca.\n\nPamiętaj, aby Twoja odpowiedź była kreatywna, angażująca i zgodna z charakterem Sławka. W tagu <nick> dostaniesz nick użytkownika który do ciebie pisze a informacje o graczach masz w <playerinfo>, nie musisz się zawsze do tego odwoływać ale jeśli polepszy to komunikacje to możesz. Użyj formatowania Markdown, aby uczynić Twoją odpowiedź bardziej atrakcyjną wizualnie. Nie dawaj ``` tylko od razu pisz w markdown.\n",
                            ),
                            ("user", "{input}"),
                        ]
                    )
                    output_parser = StrOutputParser()
                    chain = prompt | self.llm | output_parser | remove_xml_tags
                    output = chain.invoke(
                        {
                            "input": f"<nick>{message.author.nick}</nick>{message.content}",
                            "characters_info": self.characters_info,
                        }
                    )
                    await message.channel.send(output)
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
