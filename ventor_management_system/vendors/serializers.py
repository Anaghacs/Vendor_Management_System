from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
      class Meta:
            model = User
            fields = ['username', 'password']
      
      def create(self, validated_data):
            user = User.objects.create(username = validated_data['username'])
            user.set_password(validated_data['password'])
            user.save()
            return user

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