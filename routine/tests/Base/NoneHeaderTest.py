from django.test import TestCase

class NoneHeaderTest(TestCase):
    ###############################################
    # protected values
    _url = ""

    ###############################################
    # protected functions
    def _request_200(self, data):
        response = self.client.post(self._url, data)
        assert ( response.status_code == 200 )
    
    def _request_400(self, data):
        response = self.client.post(self._url, data)
        self.assertEqual(response.status_code, 400)