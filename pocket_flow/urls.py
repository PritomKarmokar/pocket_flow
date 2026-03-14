from django.contrib import admin
from django.urls import path, include

service_name = 'pocket-flow'

urlpatterns = [
    path(f'{service_name}/admin/', admin.site.urls),
]

# Admin
admin.site.site_header = 'Pocket Flow'
admin.site.index_title = 'Pocket Flow'
admin.site.site_title = 'Pocket Flow'
