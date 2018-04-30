from django.conf.urls import url
from . import views

app_name = 'Vote'
urlpatterns = [
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^results/', views.results, name='results'),
    url(r'^home/', views.home, name='home'),
    url(r'^home_hindi/', views.home_hindi, name='home_hindi'),
    url(r'^home_german/', views.home_german, name='home_german'),
    url(r'^home_spanish/', views.home_spanish, name='home_spanish'),
    url(r'^about/', views.about, name='about'),
    url(r'^voted/', views.voted, name='voted'),
]
