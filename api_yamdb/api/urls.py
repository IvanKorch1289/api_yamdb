from django.urls import include, path

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup', include('djoser.urls.jwt')),
]
