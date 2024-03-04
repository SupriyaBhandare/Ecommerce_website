from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index' ),
    path('search',views.search, name='search' ),

    path('product',views.product,name='product'),
    path('add_product',views.add_product,name='add_product'),
    path('prod_desc/<pk>',views.prod_desc,name="prod_desc"),
    path('productdata',views.ProductListView.as_view(),name='productdata'),
    path('editproductdata/<int:pk>/',views.ProductUpdateview.as_view(),name='editproductdata'),
    path('deleteproductdata/<int:pk>/',views.ProductDeleteview.as_view(),name='deleteproductdata'),

    path('cartitems',views.CartItemsListView.as_view(),name='cartitems'),
    path('add_to_cart/<pk>',views.add_to_cart, name="add_to_cart"),
    path('orderlist',views.orderlist, name="orderlist"),
    path('add_item/<int:pk>',views.add_item, name="add_item"),
    path('remove_item/<int:pk>',views.remove_item, name="remove_item"),
    path('checkout',views.checkout, name="checkout"),

    path('ordereditems',views.OrderedItemsListView.as_view(),name='ordereditems'),
    path('managedata',views.manage_data,name='managedata'),
    
    path('categorydata',views.manage_categorydata.as_view(),name='categorydata'),
    path('add_category',views.CategoryCreateView.as_view(),name='add_category'),
    path('editcategorydata/<int:pk>/',views.CategoryUpdateview.as_view(),name='editcategorydata'),
    path('deletecategorydata/<int:pk>/',views.CategoryDeleteview.as_view(),name='deletecategorydata'),
    

    

]