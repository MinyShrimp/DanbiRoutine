from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestResultRoutine

class TestResultRoutine(TokenHeaderTest):
    ###############################################
    # protected values
    _url = "/api/result/"

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
        body = { 
            "routine_id" : self.routine_id,
            "result"     : "TRY"
        }
        self._request_200(body)
    
    # 빈 값이 들어간 경우
    def test_empty(self):
        body = {}
        self._request_400(body)
        
    # 값이 현재 DB에 들어가 있지 않는 경우
    def test_invalid_db(self):
        body = { 
            "routine_id" : self.routine_id + 1,
            "result"     : "TRY"
        }
        self._request_400(body)
    
    # key값이 빠진 경우
    def test_invalid_key_result(self):
        body = { 
            "routine_id" : self.routine_id
        }
        self._request_400(body)
    
    # key값이 빠진 경우
    def test_invalid_key_id(self):
        body = { 
            "result" : "TRY"
        }
        self._request_400(body)
    
    # key값이 이상한 경우
    def test_wrong_key_id(self):
        body = { 
            "id"     : self.routine_id,
            "result" : "TRY"
        }
        self._request_400(body)
    
    # 값 type이 int가 아닌 경우
    def test_invalid_value_type(self):
        body = { 
            "routine_id" : str( self.routine_id ),
            "result"     : "TRY"
        }
        self._request_400(body)

    # key값에 sql string이 들어간 경우
    def test_sql_injection(self):
        body = { 
            "routine_id" : self.routine_id,
            "result"     : "\"OR 1=1 -"
        }
        self._request_400(body)

    # result값에 NOT, TRY, DONE 이 아닌 다른 문자가 들어간 경우
    def test_invalid_result(self):
        body = { 
            "routine_id" : self.routine_id,
            "result"     : "DRAW"
        }
        self._request_400(body)