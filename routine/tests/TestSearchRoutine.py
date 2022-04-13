from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestSearchRoutine

class TestSearchRoutine(TokenHeaderTest):
    ###############################################
    # protected values
    _url, _method = "/api/routine/", "GET"

    ###############################################
    # public functions
    def setUp(self) -> None:
        super().setUp()

        data = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : "test2",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        response = self.client.post("/api/routine/", data, "application/json", **self.header)
        self.routine_id = response.json()['data']['routine_id']

    ###############################################
    # test functions
    # 정상적으로 왔을때
    def test_logout_clean(self):
        self._url += '?routine_id={}'.format( self.routine_id )
        self._request_200({})
    
    # 빈 값이 들어간 경우
    def test_empty(self):
        self._request_400({})
    
    # 값이 안 들어간 경우
    def test_empty_value(self):
        self._url += '?routine_id='
        self._request_400({})
    
    # 값이 이상하게 들어간 경우
    def test_invaild_value(self):
        self._url += '?routine_id=test'
        self._request_400({})
    
    # 키값이 이상하게 들어간 경우
    def test_invaild_key(self):
        self._url += '?id={}'.format( self.routine_id )
        self._request_400({})