from django.urls import path, include
from vendors.views import (
      index, 
      vendors, 
      RegisterUser,
      PurchaseOrderListCreateAPIView, 
      PurchaseOrderRetrieveUpdateDestroyView,
      PurchaseOrderAcknowledgeView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'purchase_orders', PurchaseOrderListCreateAPIView)
urlpatterns = [
      
    path(
          "token/", 
          TokenObtainPairView.as_view(), 
          name = "get-token"
    ),

    path(
          "token/refresh/", 
          TokenRefreshView.as_view(), 
          name = "refresh-token"
    ),
    
    path(
          "register/",
          RegisterUser.as_view(),
          name = "register"
          
    ),

    path(
        "index/", 
        index, 
        name = "index"
    ),

    path(
        "vendors/", 
        vendors, 
        name = "vendors"
    ),

    

    path(
        "purchase_orders/", 
        PurchaseOrderListCreateAPIView.as_view(), 
        name = "purchase-order-create-list",
    ),

    path(
        "purchase_orders/<int:po_id>/", 
        PurchaseOrderRetrieveUpdateDestroyView.as_view(), 
        name = "purchase-order-read-update-delete",
    ),


    path(
        "purchase_orders/<int:po_id>/acknowledge/",
        PurchaseOrderAcknowledgeView.as_view(),
        name="purchase-order-acknowledge",
    ),
    path('login/',views.obtain_auth_token)

    
]
