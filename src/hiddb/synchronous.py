
from dataclasses import dataclass
import time
import jwt
import asyncio

import json
import zlib

from requests import Session
from urllib.parse import urljoin

from hiddb import config


async def set_timeout(seconds, callback, args=None):
    await asyncio.sleep(seconds)
    await callback(*args) if args else await callback()


class APIClient(Session):
    def __init__(self, prefix_url=None, *args, **kwargs):
        super(APIClient, self).__init__(*args, **kwargs)
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(APIClient, self).request(method, url, *args, **kwargs)

@dataclass
class BaseRequest:
    path: str
    method: str
    url: str
    body: dict = None


@dataclass
class StdRequest(BaseRequest):
    url: str = config.baseDbUrl
    body: dict = None


class HIDDB:
    state = None
    def __init__(self, key, secret):
        self.state = State(self, key, secret)
        self._machine_login(key, secret)

    def _machine_login(self, key: str, secret: str):
        body = {
            "access_key": key,
            "secret_key": secret
        }
        request_data = StdRequest(path=f"/machine/login", method="post", body=body)
        self.make_request(request_data)

    def create_database(self, name: str):
        body = {
            "database_name": name,
        }
        request_data = StdRequest(path=f"/database", method="post", body=body)
        self.make_request(request_data)

    def list_databases(self):
        request_data = StdRequest(path=f"/database", method="get")
        self.make_request(request_data)

    def get_database(self, id: str):
        request_data = StdRequest(path=f"/database/{id}", method="get")
        self.make_request(request_data)

    def delete_database(self, id: str):
        request_data = StdRequest(path=f"/database/{id}", method="delete")
        self.make_request(request_data)

    def create_instance(self, database_id: str, type: str, volume_size: str):
        body = {
            "database_id": database_id,
            "type": type,
            "volume_size": volume_size
        }
        request_data = StdRequest(path=f"/instance", method="post", body=body)
        self.make_request(request_data)

    def get_instances(self):
        request_data = StdRequest(path=f"/instance", method="get")
        self.make_request(request_data)

    def get_instance(self, id: str):
        request_data = StdRequest(path=f"/instance/{id}", method="get")
        self.make_request(request_data)

    def delete_instance(self, id: str):
        request_data = StdRequest(path=f"/instance/{id}", method="delete")
        self.make_request(request_data)

    def create_collection(self, database_id: str, collection_name: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        body = {
            "collection_name": collection_name
        }
        request_data = BaseRequest(url=url, path=f"/collection", method="post", body=body)
        self.make_request(request_data)

    def list_collections(self, database_id: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        request_data = BaseRequest(url=url, path=f"/collection", method="get")
        self.make_request(request_data)

    def get_collection(self, database_id: str, collection_name: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        request_data = BaseRequest(url=url, path=f"/collection/{collection_name}", method="get")
        self.make_request(request_data)

    def delete_collection(self, database_id: str, collection_name: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        request_data = BaseRequest(url=url, path=f"/collection/{collection_name}", method="delete")
        self.make_request(request_data)

    def create_index(self, database_id: str, collection_name: str, index_name: str, dimension: int):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/index"
        body = {
            "field_name": index_name,
            "dimension": dimension,
        }
        request_data = BaseRequest(url=url, path=path, method="post", body=body)
        self.make_request(request_data)

    def list_indices(self, database_id: str, collection_name: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/index"
        request_data = BaseRequest(url=url, path=path, method="get")
        self.make_request(request_data)

    def get_index(self, database_id: str, collection_name: str, index_name: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/index/{index_name}"
        request_data = BaseRequest(url=url, path=path, method="get")
        self.make_request(request_data)

    def delete_index(self, database_id: str, collection_name: str, index_name: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/index/{index_name}"
        request_data = BaseRequest(url=url, path=path, method="delete")
        self.make_request(request_data)

    def insert_document(self, database_id: str, collection_name: str, documents: list, request_compression=True):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/document"
        body = {
            "documents": documents
        }
        request_data = BaseRequest(url=url, path=path, method="post", body=body)
        self.make_request(request_data, request_compression=request_compression)

    def search_nearest_documents(self, database_id: str, collection_name: str, index_name: str,
                                       vectors=None, ids=None, max_neighbors=10, request_compression=True):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/document/search"
        body = {
            "field_name": index_name,
            "max_neighbors": max_neighbors
        }
        if vectors:
            body["vectors"] = vectors
        elif ids:
            body["ids"] = ids
        elif (vectors and ids) or not (vectors and ids):
            raise Exception("Provide either 'vectors' or 'ids'.")

        request_data = BaseRequest(url=url, path=path, method="post", body=body)
        self.make_request(request_data, request_compression=request_compression)

    def get_document(self, database_id: str, collection_name: str, document_id: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/document/{document_id}"
        request_data = BaseRequest(url=url, path=path, method="get")
        self.make_request(request_data)

    def delete_document(self, database_id: str, collection_name: str, document_id: str):
        url = f"{config.protocol}://{database_id}.{config.domain}"
        path = f"/collection/{collection_name}/document/{document_id}"
        request_data = BaseRequest(url=url, path=path, method="delete")
        self.make_request(request_data)

    def make_request(self, request_data: BaseRequest, request_compression=False):
        if request_compression:
            # data = zlib.compress(json.dumps(request_data.body).encode('utf-8'))
            with APIClient(request_data.url) as client:
                data = zlib.compress(json.dumps(request_data.body).encode('utf-8'))
                resp = getattr(client, request_data.method)(request_data.path, data=data, headers={
                    'Authorization': f'Bearer {self.state.access_token}',
                    **({'Content-Type': 'application/octet-stream', 'Content-Encoding': 'deflate'} if request_data.body else {})
                })
        else: 
            with APIClient(request_data.url) as client:
                data = json.dumps(request_data.body)
                resp = getattr(client, request_data.method)(request_data.path, data=data, headers={
                    'Authorization': f'Bearer {self.state.access_token}',
                    **({'Content-Type': 'application/json'} if request_data.body else {})
                })

        if resp.status_code != 200 and resp.status_code != 202:
            raise Exception(f"Status code {resp.status_code}: {resp.text}")
        try:
            return resp.json()
        except:
            return resp.text

class State:
    def __init__(self, hiddb: HIDDB, key: str, secret: str):
        self.hiddb = hiddb
        self._access_token = None
        self._decoded = None
        self._refresh = None
        self._key = key
        self._secret = secret
    
    @property
    def access_token(self):
        return self._access_token
    
    @access_token.setter
    def access_token(self, access_token):
        if not access_token:
            self._access_token = access_token
            return
        self._decoded = jwt.decode(access_token, options={"verify_signature": False})

        self._access_token = access_token

        if self._refresh:
            self._refresh.cancel()
        if 'exp' in self._decoded:
            self._refresh = asyncio.ensure_future(set_timeout(self._decoded['exp'] - time.time() - 60,
                                                              self.hiddb._machine_login, (self._key, self._secret)))
