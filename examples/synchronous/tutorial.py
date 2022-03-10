from hiddb.synchronous import HIDDB

hiddb = HIDDB("<key>", "<secret>")

print(hiddb.list_databases())

# Create database
database = hiddb.create_database("testdb")

database_id = database.id

# Create instance and assign it to the database
instance = hiddb.create_instance(database_id=database_id, type="xs", volume_size=10)

## Wait until instance is created. This can take up to two minutes

# Create a collection named "wordvectors"
hiddb.create_collection(database_id=database_id, collection_name="wordvectors")

# Create an index in that collection
hiddb.create_index(
    database_id=database_id,
    collection_name='wordvectors',
    field_name="word-vector",
    dimension=300
)

# Insert a document which is indexed
hiddb.insert_document(
    database_id=database_id,
    collection_name='wordvectors',
    document={
        "id": "test-document",
        "word-vector": [1.0]*300
    }
)

# Search for nearest documents
hiddb.search_nearest_documents(
    database_id=database_id,
    collection_name='wordvectors',
    field_name="word-vector",
    vector=[2.0]*300
)

# Delete the database and the corresponing instances
hiddb.delete_database(database_id)