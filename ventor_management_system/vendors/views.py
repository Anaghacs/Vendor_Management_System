from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import (
      Vendor, 
      PurchaseOrder
)
from rest_framework import viewsets
from .serializers import (
      VendorSerializer,
      PurchaseOrderSerializer,
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django.http import Http404
from django.db.models import Q, F, Avg

from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework_simplejwt.tokens import RefreshToken

# www.example.com/api/index


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
            username = request.data.get('username')
            password = request.data.get('password')
            
            password = make_password(password)            
            print(username, password)
            user = User.objects.create(username = username , password = password)
            print(user)
            data['user'] = user.id
            serializer = VendorSerializer(data = data)
            if serializer.is_valid():
                  serializer.user = user
                  serializer.save()
                  return Response(serializer.data)
            return Response(serializer.errors)
      
      """
      Put the vendor
      """
      if request.method == 'PUT':
            data = request.data
            try:
                  obj = Vendor.objects.get(id = data['id'])
            except:
                  return Response({"data" : "Vendor not found."}, status = status.HTTP_400_BAD_REQUEST)
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
      
      authentication_classes = [ JWTAuthentication]
      permission_classes = [IsAuthenticated]
      

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
     
class PurchaseOrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
      authentication_classes = [ JWTAuthentication]
      permission_classes = [IsAuthenticated]
      """
      An API endpoint for retrieving, updating, and deleting a particular purchase order.
      """

      queryset = PurchaseOrder.objects.all()
      serializer_class = PurchaseOrderSerializer

      def get_object(self):
            """
            Override to handle 404 (Not Found) for missing purchase orders.
            """
            pkd = self.kwargs.get("po_id")  
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
    
class PurchaseOrderAcknowledgeView(UpdateAPIView):

      authentication_classes = [ JWTAuthentication]
      permission_classes = [IsAuthenticated]
      """
      API endpoint to acknowledge a PO by the vendor.
      """

      queryset = PurchaseOrder.objects.all()
      print(queryset)
      serializer_class = PurchaseOrderSerializer
      print("==================",serializer_class)
      lookup_url_kwarg = "po_id"

      def perform_update(self, serializer):
            """
            Acknowledge a purchase order and update vendor's average response time.
            """
            serializer.save(acknowledgment_date = timezone.now())

            # Calculate new delivery date (Estimated date - 5 days after vendor acknowledgement)
            acknowledgment_date = serializer.instance.acknowledgment_date
            new_delivery_date = acknowledgment_date + timezone.timedelta(days = 5)
            serializer.instance.delivery_date = new_delivery_date
            serializer.instance.save()

            print("===============",acknowledgment_date, new_delivery_date, serializer.instance.delivery_date, serializer.instance)

            # Update average response time for the vendor
            purchase_order = serializer.instance
            
            vendor = purchase_order.vendor
            print(vendor)
            if vendor:
                  avg_response_time = PurchaseOrder.objects.filter(
                  vendor = vendor, acknowledgment_date__isnull = False
                  ).aggregate(
                  avg_response_time = Avg(F("acknowledgment_date") - F("issue_date"))
                  )[
                  "avg_response_time"
                  ]

                  average_days = avg_response_time.total_seconds() / (60 * 60 * 24)
                  avg_response_time = round(average_days, 2)

                  vendor.average_response_time = avg_response_time
                  vendor.save()

class VendorPerformanceRetrieveView(RetrieveAPIView):
      """
      API endpoint to retrieve a vendor's performance metrics.
      """

      permission_classes = [IsAuthenticated]
      authentication_classes = [ JWTAuthentication]
      queryset = Vendor.objects.all()
      serializer_class = VendorSerializer
      lookup_url_kwarg = "vendor_id"
      print("===============", queryset, serializer_class, lookup_url_kwarg)

      def retrieve(self, request, *args, **kwargs):
            vendor = self.get_object()
            print("****************", vendor)
            serializer = VendorSerializer(vendor)

            serializer.data["on_time_delivery_rate"] = vendor.on_time_delivery_rate
            serializer.data["quality_rating_avg"] = vendor.quality_rating_avg
            serializer.data["average_response_time"] = vendor.average_response_time
            serializer.data["fulfillment_rate"] = vendor.fulfillment_rate
            
            performance_data = {
                  "on_time_delivery_rate": serializer.data["on_time_delivery_rate"],
                  "quality_rating_avg": serializer.data["quality_rating_avg"],
                  "average_response_time": serializer.data["average_response_time"],
                  "fulfillment_rate": serializer.data["fulfillment_rate"],
            }
            print("=====================",performance_data)
            return Response(performance_data)




      