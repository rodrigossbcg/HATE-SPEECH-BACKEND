from django.urls import path
from .views import GPTViews

urlpatterns = [
    path('example/', GPTViews.as_view(), name='example'),
]
