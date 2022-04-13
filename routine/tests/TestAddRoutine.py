from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestAddRoutine

class TestAddRoutine(TokenHeaderTest):
    ###############################################
    # protected values
    _url = "/api/routine/"

    ###############################################
    # test functions
    # 정상적으로 왔을때
    def test_clean_data(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : "test2",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_200(body)
    
    # key값이 빠진 경우
    def test_invalid_key(self):
        body = {
            "title"    : "test1",
            "goal"     : "test_invalid_key",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( title이 str이 아닌 경우 )
    def test_invalid_value_title(self):
        body = {
            "title"    : ["test1"],
            "category" : "HOMEWORK",
            "goal"     : "test_invalid_value_title",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( category가 str이 아닌 경우 )
    def test_invalid_value_category_type(self):
        body = {
            "title"    : "test1",
            "category" : ["HOMEWORK"],
            "goal"     : "test_invalid_value_category_type",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( category가 MIRACLE / HOMEWORK가 아닌 경우 )
    def test_invalid_value_category_value(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK1234",
            "goal"     : "test_invalid_value_category_value",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( goal이 str이 아닌 경우 )
    def test_invalid_value_goal(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : ["test_invalid_value_goal"],
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( is_alarm이 bool이 아닌 경우 )
    def test_invalid_value_isalarm(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : "test_invalid_value_isalarm",
            "is_alarm" : "True",
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # 값이 이상한 경우 ( days가 list가 아닌 경우 )
    def test_invalid_value_days(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : "test_invalid_value",
            "is_alarm" : True,
            "days"     : "MON"
        }
        self._request_400(body)
    
    # key값에 sql string이 들어간 경우
    def test_sql_injection(self):
        body = {
            "title"    : "\"OR 1=1 -",
            "category" : "HOMEWORK",
            "goal"     : "test_sql_injection",
            "is_alarm" : True,
            "days"     : ["MON", "WED", "FRI"]
        }
        self._request_400(body)
    
    # days값에 MON ~ SUN 중 동일한 값이 2개 이상 들어간 경우
    def test_overlap_days(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : "test_overlap_days",
            "is_alarm" : True,
            "days"     : ["MON", "MON", "TUE"]
        }
        self._request_400(body)
    
    # days값에 MON ~ SUN 이 아닌 다른 문자가 들어간 경우
    def test_invalid_days(self):
        body = {
            "title"    : "test1",
            "category" : "HOMEWORK",
            "goal"     : "test_invalid_days",
            "is_alarm" : True,
            "days"     : ["@@@MON@@@"]
        }
        self._request_400(body)