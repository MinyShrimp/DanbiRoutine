
from django.urls import path

from routine.View.Login          import Login
from routine.View.Logout         import Logout
from routine.View.SignUp         import SignUp
from routine.View.RoutinesSearch import RoutinesSearch
from routine.View.RoutineView    import RoutineView

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    #path('hello/', helloAPI),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('signup/', SignUp),
    path('login/',  Login),
    path('logout/', Logout),

    path('routine/', RoutineView.as_view()),
    path('routines/', RoutinesSearch.as_view())
]