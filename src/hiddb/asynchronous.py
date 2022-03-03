import jwt
import time

import asyncio
import aiohttp

async def set_timeout(seconds, callback, args=None):
    await asyncio.sleep(seconds)
    await callback(*args) if args else await callback()

baseUrl = 'https://api.hiddb.io'
postHeaders = { 'Content-Type' : 'application/json' }


class HIDDB(object):
    @classmethod
    async def create(cls, key, secret):
        self = HIDDB()
        self.state = State(self, key, secret)

        await self._machine_login(key, secret)
        return self


    async def _machine_login(self, key: str, secret: str):
        url = baseUrl
        path = f"/machine/login"
        method = "post"

        body = {
            "access_key": key,
            "secret_key": secret
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            async with req(path, json=body, headers=postHeaders) as resp:
                self.state.access_token = (await resp.json())['access_token']
                return self.state.access_token


    async def create_database(self, name: str):
        url = baseUrl
        path = f"/database"
        method = "post"

        body = {
            "database_name": name,
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path, json=body, headers=postHeaders) as resp:
                return await resp.text()


    async def list_databases(self):
        url = baseUrl
        path = f"/database"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.text()


    async def get_database(self, id: str):
        url = baseUrl
        path = f"/database/{id}"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()


    async def delete_database(self, id: str):
        url = baseUrl
        path = f"/database/{id}"
        method = "delete"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()

    async def create_instance(self, database_id: str, type: str, volume_size: str):
        url = baseUrl
        path = f"/instance"
        method = "post"

        body = {
            "database_id": database_id,
            "type": type,
            "volume_size": volume_size,
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path, json=body, headers=postHeaders) as resp:
                return await resp.json()

    async def get_instances(self):
        url = baseUrl
        path = f"/instance"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.text()


    async def get_instance(self, id: str):
        url = baseUrl
        path = f"/instance/{id}"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()


    async def delete_instance(self, id: str):
        url = baseUrl
        path = f"/instance/{id}"
        method = "delete"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()
    

    async def create_collection(self, database_id: str, name: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection"
        method = "post"

        body = {
            "collection_id": name,
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path, json=body, headers=postHeaders) as resp:
                return await resp.json()


    async def list_collections(self, database_id: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()


    async def get_collection(self, database_id: str, name: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{name}"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()
    

    async def delete_collection(self, database_id: str, name: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{name}"
        method = "delete"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()


    async def create_index(self, database_id: str, collection: str, field: str, dimension: int):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/index"
        method = "post"

        body = {
            "field_id": field,
            "dimension": dimension,
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path, json=body, headers=postHeaders) as resp:
                return await resp.json()


    async def list_indices(self, database_id: str, collection: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/index"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()


    async def get_index(self, database_id: str, collection: str, name: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/index/{name}"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()
    

    async def delete_index(self, database_id: str, collection: str, name: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/index/{name}"
        method = "delete"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()


    async def insert_document(self, database_id: str, collection: str, document: dict):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/document"
        method = "post"

        body = {
            "documents": [document],
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path, json=body, headers=postHeaders) as resp:
                return await resp.json()


    async def search_nearest_documents(self, database_id: str, collection: str, field: str, vector, max_neighbors=10):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/document/search"
        method = "post"

        body = {
            "vector": vector,
            "field": field,
            "max_neighbors": max_neighbors
        }

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path, json=body, headers=postHeaders) as resp:
                return await resp.json()


    async def get_document(self, database_id: str, collection: str, id: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/document/{id}"
        method = "get"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
                return await resp.json()
    

    async def delete_document(self, database_id: str, collection: str, id: str):
        url = f"https://{database_id}.hiddb.io"
        path = f"/collection/{collection}/document/{id}"
        method = "delete"

        async with aiohttp.ClientSession(url) as session:
            req = getattr(session, method)
            session.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})
            async with req(path) as resp:
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
        self._decoded =  jwt.decode(access_token, options={"verify_signature": False})

        self._access_token = access_token

        if self._refresh:
            self._refresh.cancel()

        self._refresh = asyncio.ensure_future(set_timeout(self._decoded['exp'] - time.time() - 60, self.hiddb._machine_login, (self._key, self._secret)))