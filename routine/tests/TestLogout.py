from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestLogout

class TestLogout(TokenHeaderTest):
    ###############################################
    # protected values
    _url = "/api/logout/"

    ###############################################
    # test functions
    # 정상적으로 왔을때
    def test_logout_clean(self):
        self._request_200({})