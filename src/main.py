import requests
import jwt
from threading import Timer
import time


class HIDDB:
    def __init__(self):
        self.state = State(self)
        self.appClient = requests.Session()
        self.dbClient = requests.Session()

        self.appClient.headers.update({'Content-Type' : 'application/json'})
        self.appClient.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})

        self.dbClient.headers.update({'Content-Type' : 'application/json'})
        self.dbClient.headers.update({'Authorization' : f'Bearer {self.state.access_token}'})

    def dispatch_event():
        pass

    def add_event_listener():
        pass

    def remove_event_listener():
        pass

    def is_authenticated():
        pass

    def logout():
        pass

    def user_register(email: str, password: str):
        

class State:
    def __init__(self, hiddb: HIDDB):
        self.hiddb = hiddb
        self._access_token = None
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
        self._decoded =  jwt.decode(access_token, options={"verify_signature": False})
        if not self._accessToken and access_token:
            # TODO: Dispatch login event
            pass  

        self._access_token = access_token

        if self._refresh:
            self._refresh.cancel()

        self._refresh = Timer(self._decoded.exp - time.time() - 60, self.hiddb.user_refresh)
        self._refresh.start()


if __name__ == '__main__':
    hiddb = HIDDB()
    state = State(hiddb)
    state.access_token = ""
