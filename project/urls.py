from django.urls import path, re_path, include

from . import views

urlpatterns = [
    #re_path(r'accounts/profile/*', views.profile, name='profile'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/email/', views.email, name='email'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/othersWorkout', views.OthersWorkoutView.as_view(),name="othersWorkout"),
    path('', views.login, name='login'),
    path('accounts/search_users', views.search_users, name="userList"),
    path('accounts/submitPost/', views.submitPost, name='submitPost'),
    path('accounts/postHandling/', views.postHandling, name='postHandling'),
    path('accounts/allPost/', views.allPost, name='allPost'),
    path('accounts/nutrition', views.log_nutrition, name="nutrition"),
    path('accounts/profile/delete_favorite', views.delete_favorite, name='deleteFavorite'),
    path('accounts/editProfile/', views.editProfile, name='editProfile'),
    path('accounts/logWorkout/', views.logWorkout, name='logWorkout'),
    path('accounts/recentWorkouts/', views.recentWorkouts.as_view(), name='recentWorkouts'),
    path('accounts/nutrihistory', views.nutrihistory, name="nutrihistory"),
    path('accounts/nutrisuccess', views.nutrisuccess, name="nutrisuccess"),
    path('accounts/profile/view_favorite', views.view_favorite, name="view_favorite"),
    path('accounts/recentWorkouts/delete_workout', views.delete_workout, name='deleteWorkout'),
    path('accounts/myPost/', views.myPost, name='myPost'),
    path('accounts/deletePost/', views.deletePost, name='deletePost'),
    path('accounts/workoutsuccess', views.workoutsuccess, name="workoutsuccess"),
    #path('accounts/profile/delete_favorite', views.delete_favorite, name='deleteFavorite')
    path('accounts/recommended', views.RecommendedList.as_view(), name='recommended'),
    path('<slug:slug>/', views.RecommendedDetail.as_view(), name='recommended_detail'),
    path('accounts/delete_nutrition', views.delete_nutrition, name='deleteNutrition'),
    path('accounts/view_articles_sports', views.view_articles_sports, name="view_articles_sports"),
    path('accounts/view_articles_health', views.view_articles_health, name="view_articles_health"),
    path('accounts/view_articles_nutrition', views.view_articles_nutrition, name="view_articles_nutrition"),
    re_path(r'^.*', views.profile, name='anything_else'),
]