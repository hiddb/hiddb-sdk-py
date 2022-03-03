from hiddb.asynchronous import HIDDB


async def create_database():
    key=""
    secret=""
    hiddb = await HIDDB.create(key, secret)