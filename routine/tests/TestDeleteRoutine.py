from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestDeleteRoutine

class TestDeleteRoutine(TokenHeaderTest):
    ###############################################
    # protected values
    _url, _method = "/api/routine/", "DELETE"

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
    def test_clean_data(self):
        body = { "routine_id" : self.routine_id }
        self._request_200(body)
    
    # key값이 빠진 경우
    def test_invalid_key(self):
        body = {  }
        self._request_400(body)
    
    # 값이 현재 DB에 들어가 있지 않는 경우
    def test_invalid_db(self):
        body = { "routine_id" : self.routine_id + 1 }
        self._request_400(body)