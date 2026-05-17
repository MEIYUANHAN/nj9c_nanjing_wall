# nanjing_wall_project/urls.py
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from wall_app import views
from django.views.static import serve

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

# 静态文件和媒体文件服务（开发和生产环境都需要）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
