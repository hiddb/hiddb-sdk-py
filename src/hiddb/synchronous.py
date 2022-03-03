import asyncio
import hiddb.asynchronous

def sync(async_func):
    return asyncio.get_event_loop().run_until_complete(async_func)

class HIDDB:
    def __init__(self, key: str, secret: str):
        self.hiddb = sync(hiddb.asynchronous.HIDDB.create(key, secret))

    def create_database(self, name: str):
        return sync(self.hiddb.create_database(name))

    def list_databases(self):
        return sync(self.hiddb.list_databases())

    def get_database(self, id: str):
        return sync(self.hiddb.get_database(id))

    def delete_database(self, id: str):
        return sync(self.hiddb.delete_database(id))

    def create_instance(self, database_id: str, type: str, volume_size: str):
        return sync(self.hiddb.create_instance(database_id, type, volume_size))

    def get_instances(self):
        return sync(self.hiddb.get_instances())

    def get_instance(self, id: str):
        return sync(self.hiddb.get_instance(id))

    def delete_instance(self, id: str):
        return sync(self.hiddb.delete_instance(id))

    def create_collection(self, database_id: str, name: str):
        return sync(self.hiddb.create_collection(database_id, name))

    def list_collections(self, database_id: str):
        return sync(self.hiddb.list_collections(database_id))

    def get_collection(self, database_id: str, name: str):
        return sync(self.hiddb.get_collection(database_id, name))

    def delete_collection(self, database_id: str, name: str):
        return sync(self.hiddb.delete_collectoin(database_id, name))

    def create_index(self, database_id: str, collection: str, field: str, dimension: int):
        return sync(self.hiddb.create_index(database_id, collection, field, dimension))

    def list_indices(self, database_id: str, collection: str):
        return sync(self.hiddb.list_indices(database_id, collection))

    def get_index(self, database_id: str, collection: str, name: str):
        return sync(self.hiddb.get_index(database_id, collection, name))
    
    def delete_index(self, database_id: str, collection: str, name: str):
        return sync(self.hiddb.delete_index(database_id, collection, name))

    def insert_document(self, database_id: str, collection: str, document: dict):
        return sync(self.hiddb.insert_document(database_id, collection, document))

    def search_nearest_documents(self, database_id: str, collection: str, field: str, vector, max_neighbors=10):
        return sync(self.hiddb.search_nearest_documents(database_id, collection, field, vector, max_neighbors))

    def get_document(self, database_id: str, collection: str, id: str):
        return sync(self.hiddb.get_document(database_id, collection, id))

    def delete_document(self, database_id: str, collection: str, id: str):
        return sync(self.hiddb.delete_document(database_id, collection, id))
