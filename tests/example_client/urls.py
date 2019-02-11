import django
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from example_client.views import PrivateView

from page_exporter import urls as page_exporter_urls

urlpatterns = [
    # '',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'private/$', login_required(PrivateView.as_view())),

    url(r'^e/', include(page_exporter_urls)),

    url(r'^admin/', admin.site.urls),

    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
