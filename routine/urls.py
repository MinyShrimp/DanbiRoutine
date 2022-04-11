
from django.urls import path

from routine.View.Login          import Login
from routine.View.Logout         import Logout
from routine.View.SignUp         import SignUp
from routine.View.RoutinesSearch import RoutinesSearch
from routine.View.RoutineView    import RoutineView

urlpatterns = [
    #path('hello/', helloAPI),
    
    path('signup/', SignUp),
    path('login/',  Login),
    path('logout/', Logout),

    path('routine/', RoutineView.as_view()),
    path('routines/', RoutinesSearch.as_view())
]