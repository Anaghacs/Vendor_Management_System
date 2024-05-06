import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vendor_management_system.settings")
django.setup()

# import pytest
import datetime
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from vendors.models import Vendor, PurchaseOrder
from rest_framework_simplejwt.tokens import AccessToken

from django.db import transaction

def create_test_user():
      """
      Creates a dedicated test user with appropriate permissions.
      """
      username = "test_user"
      password = "strong_password"
      email = "test@example.com"

      if not User.objects.filter(username = username).exists():
            user = User.objects.create_user(username, email, password)
            print(f"Test user '{username}' created successfully.")
      else:
            print(f"Test user '{username}' already exists.")


      if __name__ == "__main__":
            create_test_user()
