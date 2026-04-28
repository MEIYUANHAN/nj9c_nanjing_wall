# nanjing_wall_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wall_app import views

# 全局错误处理器
handler404 = views.custom_404
handler500 = views.custom_500
handler403 = views.custom_403
handler400 = views.custom_400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wall_app.urls')),
    path('logout/', views.user_logout, name='user_logout'),
]

# 开发环境下的媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
