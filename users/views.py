import os
import uuid
import requests
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, DetailView
from django.core.files.base import ContentFile
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from . import forms, models, mixins


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


class LoginView(mixins.LoggedOutOnlyView, SuccessMessageMixin, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_message = "Welcome %(first_name)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data, first_name=self.request.user.first_name
        )

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            print(next_arg)
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

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
                raise KakaoException("Please agree with giving your email to us")
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


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    form_class = forms.UpdateProfileForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if email != self.request.user.get_username():
            self.object.username = email
            self.object.email_verified = False
            self.object.save()
            self.object.verify_email()
            messages.success(self.request, "Email updated. Please verify updated email")
        else:
            messages.success(self.request, "Profile updated")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First Name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last Name"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["bio"].widget.attrs = {"placeholder": "Biography"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birth Date"}
        form.fields["language"].widget.attrs = {"placeholder": "Language"}
        form.fields["currency"].widget.attrs = {"placeholder": "Currency"}
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm New Password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        response = HttpResponse(200)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
