from django.test import TestCase
from routine.Verification.ClearData import isClearDataEmailPwd

class DataTest(TestCase):
    # 정상적으로 왔을때
    def test_clear_data(self):
        data = { "email": "ksk7584@gmail.com", "pwd": "qwer1234!" }
        self.assertTrue( isClearDataEmailPwd(data) )

    # 아무 것도 안왔을 때
    def test_empty(self):
        data = {}
        self.assertFalse( isClearDataEmailPwd(data) )
    
    # email만 왔을때
    def test_only_email(self):
        data = { "email": "ksk7584@gmail.com" }
        self.assertFalse( isClearDataEmailPwd(data) )

    # pwd만 왔을때
    def test_only_pwd(self):
        data = { "pwd": "qwer1234!" }
        self.assertFalse( isClearDataEmailPwd(data) )
    
    # email이 비어서 왔을때 
    def test_empty_email(self):
        data = { "email": "", "pwd": "qwer1234!" }
        self.assertFalse( isClearDataEmailPwd(data) )
    
    # pwd가 비어서 왔을때 
    def test_empty_email(self):
        data = { "email": "ksk7584@gmail.com", "pwd": "" }
        self.assertFalse( isClearDataEmailPwd(data) )
    
    # key가 이상하게 올때
    def test_stange_key(self):
        data = { "id": "ksk7584@gmail.com", "pwd": "" }
        self.assertFalse( isClearDataEmailPwd(data) )
    
    # email이 이상하게 왔을때
    def test_strange_email(self):
        data = { "email": "ksk7584", "pwd": "qwer1234!" }
        self.assertFalse( isClearDataEmailPwd(data) )
    
    # pwd가 이상하게 왔을때 ( 특수문자 x, 8글자 미만, 숫자 미포함 )
    def test_strange_pwd(self):
        data = { "email": "ksk7584@gmail.com", "pwd": "qwer1234" }
        self.assertFalse( isClearDataEmailPwd(data) )