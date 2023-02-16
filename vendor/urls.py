from django.contrib import admin
from django.urls import path

from . import views
from .views import VendorListView, VendorDetailView, VendorCreateView, VendorCreateView_2, VendorUpdateView
# 不import VendorListView的話下面就是
# path('list_view', views.VendorListView.as_view(), ...)

# 避免 name 重複性的問題
app_name = 'vendors'

urlpatterns = [
    path('', views.vendor_index, name="index"),
    path('create/', views.vendor_create_view),
    path('create_2/', views.vendor_create_view_2),
    # name: 為這一個 path 命名
    path('haha<int:v_id>/', views.singleVendor, name='vendor_id'),

    # 可以用ListView 及 DetailView去取代line 13, 17
    path('list_view/', VendorListView.as_view(), name='index_2'),
    # 要把<int:id>改成<int:pk>
    path('detail_view_<int:pk>/', VendorDetailView.as_view(), name='vendor_id_2'),
    path('create_view/', VendorCreateView.as_view(), name='create'),
    path('create_view_2/', VendorCreateView_2.as_view(), name='create'),
    path('<int:pk>/update/', VendorUpdateView.as_view(), name='update'),
]
