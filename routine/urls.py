
from django.urls import path
from routine.Token.Refresh import Refresh

from routine.View.AutoLogin      import AutoLogin
from routine.View.Login          import Login
from routine.View.Logout         import Logout
from routine.View.SignUp         import SignUp
from routine.View.RoutinesSearch import RoutinesSearch
from routine.View.RoutineView    import RoutineView
from routine.View.AllRoutines    import AllRoutine


urlpatterns = [
    #path('hello/', helloAPI),

    path('signup/', SignUp),
    path('login/',  Login),
    path('logout/', Logout),
    path('autologin/', AutoLogin),

    path('routine/', RoutineView.as_view()),
    path('routines/', RoutinesSearch.as_view()),
    path('routines/all/', AllRoutine.as_view()),

    path('refresh/', Refresh.as_view())
]