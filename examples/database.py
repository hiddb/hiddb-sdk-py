from hiddb_sdk.synchronous import HIDDB


def create_database():
    key=""
    secret=""
    hiddb = HIDDB.create(key, secret)
    # print(await hiddb.create_database("tesdb"))
    # print(await hiddb.list_databases())
    # print(await hiddb.get_database("u92cccov5tsg14tq2l"))
    # print(await hiddb.delete_database("u92cccov5tsg14tq2l"))
    # print(await hiddb.get_instances())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())
