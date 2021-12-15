from django.urls import path
from . import views

urlpatterns = [ # 서버IP/artwork/
    # path('search/<str:q>/', views.WorkSearch.as_view()),
    # path('update_post/<int:pk>/', views.WorkUpdate.as_view()),
    path('create_work/', views.WorkCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),  # 서버IP/artwork/tag/slug
    path('category/<str:slug>', views.category_page), #서버IP/artwork/category/slug
    path('', views.WorkList.as_view()),
    path('<int:pk>/', views.WorkDetail.as_view()),
]