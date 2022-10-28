from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Documentation for Active Points Plus App', permission_classes=[AllowAny])),
    path('auth/', include('users.urls')),
    path('app/', include('traka.urls')),
    path('web/', include('website.urls')),
]
