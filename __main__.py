import database as db
from pprint import pprint
import uvicorn
import asyncio

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

async def main():
    config = uvicorn.Config("api:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())