from routine.tests.Base.TokenHeaderTest import TokenHeaderTest

# python manage.py test --keepdb routine.tests.TestSearchRoutineAll

class TestSearchRoutineAll(TokenHeaderTest):
    ###############################################
    # protected values
    _url, _method = "/api/routines/all/", "GET"

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
        self._request_200({})