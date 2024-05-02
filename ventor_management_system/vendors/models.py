from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
# Create your models here.

class Vendor(models.Model):
      # This model stores essential information about each vendor and their performance metrics.
      name = models.CharField(max_length = 100, blank = True)
      contact_details = models.TextField(blank = False)
      address = models.TextField(blank = False)
      vendor_code = models.CharField(max_length = 50, unique = True, blank = False)

      #Performace metrics(Calculated fields, not actual database )
      on_time_delivery_rate = models.FloatField(default = 0.0)
      quality_rating_avg = models.FloatField(default = 0.0)
      average_response_time = models.FloatField(default = 0.0)
      fulfillment_rate = models.FloatField(default = 0.0)

      def __str__(self):
            return self.name

class PurchaseOrder(models.Model):
      #This model captures the details of each purchase order
      po_number =  models.CharField(max_length = 50, unique = True)
      Vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
      order_date = models.DateTimeField(default = timezone.now)
      delivery_date = models.DateTimeField(blank = True, null = True)
      items = models.JSONField()
      quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
      STATUS_CHOICES = (
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
      )
      status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
      quality_rating = models.FloatField(blank=True, null=True)
      issue_date = models.DateTimeField(default=timezone.now)
      acknowledgment_date = models.DateTimeField(blank=True, null=True)

      def __str__(self):
            return f" PO :{self.po_number} - {self.vendor.name}"  
      
class HistoricalPerformance(models.Model):
      
      # Model representing historical performance data of vendors.
      
      vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
      date = models.DateTimeField()
      on_time_delivery_rate = models.FloatField()
      quality_rating_avg = models.FloatField()
      average_response_time = models.FloatField()
      fulfillment_rate = models.FloatField()
    
      def __str__(self):
            return f"Performance for {self.vendor.name} on {self.date}"

