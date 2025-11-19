import asyncio
import logging
import os

import asqlite
import twitchio
from dotenv import load_dotenv

from bot.default import SimpleBot
from components.basic import BasisComponent
from db import setup_database

load_dotenv()

LOGGER: logging.Logger = logging.getLogger("Bot")

CLIENT_ID: str = os.getenv("CLIENT_ID", "")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "")
BOT_ID = os.getenv("BOT_ID", "")
OWNER_ID = os.getenv("OWNER_ID", "")


# async def main() -> None:
#     async with twitchio.Client(
#         client_id=CLIENT_ID, client_secret=CLIENT_SECRET
#     ) as client:
#         await client.login()
#         user = await client.fetch_users(logins=["LexCheshir", "LexPlural"])
#         for u in user:
#             print(f"User: {u.name} - ID: {u.id}")


# if __name__ == "__main__":
#     asyncio.run(main())


def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb:
            tokens, subs = await setup_database(tdb, bot_id=BOT_ID)

            async with SimpleBot(
                logger=LOGGER,
                token_database=tdb,
                subs=subs,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                bot_id=BOT_ID,
                owner_id=OWNER_ID,
                components={
                    BasisComponent,
                },
            ) as bot:
                for pair in tokens:
                    await bot.add_token(*pair)

                await bot.start(load_tokens=False)

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")


if __name__ == "__main__":
    main()
