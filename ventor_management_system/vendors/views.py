from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
      Vendor, 
      PurchaseOrder
)
from rest_framework import viewsets
from .serializers import (
      VendorSerializer,
      PurchaseOrderSerializer
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django.http import Http404
from django.db.models import Q, F, Avg
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


class PurchaseOrderListCreateAPIView(ListCreateAPIView):
      """
      An API endpoint for both listing and creating purchase orders, with the added functionality of vendor filtering.      
      """

      queryset = PurchaseOrder.objects.all()
      serializer_class = PurchaseOrderSerializer
      filter_backends = [OrderingFilter]

      def get_queryset(self):
            """
            Include an override option for filtering by vendor (optional parameter in the query string).            
            """
            queryset = PurchaseOrder.objects.all()
            vendor_id = self.request.query_params.get("vendor")
            if vendor_id:
                  queryset = queryset.filter(Q(vendor__id = vendor_id))
            return queryset

      def post(self, request):
            """
            Create a purchase order.
            """
            serializer = PurchaseOrderSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
    
# class PurchaseOrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#       """
#       An API endpoint for retrieving, updating, and deleting a particular purchase order.    
#       """

#       queryset = PurchaseOrder.objects.all()
#       serializer_class = PurchaseOrderSerializer

#       def get_object(self):
#             """
#             Override to handle 404 (Not Found) for missing purchase orders.
#             """
#             pkd = self.kwargs.get("po_id")
#             try:
#                   return self.queryset.get(pk = pkd)
#             except PurchaseOrder.DoesNotExist:
#                   raise Http404("Purchase order ID " + str(pkd) + " is not found.")
            
     
class PurchaseOrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    An API endpoint for retrieving, updating, and deleting a particular purchase order.
    """

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_object(self):
        """
        Override to handle 404 (Not Found) for missing purchase orders.
        """
        pkd = self.kwargs.get("po_id")  # assuming 'pk' is used for the purchase order ID in the URL
        try:
            return self.queryset.get(pk = pkd)
        except PurchaseOrder.DoesNotExist:
            raise Http404("Purchase order ID " + str(pkd) + " is not found.")

    def get(self, request, *args, **kwargs):
        """
        Retrieve a particular purchase order.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a particular purchase order.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
      #   return Response(status = status.HTTP_204_NO_CONTENT)
        raise Http404("Purchase order ID " + str(instance) + " is not found.")


    def update(self, request, *args, **kwargs):
        """
        Update a particular purchase order.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)