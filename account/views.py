from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "accounts/signup.html", {"form": form})

    def post(self, request: HttpRequest):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect("staff:list_orders_staff")
        return render(request, "accounts/signup.html", {"form": form})


class Login(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm()
        return render(
            request,
            "accounts/login.html",
            {"form": form, "next": request.GET.get("next")},
        )

    def post(self, request: HttpRequest) -> HttpResponsePermanentRedirect:
        form = AuthenticationForm(data=request.POST)
        if not form.is_valid():
            return render(
                request,
                "accounts/login.html",
                {"form": form, "next": request.GET.get("next")},
            )

        # log in the user
        user = form.get_user()
        login(request, user)

        if request.user.is_superuser:
            return redirect("menu:list_menus")

        return redirect(request.POST.get("next", "staff:list_orders_staff"))


def logout_view(request: HttpRequest) -> HttpResponsePermanentRedirect:
    """
    Log out the user using logout funtion from django

    Parameters:
      request (HttpRequest): django request object
    """
    logout(request)
    return redirect("account:login")
