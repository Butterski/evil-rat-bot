from .cog import AskRat

async def setup(client):
    await client.add_cog(AskRat(client))
