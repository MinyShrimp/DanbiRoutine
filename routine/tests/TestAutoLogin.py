from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestAutoLogin

class TestLogout(TokenHeaderTest):
    ###############################################
    # protected values
    _url = "/api/autologin/"

    ###############################################
    # test functions
    # 정상적으로 왔을때
    def test_clean_data(self):
        self._request_200({})