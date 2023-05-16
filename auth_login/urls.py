from django.urls import path
from . import views
urlpatterns = [
    # path('celebritylist.html', views.actorslist),
    # path('moviegrid.html', views.movieslist),
    # path('user/<slug:user_id>', views.userprofile),
    # path('user/<slug:user_id>/favouritemovies', views.favmovies),
    # path('user/<slug:user_id>/ratedmovies', views.ratedmovies),
    path('', views.index),
    path('producer/landing', views.producerlandingpage),
    # path('normalprofile', views.userprofile),
    path('producer/list', views.produceractorlist),
    path('actor/list', views.actorslist),
    path('movie/list', views.movieslist),
    path('actor/<slug:actor_id>', views.actordata, name='singleactor'),
    path('movie/<slug:movie_id>', views.moviedata, name='singlemovie'),
    path('movie/<slug:movie_id>/review', views.createreview),
    path('user/profile', views.loadprofile),
    path('user/favourites', views.showfavourites),
    path('user/ratedmovies', views.showrated),
    path('setlogin', views.loginuser),
    path('createuser', views.registeruser),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('producer/createmovie', views.createmovie),
    path('update/view_count', views.update_view_count),
    path('update/favourites', views.add_movie_to_favourite),
    path('remove/favourites', views.remove_movie_from_favourite),
    path('user/changepassword', views.changepassword),
    path('search', views.searchdb)
    # path('profile', views.show_user_profile)
]
