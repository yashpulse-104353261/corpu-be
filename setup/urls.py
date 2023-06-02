"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from api.user_view import UserLogin,UserSignUp,UserRefreshAuthToken
from api.profile_view import Profile
from api.cv_views import CV
from api.unit_view import Unit
from api.staff_view import Staff
from api.unit_job_ad_view import UnitJobAd
from api.apply_view import Apply
from api.application_view import Application
from api.availability_view import Availability
from api.profile_status_view import ProfileStatus
from api.query_view import Query

urlpatterns = [
    path('login', UserLogin.as_view()),
    path('signup', UserSignUp.as_view()),
    path('refresh', UserRefreshAuthToken.as_view()),
    path('profile', Profile.as_view()),
    path('cv', CV.as_view()),
    path('unit', Unit.as_view()),
    path('staff', Staff.as_view()),
    path('jobs', UnitJobAd.as_view()),
    path('apply',Apply.as_view()),
    path('applications',Application.as_view()),
    path('availability',Availability.as_view()),
    path('profile/status',ProfileStatus.as_view()),
    path('query',Query.as_view())
]
