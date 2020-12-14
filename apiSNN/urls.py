from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from apiSNN import views

urlpatterns = [

    
    url('^$',views.Clasificacion.determinarDeporte,name='index'),
   #url(r'^determinarDeporte/',views.Clasificacion.determinarDeporte,name='determinarDeporte'),
    url(r'^predecirDeporte/',views.Clasificacion.predecirDeporte,name='predecirDeporte'),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)