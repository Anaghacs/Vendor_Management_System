import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vendor_Management_System.settings")
django.setup()

import pytest
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

      if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            print(f"Test user '{username}' created successfully.")
      else:
            print(f"Test user '{username}' already exists.")


if __name__ == "__main__":
    create_test_user()


@pytest.fixture(scope="function")
def jwt_token():
      """
      Retrieves the test user and generates a JWT token.
      """
      user = User.objects.get(username="test_user")
      from rest_framework_simplejwt.tokens import RefreshToken

      refresh = RefreshToken.for_user(user)
      token = refresh.access_token

      client = APIClient()
      client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
      return client


@pytest.fixture(scope="function")
def clean_db():
      """
      Fixture to ensure a clean database for each test.
      """
      with transaction.atomic():
            PurchaseOrder.objects.all().delete()

            from vendors.models import Vendor

            Vendor.objects.all().delete()

      yield

      transaction.rollback()


@pytest.fixture(scope="function")
def create_vendor():
      vendor = Vendor.objects.create(
            id=1,
            name="Test Vendor",
            contact_details="123-456-7890",
            address="123 Main St",
            vendor_code="ABC123",
      )
      return vendor.id


@pytest.fixture(scope="function")
def create_vendors():
      vendor1 = Vendor.objects.create(
            name="Test Vendor 1",
            contact_details="123-456-7890",
            address="123 Main St",
            vendor_code="ABC123",
      )
      vendor2 = Vendor.objects.create(
            name="Test Vendor 2",
            contact_details="987-654-3210",
            address="456 Elm St",
            vendor_code="XYZ789",
      )
      return vendor1.id, vendor2.id


@pytest.fixture(scope="function")
def create_purchase_order():
      """
      Fixture to create a purchase order for testing.
      """
      vendor = Vendor.objects.create(
            id=1,
            name="Test Vendor",
            contact_details="123-456-7890",
            address="123 Main St",
            vendor_code="ABC123",
      )
      po_data = {
            "po_number": "PO123",
            "vendor": vendor,
            "order_date": "2024-05-01T12:00:00Z",
            "delivery_date": "2024-05-10T12:00:00Z",
            "items": [
                  {"name": "Item 1", "quantity": 5, "unit_price": 10.99},
                  {"name": "Item 2", "quantity": 3, "unit_price": 15.99},
            ],
            "quantity": 8,
            "status": "pending",
      }
      return PurchaseOrder.objects.create(**po_data).id


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_create_vendor(jwt_token):
      """
      Tests creating a vendor with a JWT token.
      """
      vendor_data = {
            "name": "Test Vendor",
            "contact_details": "123-456-7890",
            "address": "123 Main St",
            "vendor_code": "ABC123",
      }
      response = jwt_token.post("/api/vendors/", vendor_data, format="json")
      assert response.status_code == 201
      assert Vendor.objects.count() == 1


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_list_vendors(jwt_token):
      """
      Tests listing all vendors.
      """
      url = reverse("vendor-create-list")
      response = jwt_token.get(url)
      assert response.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_retrieve_vendor(jwt_token):
      """
      Tests retrieving a specific vendor.
      """
      vendor_data = {
            "name": "Test Vendor",
            "contact_details": "123-456-7890",
            "address": "123 Main St",
            "vendor_code": "ABC123",
      }
      create_response = jwt_token.post("/api/vendors/", vendor_data, format="json")
      assert create_response.status_code == 201
      created_vendor_id = create_response.data["id"]

      retrieve_url = reverse(
            "vendor-read-update-delete", kwargs={"pk": created_vendor_id}
      )
      retrieve_response = jwt_token.get(retrieve_url)
      assert retrieve_response.status_code == 200
      assert retrieve_response.data["name"] == "Test Vendor"
      assert retrieve_response.data["contact_details"] == "123-456-7890"
      assert retrieve_response.data["address"] == "123 Main St"
      assert retrieve_response.data["vendor_code"] == "ABC123"


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_update_vendor(jwt_token):
      """
      Tests updating a specific vendor.
      """
      vendor_data = {
            "name": "Test Vendor",
            "contact_details": "123-456-7890",
            "address": "123 Main St",
            "vendor_code": "ABC123",
      }
      create_response = jwt_token.post("/api/vendors/", vendor_data, format="json")
      assert create_response.status_code == 201
      created_vendor_id = create_response.data["id"]

      update_data = {
            "name": "Updated Vendor Name",
            "contact_details": "987-654-3210",
            "address": "456 Elm St",
            "vendor_code": "XYZ789",
      }
      update_url = reverse("vendor-read-update-delete", kwargs={"pk": created_vendor_id})
      update_response = jwt_token.put(update_url, update_data, format="json")
      assert update_response.status_code == 200
      assert update_response.data["name"] == "Updated Vendor Name"
      assert update_response.data["contact_details"] == "987-654-3210"
      assert update_response.data["address"] == "456 Elm St"
      assert update_response.data["vendor_code"] == "XYZ789"


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_delete_vendor(jwt_token):
      """
      Tests deleting a specific vendor.
      """
      vendor_data = {
            "name": "Test Vendor",
            "contact_details": "123-456-7890",
            "address": "123 Main St",
            "vendor_code": "ABC123",
      }
      create_response = jwt_token.post("/api/vendors/", vendor_data, format="json")
      assert create_response.status_code == 201
      created_vendor_id = create_response.data["id"]

      delete_url = reverse("vendor-read-update-delete", kwargs={"pk": created_vendor_id})
      delete_response = jwt_token.delete(delete_url)
      assert delete_response.status_code == 204


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_vendor")
def test_create_purchase_order(jwt_token, create_vendor):
      """
      Tests creating a purchase order with a JWT token.
      """
      vendor_id = create_vendor

      po_data = {
            "po_number": "PO123",
            "vendor": vendor_id,
            "order_date": "2024-05-01T12:00:00Z",
            "delivery_date": "2024-05-10T12:00:00Z",
            "items": [
                  {
                  "name": "Item 1",
                  "quantity": 5,
                  "unit_price": 10.99,
                  },
                  {
                  "name": "Item 2",
                  "quantity": 3,
                  "unit_price": 15.99,
                  },
            ],
            "quantity": 8,
            "status": "pending",
      }

      response = jwt_token.post("/api/purchase_orders/", po_data, format="json")

      assert response.status_code == 201

      assert PurchaseOrder.objects.count() == 1

      assert response.data["po_number"] == "PO123"
      assert response.data["vendor"] == vendor_id


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_vendors")
def test_list_all_purchase_orders(jwt_token, create_vendors):
      """
      Tests listing all purchase orders.
      """
      vendor_id1, vendor_id2 = create_vendors

      PurchaseOrder.objects.create(
            po_number="PO1",
            vendor_id=vendor_id1,
            order_date="2024-05-01T12:00:00Z",
            delivery_date="2024-05-10T12:00:00Z",
            items=[{"name": "Item 1", "quantity": 5, "unit_price": 10.99}],
            quantity=5,
            status="pending",
      )
      PurchaseOrder.objects.create(
            po_number="PO2",
            vendor_id=vendor_id2,
            order_date="2024-05-02T12:00:00Z",
            delivery_date="2024-05-11T12:00:00Z",
            items=[{"name": "Item 2", "quantity": 3, "unit_price": 15.99}],
            quantity=3,
            status="pending",
      )

      url = reverse("purchase-order-create-list")
      response = jwt_token.get(url)

      assert response.status_code == status.HTTP_200_OK
      assert len(response.data) == 2


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_vendor")
def test_list_purchase_orders_by_vendor(jwt_token, create_vendor):
      """
      Tests listing purchase orders by a specific vendor.
      """
      vendor_id = create_vendor

      po_data = {
            "po_number": "PO123",
            "vendor": vendor_id,
            "order_date": "2024-05-01T12:00:00Z",
            "delivery_date": "2024-05-10T12:00:00Z",
            "items": [
                  {
                  "name": "Item 1",
                  "quantity": 5,
                  "unit_price": 10.99,
                  },
                  {
                  "name": "Item 2",
                  "quantity": 3,
                  "unit_price": 15.99,
                  },
            ],
            "quantity": 8,
            "status": "pending",
      }

      response = jwt_token.post("/api/purchase_orders/", po_data, format="json")

      url = reverse("purchase-order-create-list")
      response = jwt_token.get(url, {"vendor": vendor_id})

      assert response.status_code == status.HTTP_200_OK
      assert len(response.data) == 1
      for purchase_order in response.data:
            assert purchase_order["vendor"] == vendor_id


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_purchase_order")
def test_retrieve_purchase_order(jwt_token, create_purchase_order):
      """
      Tests retrieving details of a specific purchase order.
      """
      po_id = create_purchase_order

      url = reverse("purchase-order-read-update-delete", kwargs={"po_id": po_id})
      response = jwt_token.get(url)

      assert response.status_code == status.HTTP_200_OK

      expected_keys = [
            "id",
            "po_number",
            "vendor",
            "order_date",
            "delivery_date",
            "items",
            "quantity",
            "status",
      ]
      for key in expected_keys:
            assert key in response.data

      assert response.data["id"] == po_id


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_retrieve_non_existing_purchase_order(jwt_token):
      """
      Tests retrieving details of a non-existing purchase order.
      """
      non_existing_po_id = 99999
      url = reverse(
            "purchase-order-read-update-delete", kwargs={"po_id": non_existing_po_id}
      )
      response = jwt_token.get(url)

      assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_purchase_order")
def test_update_purchase_order(jwt_token, create_purchase_order):
      """
      Test updating a purchase order via PUT request.
      """
      purchase_order_id = create_purchase_order

      new_data = {
            "po_number": "Updated PO Number",
            "vendor": Vendor.objects.get(
                  id=PurchaseOrder.objects.get(id=purchase_order_id).vendor_id
            ).id,
            "order_date": "2024-05-15T12:00:00Z",
            "delivery_date": "2024-05-20T12:00:00Z",
            "items": [
                  {"name": "Updated Item 1", "quantity": 10, "unit_price": 20.99},
                  {"name": "Updated Item 2", "quantity": 7, "unit_price": 25.99},
            ],
            "quantity": 17,
            "status": "pending",
      }

      url = reverse(
            "purchase-order-read-update-delete", kwargs={"po_id": purchase_order_id}
      )
      response = jwt_token.put(url, new_data, format="json")

      if response.status_code != status.HTTP_200_OK:
            print("Update failed. Response content:")
            print(response.content)

      assert response.status_code == status.HTTP_200_OK

      updated_purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

      assert updated_purchase_order.po_number == new_data["po_number"]
      assert str(updated_purchase_order.order_date) == datetime.datetime.strptime(
            new_data["order_date"], "%Y-%m-%dT%H:%M:%SZ"
      ).strftime("%Y-%m-%d %H:%M:%S+00:00")
      assert str(updated_purchase_order.delivery_date) == datetime.datetime.strptime(
            new_data["delivery_date"], "%Y-%m-%dT%H:%M:%SZ"
      ).strftime("%Y-%m-%d %H:%M:%S+00:00")
      assert updated_purchase_order.quantity == new_data["quantity"]
      assert updated_purchase_order.status == new_data["status"]


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_purchase_order")
def test_delete_purchase_order(jwt_token, create_purchase_order):
      """
      Test deleting a purchase order via DELETE request.
      """
      purchase_order_id = create_purchase_order

      initial_count = PurchaseOrder.objects.count()

      url = reverse(
            "purchase-order-read-update-delete", kwargs={"po_id": purchase_order_id}
      )
      response = jwt_token.delete(url)

      assert response.status_code == status.HTTP_204_NO_CONTENT

      assert PurchaseOrder.objects.count() == initial_count - 1
      assert not PurchaseOrder.objects.filter(id=purchase_order_id).exists()


@pytest.mark.usefixtures("clean_db", "jwt_token", "create_purchase_order")
def test_retrieve_vendor_performance(jwt_token, create_purchase_order):
      """
      Test retrieving performance metrics of a specific vendor.
      """
      purchase_order_id = create_purchase_order
      vendor_id = PurchaseOrder.objects.get(id=purchase_order_id).vendor_id

      url = reverse("vendor-performance-retrieve", kwargs={"vendor_id": vendor_id})
      response = jwt_token.get(url)

      assert response.status_code == status.HTTP_200_OK

      print("Response Data:", response.data)

      expected_keys = [
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
      ]
      for key in expected_keys:
            assert key in response.data


@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_acknowledge_purchase_order(jwt_token, create_purchase_order):
      """
      Tests acknowledging a purchase order.
      """
      purchase_order_id = create_purchase_order

      url = reverse("purchase-order-acknowledge", kwargs={"po_id": purchase_order_id})
      response = jwt_token.patch(url)

      assert response.status_code == status.HTTP_200_OK

      purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
      assert purchase_order.acknowledgment_date is not None
      assert (
            purchase_order.delivery_date
            == purchase_order.acknowledgment_date + timezone.timedelta(days=5)
      )

      vendor = purchase_order.vendor
      assert vendor.average_response_time is not None