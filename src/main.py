import requests

class HIDDB:
    def __init__(self):
        self.state = State(self)
        pass

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
        

if __name__ == '__main__':
    hiddb = HIDDB()
    state = State(hiddb)
    state.access_token = ""
