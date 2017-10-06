"""labyrinth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from riddles import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.signin),
    url(r'^signin/$', views.signin),
    url(r'^signup/$', views.signup),
    url(r'^about/$', views.about),
    url(r'^lb/$', views.lb),
    url(r'^logout/$', views.logout_user),

    url(r'^levels/$', views.levels, name='levels'),
    url(r'^levels/(?P<level_id>\d+\.\d{1})$', views.levels_quest),
    url(r'^levels/(?P<level_id>\d+\.\d{1})/(?P<userlevel_url>[A-z0-9]+)$', views.levels_quest_url),

	url(r'^answers/(?P<level_id>\d+\.\d{1})$', views.answers),

    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^.*$', views.error404),
]
