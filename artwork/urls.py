from django.urls import path
from . import views

urlpatterns = [ # 서버IP/artwork/
    path('category/<str:slug>', views.category_page), #서버IP/artwork/category/slug
    path('', views.WorkList.as_view()),
    path('<int:pk>/', views.WorkDetail.as_view()),
]