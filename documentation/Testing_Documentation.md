# Testing Documentation

This document provides guidance on testing the API endpoints of the Vendor Management System.

## Table of Contents

1. [Introduction](#introduction)
2. [Testing Environment Setup](#testing-environment-setup)
3. [Running Tests](#running-tests)
4. [Test Cases](#test-cases)
    - [Test Case 1: Create Vendor](#test-case-1-create-vendor)
    - [Test Case 2: List Vendors](#test-case-2-list-vendors)
    - [Test Case 3: Retrieve Vendor](#test-case-3-retrieve-vendor)
    - [Test Case 4: Update Vendor](#test-case-4-update-vendor)
    - [Test Case 5: Delete Vendor](#test-case-5-delete-vendor)
    - [Test Case 6: Create Purchase Order](#test-case-6-create-purchase-order)
    - [Test Case 7: List All Purchase Orders](#test-case-7-list-all-purchase-orders)
    - [Test Case 8: List Purchase Orders by Vendor](#test-case-8-list-purchase-orders-by-vendor)
    - [Test Case 9: Retrieve Purchase Order](#test-case-9-retrieve-purchase-order)
    - [Test Case 10: Retrieve a Non-existing Purchase Order](#test-case-10-retrieve-a-non-existing-purchase-order)
    - [Test Case 11: Update Purchase Order](#test-case-11-update-purchase-order)
    - [Test Case 12: Delete Purchase Order](#test-case-12-delete-purchase-order)
    - [Test Case 13: Retrieve Vendor Performance](#test-case-13-retrieve-vendor-performance)
    - [Test Case 14: Acknowledge Purchase Order](#test-case-14-acknowledge-purchase-order)
5. [Conclusion](#conclusion)

## Introduction

The Vendor Management System API provides various endpoints for managing vendors, purchase orders, and vendor performance metrics. Testing these endpoints ensures that the system functions correctly and meets the requirements.

## Testing Environment Setup

To set up the testing environment:

1. Clone the repository from GitHub.
2. Navigate to the app/ directory and activate the virtual environment (create one if you don't have it).
2. Install the required dependencies using pip.(The requirements file is inside app/Vendor_Management_System/requirements.txt) -> pip install -r Vendor_Management_System/requirements.txt

## Running Tests

To run the tests:

1. Navigate to the project directory in the terminal.(VENDOR_MANAGEMENT_SYSTEM/app/Vendor_Management_System)
2. The test files are located inside the "tests" folder in app/Vendor_Management_System.
3. Execute the command `pytest` to run all tests in the project.
4. Optionally, use additional arguments or options to customize the testing process.

## Test Cases

### Test Case 1: Create Vendor

- **Objective**: Test the endpoint for creating a vendor.
- **Steps**:
  1. Create a new vendor with valid data.
  2. Verify that the vendor is created successfully.

### Test Case 2: List Vendors

- **Objective**: Test the endpoint for listing all vendors.
- **Steps**:
  1. List all vendors.
  2. Verify that the response contains a list of vendors.

### Test Case 3: Retrieve Vendor

- **Objective**: Test the endpoint for retrieving a specific vendor.
- **Steps**:
  1. Retrieve a specific vendor by its ID.
  2. Verify that the response contains the expected vendor data.

### Test Case 4: Update Vendor

- **Objective**: Test the endpoint for updating vendor information.
- **Steps**:
  1. Update the information of a specific vendor.
  2. Verify that the vendor information is updated correctly.

### Test Case 5: Delete Vendor

- **Objective**: Test the endpoint for deleting a specific vendor.
- **Steps**:
  1. Delete a specific vendor.
  2. Verify that the vendor is deleted successfully.

### Test Case 6: Create Purchase Order

- **Objective**: Test the endpoint for creating a purchase order.
- **Steps**:
  1. Create a new purchase order with valid data.
  2. Verify that the purchase order is created successfully.

### Test Case 7: List All Purchase Orders

- **Objective**: Test the endpoint for listing all purchase orders.
- **Steps**:
  1. List all purchase orders.
  2. Verify that the response contains a list of purchase orders.

### Test Case 8: List Purchase Orders by Vendor

- **Objective**: Test the endpoint for listing purchase orders by a specific vendor.
- **Steps**:
  1. List all purchase orders for a specific vendor.
  2. Verify that the response contains the expected purchase orders.

### Test Case 9: Retrieve Purchase Order

- **Objective**: Test the endpoint for retrieving details of a specific purchase order.
- **Steps**:
  1. Retrieve details of a specific purchase order.
  2. Verify that the response contains the expected purchase order details.

### Test Case 10: Retrieve a Non-existing Purchase Order

- **Objective**: Test the endpoint for retrieving details of a specific purchase order(Which doesn't exist).
- **Steps**:
  1. Retrieve details of a specific purchase order.
  2. Verify that the response contains 404 Not found error.  

### Test Case 11: Update Purchase Order

- **Objective**: Test the endpoint for updating a specific purchase order.
- **Steps**:
  1. Update the details of a specific purchase order.
  2. Verify that the purchase order is updated correctly.

### Test Case 12: Delete Purchase Order

- **Objective**: Test the endpoint for deleting a specific purchase order.
- **Steps**:
  1. Delete a specific purchase order.
  2. Verify that the purchase order is deleted successfully.

### Test Case 13: Retrieve Vendor Performance

- **Objective**: Test the endpoint for retrieving performance metrics of a specific vendor.
- **Steps**:
  1. Retrieve performance metrics of a specific vendor.
  2. Verify that the response contains the expected performance metrics.

### Test Case 14: Acknowledge Purchase Order

- **Objective**: Test the endpoint for acknowledging a specific purchase order.
- **Steps**:
  1. Acknowledge a specific purchase order.
  2. Verify that the acknowledgment is successful and update the necessary fields.

## Conclusion

Testing the API endpoints is essential to ensure the reliability and functionality of the Vendor Management System. By following the provided test cases and running the tests regularly, you can identify and fix issues early, leading to a more robust and stable system.
