
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    #  path('student/', include('student.urls')),
    # path('faculty/', include('faculty.urls')),
    path('faculty/',include('faculty.urls',namespace='faculty')),
    path('student/', include('student.urls', namespace='student')),
]
