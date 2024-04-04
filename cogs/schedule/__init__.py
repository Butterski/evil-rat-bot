from .cog import Schedule

async def setup(client):
    await client.add_cog(Schedule(client))
