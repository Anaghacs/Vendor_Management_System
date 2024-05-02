from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import (
      VendorSerializer,
      PurchaseOrderSerializer
)

# www.example.com/api/index

@api_view(['GET'])
def index(request):
      vendors_details = {
            'name' : 'Anagha',
            'age' : 23,
            'job' : 'software engineer'
      }

      return Response(vendors_details)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def vendors(request):
      
      """
      View all vendor
      """
      if request.method == 'GET':
            obj_Vendors = Vendor.objects.all()
            serializer = VendorSerializer(obj_Vendors, many = True)
            return Response(serializer.data)
      
      """
      Create new vendor
      """
      if request.method == 'POST':
            data = request.data
            serializer = VendorSerializer(data = data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data)
            return Response(serializer.errors)
      
      """
      Put the vendor
      """
      if request.method == 'PUT':
            data = request.data
            obj = Vendor.objects.get(id = data['id'])
            serializer = VendorSerializer(obj, data = data, partial = False)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data)
            return Response(serializer.errors)
      
      """
      Patch the vendor
      """
      if request.method == 'PATCH':
            data = request.data
            obj = Vendor.objects.get(id = data['id'])
            serializer = VendorSerializer(obj, data = data, partial = True)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data)
            return Response(serializer.errors)
      
      
      else:
            """
            delete new vendor
            """

            data = request.data
            obj = Vendor.objects.get(id = data['id'])
            obj.delete()
            return Response({'message' : 'Vendor deleted'})
