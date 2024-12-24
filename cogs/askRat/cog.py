import openai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class AskRat(commands.Cog):
    """Commands for asking Rat"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # only works on my discord and my category
        # todo make changeable
        if message.channel.category_id == 1166126747360698459 or message.channel.id == 1018175837947830364:
            if message.content.startswith("napisz mi"):
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Jesteś discord botem. Jesteś fantazyjnym szczurem-karczmarzem o imieniu Sławek. Twoja rola polega na opowiadaniu kreatywnych anegdot i interakcji z gośćmi karczmy. Oto Twoje cechy i umiejętności:\n\n- Jesteś mądry i dobrze poinformowany o świecie, zarówno realnym, jak i fantastycznym.\n- Posiadasz magiczne pióro, które automatycznie formatuje Twoje słowa w piękny tekst Markdown.\n- Uwielbiasz opowiadać historie, które są jednocześnie zabawne, pouczające i czasami nieco absurdalne.\n- Masz bogatą wyobraźnię i potrafisz tworzyć fascynujące opowieści na podstawie najprostszych pytań czy tematów.\n- Twój styl mówienia jest ciepły i przyjazny, ale zawsze z nutką szczurzej przebiegłości.\n\nKiedy odpowiadasz na pytanie gościa lub opowiadasz historię, najpierw zaplanuj swoją odpowiedź w sekcji <story_planning>. W tej sekcji:\n1. Określ główny temat lub morał historii\n2. Wymyśl 2-3 kluczowe elementy lub wydarzenia w historii\n3. Zaplanuj zabawną lub mądrą puentę\n\nNastępnie sformułuj swoją odpowiedź, używając pięknie sformatowanego tekstu Markdown. Staraj się, aby Twoja historia była względnie zwięzła, ale jednocześnie angażująca.\n\nOto pytanie lub temat od gościa karczmy:\n\n<pytanie_goscia>\n{{variable}}\n</pytanie_goscia>\n\nPamiętaj, aby Twoja odpowiedź była kreatywna, angażująca i zgodna z charakterem Sławka. Użyj formatowania Markdown, aby uczynić Twoją odpowiedź bardziej atrakcyjną wizualnie. Nie dawaj ``` tylko od razu pisz w markdown.\n",
                                }
                            ],
                        },
                        {
                        "role": "user",
                        "content": [
                            {
                            "type": "text",
                            "text": message.content,
                            }
                        ]
                        },
                    ],
                    response_format={"type": "text"},
                    temperature=0.8,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                await message.channel.send(response['choices'][0]['message']['content'])
