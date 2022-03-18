# HIDDB Python SDK

The official SDK for the [HIDDB](https://hiddb.com) vector database.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the sdk.

```bash
pip install hiddb
```

## Usage

Create a collection within a database `<your database_id>`.

```python
from hiddb.synchronous import HIDDB

hiddb = HIDDB("<key>", "<secret>")

# Create a collection named 'wordvectors'
hiddb.create_collection(database_id="<your database_id>", collection_id="wordvectors")
```

Create an index within this collection:

```python
# Create an index on field 'vector' within the collection and dimension 300
hiddb.create_index(
    database_id="<your database_id>",
    collection_name='wordvectors',
    field_name="vector",
    dimension=300
)
```

Insert documents like that:

```python
document = {
    "vector": [0.0]*300,
    "id": "my first document"
}

hiddb.insert_document(
    database_id=database_id,
    collection_name='wordvectors',
    documents=[document]
)
```

Search for nearest documents:

```python
similar_words = hiddb.search_nearest_documents(
    database_id="<your database_id>",
    collection_name='wordvectors',
    field_name="vector",
    vectors=[[42.0]*300],
    max_neighbors=10
)
```

More examples are coming 🚀

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
