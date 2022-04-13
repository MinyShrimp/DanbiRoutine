from routine.tests.Base.NoneHeaderTest import NoneHeaderTest

# python manage.py test --keepdb routine.tests.TestSignup

class TestSignup(NoneHeaderTest):   
    ###############################################
    # protected values 
    _url = '/api/signup/'

    ###############################################
    # test functions
    # 정상적으로 왔을때
    def test_clean_data(self):
        self._request_200({ "email": "ksk7584@gmail.com", "pwd": "qwer1234!" })

    # 아무 것도 안왔을 때
    def test_empty(self):
        self._request_400({})
    
    # email만 왔을때
    def test_only_email(self):
        self._request_400({ "email": "ksk7584@gmail.com" })

    # pwd만 왔을때
    def test_only_pwd(self):
        self._request_400({ "pwd": "qwer1234!" })
    
    # email이 비어서 왔을때 
    def test_empty_email(self):
        self._request_400({ "email": "", "pwd": "qwer1234!" })
    
    # pwd가 비어서 왔을때 
    def test_empty_email(self):
        self._request_400({ "email": "ksk7584@gmail.com", "pwd": "" })
    
    # key가 이상하게 올때
    def test_stange_key(self):
        self._request_400({ "id": "ksk7584@gmail.com", "pwd": "" })
    
    # email이 이상하게 왔을때
    def test_strange_email(self):
        self._request_400({ "email": "`?DELETE", "pwd": "qwer1234!" })
    
    # pwd가 이상하게 왔을때 ( 특수문자 x, 8글자 미만, 숫자 미포함 )
    def test_strange_pwd(self):
        self._request_400({ "email": "ksk7584@gmail.com", "pwd": "qwer1234" })