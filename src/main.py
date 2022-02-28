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

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(f"{base}user/register", headers=header, json=data)
        return resp

    def userUpdateVerify(self, userId, otpId):
        self.userId = userId
        self.otpId = otpId

        data = {
            "user_id": self.userId,
            "otp_id": self.otpId,
        }

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(f"{base}user/update/verify",
                             headers=header, json=data)
        return resp

    def userResetPassword(self, email):
        self.email = email

        data = {
            "email": self.email,
        }

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(f"{base}user/reset",
                             headers=header, json=data)
        return resp

    def userUpdateResetPassword(self, userId, otpId, password):
        self.userId = userId
        self.otpId = otpId
        self.password = password

        data = {
            "user_id": self.userId,
            "otp_id": self.otpId,
            "password": password
        }

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(f"{base}user/update/reset",
                             headers=header, json=data)
        return resp

    def userLogin(self, email, password):
        self.email = email
        self.password = password

        data = {
            "email": self.email,
            "password": self.password,
        }

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(f"{base}user/login", headers=header, json=data)
        self.state.access_token = resp.text
        print(resp.text)
        return

    def userRefresh(self):
        resp = requests.post(f"{base}user/refresh")
        self.state.access_token = resp.text
        return

    def machineLogin(self, key, secret):
        self.key = key
        self.secret = secret

        data = {
            "key": self.key,
            "secret": self.secret,
        }

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(f"{base}machine/login", headers=header, json=data)
        self.state.access_token = resp.text
        return

    # TODO : take 2 values in permission parameter
    def createMachineAccount(self, organizationId, permission):
        self.organizationId = organizationId
        self.permission = permission

        data = {
            "permission": self.permission,
        }

        header = {
            "Content-Type": "application/json"
        }

        resp = requests.post(
            f"{base}organization/{self.organizationId}/machine", headers=header, json=data)
        return resp

    def deleteMachineAccount(self, organizationId):
        self.organizationId = organizationId

        resp = requests.delete(f"{base}organization/{organizationId}/machine")
        return resp

    def createDatabase(self, name):
        self.name = name

        data = {
            "database_name": self.name,
        }
        header = {
            "Content-Type": "application/json"
        }
        resp = requests.post(f"{base}database", headers=header, json=data)

        # dispatchEvent
        return resp

    def listDatabases(self):
        resp = requests.get(f"{base}database")
        return resp

    def getDatabase(self, id):
        self.id = id
        resp = requests.get(f"{base}database{self.id}")
        return resp

    def deleteDatabase(self, id):
        self.id = id
        resp = requests.delete(f"{base}database{self.id}")

        # dispatchEvent
        return resp

    def createInstance(self, id, volume_size, type):
        self.id = id
        self.volume_size = volume_size
        self.type = type

        data = {
            "database_id": self.id,
            "volume_size": self.volume_size,
            "type": self.type
        }

        header = {
            "Content-Type": "application/json"
        }

        # dispatchEvent
        resp = requests.post(f"{base}instance", headers=header, json=data)
        return resp

    def listInstances(self):
        resp = requests.get(f"{base}instance")
        return resp

    def getInstance(self, id):
        self.id = id
        resp = requests.get(f"{base}instance{self.id}")
        return resp

    def deleteInstance(self, id):
        self.id = id
        resp = requests.delete(f"{base}instance{self.id}")

        # dispatchEvent
        return resp

    #TODO : Still working on this

    # def createCollection(self, databaseId, name):
    #     self.databaseId = databaseId
    #     self.name = name

    #     data = {
    #         "collection_id": self.name,
    #     }

    #     header = {
    #         "Content-Type": "application/json"
    #     }

    #     # dispatchEvent
    #     resp = requests.post(f"https://{self.databaseId}.hiddb.io/collection", headers=header, json=data)
    #     return resp

    # def listCollections(self, databaseId):
    #     self.databaseId = databaseId
    #     path = f'/collection'
    #     resp = requests.get(f"https://{self.databaseId}.hiddb.io{path}")
    #     return resp

    # def getCollection(self, databaseId, name):
    #     self.databaseId = databaseId
    #     self.name = name
    #     path = f'/collection/{self.name}'
    #     resp = requests.get(f"https://{self.databaseId}.hiddb.io{path}")
    #     return resp

    # def deleteCollection(self, databaseId, name):
    #     self.databaseId = databaseId
    #     self.name = name
    #     path = f'/collection/{self.name}'
    #     resp = requests.delete(f"https://{self.databaseId}.hiddb.io{path}")
    #     # dispatchEvent
    #     return resp

    # def createIndex(self, databaseId, field_name, dimension):
    #     self.field_id = field_name
    #     self.dimension = dimension
    #     path = "/collection/{collection_id}/index"

    #     data = {
    #         "field_id": self.field_id,
    #         "dimension": self.dimension
    #     }

    #     header = {
    #         "Content-Type": "application/json"
    #     }

    #     # dispatchEvent
    #     resp = requests.post(
    #         f"https://${self.databaseId}.hiddb.io${path}", headers=header, json=data)
    #     return resp

    # def listIndices(self, databaseId):
    #     self.databaseId = databaseId
    #     path = "/collection/{collection_id}/index"
    #     resp = requests.get(f"https://{self.databaseId}.hiddb.io{path}")
    #     return resp

    # def getIndex(self, databaseId, name):
    #     self.databaseId = databaseId
    #     self.name = name
    #     path = f'/collection/{collection_id}/index/{name}'
    #     resp = requests.get(f"https://{self.databaseId}.hiddb.io{path}")
    #     return resp

    # def deleteIndex(self, databaseId, name):
    #     self.databaseId = databaseId
    #     self.name = name
    #     path = f'/collection/{collection_id}/index/${name}'
    #     resp = requests.delete(f"https://${self.databaseId}.hiddb.io${path}/index")
    #     # dispatchEvent
    #     return resp


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

        # self._decoded = jwt.decode(access_token, algorithms=["RS256"])


if __name__ == '__main__':
    hiddb = HIDDB()
    state = State(hiddb)
    state.access_token = ""

# obj = HIDDB()
# # obj.userRegister("demo5@gmail.com","demo1234")
# obj.userLogin("demo5@gmail.com","demo1234")
# # obj.createDatabase("database")
