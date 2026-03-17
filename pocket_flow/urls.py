# Django Imports
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

api_prefix = "api/v1"
service_name = settings.SERVICE_NAME

urlpatterns = [
    path(f'{service_name}/admin/', admin.site.urls),
    path(f'{service_name}/{api_prefix}/auth/', include('authentication.urls')),
]

# Admin
admin.site.site_header = 'Pocket Flow'
admin.site.index_title = 'Pocket Flow'
admin.site.site_title = 'Pocket Flow'
