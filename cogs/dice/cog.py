import d20
import discord
from discord.ext import commands

from utils.critical_texts import getRandomNat1Text, getRandomNat20Text
from utils.functions import try_delete

from .utils import VerboseMDStringifier, string_search_adv


class Dice(commands.Cog):
    """Commands for rolling dice"""

    def __init__(self, bot):
        self.bot = bot

    # ==== commands ====
    @commands.command(name="roll", aliases=["r"])
    async def roll_cmd(self, ctx, *, dice: str = "1d20"):
        if dice == "0/0":
            return await ctx.send("debil")

        dice, adv = string_search_adv(dice)

        res = d20.roll(
            dice, advantage=adv, allow_comments=True, stringifier=VerboseMDStringifier()
        )

        emo = (
            self.bot.get_emoji(1165744876298706964)
            if res.crit == d20.CritType.FAIL
            else self.bot.get_emoji(1165641280110473226)
            if res.crit == d20.CritType.CRIT
            else self.bot.get_emoji(1165744878899167353)
        )

        crit_text = (
            getRandomNat1Text()
            if res.crit == d20.CritType.FAIL
            else getRandomNat20Text()
            if res.crit == d20.CritType.CRIT
            else ""
        )
        if crit_text:
            out = f"{ctx.author.mention} {emo} *{crit_text}*\n{str(res)}"
        else:
            out = f"{ctx.author.mention} {emo}\n{str(res)}"

        if len(out) > 1999:
            out = f"{ctx.author.mention}  {emo}\n{str(res)[:100]}...\n**Total**: {res.total}"

        await try_delete(ctx.message)
        await ctx.send(
            out, allowed_mentions=discord.AllowedMentions(users=[ctx.author])
        )

    @commands.command(name="multiroll", aliases=["rr"])
    async def rr(self, ctx, iterations: int, *, dice):
        """Rolls dice in xdy format a given number of times.
        Usage: !rr <iterations> <dice>"""
        dice, adv = string_search_adv(dice)
        await self._roll_many(ctx, iterations, dice, adv=adv)

    @commands.command(name="iterroll", aliases=["rrr"])
    async def rrr(self, ctx, iterations: int, dice, dc: int = None, *, args=""):
        """Rolls dice in xdy format, given a set dc.
        Usage: !rrr <iterations> <xdy> <DC> [args]"""
        _, adv = string_search_adv(args)
        await self._roll_many(ctx, iterations, dice, dc, adv)

    @staticmethod
    async def _roll_many(ctx, iterations, roll_str, dc=None, adv=None):
        if iterations < 1 or iterations > 100:
            return await ctx.send("Pogrzało cię? Nie będę tyle razy rzucać")
        if adv is None:
            adv = d20.AdvType.NONE
        results = []
        successes = 0
        ast = d20.parse(roll_str, allow_comments=True)
        roller = d20.Roller()

        for _ in range(iterations):
            res = roller.roll(ast, advantage=adv)
            if dc is not None and res.total >= dc:
                successes += 1
            results.append(res)

        if dc is None:
            header = f"Rzucam {iterations} razy."
            footer = f"{sum(o.total for o in results)} razem"
        else:
            header = f"Rzucam {iterations} razy, stopień trudności {dc}..."
            footer = f"{successes} successes, {sum(o.total for o in results)} razem."

        if ast.comment:
            header = f"{ast.comment}: {header}"

        result_strs = "\n".join(str(o) for o in results)

        out = f"{header}\n{result_strs}\n{footer}"

        if len(out) > 1500:
            one_result = str(results[0])
            out = f"{header}\n{one_result}\n[{len(results) - 1} wyniki pominięte dla rozmiaru wyjściowego.]\n{footer}"

        await try_delete(ctx.message)
        await ctx.send(f"{ctx.author.mention}\n{out}", allowed_mentions=discord.AllowedMentions(users=[ctx.author]))