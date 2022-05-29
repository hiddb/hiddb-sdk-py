from dataclasses import dataclass
import asyncio
import aiohttp
import time
import jwt


async def set_timeout(seconds, callback, args=None):
    await asyncio.sleep(seconds)
    await callback(*args) if args else await callback()

secure = True
domain = 'hiddb.io'

protocol = 'https' if secure else 'http'
baseDbUrl = f'{protocol}://api.{domain}'
postHeaders = {'Content-Type': 'application/json'}


@dataclass
class BaseRequest:
    path: str
    method: str
    url: str
    body: dict = None


@dataclass
class StdRequest(BaseRequest):
    url: str = baseDbUrl
    body: dict = None


class HIDDB:
    state = None

    @classmethod
    async def create(cls, key, secret):
        self = HIDDB()
        self.state = State(self, key, secret)

        await self._machine_login(key, secret)
        return self

    async def _machine_login(self, key: str, secret: str):
        body = {
            "access_key": key,
            "secret_key": secret
        }
        request_data = StdRequest(path=f"/machine/login", method="post", body=body)
        await self.make_request(request_data)

    async def create_database(self, name: str):
        body = {
            "database_name": name,
        }
        request_data = StdRequest(path=f"/database", method="post", body=body)
        await self.make_request(request_data)

    async def list_databases(self):
        request_data = StdRequest(path=f"/database", method="get")
        await self.make_request(request_data)

    async def get_database(self, id: str):
        request_data = StdRequest(path=f"/database/{id}", method="get")
        await self.make_request(request_data)

    async def delete_database(self, id: str):
        request_data = StdRequest(path=f"/database/{id}", method="delete")
        await self.make_request(request_data)

    async def create_instance(self, database_id: str, type: str, volume_size: str):
        body = {"database_id": database_id,
                "type": type,
                "volume_size": volume_size
                }
        request_data = StdRequest(path=f"/instance", method="post", body=body)
        await self.make_request(request_data)

    async def get_instances(self):
        request_data = StdRequest(path=f"/instance", method="get")
        await self.make_request(request_data)

    async def get_instance(self, id: str):
        request_data = StdRequest(path=f"/instance/{id}", method="get")
        await self.make_request(request_data)

    async def delete_instance(self, id: str):
        request_data = StdRequest(path=f"/instance/{id}", method="delete")
        await self.make_request(request_data)

    async def create_collection(self, database_id: str, collection_name: str):
        url = f"{protocol}://{database_id}.{domain}"
        body = {"collection_name": collection_name}
        request_data = BaseRequest(url=url, path=f"/collection", method="post", body=body)
        await self.make_request(request_data)

    async def list_collections(self, database_id: str):
        url = f"{protocol}://{database_id}.{domain}"
        request_data = BaseRequest(url=url, path=f"/collection", method="get")
        await self.make_request(request_data)

    async def get_collection(self, database_id: str, collection_name: str):
        url = f"{protocol}://{database_id}.{domain}"
        request_data = BaseRequest(url=url, path=f"/collection/{collection_name}", method="get")
        await self.make_request(request_data)

    async def delete_collection(self, database_id: str, collection_name: str):
        url = f"{protocol}://{database_id}.{domain}"
        request_data = BaseRequest(url=url, path=f"/collection/{collection_name}", method="delete")
        await self.make_request(request_data)

    async def create_index(self, database_id: str, collection_name: str, index_name: str, dimension: int):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/index"
        body = {
            "field_name": index_name,
            "dimension": dimension,
        }
        request_data = BaseRequest(url=url, path=path, method="post", body=body)
        await self.make_request(request_data)

    async def list_indices(self, database_id: str, collection_name: str):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/index"
        request_data = BaseRequest(url=url, path=path, method="get")
        await self.make_request(request_data)

    async def get_index(self, database_id: str, collection_name: str, index_name: str):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/index/{index_name}"
        request_data = BaseRequest(url=url, path=path, method="get")
        await self.make_request(request_data)

    async def delete_index(self, database_id: str, collection_name: str, index_name: str):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/index/{index_name}"
        request_data = BaseRequest(url=url, path=path, method="delete")
        await self.make_request(request_data)

    async def insert_document(self, database_id: str, collection_name: str, documents: dict):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/document"
        body = {"documents": documents}
        request_data = BaseRequest(url=url, path=path, method="post", body=body)
        await self.make_request(request_data)

    async def search_nearest_documents(self, database_id: str, collection_name: str, index_name: str,
                                       vectors=None, ids=None, max_neighbors=10):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/document/search"
        body = {
            "field_name": index_name,
            "max_neighbors": max_neighbors
        }
        if vectors:
            body["vectors"] = vectors
        elif ids:  # elif or if?
            body["ids"] = ids
        else:
            # what here ?
            pass
        request_data = BaseRequest(url=url, path=path, method="post", body=body)
        await self.make_request(request_data)

    async def get_document(self, database_id: str, collection_name: str, document_id: str):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/document/{document_id}"
        request_data = BaseRequest(url=url, path=path, method="get")
        await self.make_request(request_data)

    async def delete_document(self, database_id: str, collection_name: str, document_id: str):
        url = f"{protocol}://{database_id}.{domain}"
        path = f"/collection/{collection_name}/document/{document_id}"
        request_data = BaseRequest(url=url, path=path, method="delete")
        await self.make_request(request_data)

    async def make_request(self, request_data: BaseRequest):
        async with aiohttp.ClientSession(request_data.url) as session:
            req = getattr(session, request_data.method)
            session.headers.update({'Authorization': f'Bearer {self.state.access_token}'})
            post_headers_aux = postHeaders if request_data.body else postHeaders
            async with req(request_data.path, json=request_data.body, headers=post_headers_aux) as resp:
                if resp.status != 200:
                    raise Exception(f"Status code {resp.status}: {await resp.text()}")
                return await resp.json()


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
