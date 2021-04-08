from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("form", views.form_name_view),
    path("addtrainer", views.form_add_trainer_view),
    path("addcollege", views.form_add_college_view),
    path("allcollege", views.allcollege),
    path("alltrainer", views.alltrainer),
]