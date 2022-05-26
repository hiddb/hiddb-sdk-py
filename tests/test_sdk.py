from hiddb.synchronous import HIDDB


def test_sdk():
    hiddb = HIDDB('XXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXX')

    database_id = "ojzlyjbxwqgscqluue"
    instance_id = "brslsjpvwrgucrlrxi"
    collection_name = "collection_name"
    index_name = "index_name"
    document_id = "document_id"

    hiddb.create_database(database_id)
    hiddb.list_databases()
    hiddb.get_database(database_id)
    hiddb.delete_database(database_id)

    hiddb.create_instance(database_id, "xs", 10)
    hiddb.get_instances()
    hiddb.get_instance(instance_id)
    hiddb.delete_instance(instance_id)

    hiddb.create_collection(database_id, collection_name)
    hiddb.list_collections(database_id)
    hiddb.get_collection(database_id, collection_name)
    hiddb.delete_collection(database_id, collection_name)

    hiddb.create_index(database_id, collection_name, index_name, 10)
    hiddb.list_indices(database_id, collection_name)
    hiddb.get_index(database_id, collection_name, index_name)
    hiddb.delete_index(database_id, collection_name, index_name)

    hiddb.insert_document(database_id, collection_name, [{"id": document_id, index_name: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}])
    hiddb.search_nearest_documents(database_id, collection_name, index_name, vectors=[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])
    hiddb.search_nearest_documents(database_id, collection_name, index_name, ids=[document_id])
    hiddb.get_document(database_id, collection_name, document_id)
    hiddb.delete_document(database_id, collection_name, document_id)