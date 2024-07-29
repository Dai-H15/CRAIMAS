"""
URL configuration for settings project.

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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .settings import DEBUG as setting_debug
if setting_debug:
    import debug_toolbar

admin.site.site_title = '管理者ページ'
admin.site.site_header = 'CRAIMAS 【クレイマス】 管理サイト'
admin.site.index_title = '管理対象シート一覧'

urlpatterns = [
    path('admin_site/', admin.site.urls),
    path("", include("main.urls")),
    path("auth/", include("authUser.urls")),
    path("task_calendar/", include("task_calendar.urls")),
    path("management/", include("management.urls")),
    path("support/", include("support.urls")),
]
if setting_debug:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
urlpatterns += staticfiles_urlpatterns()
