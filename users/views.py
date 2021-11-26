import os
import requests
import uuid
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import FormView
from django.core.files.base import ContentFile
from . import forms, models


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm()
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complate_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        messages.info(request, f"{request.user.email} is Verified!")
    except models.User.DoesNotExist:
        messages.warning(request, f"Sorry {request.user.first_name} Something is Wrong")
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    base_url = "https://github.com/login/oauth/authorize?"
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"{base_url}client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user&allow_signup=true"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        base_url = "https://github.com/login/oauth/access_token?"
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            token_request = requests.post(
                f"{base_url}client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                },
            )
            profile_json = profile_request.json()
            username = profile_json.get("login", None)
            if username is not None:
                name = profile_json.get("name")
                email = profile_json.get("email")
                bio = profile_json.get("bio")
                try:
                    user = models.User.objects.get(email=email)
                    if user.login_method != models.User.LOGIN_GITHUB:
                        raise GithubException(f"Please log in with {user.login_method}")
                except models.User.DoesNotExist:
                    user = models.User.objects.create(
                        email=email,
                        first_name=name,
                        username=email,
                        bio=bio,
                        login_method=models.User.LOGIN_GITHUB,
                        email_verified=True,
                    )
                    user.set_unusable_password()
                    user.save()
                    avatar_url = profile_json.get("avatar_url", None)
                    if avatar_url is not None:
                        photo_request = requests.get(avatar_url)
                        user.avatar.save(
                            f"{name}-avatar.jpg", ContentFile(photo_request.content)
                        )
                messages.success(request, f"Welcome Back {user.first_name}")
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get your code")
    except GithubException as error:
        messages.error(request, error)
        return redirect(reverse("users:login"))


def kakao_login(request):
    base_url = "https://kauth.kakao.com/oauth/authorize?"
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"{base_url}client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        base_url = "https://kauth.kakao.com/oauth/token?"
        code = request.GET.get("code", None)
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        if code is not None:
            token_request = requests.post(
                f"{base_url}grant_type=authorization_code&client_id={client_id}&code={code}&redirect_uri={redirect_uri}"
            )
            token_json = token_request.json()
            error = token_json.get("error")
            if error is not None:
                raise KakaoException("Can't get access token")

            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            email = profile_json.get("kakao_account").get("email", None)
            if email is None:
                raise KakaoException("There is no E-mail on kakao profile")
            profile = profile_json.get("kakao_account").get("profile", None)
            if profile is None:
                raise KakaoException("Kakao profile does not exist")
            else:
                nickname = profile.get("nickname")
                profile_image = profile.get("profile_image_url")
                try:
                    user = models.User.objects.get(email=email)
                    if user.login_method != models.User.LOGIN_KAKAO:
                        raise KakaoException(f"Please log in with {user.login_method}")
                except models.User.DoesNotExist:
                    user = models.User.objects.create(
                        email=email,
                        username=email,
                        first_name=nickname,
                        login_method=models.User.LOGIN_KAKAO,
                        email_verified=True,
                    )
                    user.set_unusable_password()
                    user.save()
                    if profile_image is not None:
                        photo_request = requests.get(profile_image)
                        user.avatar.save(
                            f"{nickname}-avatar.jpg", ContentFile(photo_request.content)
                        )
                messages.success(request, f"Welcome Back {user.first_name}")
                login(request, user)
                return redirect(reverse("core:home"))
    except KakaoException as error:
        messages.error(request, error)
        return redirect(reverse("users:login"))


def naver_login(request):
    base_url = "https://nid.naver.com/oauth2.0/authorize?"
    client_id = os.environ.get("NAVER_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback"
    state = uuid.uuid4().hex[:10]
    return redirect(
        f"{base_url}client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}"
    )


class NaverException(Exception):
    pass


def naver_callback(request):
    try:
        base_url = "https://nid.naver.com/oauth2.0/token?"
        code = request.GET.get("code", None)
        state = request.GET.get("state", None)
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
        if code is not None:
            token_request = requests.post(
                f"{base_url}grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
            )
            token_json = token_request.json()
            error = token_json.get("error")
            if error is not None:
                raise NaverException("Invalid Token")
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            message = profile_json.get("message")
            if message == "success":
                response = profile_json.get("response", None)
                if response is None:
                    raise NaverException("Naver profile does not exist")
                email = response.get("email")
                profile_image = response.get("profile_image")
                name = response.get("name")
                try:
                    user = models.User.objects.get(email=email)
                    if user.login_method != models.User.LOGIN_NAVER:
                        raise NaverException(f"Please log in with {user.login_method}")
                except models.User.DoesNotExist:
                    user = models.User.objects.create(
                        email=email,
                        username=email,
                        first_name=name,
                        login_method=models.User.LOGIN_NAVER,
                        email_verified=True,
                    )
                    user.set_unusable_password()
                    user.save()
                    if profile_image is not None:
                        photo_request = requests.get(profile_image)
                        user.avatar.save(
                            f"{name}-avatar.jpg", ContentFile(photo_request.content)
                        )
                messages.success(request, f"Welcome Back {user.first_name}")
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                raise NaverException("Can't login with Naver")
    except NaverException as error:
        messages.error(request, error)
        return redirect(reverse("users:login"))
