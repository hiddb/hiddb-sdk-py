import requests
import jwt

base = "https://api.hiddb.io/"


class HIDDB:
    def __init__(self):
        self.state = State(self)
        pass

    def userRegister(self, email, password):
        self.email = email
        self.password = password

        data = {
            "email": self.email,
            "password": self.password,
        }

        header = {"Content-Type": "application/json"}

        resp = requests.post(f"{base}user/register", headers=header, json=data)
        return resp.text

    def userUpdateVerify(self, userId, otpId):
        self.userId = userId
        self.otpId = otpId

        data = {
            "user_id": self.userId,
            "otp_id": self.otpId,
        }

        header = {"Content-Type": "application/json"}

        resp = requests.post(f"{base}user/update/verify", headers=header, json=data)
        return resp.text

    def userResetPassword(self, email):
        self.email = email

        data = {
            "email": self.email,
        }

        header = {"Content-Type": "application/json"}

        resp = requests.post(f"{base}user/reset", headers=header, json=data)
        return resp.text

    def userUpdateResetPassword(self, userId, otpId, password):
        self.userId = userId
        self.otpId = otpId
        self.password = password

        data = {"user_id": self.userId, "otp_id": self.otpId, "password": password}

        header = {"Content-Type": "application/json"}

        resp = requests.post(f"{base}user/update/reset", headers=header, json=data)
        return resp.text

    def userLogin(self, email, password):
        self.email = email
        self.password = password

        data = {
            "email": self.email,
            "password": self.password,
        }

        header = {"Content-Type": "application/json"}

        resp = requests.post(f"{base}user/login", headers=header, json=data)
        self.state.accessToken = resp.text

        return resp.text

    def userRefresh(self):

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.state.accessToken}",
        }

        resp = requests.post(f"{base}user/refresh", headers=header)
        self.state.accessToken = resp.text
        return resp.text

    def machineLogin(self, key, secret):
        self.key = key
        self.secret = secret

        data = {
            "key": self.key,
            "secret": self.secret,
        }

        header = {"Content-Type": "application/json"}

        resp = requests.post(f"{base}machine/login", headers=header, json=data)
        return resp.text

    def createMachineAccount(self, permission):
        encoded_jwt = self.state.accessToken
        data = jwt.decode(
            encoded_jwt, options={"verify_signature": False}, algorithms=["RS256"]
        )
        self.organizationId = str(data["organization"])
        self.permission = permission

        data = {
            "permission": self.permission,
        }
        l1 = ["read", "write"]
        if data["permission"] in l1:
            header = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.state.accessToken}",
            }
            resp = requests.post(
                f"{base}organization/{self.organizationId}/machine",
                headers=header,
                json=data,
            )

            return resp.text
        else:
            return "request.body.permission should be equal to one of the allowed values:read,write"

    def deleteMachineAccount(self, organizationId):
        self.organizationId = organizationId

        resp = requests.delete(f"{base}organization/{organizationId}/machine")
        return resp.text

    def createDatabase(self, name):
        self.name = name
        data = {
            "database_name": self.name,
        }
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.state.accessToken}",
        }
        resp = requests.post(f"{base}database", headers=header, json=data)
        return resp.text

    def listDatabases(self):
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"{base}database", headers=header)

        return resp.text

    def getDatabase(self, id):
        self.id = id
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"{base}database/{self.id}", headers=header)

        return resp.text

    def deleteDatabase(self, id):
        self.id = id
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.delete(f"{base}database/{self.id}", headers=header)

        # dispatchEvent
        return resp.text

    def createInstance(self, id, volume_size, type):
        self.id = id
        self.volume_size = volume_size
        self.type = type

        data = {
            "database_id": self.id,
            "volume_size": self.volume_size,
            "type": self.type,
        }

        l1 = ["free", "s", "m", "l"]
        if data["type"] in l1:
            header = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.state.accessToken}",
            }

            # dispatchEvent
            resp = requests.post(f"{base}instance", headers=header, json=data)

            return resp.text
        else:
            return "request.body.type should be equal to one of the allowed values: free, s, m, l"

    def listInstances(self):
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"{base}instance", headers=header)

        return resp.text

    def getInstance(self, id):
        self.id = id
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"{base}instance/{self.id}", headers=header)

        return resp.text

    def deleteInstance(self, id):
        self.id = id
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.delete(f"{base}instance/{self.id}", headers=header)

        # dispatchEvent
        return resp.text

    def createCollection(self, databaseId, name):
        self.name = name

        data = {
            "collection_id": self.name,
        }

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.state.accessToken}",
        }

        # dispatchEvent
        resp = requests.post(
            f"https://{databaseId}.hiddb.io/collection", headers=header, json=data
        )
        return resp.text

    def listCollections(self, databaseId):
        path = f"/collection"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"https://{databaseId}.hiddb.io{path}", headers=header)
        return resp.text

    def getCollection(self, databaseId, name):
        self.name = name
        path = f"/collection/{self.name}"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"https://{databaseId}.hiddb.io{path}", headers=header)
        return resp.text

    def deleteCollection(self, databaseId, name):
        self.name = name
        path = f"/collection/{self.name}"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.delete(f"https://{databaseId}.hiddb.io{path}", headers=header)
        # dispatchEvent
        return resp.text

    def createIndex(self, databaseId, field_name, dimension, collection_id):
        self.field_id = field_name
        self.dimension = dimension
        path = f"/collection/{collection_id}/index"

        data = {"field_id": self.field_id, "dimension": self.dimension}

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.state.accessToken}",
        }

        # dispatchEvent
        resp = requests.post(
            f"https://{databaseId}.hiddb.io{path}", headers=header, json=data
        )
        return resp.text

    def listIndices(self, databaseId, collection_id):
        path = f"/collection/{collection_id}/index"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"https://{databaseId}.hiddb.io{path}", headers=header)
        return resp.text

    def getIndex(self, databaseId, name, collection_id):
        self.databaseId = databaseId
        self.name = name
        path = f"/collection/{collection_id}/index/{name}"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"https://{databaseId}.hiddb.io{path}", headers=header)
        return resp.text

    def deleteIndex(self, databaseId, name, collection_id):
        self.databaseId = databaseId
        self.name = name
        path = f"/collection/{collection_id}/index/{name}"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.delete(
            f"https://{databaseId}.hiddb.io{path}/index", headers=header
        )
        # dispatchEvent
        return resp.text

    def insertDocument(self, databaseId, document, collection_id):

        path = f"/collection/{collection_id}/document"

        data = {"documents": [document]}

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.state.accessToken}",
        }

        # dispatchEvent
        resp = requests.post(
            f"https://{databaseId}.hiddb.io{path}", headers=header, json=data
        )
        return resp.text

    def searchNearestDocuments(self, databaseId, collection_id):
        path = f"/collection/{collection_id}/document/search"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"https://{databaseId}.hiddb.io{path}", headers=header)
        return resp.text

    def getDocument(self, databaseId, name, collection_id):

        path = f"/collection/{collection_id}/document/{id}"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.get(f"https://{databaseId}.hiddb.io{path}", headers=header)
        return resp.text

    def deleteDocument(self, databaseId, name, collection_id):

        path = f"/collection/{collection_id}/index/${name}"
        header = {"Authorization": f"Bearer {self.state.accessToken}"}
        resp = requests.delete(
            f"https://${databaseId}.hiddb.io${path}/index", headers=header
        )
        # dispatchEvent
        return resp.text


class State:
    def __init__(self, hiddb: HIDDB):
        self.hiddb = hiddb
        self._accessToken = None
        self._decoded = None
        self._refresh = None

    @property
    def access_token(self):
        return self._accessToken

    @access_token.setter
    def access_token(self, access_token):
        if not access_token:
            self.accessToken = access_token
            return


if __name__ == "__main__":
    hiddb = HIDDB()
    state = State(hiddb)
    state.access_token = ""
