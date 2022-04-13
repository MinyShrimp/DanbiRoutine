from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestUpdateRoutine

class TestUpdateRoutine(TokenHeaderTest):
    ###############################################
    # protected values
    _url, _method = "/api/routine/", "PUT"

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
        body = { 
            "routine_id" : self.routine_id,
            "title"      : "change_test",
            "category"   : "HOMEWORK",
            "goal"       : "test_clean_data",
            "is_alarm"   : False,
            "days"       : [ "MON" ]
        }
        self._request_200(body)
    
    # 빈 값이 들어간 경우
    def test_empty(self):
        body = {  }
        self._request_400(body)

    # 값이 현재 DB에 들어가 있지 않는 경우
    def test_invalid_db(self):
        body = { 
            "routine_id" : self.routine_id + 1,
            "title"      : "change_test",
            "category"   : "HOMEWORK",
            "goal"       : "test_invalid_db",
            "is_alarm"   : False,
            "days"       : [ "MON" ]
        }
        self._request_400(body)
    
    # 값 type이 int가 아닌 경우
    def test_invalid_value_type(self):
        body = { 
            "routine_id" : str( self.routine_id ),
            "title"      : "change_test",
            "category"   : "HOMEWORK",
            "goal"       : "test_invalid_db",
            "is_alarm"   : False,
            "days"       : [ "MON" ]
        }
        self._request_400(body)
    
    # key값이 빠진 경우
    def test_invalid_key(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "goal"       : "test_invalid_key",
            "is_alarm"   : True,
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( title이 str이 아닌 경우 )
    def test_invalid_value_title(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : ["test1"],
            "category"   : "HOMEWORK",
            "goal"       : "test_invalid_value_title",
            "is_alarm"   : True,
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( category가 str이 아닌 경우 )
    def test_invalid_value_category_type(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : ["HOMEWORK"],
            "goal"       : "test_invalid_value_category_type",
            "is_alarm"   : True,
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( category가 MIRACLE / HOMEWORK가 아닌 경우 )
    def test_invalid_value_category_value(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : "HOMEWORK1234",
            "goal"       : "test_invalid_value_category_value",
            "is_alarm"   : True,
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( goal이 str이 아닌 경우 )
    def test_invalid_value_goal(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : "HOMEWORK",
            "goal"       : ["test_invalid_value_goal"],
            "is_alarm"   : True,
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( is_alarm이 bool이 아닌 경우 )
    def test_invalid_value_isalarm(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : "HOMEWORK",
            "goal"       : "test_invalid_value_isalarm",
            "is_alarm"   : "True",
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( days가 list가 아닌 경우 )
    def test_invalid_value_days(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : "HOMEWORK",
            "goal"       : "test_invalid_value",
            "is_alarm"   : True,
            "days"       : "MON"
        }
        self._request_400(body)
    
    # key값에 sql string이 들어간 경우
    def test_sql_injection(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "\"OR 1=1 -",
            "category"   : "HOMEWORK",
            "goal"       : "test_sql_injection",
            "is_alarm"   : True,
            "days"       : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # days값에 MON ~ SUN 중 동일한 값이 2개 이상 들어간 경우
    def test_overlap_days(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : "HOMEWORK",
            "goal"       : "test_overlap_days",
            "is_alarm"   : True,
            "days"       : ["MON", "MON", "TUE"]
        }
        self._request_400(body)
    
    # days값에 MON ~ SUN 이 아닌 다른 문자가 들어간 경우
    def test_invalid_days(self):
        body = {
            "routine_id" : self.routine_id,
            "title"      : "test1",
            "category"   : "HOMEWORK",
            "goal"       : "test_invalid_days",
            "is_alarm"   : True,
            "days"       : ["@@@MON@@@"]
        }
        self._request_400(body)