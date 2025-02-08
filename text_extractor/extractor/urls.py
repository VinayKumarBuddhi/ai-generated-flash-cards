from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='upload/')),
    path('upload/', views.upload_file, name='upload_file'),
]