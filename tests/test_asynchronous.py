from hiddb.asynchronous import HIDDB
import pytest

@pytest.mark.asyncio
async def test_asynchronous():
    hiddb = await HIDDB.create('XXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXX')

    database_id = "ojzlyjbxwqgscqluue"
    instance_id = "brslsjpvwrgucrlrxi"
    collection_name = "collection_name"
    field_name = "field_name"
    document_id = "document_id"

    await hiddb.create_database(database_id)
    await hiddb.list_databases()
    await hiddb.get_database(database_id)
    await hiddb.delete_database(database_id)

    await hiddb.create_instance(database_id, "xs", 10)
    await hiddb.get_instances()
    await hiddb.get_instance(instance_id)
    await hiddb.delete_instance(instance_id)

    await hiddb.create_collection(database_id, collection_name)
    await hiddb.list_collections(database_id)
    await hiddb.get_collection(database_id, collection_name)
    await hiddb.delete_collection(database_id, collection_name)

    await hiddb.create_index(database_id, collection_name, field_name, 10)
    await hiddb.list_indices(database_id, collection_name)
    await hiddb.get_index(database_id, collection_name, field_name)
    await hiddb.delete_index(database_id, collection_name, field_name)

    await hiddb.insert_document(database_id, collection_name, [{"id": document_id, field_name: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}], request_compression=False)
    await hiddb.search_nearest_documents(database_id, collection_name, field_name, vectors=[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], request_compression=False)
    await hiddb.search_nearest_documents(database_id, collection_name, field_name, ids=[document_id], request_compression=False)

    await hiddb.insert_document(database_id, collection_name, [{"id": document_id, field_name: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}], request_compression=True)
    await hiddb.search_nearest_documents(database_id, collection_name, field_name, vectors=[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], request_compression=True)
    await hiddb.search_nearest_documents(database_id, collection_name, field_name, ids=[document_id], request_compression=True)

    await hiddb.get_document(database_id, collection_name, document_id)
    await hiddb.delete_document(database_id, collection_name, document_id)