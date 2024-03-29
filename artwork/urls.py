from django.urls import path
from . import views

urlpatterns = [ # 서버IP/artwork/
    path('search/<str:q>/', views.WorkSearch.as_view()),
    path('update_work/<int:pk>/', views.WorkUpdate.as_view()),
    path('create_work/', views.WorkCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),  # 서버IP/artwork/tag/slug
    path('category/<str:slug>', views.category_page), #서버IP/artwork/category/slug
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/', views.WorkDetail.as_view()),
    path('', views.WorkList.as_view()),
]