from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

# Serializer for Vendor models
class VendorSerializer(serializers.ModelSerializer):
      
      class Meta:
            model = Vendor
            fields = '__all__'
      
# Serializer for the PurchaseOrder model.
class PurchaseOrderSerializer(serializers.ModelSerializer):

      class Meta:
            model = PurchaseOrder
            fields = '__all__'

# Serializer for HistoricalPerformance model.
class HistoricalPerformanceSerializer(serializers.ModelSerializer):

      class Meta:
            model = HistoricalPerformance
            fields = '__all__'