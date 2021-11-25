from django.urls import path
from . import views

urlpatterns = [ #서버IP/artwork/
    path('', views.WorkList.as_view()),
    path('<int:pk>/', views.WorkDetail.as_view()),
]