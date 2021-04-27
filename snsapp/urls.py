from django.urls import path
from .views import signupfunc, loginfunc, listfunc, logoutfunc, detailfunc, goodfunc, readfunc, SnsCreate, deletefunc, mylistfunc, apigoodfunc, SnsNews

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('list/', listfunc, name='list'),
    path('logout/', logoutfunc, name='logout'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('read/<int:pk>', readfunc, name='read'),
    path('create', SnsCreate.as_view(), name='create'),
    path('delete/<int:pk>', deletefunc, name='delete'),
    path('mylist/', mylistfunc, name='mylist'),
    path("api/good/<int:pk>/", apigoodfunc, name="apigood"),
    path("news/", SnsNews.as_view(), name='news'),
]
