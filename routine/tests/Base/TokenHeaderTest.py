import json
from django.test import TestCase

class TokenHeaderTest(TestCase):
    ###############################################
    # protected values
    _url, _method = "", "POST"

    ###############################################
    # protected functions
    def _request(self, data):
        if self._method == "POST":
            return self.client.post(self._url, data, "application/json", **self.header)
        elif self._method == "GET":
            return self.client.get(self._url, **self.header)
        elif self._method == "PUT":
            return self.client.put(self._url, data, "application/json", **self.header)
        elif self._method == "DELETE":
            return self.client.delete(self._url, data, "application/json", **self.header)
        else:
            raise "METHOD ERROR"

    def _request_200(self, data):
        _data    = json.dumps( data, ensure_ascii="UTF-8" )
        response = self._request(_data)
        self.assertEqual(response.status_code, 200)
    
    def _request_400(self, data):
        _data    = json.dumps( data, ensure_ascii="UTF-8" )
        response = self._request(_data)
        self.assertEqual(response.status_code, 400)

    ###############################################
    # public functions
    def setUp(self) -> None:
        if self._url != '':
            data = { "email": "ksk7584@gmail.com", "pwd": "qwer1234!" }

            self.client.post('/api/signup/', data)
            response = self.client.post('/api/login/', data)

            self.header = { 'HTTP_TOKEN': response.json()['data']['access_token'] }
    
    ###############################################
    # test functions
    # def test_unvailed_token(self):
    #     if self._url != '':
    #         header = { 'HTTP_TOKEN': 'j.w.t' }
    #         response = self.client.post(self._url, {}, **header)
    #         self.assertEqual(response.status_code, 400)