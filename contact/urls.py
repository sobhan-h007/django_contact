"""contact URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# import requests
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
# from ..contactlist.admin import admin_view
from django.views.defaults import page_not_found
from django.conf.urls import handler404, handler500
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from functools import update_wrapper
from django.views.static import serve
from baton.autodiscover import admin

def admin_view(view, cacheable=False):
    """
    Overwrite the default admin view to return 404 for not loggedin users.
    """
    def inner(request, *args, **kwargs):
        if not request.user.is_active and not request.user.is_staff:
            raise Http404
        return view(request, *args, **kwargs)

    if not cacheable:
        inner = never_cache(inner)

    # We add csrf_protect here so this function can be used as a utility
    # function for any view, without having to repeat 'csrf_protect'.
    if not getattr(view, 'csrf_exempt', False):
        inner = csrf_protect(inner)

    return update_wrapper(inner, view)




admin.site.admin_view = admin_view

urlpatterns = [
    path('admin/login/', page_not_found),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('', include("contactlist.urls")),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]




handler404 = 'contactlist.views.error_404_view'
handler500 = 'contactlist.views.error_500'
