from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import view
import ADatabase.dash_app

urlpatterns = [
    re_path(r'^$', view.homePage),
    re_path(r'^query1/$', view.query1),
    re_path(r'^query2/$', view.query2),
    re_path(r'^query3/$', view.query3),
    re_path(r'^dash/', include('django_plotly_dash.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)