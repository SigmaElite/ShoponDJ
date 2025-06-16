from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),#slug указ что приним онли слаги
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('api/search/', views.life_search, name=('life_search'))
]
