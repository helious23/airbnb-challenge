from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github-login"),
    path("login/github/callback", views.github_callback, name="github-callback"),
    path("login/kakao", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback", views.kakao_callback, name="kakao-callback"),
    path("login/naver", views.naver_login, name="naver-login"),
    path("login/naver/callback", views.naver_callback, name="naver-callback"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", views.complate_verification, name="verify"),
    path("logout/", views.log_out, name="logout"),
]
