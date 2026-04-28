from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('about/', views.about_page, name='about_page'),
    path('map/', views.map_view, name='interactive_map'),
    path('history/', views.history_view, name='history'),
    path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    path('pictures/', views.picture_gallery, name='picture_gallery'),
    path('contribution_detail/<int:contribution_id>/', views.contribution_detail, name='contribution_detail'),
    path('create_historical_event/', views.create_historical_event, name='create_historical_event'),
    
    # 用户认证相关
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # 用户贡献相关
    path('create_contribution/', views.create_contribution, name='create_contribution'),
    path('contributions/', views.user_contributions, name='user_contributions'),
    path('profile/', views.user_profile, name='user_profile'),

]