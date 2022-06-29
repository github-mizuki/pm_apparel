from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/smallcategory/get/', views.ajax_get_smallcategory, name='ajax_get_smallcategory'),
    path('api/largecategory/get/', views.ajax_select_largecategory, name='ajax_select_largecategory'),
    path('baseproduct_regist/', views.BaseProductRegistView.as_view(),name='baseproduct_regist'),
    path('baseproduct_update/<int:pk>',views.BaseProductUpdateView.as_view(), name='baseproduct_update'),
    path('baseproduct_detail/<int:pk>', views.BaseProductDetailView.as_view(), name='baseproduct_detail'),
    path('product_regist/<int:pk>', views.ProductRegistView.as_view(), name='product_regist'),
    path('product_copy/<int:pk>', views.ProductTakeOverView.as_view(), name='product_copy'),
    path('product_update/<int:pk>', views.ProductUpdateView.as_view(), name='product_update'),
    path('product_detail/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('config_top/', views.ConfigTopView.as_view(), name='config_top'),
    path('creator_regist/', views.CreatorRegistView.as_view(), name='creator_regist'),
    path('creator_update/<int:pk>',views.CreatorUpdateView.as_view(), name='creator_update'),
    path('creator_delete/<int:pk>', views.CreatorDeleteView.as_view(), name='creator_delete'),
    path('category_regist/', views.CategoryRegistView.as_view(), name='category_regist'),
    path('largecategory_update/<int:pk>', views.LargeCategoryUpdateView.as_view(), name='largecategory_update'),
    path('largecategory_delete/<int:pk>', views.LargeCategoryDeleteView.as_view(), name='largecategory_delete'),
    path('smallcategory_update/<int:pk>', views.SmallCategoryUpdateView.as_view(), name='smallcategory_update'),
    path('smallcategory_delete', views.SmallCategoryDeleteView.as_view(), name='smallcategory_delete'),

]