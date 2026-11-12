from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static  
from django.http import JsonResponse

def health(request):
    """Simple health-check endpoint for external probes/monitors."""
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('MainApp.urls')),
    path('health', health, name='health'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)