from django.db import models
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from django.core.validators import MinValueValidator
from decimal import Decimal
# Create your models here.

class Vendor(models.Model):
      # This model stores essential information about each vendor.
      name = models.CharField(max_length = 100, blank = True)
      contact_details = models.TextField(blank = False)
      address = models.TextField(blank = False)
      vendor_code = models.CharField(max_length = 50, unique = True, blank = False)

      #Performace metrics(Calculated fields, not actual database).
      on_time_delivery_rate = models.FloatField(default = 0.0)
      quality_rating_avg = models.FloatField(default = 0.0)
      average_response_time = models.FloatField(default = 0.0)
      fulfillment_rate = models.FloatField(default = 0.0)

      def __str__(self):
            return self.name
      
      def calculate_on_time_delivery_rate(self):
            """
            Calculates the on-time delivery rate for a vendor.
            Returns: The on-time delivery rate as a Decimal (percentage) or None if no completed POs exist.
            """
            completed_orders = PurchaseOrder.objects.filter(vendor = self, status = "completed")
            if not completed_orders.count():
                  return Decimal("0.00")
            
            current_time = timezone.now()

            on_time_deliveries = completed_orders.filter(delivery_date__date__gte = current_time).count()
            total_completed_orders = completed_orders.count()

            if not total_completed_orders:
                  return Decimal("0.00")

            on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100
            return Decimal(str(on_time_delivery_rate)).quantize(Decimal(".01"))
      

      # def calculate_quality_rating_average(self):
      #       """
      #       Calculates the average quality rating for a vendor.
      #       Returns: The average quality rating as a Decimal or None if no completed POs with ratings exist.
      #       """
      #       completed_orders = PurchaseOrder.objects.filter(vendor = self, status = "completed", quality_rating__isnull = False)
      #       if not completed_orders.count():
      #             return Decimal("0.00")

      #       average_rating = completed_orders.aggregate(avg_rating = Avg("quality_rating"))[
      #             "avg_rating"
      #       ]
      #       if not average_rating:
      #             return Decimal("0.00")

      #       return Decimal(str(average_rating)).quantize(Decimal(".01"))
      
      
      # def calculate_fulfillment_rate(self):
      #       """
      #       Calculates the fulfillment rate for a vendor.
      #       Args: vendor_id: ID of the vendor.
      #       Returns: The fulfillment rate as a Decimal (percentage) or None if no POs exist.
      #       """
      #       total_orders = PurchaseOrder.objects.filter(vendor = self).count()

      #       if not total_orders:
      #           return Decimal("0.00")
            
      #       completed_orders = PurchaseOrder.objects.filter(vendor = self, status = "completed")
      #       fulfilled_orders = completed_orders.count()

      #       if not total_orders:
      #           return Decimal("0.00")
            
      #       fulfillment_rate = (fulfilled_orders / total_orders) * 100
      #       return Decimal(str(fulfillment_rate)).quantize(Decimal(".01"))

class PurchaseOrder(models.Model):

      #This model captures the details of each purchase order

      po_number =  models.CharField(max_length = 50, unique = True)
      Vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
      order_date = models.DateTimeField(default = timezone.now)
      delivery_date = models.DateTimeField(blank = True, null = True)
      items = models.JSONField()
      quantity = models.PositiveIntegerField(validators = [MinValueValidator(1)])
      STATUS_CHOICES = (
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
      )
      status = models.CharField(max_length=20, choices = STATUS_CHOICES, default = 'pending')
      quality_rating = models.FloatField(blank = True, null = True)
      issue_date = models.DateTimeField(default = timezone.now)
      acknowledgment_date = models.DateTimeField(blank = True, null = True)


      def __str__(self):
            return f" PO :{self.po_number} - {self.vendor.name}"  
      
class HistoricalPerformance(models.Model):
      
      # This model optionally stores historical data on vendor performance, enabling trend analysis.
      
      vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
      date = models.DateTimeField()
      on_time_delivery_rate = models.FloatField()
      quality_rating_avg = models.FloatField()
      average_response_time = models.FloatField()
      fulfillment_rate = models.FloatField()
    
      def __str__(self):
            return f"Performance for {self.vendor.name} on {self.date}"

