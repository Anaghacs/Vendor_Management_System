from django.urls import path, include
from vendors.views import (
      index, 
      vendors, 
      PurchaseOrderListCreateAPIView, 
      PurchaseOrderRetrieveUpdateDestroyView,
      PurchaseOrderAcknowledgeView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'purchase_orders', PurchaseOrderListCreateAPIView)
urlpatterns = [
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
    
]