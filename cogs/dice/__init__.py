from .cog import Dice


async def setup(client):
    await client.add_cog(Dice(client))
