"""
URL configuration for moviesstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from cart import views as cart_views
from cart.admin_views import top_purchasers
urlpatterns = [
    path(
        "admin/reports/top-purchasers/",
        admin.site.admin_view(top_purchasers),
        name="admin_top_purchasers",
    ),
    path('admin/user-engagement/', admin.site.admin_view(cart_views.user_engagement),name='admin_user_engagement'),
    path('admin/movie-statistics/', admin.site.admin_view(cart_views.movie_statistics), name='admin_movie_statistics'),
    path('admin/reports/top-purchasers/', admin.site.admin_view(top_purchasers), name='admin_top_purchasers'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('movies/', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
