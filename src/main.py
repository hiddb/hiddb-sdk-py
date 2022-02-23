import requests
import jwt

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
        
        # self._decoded = jwt.decode(access_token, algorithms=["RS256"])


if __name__ == '__main__':
    hiddb = HIDDB()
    state = State(hiddb)
    state.access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRRZzJmd09YMUZ2ZFRyR2szRm9fVEd1VE14dUR0clBHNTdlTU1rYWhIUWMifQ.eyJzdWIiOiIyYWhodXh3aDBzbDFmb3V5NnEiLCJhbXIiOlsicmVmcmVzaF90b2tlbiJdLCJzY29wZSI6IiIsImVtYWlsIjoiYi5ib2xicmlua2VyQGdteC5kZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicm9sZSI6ImFkbWluIiwicGxhbiI6ImZyZWUiLCJvcmdhbml6YXRpb24iOiI0YW1odXh3aDBzbDFmb3V5NnEiLCJpYXQiOjE2NDUyMDA5ODEsImV4cCI6MTY0NTIwMjE4MX0.X8Tmf0Np--uj-Z-E8_QEVsmKDw2qtFFjesuhmIe5zpIP83UYF7cTHWstkcMPmyZNvGQd4F0nKVIWb8phGccMlw"