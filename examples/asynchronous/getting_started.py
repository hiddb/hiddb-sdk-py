from hiddb.asynchronous import HIDDB
import asyncio

async def main():
    hiddb = await HIDDB.create("<key>", "<secret>")

    # Create a database via dashboard and insert the database_id here
    database_id = "<database_id>"

    # Create a collection named "wordvectors"
    await hiddb.create_collection(database_id=database_id, collection_name="wordvectors")

    # Create an index in that collection
    await hiddb.create_index(
        database_id=database_id,
        collection_name='wordvectors',
        index_name="word-vector",
        dimension=300
    )

    # Insert a document which is indexed
    await hiddb.insert_document(
        database_id=database_id,
        collection_name='wordvectors',
        documents=[{
            "id": "test-document",
            "word-vector": [42.0]*300
        }]
    )

    # Search for nearest documents
    await hiddb.search_nearest_documents(
        database_id=database_id,
        collection_name='wordvectors',
        index_name="word-vector",
        vectors=[[43.0]*300]
    )

    # Delete collection and corresponding indices
    await hiddb.delete_collection(database_id=database_id, collection_name="wordvectors")

if __name__ == '__main__':
    asyncio.run(main())