from hiddb.synchronous import HIDDB


hiddb = HIDDB("<key>", "<secret>")

# Create a database via dashboard and insert the database_id here
database_id = "<database_id>"

# Create a collection named "wordvectors"
hiddb.create_collection(database_id=database_id, collection_name="wordvectors")

# Create an index in that collection
hiddb.create_index(
    database_id=database_id,
    collection_name='wordvectors',
    index_name="word-vector",
    dimension=300
)

# Insert a document which is indexed
hiddb.insert_document(
    database_id=database_id,
    collection_name='wordvectors',
    documents=[{
        "id": "test-document",
        "word-vector": [42.0]*300
    }]
)

# Search for nearest documents
hiddb.search_nearest_documents(
    database_id=database_id,
    collection_name='wordvectors',
    index_name="word-vector",
    vectors=[[43.0]*300]
)

# Delete collection and corresponding indices
hiddb.delete_collection(database_id=database_id, collection_name="wordvectors")