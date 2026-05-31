from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, register_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
